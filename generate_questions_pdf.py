#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ==========================================================================
# COMPREHENSIVE Q&A BANK – Data Engineer (DAC Data Technology / Hakuhodo)
# ==========================================================================

SECTIONS = [
    # -----------------------------------------------------------------------
    {
        "title": "I. Python cho Data Engineering",
        "color": colors.HexColor("#1A5276"),
        "questions": [
            "Giải thích sự khác biệt giữa list, tuple, set và dict. Khi nào nên dùng từng loại trong data pipeline?",
            "Generator expression vs list comprehension: khác nhau về bộ nhớ như thế nào? Cho ví dụ xử lý file 10 GB.",
            "Viết hàm Python đọc file CSV lớn (> 10 GB) theo từng chunk mà không load toàn bộ vào RAM.",
            "Context manager (`with` statement): Viết context manager tùy chỉnh bằng class và bằng `@contextmanager`.",
            "Phân biệt `multiprocessing` và `multithreading`. Khi nào dùng cái nào cho tác vụ data engineering?",
            "GIL (Global Interpreter Lock) là gì? Ảnh hưởng đến xử lý song song như thế nào? Cách vượt qua GIL?",
            "Giải thích `asyncio` và `async/await`. Cho ví dụ gọi 50 API endpoint đồng thời dùng `asyncio.gather`.",
            "Viết decorator `@retry(max_attempts, delay)` tự động thử lại hàm khi gặp exception.",
            "Viết decorator `@timer` đo thời gian thực thi của bất kỳ hàm nào.",
            "Pandas vs Polars vs Dask: So sánh hiệu năng, memory usage và use-case phù hợp cho từng thư viện.",
            "Viết code Python dùng Pandas để: đọc nhiều CSV, nối lại, xử lý missing values, ghi ra Parquet.",
            "Giải thích `*args` và `**kwargs`. Viết hàm tổng quát nhận cấu hình kết nối database qua `**kwargs`.",
            "Type hints trong Python 3: Lợi ích khi dùng trong data pipeline. Cho ví dụ với `TypedDict`, `Optional`, `Union`, `Literal`.",
            "Viết script kết nối GCS dùng `google-cloud-storage`, đọc và ghi file Parquet.",
            "Dùng `pydantic` để validate schema một record từ API bên ngoài. Xử lý validation error như thế nào?",
            "Giải thích Python memory management: reference counting, garbage collection, `__del__`. Cách profile memory dùng `memory_profiler`.",
            "Phân biệt `deepcopy` và `shallowcopy`. Khi nào cần deepcopy trong data processing?",
            "Giải thích `__slots__` trong Python class. Lợi ích về memory khi dùng trong data models?",
            "Viết Python script đọc dữ liệu từ PostgreSQL dùng `psycopg2` hoặc `sqlalchemy`, transform và ghi vào BigQuery.",
            "Giải thích `functools.lru_cache` và `functools.cache`. Khi nào dùng cache trong data pipeline?",
            "Viết một class `DataPipeline` với phương thức `extract()`, `transform()`, `load()` theo pattern Template Method.",
            "Giải thích Pythonic code: list comprehension, ternary operator, unpacking, walrus operator (`:=`). Cho ví dụ từng cái.",
            "Dùng `concurrent.futures.ThreadPoolExecutor` và `ProcessPoolExecutor` để song song hóa I/O-bound và CPU-bound tasks.",
            "Viết pipeline đơn giản dùng Python `queue.Queue` để producer-consumer pattern xử lý records.",
            "Giải thích `dataclasses` và so sánh với `namedtuple`, `TypedDict`, và `pydantic BaseModel`. Khi nào dùng cái nào?",
            "Python logging best practices trong data pipeline: structured logging, log levels, log rotation, tích hợp với Cloud Logging.",
            "Viết unit test cho hàm transform dữ liệu dùng `pytest` và `pytest-mock`. Cách mock external dependencies.",
            "Giải thích `pathlib.Path` so với `os.path`. Tại sao `pathlib` được ưa chuộng hơn trong Python hiện đại?",
            "Dùng `argparse` hoặc `click` để tạo CLI tool cho ETL script, nhận các tham số như `--date`, `--env`, `--dry-run`.",
            "Giải thích `__init__.py`, `__main__.py`, và cấu trúc thư mục Python package chuẩn cho data engineering project.",
            "Viết hàm tính checksum (MD5/SHA256) của file để verify data integrity sau khi transfer.",
            "Dùng `boto3` (AWS SDK) và `google-cloud-bigquery` trong cùng một script để migrate data từ S3 sang BigQuery.",
            "Giải thích Python `typing.Protocol` và duck typing. Cách dùng Protocol để định nghĩa interface cho connector classes.",
            "Viết code dùng `aiohttp` để gọi REST API async, xử lý rate limiting (429), và save response vào file JSONL.",
            "Explain the difference between `is` and `==` in Python. When can this cause bugs in data processing?",
            "Viết hàm `flatten_dict` chuyển nested dict `{'a': {'b': {'c': 1}}}` thành `{'a.b.c': 1}`. Dùng để xử lý JSON từ API.",
            "Giải thích Python `abc` module (Abstract Base Classes). Thiết kế abstract class cho các loại data source khác nhau.",
            "Viết script Python tự động detect encoding của file text (UTF-8, UTF-16, Latin-1) trước khi đọc.",
            "Giải thích `contextlib.suppress`, `contextlib.redirect_stdout`. Ứng dụng trong testing và logging?",
            "Dùng `pandas.DataFrame.pipe()` để xây dựng transformation pipeline dạng function chaining. Ưu điểm gì?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "II. Java cho Data Engineering",
        "color": colors.HexColor("#1A5276"),
        "questions": [
            "Giải thích sự khác biệt giữa `HashMap`, `LinkedHashMap`, `TreeMap`, `ConcurrentHashMap`. Khi nào dùng cái nào?",
            "Java Streams API: Viết stream pipeline filter record log, extract field, group by, count dùng `Collectors.groupingBy`.",
            "Giải thích Java memory model: heap, stack, metaspace. Cách tune JVM (`-Xms`, `-Xmx`, `-XX:+UseG1GC`) cho ứng dụng Big Data?",
            "Giải thích Java garbage collectors: G1GC, ZGC, Shenandoah. Khi nào chọn ZGC?",
            "Checked vs unchecked exceptions trong Java. Best practice xử lý exception trong data pipeline?",
            "Giải thích `Optional<T>` trong Java 8. Cách dùng để tránh NullPointerException trong data processing?",
            "Java `CompletableFuture`: Viết ví dụ gọi nhiều API đồng thời và combine kết quả. So sánh với Python asyncio.",
            "Giải thích `Comparable` và `Comparator` interface. Cách sort custom objects trong stream?",
            "Generics trong Java: bounded wildcards (`? extends T`, `? super T`). Tại sao cần trong collection processing?",
            "Apache Kafka Java client: Producer và Consumer API. Cách implement consumer group với auto offset commit?",
            "Viết Flink job đơn giản đọc từ Kafka topic, aggregate theo window 5 phút, ghi kết quả ra BigQuery.",
            "Giải thích Java `ExecutorService`, `ScheduledExecutorService`. Cách tạo thread pool cho parallel ETL?",
            "Lombok: Giải thích các annotation thường dùng (`@Data`, `@Builder`, `@Slf4j`). Ưu/nhược điểm?",
            "Giải thích design pattern Builder trong Java. Áp dụng khi xây dựng complex query/config object?",
            "Maven vs Gradle: Phân biệt và khi nào chọn Gradle cho data engineering project?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "III. SQL & Database Systems",
        "color": colors.HexColor("#1E8449"),
        "questions": [
            "Viết SQL tính rolling 7-day average của doanh thu theo ngày từ bảng `orders(order_date, revenue)`.",
            "Giải thích Window Functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `NTILE()`. Cho ví dụ từng hàm.",
            "CTE vs Subquery vs Temporary Table: So sánh hiệu năng và readability. Khi nào dùng recursive CTE?",
            "Viết SQL tìm session từ event logs: session là chuỗi sự kiện cùng user, không có khoảng trống > 30 phút.",
            "Giải thích EXPLAIN ANALYZE trong PostgreSQL. Đọc query plan: Seq Scan, Index Scan, Hash Join, Nested Loop?",
            "Index B-tree, Hash, GIN, GiST, Partial, Covering Index. Khi nào tạo composite index? Tại sao index làm WRITE chậm hơn?",
            "Partitioning trong BigQuery: ingestion time, column partition, clustering. Ảnh hưởng đến chi phí query?",
            "Viết BigQuery SQL dùng `UNNEST` xử lý ARRAY và STRUCT. Ví dụ với bảng dữ liệu quảng cáo.",
            "Normalization 1NF, 2NF, 3NF, BCNF. Tại sao data warehouse thường denormalize?",
            "ACID properties: Atomicity, Consistency, Isolation, Durability. Phân biệt với BASE trong NoSQL.",
            "Transaction isolation levels: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE và các anomaly.",
            "Slowly Changing Dimension (SCD) Type 1, 2, 3, 4, 6. Implement SCD Type 2 trong BigQuery.",
            "Viết BigQuery SQL deduplicate records, giữ bản ghi mới nhất theo `updated_at` với mỗi `id`.",
            "BigQuery cost optimization: slot reservation, BI Engine, materialized views, partitioning best practices.",
            "INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF JOIN. Khi nào CROSS JOIN gây vấn đề hiệu năng nghiêm trọng?",
            "Viết SQL tính cohort retention: tỷ lệ user quay lại theo tháng kể từ tháng đầu tiên dùng sản phẩm.",
            "MERGE (UPSERT) vs INSERT OVERWRITE. Dùng MERGE trong BigQuery như thế nào? Khi nào prefer INSERT OVERWRITE?",
            "Database Sharding và Replication: horizontal sharding, read replicas, leader-follower, multi-master. Trade-offs?",
            "Temporal tables / bi-temporal data: lưu lịch sử thay đổi dữ liệu. Áp dụng trong BigQuery?",
            "Viết SQL phát hiện anomaly: giá trị outlier dùng IQR hoặc Z-score ngay trong BigQuery SQL.",
            "Viết SQL tính *percentile* (p50, p90, p99) của latency từ bảng request logs dùng `APPROX_QUANTILES` trong BigQuery.",
            "Giải thích PIVOT và UNPIVOT trong SQL. Viết query chuyển rows thành columns cho báo cáo.",
            "Viết SQL tìm chuỗi liên tiếp (consecutive days) user đăng nhập dùng window functions.",
            "Giải thích Materialized View: khác thế nào với regular view? Khi nào dùng trong BigQuery?",
            "Viết BigQuery SQL tính *market basket analysis*: những sản phẩm nào thường được mua cùng nhau?",
            "Giải thích GROUPING SETS, ROLLUP, CUBE. Cho ví dụ tính tổng doanh thu theo nhiều chiều.",
            "Viết SQL detect circular reference trong bảng có quan hệ parent-child (ví dụ: org chart).",
            "Giải thích *query optimizer* trong BigQuery. Tại sao đôi khi viết query 'ngây thơ' lại nhanh hơn query 'tối ưu tay'?",
            "Viết SQL tính *funnel conversion rate*: từ impression → click → add_to_cart → purchase.",
            "Giải thích `QUALIFY` clause trong BigQuery / Snowflake. Thay thế cho subquery với window function như thế nào?",
            "Viết SQL tạo calendar dimension table với tất cả ngày trong năm, flag weekend/holiday, quarter, week number.",
            "Giải thích *approximate aggregations* trong BigQuery: `APPROX_COUNT_DISTINCT`, `APPROX_TOP_COUNT`. Khi nào dùng?",
            "Viết stored procedure / scripting trong BigQuery để tự động partition table theo tháng.",
            "Giải thích column encryption trong BigQuery: AEAD functions. Mã hóa dữ liệu nhạy cảm ngay trong SQL.",
            "Viết SQL tính *time-to-first-purchase* cho mỗi user: khoảng cách từ lần đầu tiên thấy quảng cáo đến lần mua đầu tiên.",
            "Giải thích difference giữa `COUNT(1)`, `COUNT(*)`, `COUNT(col)`. Cái nào nhanh hơn trong BigQuery?",
            "Viết query dùng `WITH RECURSIVE` để traverse tree structure (ví dụ: comment thread, org chart).",
            "Giải thích *query cache* trong BigQuery. Khi nào cache được dùng và khi nào không?",
            "Viết SQL tính *longest streak*: chuỗi ngày dài nhất mà user liên tục hoạt động.",
            "Giải thích `SAFE_CAST`, `SAFE_DIVIDE`, `COALESCE`, `NULLIF`, `IF`, `IFF` trong BigQuery. Tại sao quan trọng trong production?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "IV. Data Modeling & Architecture",
        "color": colors.HexColor("#7D3C98"),
        "questions": [
            "Star Schema vs Snowflake Schema vs Data Vault: So sánh ưu/nhược điểm. Khi nào chọn từng loại?",
            "Fact Table và Dimension Table: Thiết kế star schema cho hệ thống quảng cáo online.",
            "Data Vault 2.0: Hubs, Links, Satellites. Ưu điểm trong môi trường agile và schema evolution?",
            "Medallion Architecture (Bronze/Silver/Gold): mô tả data flow và transformations qua từng tầng.",
            "Lambda Architecture vs Kappa Architecture: Phân biệt, ưu/nhược, khi nào chọn cái nào?",
            "Data Mesh: 4 nguyên tắc. Áp dụng ở công ty vừa và nhỏ có thực tế không?",
            "Thiết kế schema tracking hành vi người dùng trên website quảng cáo. Volume và query patterns cần cân nhắc?",
            "Data lineage và data catalog. Công cụ hỗ trợ: OpenMetadata, DataHub, Amundsen, Google Data Catalog.",
            "Idempotency trong data pipeline: tại sao cần? Cách implement cho ETL job chạy định kỳ?",
            "Cardinality: high-cardinality vs low-cardinality column. Ảnh hưởng đến performance và storage?",
            "Schema evolution với Avro / Protobuf / JSON Schema. Backward compatibility vs forward compatibility?",
            "Thiết kế data model cho hệ thống marketing attribution: first touch, last touch, multi-touch, data-driven.",
            "OLTP vs OLAP: Tại sao không nên chạy báo cáo OLAP trực tiếp trên OLTP database?",
            "Data Quality dimensions: Completeness, Accuracy, Consistency, Timeliness, Validity, Uniqueness. Cách đo lường?",
            "Thiết kế ERD cho hệ thống quản lý chiến dịch quảng cáo: campaigns, ad groups, ads, keywords, conversions.",
            "Wide table vs Normalized tables trong BigQuery. Tại sao BigQuery thường prefer wide table?",
            "Aggregate table / Pre-aggregation: khi nào nên tạo aggregate table thay vì query on-the-fly?",
            "Surrogate key vs Natural key: phân biệt và khi nào dùng surrogate key trong data warehouse?",
            "Junk dimension là gì? Khi nào dùng junk dimension để gom các low-cardinality flags?",
            "Role-playing dimension: ví dụ `date_dim` dùng cho nhiều foreign keys khác nhau trong fact table.",
            "Conformed dimension: tại sao quan trọng trong data warehouse để đảm bảo cross-domain reporting?",
            "Fact-less fact table: là gì và khi nào dùng? Ví dụ trong hệ thống quảng cáo?",
            "Giải thích *grain* của fact table. Tại sao việc xác định đúng grain là bước quan trọng nhất trong data modeling?",
            "Thiết kế schema cho hệ thống A/B testing: experiments, variants, user assignments, metric events.",
            "Data contract là gì? Làm thế nào enforce data contract giữa producer và consumer trong data platform?",
            "Event-driven schema design: thiết kế schema cho event streaming (Kafka) vs batch (BigQuery). Khác nhau như thế nào?",
            "Inmon vs Kimball approach: So sánh hai trường phái data warehouse design kinh điển.",
            "Thiết kế master data management (MDM) cho customer identity resolution: merge records từ nhiều nguồn.",
            "Giải thích *denormalized lookup*: nhúng dimension values vào fact table. Trade-off giữa storage và query performance?",
            "Hub-and-spoke vs Bus architecture trong data warehouse. Ảnh hưởng đến cross-domain analytics?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "V. ETL / ELT & Data Pipeline",
        "color": colors.HexColor("#C0392B"),
        "questions": [
            "ETL vs ELT: Tại sao với cloud data warehouse như BigQuery, ELT thường được ưa chuộng hơn?",
            "Thiết kế ETL pipeline lấy dữ liệu từ REST API, transform, load vào BigQuery. Mô tả kiến trúc.",
            "Dead-letter queue, retry, alert, circuit breaker trong data pipeline. Implement như thế nào?",
            "Incremental load vs Full refresh: khi nào dùng cái nào? Implement incremental load dựa trên `updated_at`?",
            "Change Data Capture (CDC): timestamp-based, trigger-based, log-based (Debezium). Ưu/nhược?",
            "Xử lý duplicate data trong pipeline: nguyên nhân và cách phòng ngừa/xử lý?",
            "Data backfill: chiến lược backfill lịch sử mà không ảnh hưởng pipeline production?",
            "Exactly-once, at-least-once, at-most-once delivery semantics. Cái nào khó đạt nhất và tại sao?",
            "Watermarking trong stream processing: tại sao cần khi có late events?",
            "Thiết kế pipeline xử lý log access 100M events/ngày → tính DAU, WAU, MAU.",
            "Fan-out và fan-in pattern trong data pipeline. Ví dụ thực tế?",
            "JSON, CSV, Avro, Parquet, ORC: So sánh về kích thước, tốc độ, schema evolution support.",
            "Apache Airflow: DAG, Task, Operator, XCom, Sensor, TaskGroup. Xử lý task failure và retry.",
            "Viết Airflow DAG: mỗi ngày lúc 2AM extract từ MySQL, transform Python, load lên BigQuery.",
            "dbt (data build tool): models, sources, tests, snapshots, macros. Khác traditional ETL như thế nào?",
            "Kafka cơ bản: Topic, Partition, Consumer Group, Offset. Tại sao tăng partition tăng throughput?",
            "GCP Pub/Sub: So sánh với Apache Kafka. Khi nào dùng Pub/Sub thay vì self-hosted Kafka?",
            "Thiết kế pipeline real-time ad click fraud detection: latency < 1 giây, volume 10,000 events/giây.",
            "Monitoring data pipeline: metrics quan trọng, công cụ, cách setup alert khi pipeline fail?",
            "Giải thích *pipeline orchestration*. Khi pipeline có hàng trăm tasks, quản lý dependencies thế nào?",
            "Thiết kế data pipeline có *schema inference*: tự động detect schema từ JSON API và tạo BigQuery table.",
            "Giải thích *data lineage tracking* tích hợp trong pipeline. Công cụ: OpenLineage, Marquez.",
            "Xử lý NULL values trong pipeline: khi nào drop, khi nào impute, khi nào giữ nguyên? Tại sao quan trọng?",
            "Giải thích *data freshness*: SLA là data phải cập nhật trong 2 giờ. Cách enforce và monitor?",
            "Thiết kế pipeline *event deduplication*: nhận event từ nhiều nguồn, đảm bảo mỗi event chỉ được xử lý 1 lần.",
            "Streaming join: join 2 Kafka stream. Các loại join: inner, left, temporal. Thách thức là gì?",
            "Giải thích *Kappa Architecture* với ví dụ cụ thể: xây dựng toàn bộ data platform dùng streaming only.",
            "Viết Python class `BaseExtractor` abstract với method `extract(start_date, end_date)`. Implement cho MySQL và REST API.",
            "Giải thích *pipeline versioning*: khi logic transform thay đổi, cần reprocess historical data như thế nào?",
            "Apache Airflow vs Prefect vs Dagster vs Mage: so sánh về developer experience, features, và maturity.",
            "Thiết kế multi-tenant ETL pipeline: cùng một pipeline chạy cho nhiều clients với config khác nhau.",
            "Giải thích *data vault loading patterns*: raw vault load, business vault, information mart.",
            "Xử lý timezone trong data pipeline: UTC vs local time. Best practice khi lưu timestamp trong BigQuery?",
            "Viết Python code parse và validate nested JSON từ ad platform API (Google Ads, Meta Ads) trước khi load vào BigQuery.",
            "Giải thích *pipeline DAG dependency*: task A phụ thuộc task B đang chạy hàng ngày. Cách quản lý cross-DAG dependency?",
            "Thiết kế *hot/cold data tiering* cho data pipeline: data mới trong BigQuery, data cũ archive xuống GCS Coldline.",
            "Giải thích Pub/Sub *message ordering* và *message retention*. Cách đảm bảo xử lý message theo đúng thứ tự?",
            "Spark vs Dataflow vs BigQuery SQL: khi nào chọn mỗi công cụ để transform data?",
            "Viết Airflow *dynamic DAG* tự động tạo tasks dựa trên danh sách bảng cần sync từ database.",
            "Giải thích *pipeline testing pyramid*: unit test, integration test, end-to-end test cho data pipeline.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "VI. Google Cloud Platform (GCP)",
        "color": colors.HexColor("#1A5276"),
        "questions": [
            "BigQuery architecture: phân tách compute và storage. Dremel và Colossus. Tại sao query nhanh?",
            "BigQuery pricing: On-demand vs Slot-based (flex/standard/enterprise). Khi nào dùng slot reservation?",
            "Viết BigQuery query tối ưu: tránh SELECT *, dùng partition pruning, tránh self-join trên bảng lớn.",
            "BigQuery Storage Read API vs Export: khi nào dùng Storage Read API thay vì export ra GCS?",
            "Cloud Composer vs Cloud Workflows vs Cloud Scheduler: so sánh use-case từng dịch vụ orchestration.",
            "Cloud Run: containerized workloads, concurrency, memory, timeout cho ETL job. Cold start là gì?",
            "Cloud Scheduler: trigger Cloud Run để chạy ETL hàng ngày. Xử lý job fail như thế nào?",
            "GCS storage classes: Standard, Nearline, Coldline, Archive. Lifecycle management và Object Versioning.",
            "Dataflow (Apache Beam): Batch vs Streaming mode. Autoscaling và worker configuration.",
            "Pub/Sub + Dataflow + BigQuery: streaming pipeline. Xử lý late data như thế nào?",
            "IAM trong GCP: Principle of least privilege. Service Account với quyền tối thiểu. Workload Identity Federation.",
            "Secret Manager vs Environment Variables: khi nào dùng Secret Manager? Truy cập từ Cloud Run?",
            "Cloud Monitoring và Logging: setup dashboard và alert cho data pipeline. Structured logging.",
            "Artifact Registry: lưu Docker image. Tích hợp với Cloud Build CI/CD.",
            "Terraform trên GCP: tạo BigQuery dataset, GCS bucket, Cloud Run service. State management.",
            "Dataproc vs Dataflow vs BigQuery: khi nào chọn Spark on Dataproc?",
            "BigQuery ML: tạo và train model bằng SQL. Use-case phù hợp? Giới hạn so với Vertex AI?",
            "Vertex AI: Pipelines, Feature Store, Model Registry. Tích hợp với BigQuery như thế nào?",
            "GCP networking: VPC, Firewall rules, Private Google Access. Tại sao cần Private Google Access cho BigQuery?",
            "Cloud Build: CI/CD pipeline tự động test và deploy Cloud Run service khi push lên main.",
            "BigQuery Omni: query dữ liệu trên AWS S3 hoặc Azure Blob từ BigQuery không cần move data.",
            "Giải thích BigQuery *Information Schema*: truy vấn metadata về tables, columns, jobs, reservations.",
            "Cloud Spanner: khi nào dùng thay vì Cloud SQL hoặc BigQuery? Giải thích globally distributed ACID transactions.",
            "Firestore vs Bigtable vs Spanner: so sánh use-case trong data engineering context.",
            "Cloud Tasks vs Pub/Sub: phân biệt. Khi nào dùng Cloud Tasks cho asynchronous job dispatch?",
            "BigQuery Connected Sheets: giải thích và use-case. Hạn chế về security và governance?",
            "Vertex AI Feature Store: tại sao cần? Giải thích online store vs offline store. Tích hợp với training pipeline.",
            "Cloud Composer 2 vs Cloud Composer 1: những cải tiến chính. Airflow version và autoscaling.",
            "BigQuery *authorized views* và *authorized routines*: cách share data mà không cần grant quyền trực tiếp vào table.",
            "Giải thích *BigQuery Reservations* và *Workload Management*: slot pools, reservation assignments, idle capacity.",
            "GCP Data Catalog: tự động tag BigQuery tables, tìm kiếm data assets, policy tags. Tích hợp với IAM?",
            "Cloud Run Jobs vs Cloud Run Services: phân biệt. Khi nào dùng Cloud Run Jobs cho batch ETL?",
            "Eventarc: trigger Cloud Run từ Pub/Sub, GCS events, Audit Logs. Use-case event-driven pipeline.",
            "BigQuery *Authorized Datasets*: chia sẻ dataset giữa các projects mà không expose underlying tables.",
            "Giải thích GCP *Organization Policies*: enforce resource restrictions ở organization level. Ảnh hưởng đến data pipeline deployment?",
            "Cloud Storage FUSE (gcsfuse): mount GCS bucket như filesystem. Use-case và limitations?",
            "BigQuery *table snapshot* và *table clone*: phân biệt, use-case cho testing và rollback.",
            "Dataplex: GCP data mesh platform. Giải thích Lakes, Zones, Assets, Tasks, và Data Quality rules.",
            "Giải thích *BigQuery Continuous Queries* (preview): streaming SQL queries chạy liên tục trên Pub/Sub.",
            "AlloyDB vs Cloud SQL: khi nào chọn AlloyDB? Columnar engine trong AlloyDB giúp analytics thế nào?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "VII. Git, GitFlow & CI/CD",
        "color": colors.HexColor("#117A65"),
        "questions": [
            "GitFlow workflow: main, develop, feature, release, hotfix branches. Khi nào dùng GitFlow vs trunk-based?",
            "Git rebase vs merge: phân biệt, ưu/nhược. Khi nào KHÔNG nên dùng rebase?",
            "Git cherry-pick: dùng khi nào? Nguy cơ khi cherry-pick nhiều commit?",
            "Git stash, reset (soft/mixed/hard), revert. Sự khác biệt giữa `reset` và `revert`?",
            "`.gitignore` và `.gitattributes`. Cấu hình `.gitattributes` xử lý line endings cross-platform?",
            "Git hooks: pre-commit, commit-msg, pre-push. Dùng husky hoặc pre-commit framework enforce code quality.",
            "Semantic versioning (SemVer): MAJOR.MINOR.PATCH. Tích hợp với CI/CD để auto-tag release.",
            "CI/CD pipeline cho data pipeline: lint, test, build docker, push, deploy. Công cụ: GitHub Actions, Cloud Build.",
            "Infrastructure as Code (IaC): tại sao version control infrastructure? Terraform vs Pulumi.",
            "Testing strategy cho data pipeline: unit test, integration test, data quality test. Công cụ phù hợp.",
            "Canary deployment vs Blue/Green deployment. Áp dụng cho Cloud Run service.",
            "Docker multi-stage build: tại sao dùng? Viết Dockerfile tối ưu cho Python ETL application.",
            "Secrets management trong CI/CD: lưu và truy cập secrets an toàn trong GitHub Actions hoặc Cloud Build.",
            "Monorepo vs Polyrepo: ưu/nhược điểm khi quản lý nhiều data pipeline projects.",
            "Code review best practices: checklist khi review data pipeline PR.",
            "Giải thích `git bisect`: tìm commit gây ra bug bằng binary search. Áp dụng trong data pipeline regression?",
            "Giải thích *conventional commits*: format commit message chuẩn. Tại sao quan trọng với auto-changelog?",
            "GitHub Actions: viết workflow tự động chạy pytest khi có PR, generate coverage report, comment vào PR.",
            "Giải thích *trunk-based development*: developer commit thẳng vào main với feature flags. Khác GitFlow thế nào?",
            "Giải thích *GitOps*: dùng Git là single source of truth cho infrastructure. Công cụ: ArgoCD, Flux.",
            "Container registry security: scan Docker image tìm CVE với Trivy hoặc Container Analysis. Integrate vào CI?",
            "Giải thích *dependency management* trong Python: `requirements.txt`, `pyproject.toml`, `poetry`, `uv`. Best practices.",
            "Viết GitHub Actions workflow: khi merge vào main, tự động build Docker image, push lên Artifact Registry, deploy lên Cloud Run.",
            "Giải thích *release train* vs *continuous deployment*. Khi nào phù hợp với team data engineering?",
            "Pre-commit hooks: `black`, `isort`, `flake8`, `mypy`. Tự động format và lint code trước khi commit.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "VIII. Looker & Data Visualization",
        "color": colors.HexColor("#784212"),
        "questions": [
            "LookML: view, model, explore, dimension, measure, join. Giải thích từng khái niệm cơ bản.",
            "Phân biệt `dimension`, `measure`, `dimension_group`, `filter` trong LookML. Ví dụ với dữ liệu quảng cáo.",
            "Looker Derived Tables: Native vs SQL vs Persistent Derived Table (PDT). Khi nào dùng PDT?",
            "Tối ưu LookML giảm chi phí BigQuery: Aggregate Awareness là gì và cách implement?",
            "Looker Explores và Joins: các loại join, fan trap và chasm trap là gì? Cách tránh?",
            "Looker Dashboards: Look vs Dashboard. Share và embed Looker vào ứng dụng (Embedded Analytics)?",
            "Looker API: tạo/update content, chạy queries, extract data programmatically. Use-case thực tế?",
            "Looker git integration: tại sao LookML được version control giống code?",
            "Looker data tests và assertions: viết test trong LookML để đảm bảo data quality?",
            "So sánh Looker với Power BI và Tableau về semantic layer, governance, và GCP ecosystem fit.",
            "Thiết kế Looker dashboard cho CMO: chi phí quảng cáo, CPC, CPM, CTR, ROAS theo kênh và thời gian.",
            "Looker Studio vs Looker: khi nào dùng cái nào? Sự khác biệt về governance và scalability.",
            "Giải thích *Looker semantic layer*: tại sao định nghĩa metric một lần trong LookML tốt hơn define trong BI tool?",
            "LookML `label`, `description`, `group_label`, `hidden`: cách organize và document metrics cho business users.",
            "Giải thích Looker *access filters* và *user attributes*: implement row-level security theo user location.",
            "Looker *liquid templating*: dùng Liquid trong LookML để dynamic dimension/measure. Ví dụ?",
            "Giải thích Looker *refinements*: extend LookML models mà không sửa code gốc. Use-case?",
            "Looker Marketplace: tìm và install block. Ví dụ Google Analytics 4 block tiết kiệm công triển khai thế nào?",
            "Viết LookML dimension tính *days_since_last_order* dùng `datediff`. Tại sao cần type: duration?",
            "Looker Scheduler và Alerts: setup tự động gửi báo cáo qua email hoặc Slack khi metric vượt ngưỡng.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "IX. AWS, Redshift & Treasure Data",
        "color": colors.HexColor("#1F618D"),
        "questions": [
            "Amazon Redshift architecture: leader node vs compute nodes. Redshift Spectrum. Khi nào dùng thay BigQuery?",
            "Redshift distribution styles: EVEN, KEY, ALL, AUTO. Cách chọn distribution key?",
            "Redshift sort keys: Compound vs Interleaved. VACUUM và ANALYZE trong Redshift.",
            "Redshift Serverless vs Provisioned Clusters: trade-offs chi phí và hiệu năng.",
            "AWS Glue: Glue Catalog, Crawler, ETL Jobs, Glue Studio. So sánh với GCP Dataflow.",
            "AWS S3 vs GCS: so sánh về tính năng, pricing, integration với data warehouse.",
            "Treasure Data (TD): kiến trúc Customer Data Platform (CDP). TD Workflow, TD Query (Presto/Hive), TD Bulk Load.",
            "TD Segment Builder và Audience Builder: tạo audience segment từ dữ liệu hành vi người dùng.",
            "Tích hợp Treasure Data với hệ thống quảng cáo (Google Ads, Facebook Ads): luồng dữ liệu.",
            "Amazon Kinesis vs Kafka vs GCP Pub/Sub: so sánh throughput, latency, managed service trade-offs.",
            "AWS Lake Formation: quản lý data lake permissions ở column/row level. So sánh với GCP Data Catalog.",
            "AWS Step Functions vs Apache Airflow vs Cloud Composer: so sánh orchestration options.",
            "Amazon EMR vs Dataproc: managed Spark clusters. So sánh pricing và feature parity.",
            "Redshift COPY command: load data từ S3 vào Redshift. Tối ưu với WLM (Workload Management)?",
            "AWS DMS (Database Migration Service): migrate từ on-premise Oracle sang Redshift. Thách thức gì?",
            "Treasure Data *TD Agent* (Fluentd): collect và ship logs từ server lên TD. Cấu hình như thế nào?",
            "Giải thích *Presto/Trino* dùng trong Treasure Data. Khi nào query Presto nhanh hơn Hive?",
            "AWS Athena: query trực tiếp S3 dùng SQL. So sánh với BigQuery Omni và Redshift Spectrum.",
            "TD Workflow: viết workflow YAML định nghĩa multi-step data pipeline trong Treasure Data.",
            "Giải thích *CDP (Customer Data Platform)*: các thành phần chính và cách TD platform fit vào kiến trúc?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "X. Big Data & Distributed Systems",
        "color": colors.HexColor("#6E2F79"),
        "questions": [
            "CAP theorem: Consistency, Availability, Partition Tolerance. Ví dụ hệ thống ưu tiên CP và AP.",
            "Apache Spark: RDD, DataFrame, Dataset. Tại sao DataFrame được ưu tiên hơn RDD trong Spark hiện đại?",
            "Spark execution model: Driver, Executor, Job, Stage, Task. Quá trình shuffle và tại sao tốn kém.",
            "Spark tối ưu: Broadcast join, partition pruning, predicate pushdown, caching/persist.",
            "Spark Structured Streaming: micro-batch vs continuous processing. Watermarking và stateful operations.",
            "Data skew trong Spark: nguyên nhân và cách xử lý (salting, broadcast, repartition).",
            "Parquet: row group, column chunk, page. Tại sao tốt cho analytical workloads? Predicate pushdown?",
            "Iceberg, Delta Lake, Hudi: so sánh ba table format. ACID transactions trên data lake.",
            "Distributed caching: Redis vs Memcached. Khi nào dùng cache trong data pipeline?",
            "Consistent hashing: dùng trong distributed systems. Tại sao tốt hơn modulo hashing?",
            "MapReduce: Map, Shuffle, Reduce. Hạn chế so với Spark?",
            "Data skewness trong thống kê và distributed computing. Cách detect và handle?",
            "Event sourcing vs traditional CRUD: ưu/nhược. Khi nào nên dùng?",
            "Micro-batching vs True Streaming: Spark Structured Streaming, Flink, Dataflow về latency và throughput.",
            "Columnar storage vs Row storage: tại sao columnar tốt hơn cho OLAP? I/O savings cụ thể.",
            "Giải thích *vector clock* và *lamport timestamp* trong distributed systems. Dùng để làm gì?",
            "Two Generals Problem và Byzantine Fault Tolerance: tại sao không thể có 100% reliable messaging?",
            "Paxos vs Raft consensus algorithms: giải thích ý tưởng cơ bản của Raft. Dùng trong Kafka, etcd như thế nào?",
            "Giải thích *backpressure* trong stream processing. Cách Kafka và Flink xử lý backpressure?",
            "Giải thích *exactly-once* trong Kafka: idempotent producer, transactional API. Overhead so với at-least-once?",
            "Flink vs Spark Streaming: so sánh về true streaming, state management, và event time processing.",
            "Apache Iceberg table format: hidden partitioning, time travel, schema evolution. So sánh với Delta Lake.",
            "Giải thích *compaction* trong data lake: tại sao cần compact small files? Công cụ và trigger strategy.",
            "Giải thích *Z-ordering* trong Delta Lake / Iceberg. Tại sao giúp data skipping hiệu quả hơn?",
            "Distributed transactions: 2PC (Two-Phase Commit) vs Saga pattern. Khi nào dùng Saga cho data pipeline?",
            "Giải thích *CRDT* (Conflict-free Replicated Data Type): use-case trong distributed systems?",
            "Bloom filter: giải thích và ứng dụng trong Parquet, HBase, Kafka để tăng performance.",
            "Giải thích *hot partition problem* trong Kafka. Cách chọn partition key tốt để phân phối đều?",
            "Apache Hudi: Copy-on-Write vs Merge-on-Read table types. Trade-off giữa read và write performance?",
            "Giải thích *lakehouse* concept: kết hợp data lake và data warehouse. Tại sao đây là xu hướng hiện tại?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XI. System Design cho Data Engineer",
        "color": colors.HexColor("#0E6655"),
        "questions": [
            "Thiết kế data platform cho công ty quảng cáo: 1 tỷ ad impressions/ngày, cần real-time và batch reporting.",
            "Thiết kế pipeline đồng bộ dữ liệu từ 10 nguồn (MySQL, Oracle, REST API, FTP, S3) vào BigQuery.",
            "BigQuery query đang chạy 30 phút, chi phí cao. Quy trình debug và tối ưu từng bước.",
            "Pipeline fail lúc nửa đêm, data không load vào BigQuery. Quy trình xử lý incident.",
            "Thiết kế hệ thống tracking conversion cho chiến dịch quảng cáo: click → purchase, nhiều touch points, deduplication.",
            "Dữ liệu trong Looker dashboard sai lệch so với source. Quy trình điều tra và fix root cause.",
            "Thiết kế data retention policy: raw data 90 ngày, aggregated 2 năm. GCS Lifecycle + BigQuery partitioning.",
            "Thiết kế hệ thống cho phép business user chạy ad-hoc query mà không ảnh hưởng production pipeline.",
            "Multi-tenancy trong data platform: cô lập dữ liệu và compute resource cho nhiều clients/teams.",
            "Disaster recovery cho data pipeline: RTO và RPO. Backup và recovery strategy cho BigQuery và GCS.",
            "Thiết kê A/B testing data pipeline: phân nhóm users, track metrics, tính statistical significance.",
            "Rate limiting và throttling khi gọi external API: exponential backoff, respect API limits.",
            "Push-based vs pull-based data pipeline: ưu/nhược điểm từng cách?",
            "Thiết kế data quality monitoring: tự động phát hiện anomaly (volume drop, null spike, distribution shift).",
            "Thiết kế *event-driven data platform*: mỗi khi data thay đổi, trigger downstream pipeline tự động.",
            "Thiết kế hệ thống *real-time recommendation* cho quảng cáo: từ click event đến serving recommendation < 100ms.",
            "Thiết kế *data sharing platform*: nhiều team/partner có thể query data của nhau với access control chặt chẽ.",
            "Thiết kế pipeline tự động *detect schema drift* và alert khi schema nguồn thay đổi không báo trước.",
            "Giải thích *exactly-once data platform*: từ source extraction đến destination write, không mất và không duplicate.",
            "Thiết kế *cross-cloud data pipeline*: data ở AWS S3, processing ở GCP Dataflow, result vào BigQuery và Redshift.",
            "Thiết kế *data lake governance*: access control, data classification, PII detection, và audit trail.",
            "Thiết kế hệ thống *cost attribution*: theo dõi chi phí BigQuery, GCS, Dataflow cho từng team/project.",
            "Thiết kế *metadata-driven pipeline framework*: config-driven ETL không cần viết code cho mỗi nguồn mới.",
            "Khi có 50 data sources mỗi nguồn có schedule và SLA khác nhau, quản lý dependencies và alerting thế nào?",
            "Thiết kế *hot storage vs cold storage* strategy: query-ready data trong BigQuery, archive trong GCS với lifecycle policy.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XII. API Integration & Web Services",
        "color": colors.HexColor("#17202A"),
        "questions": [
            "REST vs GraphQL vs gRPC: so sánh use-case, performance, phù hợp với data engineering.",
            "OAuth 2.0 flows: Authorization Code, Client Credentials, Device Code. Khi nào dùng Client Credentials?",
            "Viết Python code gọi Google Ads API lấy campaign performance metrics, xử lý pagination, lưu vào BigQuery.",
            "Webhook vs Polling: phân biệt. Khi nào dùng webhook để nhận data từ external system?",
            "Rate limiting: xử lý HTTP 429. Implement retry với exponential backoff và jitter.",
            "API versioning strategies: URL, Header, Query parameter. Ảnh hưởng đến backward compatibility?",
            "Idempotent HTTP methods: PUT và DELETE idempotent còn POST thì không. Tại sao quan trọng?",
            "Thiết kế Python API wrapper class: authentication, retry, rate limiting, logging, error handling.",
            "OpenAPI/Swagger specification: lợi ích khi tài liệu hóa API cho data pipeline integration.",
            "Giải thích CORS và ảnh hưởng đến API calls. Liên quan đến data engineering như thế nào?",
            "Giải thích *pagination strategies*: offset-based, cursor-based, keyset pagination. Cái nào tốt hơn cho large datasets?",
            "Viết code consume Google Analytics 4 Data API: authentication, report request, handle quota limits.",
            "Giải thích *webhook reliability*: retry strategy khi webhook endpoint down. Dead letter, idempotency key.",
            "Tích hợp Meta Ads (Facebook) API: Business SDK, rate limits, versioning policy. Thách thức thực tế?",
            "Giải thích *service mesh* (Istio/Envoy): quan trọng trong microservices data platform. Liên quan đến retry và circuit breaker?",
            "Viết Python code dùng `httpx` async để call nhiều ad platform APIs đồng thời: Google Ads, Meta, TikTok Ads.",
            "Giải thích *API gateway pattern*: Kong, Apigee. Use-case trong data engineering để rate limit và auth external APIs.",
            "Giải thích *long polling* vs *WebSocket* vs *Server-Sent Events*. Khi nào dùng cái nào để nhận real-time data?",
            "Giải thích *JSON:API*, *HAL*, *OData* specifications. Tại sao standardized API format giúp data integration dễ hơn?",
            "Viết Python code tự động handle token refresh (OAuth 2.0 refresh token flow) khi access token hết hạn.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XIII. Monitoring, Observability & Performance",
        "color": colors.HexColor("#117864"),
        "questions": [
            "Ba pillars of observability: Metrics, Logs, Traces. Công cụ GCP cho từng pillar.",
            "SLA, SLO, SLI: phân biệt. Ví dụ với data pipeline: SLO 99.5% freshness trong 2 giờ.",
            "OpenTelemetry: add tracing vào data pipeline để track latency của từng step.",
            "Alerting fatigue: cách thiết kế alert strategy tránh false positives mà không bỏ sót incident thật.",
            "Profiling Python code: `cProfile`, `py-spy`, `memory_profiler`. Tìm bottleneck trong ETL script.",
            "EXPLAIN và EXPLAIN ANALYZE để diagnose slow queries. Patterns cần tránh.",
            "Cost optimization GCP: Committed Use Discounts, Spot VMs, BigQuery slot reservations, GCS lifecycle.",
            "Data freshness monitoring: detect khi pipeline delay và data không cập nhật đúng lịch.",
            "Runbook và Playbook trong incident management. Bạn sẽ viết runbook cho gì với data pipeline?",
            "Load testing cho data pipeline: simulate high load, measure throughput/latency. Công cụ nào?",
            "Giải thích *P99 latency* vs *average latency*. Tại sao P99 quan trọng hơn average cho SLO?",
            "Giải thích *error budget*: nếu SLO là 99.9%, error budget trong 30 ngày là bao nhiêu phút?",
            "Viết Python structured logging cho data pipeline: log với fields như `pipeline_name`, `execution_id`, `duration_ms`.",
            "Giải thích *synthetic monitoring* vs *real user monitoring*. Áp dụng cho data pipeline như thế nào?",
            "Dashboard design best practices: RED method (Rate, Errors, Duration) và USE method (Utilization, Saturation, Errors).",
            "Giải thích *flame graph* trong profiling. Đọc flame graph như thế nào để tìm hotspot?",
            "BigQuery *INFORMATION_SCHEMA.JOBS*: query để monitor expensive queries, slot usage, và billing. Viết query cụ thể.",
            "Giải thích *cardinality* vấn đề trong monitoring systems (Prometheus): tại sao tránh high-cardinality labels?",
            "Giải thích *chaos engineering* (Netflix): áp dụng cho data platform để test resilience.",
            "Thiết kế *data freshness dashboard* trong Looker: hiển thị thời gian cập nhật cuối cùng của từng table quan trọng.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XIV. Security & Compliance trong Data Engineering",
        "color": colors.HexColor("#922B21"),
        "questions": [
            "PII: xử lý và bảo vệ dữ liệu cá nhân trong data pipeline. GDPR và PDPA (Việt Nam) yêu cầu gì?",
            "Data masking vs Data tokenization vs Data encryption: phân biệt và use-case phù hợp.",
            "Column-level security trong BigQuery: Policy Tags và Data Catalog để kiểm soát truy cập cột nhạy cảm.",
            "Row-level security trong BigQuery: RLS để user chỉ thấy data của team/region được phép.",
            "Encryption at rest và in transit: BigQuery và GCS handle encryption thế nào? CMEK là gì?",
            "SQL injection trong dynamic queries: cách tránh khi build query dynamically trong Python.",
            "Audit logging: tại sao cần log ai đã query gì trong BigQuery? Dùng Cloud Audit Logs.",
            "Network security: Private endpoints, VPC Service Controls, Cloud Armor. Ngăn data exfiltration.",
            "Zero trust security model: áp dụng cho data platform như thế nào?",
            "SOC 2, ISO 27001, PCI DSS: data engineer cần biết gì về các compliance framework này?",
            "Giải thích *data classification*: Public, Internal, Confidential, Restricted. Áp dụng vào BigQuery tagging.",
            "Giải thích *RBAC* (Role-Based Access Control) và *ABAC* (Attribute-Based Access Control). BigQuery dùng loại nào?",
            "Giải thích *credential rotation*: tự động rotate service account keys và secrets. Best practice tần suất?",
            "Giải thích *DLP (Data Loss Prevention)* API của GCP: scan và mask PII tự động trong data pipeline.",
            "Viết thiết kế *data access review* process: hàng quý review và revoke quyền truy cập không cần thiết.",
            "Giải thích *supply chain attack* trong data engineering: dependencies, Docker images, và cách mitigate?",
            "Giải thích *SAST* và *DAST* trong security testing. Áp dụng vào CI/CD của data pipeline?",
            "Xử lý *secrets rotation* trong production pipeline không downtime: chiến lược là gì?",
            "Giải thích *data residency* và *data sovereignty*: ảnh hưởng đến thiết kế pipeline cross-region?",
            "Implement *consent management* trong data pipeline: chỉ process data của users đã cho phép marketing.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XV. Containers & Infrastructure",
        "color": colors.HexColor("#1A5276"),
        "questions": [
            "Docker: image, container, layer, Dockerfile, .dockerignore. Giải thích build cache hoạt động như thế nào?",
            "Docker multi-stage build: viết Dockerfile tối ưu cho Python ETL app (builder stage + runtime stage).",
            "Docker networking: bridge, host, overlay network. Khi nào dùng host network?",
            "Docker volumes vs bind mounts: phân biệt và khi nào dùng trong data pipeline container?",
            "Kubernetes cơ bản: Pod, Deployment, Service, ConfigMap, Secret, Namespace. Khi nào cần K8s thay vì Cloud Run?",
            "Kubernetes resource requests và limits: tầm quan trọng khi chạy ETL jobs trên K8s.",
            "Giải thích Kubernetes *Job* và *CronJob*. Dùng để chạy batch ETL pipeline. Retry policy?",
            "Helm charts: tại sao dùng Helm để manage K8s deployments? Viết values.yaml cho ETL application.",
            "GKE (Google Kubernetes Engine) vs Cloud Run: khi nào chọn GKE cho data pipeline workloads?",
            "Giải thích *sidecar pattern* trong Kubernetes: dùng để collect logs, proxy, hoặc sync data?",
            "Terraform best practices: modules, remote state (GCS backend), workspace, và version pinning.",
            "Giải thích *immutable infrastructure*: tại sao không SSH vào server để fix? Liên quan đến data engineering?",
            "Giải thích *container image scanning*: Trivy, Snyk. Integrate vào CI/CD pipeline.",
            "Giải thích *resource quotas* và *LimitRange* trong Kubernetes namespace. Quản lý cost trong shared cluster?",
            "Viết `docker-compose.yml` để local development: Airflow + PostgreSQL + Redis. Giải thích từng service.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XVI. Data Quality & Testing",
        "color": colors.HexColor("#186A3B"),
        "questions": [
            "Giải thích data quality testing trong data pipeline: unit tests, schema tests, referential integrity tests.",
            "Great Expectations: tạo expectation suite, checkpoint, và data docs. So sánh với dbt tests.",
            "dbt tests: `unique`, `not_null`, `accepted_values`, `relationships`. Viết custom generic test.",
            "Giải thích *data contract testing*: consumer-driven contract. Công cụ: Pact, Schemathesis.",
            "Thiết kế data quality *scorecard*: tổng hợp DQ scores theo table, domain, và trend theo thời gian.",
            "Anomaly detection cho data quality: dùng statistical methods (Z-score, IQR) hoặc ML để phát hiện anomaly.",
            "Giải thích *data profiling*: phân tích distribution, uniqueness, nullability, và patterns của data.",
            "Viết dbt snapshot test: đảm bảo số bản ghi không giảm quá 10% so với hôm qua (volume anomaly).",
            "Giải thích *quarantine pattern*: data không pass quality check thì đưa vào quarantine table để review.",
            "Thiết kế *data observability platform*: Monte Carlo, Acceldata, hoặc tự build. Các tính năng cốt lõi?",
            "Giải thích *referential integrity*: tại sao BigQuery không enforce FK? Cách implement bằng dbt tests?",
            "Viết pytest test cho hàm transform: mock BigQuery client, kiểm tra output schema và row count.",
            "Giải thích *golden dataset testing*: so sánh output của pipeline mới vs pipeline cũ trên cùng input.",
            "Giải thích *shadow mode deployment*: chạy pipeline mới song song với pipeline cũ để compare kết quả.",
            "Thiết kế QA checklist trước khi release pipeline mới vào production: các bước cần kiểm tra.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XVII. Machine Learning Engineering cho Data Engineer",
        "color": colors.HexColor("#7D3C98"),
        "questions": [
            "Giải thích MLOps: tại sao data engineer cần biết về MLOps? Vai trò data engineer trong ML pipeline.",
            "Feature engineering: one-hot encoding, target encoding, embedding. Cách implement trong BigQuery SQL.",
            "Giải thích *feature store*: tại sao cần? Online store vs offline store. Vertex AI Feature Store vs Feast.",
            "Train/validation/test split trong time-series data: tại sao không dùng random split? Walk-forward validation là gì?",
            "Giải thích *data leakage*: nguyên nhân và cách phát hiện. Tại sao đặc biệt nguy hiểm?",
            "Thiết kế pipeline cung cấp training data cho ML model: từ raw events đến feature matrix trong BigQuery.",
            "Giải thích *model versioning* và *model registry*: MLflow, Vertex AI Model Registry. Tại sao cần?",
            "Batch inference vs Online inference: thiết kế data pipeline cho mỗi loại.",
            "Giải thích *data drift* và *concept drift*: monitor ML model performance theo thời gian.",
            "Vertex AI Pipelines: tạo ML pipeline YAML/Python SDK. Tích hợp với BigQuery và GCS.",
            "Giải thích *ONNX* (Open Neural Network Exchange): tại sao quan trọng cho model portability?",
            "Thiết kế pipeline tự động retrain model khi data drift được phát hiện. Trigger là gì?",
            "Giải thích *A/B testing cho ML models*: cách route traffic, track metrics, và đánh giá statistical significance.",
            "BigQuery ML: CREATE MODEL, ML.PREDICT, ML.EVALUATE. Khi nào BigQuery ML đủ tốt vs khi nào cần Vertex AI?",
            "Giải thích *class imbalance*: SMOTE, class weights, undersampling. Ảnh hưởng đến training data pipeline?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XVIII. Networking & Distributed Systems Fundamentals",
        "color": colors.HexColor("#1F618D"),
        "questions": [
            "TCP vs UDP: phân biệt. Kafka dùng TCP. Tại sao không dùng UDP cho data streaming?",
            "HTTP/1.1 vs HTTP/2 vs HTTP/3: các cải tiến chính. gRPC dùng HTTP/2, lợi ích gì?",
            "DNS: giải thích A record, CNAME, TTL. Liên quan đến service discovery trong data platform?",
            "TLS/SSL handshake: quá trình diễn ra như thế nào? Tại sao HTTPS quan trọng cho API calls trong pipeline?",
            "Giải thích *load balancer*: L4 vs L7. Cloud Load Balancing trong GCP dùng loại nào cho Cloud Run?",
            "Giải thích *CDN* (Content Delivery Network): áp dụng cho static data assets như thế nào?",
            "NAT Gateway vs Direct Egress: khi nào dùng NAT cho private Cloud Run service gọi ra internet?",
            "Giải thích *service discovery*: Cloud Run dùng DNS-based discovery. Kubernetes dùng kube-dns.",
            "Giải thích *network latency* và *bandwidth*: tại sao latency quan trọng hơn bandwidth trong distributed systems?",
            "VPC Peering vs Shared VPC vs VPN vs Cloud Interconnect: khi nào dùng cái nào để connect on-premise với GCP?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XIX. Quảng cáo & Marketing Technology (Domain Knowledge)",
        "color": colors.HexColor("#784212"),
        "questions": [
            "Giải thích các metrics quảng cáo cơ bản: Impressions, Clicks, CTR, CPC, CPM, CPA, ROAS, ROMI.",
            "Attribution models: First Touch, Last Touch, Linear, Time Decay, Data-Driven. Ưu/nhược từng model?",
            "Giải thích *programmatic advertising*: DSP, SSP, Ad Exchange, DMP. Data engineer xử lý dữ liệu từ đâu?",
            "Cookie và Third-party cookie: tại sao third-party cookie bị deprecated? Ảnh hưởng đến tracking và attribution?",
            "Giải thích *ITP (Intelligent Tracking Prevention)* của Safari và ảnh hưởng đến tracking data.",
            "Google Ads API và Meta Ads API: cấu trúc hierarchy của account (Account → Campaign → AdGroup → Ad).",
            "Giải thích *conversion tracking*: pixel, server-side tracking, và Conversions API (CAPI) của Meta.",
            "UTM parameters: utm_source, utm_medium, utm_campaign, utm_content, utm_term. Cách parse và analyze.",
            "Giải thích *frequency capping* và *reach*: tại sao cần deduplication khi tính unique reach?",
            "Giải thích *viewability*: VAST, VPAID, Open Measurement SDK. Dữ liệu viewability được thu thập thế nào?",
            "Giải thích *Customer Journey*: touchpoints, sessions, và cách model trong data warehouse.",
            "Real-time bidding (RTB): quy trình đấu thầu diễn ra trong < 100ms. Data engineer cần xử lý dữ liệu gì?",
            "Giải thích *lookalike audience*: dùng ML để tìm users tương tự với existing customers. Data pipeline cần gì?",
            "Google Analytics 4 (GA4): event-based model vs session-based (Universal Analytics). Export sang BigQuery?",
            "Giải thích *identity resolution*: match users across devices và channels dùng deterministic vs probabilistic matching.",
            "Giải thích *LTV (Lifetime Value)*: cách tính và predict LTV. Ứng dụng trong targeting quảng cáo.",
            "Giải thích *incrementality testing*: đo lường thực sự quảng cáo có tăng doanh số không. Khác A/B test thế nào?",
            "Giải thích *media mix modeling (MMM)*: phân bổ ngân sách quảng cáo tối ưu. Data requirements là gì?",
            "Giải thích *cross-device tracking*: user dùng nhiều thiết bị. Graph-based identity resolution hoạt động thế nào?",
            "Giải thích Privacy Sandbox của Google (FLEDGE, Topics API, Attribution Reporting API) thay thế third-party cookie.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XX. Soft Skills & Behavioral Questions",
        "color": colors.HexColor("#1B4F72"),
        "questions": [
            "Mô tả dự án data engineering phức tạp nhất bạn từng làm. Thách thức lớn nhất và cách giải quyết?",
            "Bạn phát hiện dữ liệu sai trong production. Bạn làm gì? Quy trình xử lý và báo cáo?",
            "Khi yêu cầu từ business không rõ ràng hoặc có thể dẫn đến thiết kế kỹ thuật không tốt, bạn xử lý thế nào?",
            "Prioritize tasks khi có nhiều deadline cùng lúc và resources hạn chế. Cách bạn quyết định?",
            "Bạn học công nghệ mới như thế nào? Ví dụ về lần tự học công nghệ hoàn toàn mới trong thời gian ngắn.",
            "Đảm bảo code quality trong team: quy trình code review của bạn như thế nào?",
            "Một lần không đồng ý với quyết định kỹ thuật của team lead. Bạn xử lý thế nào?",
            "Tài liệu hóa data pipeline đủ tốt để người mới có thể hiểu và maintain. Cách bạn làm?",
            "Onboard vào dự án mới với codebase phức tạp: chiến lược hiểu hệ thống nhanh nhất là gì?",
            "Describe a time you optimized a slow data pipeline under pressure. What was your approach?",
            "How do you stay updated with the rapidly evolving data engineering landscape?",
            "Làm việc với tài liệu kỹ thuật tiếng Anh hoặc tiếng Nhật không có người hỗ trợ. Bạn xử lý thế nào?",
            "Chịu áp lực cao về deadline và chất lượng sản phẩm cùng lúc. Kết quả như thế nào?",
            "Kinh nghiệm làm việc trong Agile/Scrum: vai trò của Data Engineer trong sprint planning?",
            "Tại sao muốn làm việc trong ngành quảng cáo và marketing technology?",
            "Bạn đã từng phải explain technical concept phức tạp cho stakeholder không có background kỹ thuật. Ví dụ?",
            "Khi bạn phát hiện technical debt lớn trong codebase, bạn propose cải thiện như thế nào mà không gây disrupt?",
            "Bạn làm thế nào để estimate effort cho task data engineering mà bạn chưa từng làm trước đây?",
            "Bạn có kinh nghiệm mentor junior engineer không? Cách bạn guide họ trong data engineering?",
            "Describe a situation where you had to make a trade-off between data quality and delivery speed.",
            "Khi pipeline của bạn break production và bạn chưa biết root cause, bước đầu tiên bạn làm là gì?",
            "Bạn xây dựng mối quan hệ với business stakeholders như thế nào để hiểu rõ data requirements?",
            "Giải thích làm thế nào bạn sẽ onboard một data source mới (ví dụ: một CRM mới) vào data platform hiện tại.",
            "Bạn đã từng phải refactor toàn bộ data pipeline mà không downtime. Cách tiếp cận là gì?",
            "Nếu phỏng vấn thành công và join công ty, 90 ngày đầu tiên của bạn sẽ làm gì?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XXI. Japanese & English Communication",
        "color": colors.HexColor("#117A65"),
        "questions": [
            "JLPT level của bạn? Bạn đã đọc tài liệu kỹ thuật tiếng Nhật chưa? Cho ví dụ cụ thể.",
            "TOEIC score của bạn? Đánh giá kỹ năng tiếng Anh kỹ thuật của bạn.",
            "Dịch: 'データパイプラインの設計において、冪等性を保証することが重要です。'",
            "Dịch: 'ビッグデータ処理において、スキーマの進化を適切に管理することで、ダウンタイムなしにシステムを更新できます。'",
            "Dịch và giải thích: 'バッチ処理とストリーミング処理のトレードオフを理解した上で、適切なアーキテクチャを選択してください。'",
            "Chiến lược đọc tài liệu kỹ thuật tiếng Nhật hiệu quả mà không cần dịch từng từ?",
            "Explain (in English) the concept of idempotency in data pipelines to a non-technical stakeholder.",
            "Explain (in English) why BigQuery uses columnar storage and how it benefits analytical queries.",
            "Explain (in English) the difference between a data lake and a data warehouse to a business manager.",
            "Write a professional email (in English) to a client explaining that their data pipeline will have a 2-hour delay due to upstream issues.",
            "Write a pull request description (in English) for a change that optimizes a BigQuery query from 30 minutes to 2 minutes.",
            "Giải thích concept ETL cho một developer Nhật Bản không có background data engineering bằng tiếng Anh đơn giản.",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XXII. Câu hỏi tình huống & Problem Solving",
        "color": colors.HexColor("#6E2F79"),
        "questions": [
            "BigQuery table của bạn có 500 triệu rows và query P90 là 45 giây. Làm thế nào giảm xuống dưới 5 giây?",
            "Airflow DAG của bạn bị stuck: task đang RUNNING đã 3 tiếng nhưng không có progress. Điều tra và fix thế nào?",
            "Pipeline load data từ API bên ngoài, hôm nay API trả về empty response. Bạn xử lý tình huống này ra sao?",
            "BigQuery billing tháng này tăng đột biến 300% so với tháng trước. Cách điều tra nguyên nhân và fix?",
            "Một developer mới commit thẳng credentials (API key) vào Git public repo. Bạn phản ứng thế nào? Các bước khẩn cấp?",
            "Data trong dashboard sáng nay thấy revenue âm. Root cause analysis từng bước như thế nào?",
            "Pipeline đang chạy ổn 6 tháng, đột nhiên hôm nay fail với lỗi 'Out of Memory'. Nguyên nhân có thể là gì?",
            "Stakeholder yêu cầu báo cáo mới phải xong trong 2 ngày, nhưng data source chưa được ingest. Bạn làm gì?",
            "Phát hiện có data leak: log file bị upload nhầm lên public GCS bucket. Xử lý incident thế nào?",
            "Cần migrate toàn bộ data warehouse từ Redshift sang BigQuery với zero downtime. Kế hoạch chi tiết?",
            "API nguồn thay đổi format response mà không thông báo, pipeline fail. Thiết kế pipeline resilient hơn thế nào?",
            "Business yêu cầu real-time dashboard (< 5 phút freshness) nhưng hiện tại pipeline chạy batch mỗi giờ. Cách approach?",
            "Pipeline xử lý 1 triệu records/ngày, đột nhiên cần xử lý 100 triệu records/ngày do viral campaign. Scale thế nào?",
            "Cần add thêm cột vào BigQuery table đang được hàng chục downstream pipelines và dashboards sử dụng. Approach?",
            "Bạn join công ty, phát hiện toàn bộ data pipeline không có test và documentation. Bạn sẽ cải thiện từ đâu?",
            "Pipeline cần join 2 bảng: fact table 10 tỷ rows và dimension table 1 triệu rows. Cách tối ưu join này?",
            "Dữ liệu từ nguồn A và nguồn B cho cùng metric nhưng cho kết quả khác nhau 5%. Điều tra thế nào?",
            "Cần implement GDPR right-to-erasure: xóa toàn bộ data của một user khỏi data warehouse. Approach?",
            "Nhận được yêu cầu: 'Hãy build thứ gì đó để chúng ta có thể dự đoán ad click-through rate.' Bạn làm gì đầu tiên?",
            "Pipeline nhận event từ mobile app, nhưng 20% events đến muộn > 24 giờ. Thiết kế pipeline xử lý late events?",
        ]
    },
    # -----------------------------------------------------------------------
    {
        "title": "XXIII. Coding Challenges & Algorithms",
        "color": colors.HexColor("#17202A"),
        "questions": [
            "Viết Python function `merge_intervals(intervals)`: nhận list [(1,3),(2,6),(8,10)] trả về [(1,6),(8,10)].",
            "Viết Python function tính số lần xuất hiện của mỗi từ trong file text lớn, sử dụng ít memory nhất có thể.",
            "Implement một LRU Cache bằng Python mà không dùng `functools.lru_cache`.",
            "Viết Python function `flatten(lst)` làm phẳng nested list bất kỳ độ sâu: `[[1,[2,3]],[4]]` → `[1,2,3,4]`.",
            "Viết Python generator `chunk(iterable, size)` chia iterable thành chunks kích thước cố định.",
            "Viết SQL: từ bảng `events(user_id, event_time, event_type)`, tìm users đã thực hiện event 'purchase' trong vòng 24h sau 'add_to_cart'.",
            "Viết Python code sort 1 tỷ integers từ file, memory limit 1 GB. Dùng thuật toán gì? (External Sort)",
            "Viết Python function detect và remove cycle trong linked list dùng Floyd's algorithm.",
            "Viết SQL tìm median salary trong bảng employees mà không dùng hàm MEDIAN().",
            "Viết Python function kiểm tra xem một JSON object có match với một JSON Schema đơn giản không.",
            "Viết Python function `retry_with_backoff(func, max_retries, base_delay)` với jitter.",
            "Viết Python code đọc Parquet file từ GCS, lọc rows theo điều kiện, và ghi kết quả vào BigQuery.",
            "Viết SQL query: mỗi user, tìm 3 sản phẩm gần đây nhất họ đã xem, formatted thành một string ngăn cách bởi dấu phẩy.",
            "Viết Python script so sánh schema của 2 BigQuery tables và in ra danh sách các cột khác nhau.",
            "Implement thread-safe singleton pattern trong Python cho database connection pool.",
            "Viết Python function parse log line: `2024-01-15 10:23:45 ERROR [pipeline] Failed to load table: row_count=0` thành dict.",
            "Viết SQL: từ bảng `transactions(id, user_id, amount, created_at)`, tìm users có 3 giao dịch liên tiếp tăng dần.",
            "Viết Python context manager `timer()` đo và log thời gian thực thi của code block.",
            "Viết Python code tự động paginate API endpoint và collect tất cả results (có thể có hàng triệu records).",
            "Viết SQL dùng window function tính cumulative revenue và ngày đầu tiên revenue vượt mốc 1 triệu đô.",
        ]
    },
]

# ==========================================================================
# PDF generation
# ==========================================================================

def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Bộ câu hỏi ôn tập – Data Engineer (DAC Data Technology)",
        author="Tự động sinh bởi script",
    )

    styles = getSampleStyleSheet()

    cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#1A3A5C"),
        spaceAfter=10,
        alignment=TA_CENTER,
    )
    cover_sub = ParagraphStyle(
        "CoverSub",
        parent=styles["Normal"],
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#5D6D7E"),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    section_title_base = ParagraphStyle(
        "SectionTitleBase",
        parent=styles["Heading1"],
        fontSize=12,
        leading=16,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.white,
        leftIndent=4,
        rightIndent=4,
        borderPad=4,
    )
    question_style = ParagraphStyle(
        "Question",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14,
        spaceAfter=5,
        leftIndent=12,
        firstLineIndent=-12,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1C2833"),
    )
    note_style = ParagraphStyle(
        "Note",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#717D7E"),
        alignment=TA_CENTER,
    )
    toc_title_style = ParagraphStyle(
        "TocTitle",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#1A3A5C"),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    toc_item_style = ParagraphStyle(
        "TocItem",
        parent=styles["Normal"],
        fontSize=9,
        leading=14,
        leftIndent=16,
    )

    story = []

    # ── Cover ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("BỘ CÂU HỎI ÔN TẬP TOÀN DIỆN", cover_title))
    story.append(Paragraph("Vị trí: DATA ENGINEER", cover_title))
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1A5276"), hAlign="CENTER"))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("DAC Data Technology Vietnam – Hakuhodo DY One", cover_sub))
    story.append(Paragraph("Da Nang Office  |  Full-time  |  Tháng 9 / 2026", cover_sub))
    story.append(Spacer(1, 1 * cm))

    total_q = sum(len(s["questions"]) for s in SECTIONS)
    stats = [
        ["Tổng số câu hỏi", str(total_q)],
        ["Số chủ đề", str(len(SECTIONS))],
        ["Cấp độ", "Junior → Senior"],
        ["Ngôn ngữ", "Tiếng Việt + English"],
    ]
    stat_table = Table(stats, colWidths=[7 * cm, 6 * cm])
    stat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D6EAF8")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#EBF5FB")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1A3A5C")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AED6F1")),
        ("ROWHEIGHT", (0, 0), (-1, -1), 22),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "Tài liệu được tổng hợp từ JD chính thức của DAC Data Technology Vietnam. "
        "Câu hỏi bao phủ toàn bộ kỹ năng: Python, Java, SQL, GCP, ETL, CI/CD, "
        "Looker, AWS, Big Data, System Design, Security, MLOps, Domain Knowledge và Soft Skills.",
        note_style,
    ))
    story.append(PageBreak())

    # ── Table of Contents ─────────────────────────────────────────────────
    story.append(Paragraph("MỤC LỤC", toc_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#AED6F1")))
    story.append(Spacer(1, 0.3 * cm))
    for sec in SECTIONS:
        n = len(sec["questions"])
        story.append(Paragraph(f"• {sec['title']}  ({n} câu)", toc_item_style))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(f"Tổng cộng: {total_q} câu hỏi / {len(SECTIONS)} chủ đề", note_style))
    story.append(PageBreak())

    # ── Sections ──────────────────────────────────────────────────────────
    q_global = 1
    for sec in SECTIONS:
        sec_style = ParagraphStyle(
            f"SecH_{q_global}",
            parent=section_title_base,
            backColor=sec["color"],
        )
        story.append(KeepTogether([
            Paragraph(sec["title"], sec_style),
            Spacer(1, 0.15 * cm),
        ]))

        for i, q in enumerate(sec["questions"], 1):
            q_text = f"<b>Câu {q_global}.</b>  {q}"
            story.append(Paragraph(q_text, question_style))
            if i % 5 == 0 and i < len(sec["questions"]):
                story.append(HRFlowable(
                    width="95%", thickness=0.25,
                    color=colors.HexColor("#D5D8DC"), hAlign="CENTER",
                ))
            q_global += 1

        story.append(Spacer(1, 0.4 * cm))

    # ── Footer ────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#AED6F1")))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        f"Tổng cộng {total_q} câu hỏi  •  {len(SECTIONS)} chủ đề  "
        f"•  Chúc bạn ôn tập tốt và thành công trong buổi phỏng vấn tại DAC Data Technology Vietnam!",
        note_style,
    ))

    doc.build(story)
    print(f"✅ PDF created: {output_path}")
    print(f"   Total questions : {total_q}")
    print(f"   Total sections  : {len(SECTIONS)}")
    for sec in SECTIONS:
        print(f"   {sec['title']}: {len(sec['questions'])} câu")


if __name__ == "__main__":
    out = "/workspace/Data_Engineer_Interview_Questions.pdf"
    build_pdf(out)
