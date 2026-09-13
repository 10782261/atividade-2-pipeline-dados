CREATE DATABASE IF NOT EXISTS atividade2;

CREATE EXTERNAL TABLE atividade2.clientes (
    cliente_id INT,
    nome STRING,
    uf STRING
)
PARTITIONED BY (ingest_date STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar'=','
)
STORED AS TEXTFILE
LOCATION 's3://atividade2-pipeline-mariana10782261-2026/raw/clientes/';

CREATE EXTERNAL TABLE atividade2.produtos (
    product_id INT,
    descricao STRING,
    categoria STRING,
    preco DOUBLE
)
PARTITIONED BY (ingest_date STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar'=','
)
STORED AS TEXTFILE
LOCATION 's3://atividade2-pipeline-mariana10782261-2026/raw/produtos/';

CREATE EXTERNAL TABLE atividade2.pedidos (
    pedido_id INT,
    cliente_id INT,
    product_id INT,
    quantidade INT
)
PARTITIONED BY (ingest_date STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar'=','
)
STORED AS TEXTFILE
LOCATION 's3://atividade2-pipeline-mariana10782261-2026/raw/pedidos/';

ALTER TABLE atividade2.clientes
SET TBLPROPERTIES ('skip.header.line.count'='1');

ALTER TABLE atividade2.produtos
SET TBLPROPERTIES ('skip.header.line.count'='1');

ALTER TABLE atividade2.pedidos
SET TBLPROPERTIES ('skip.header.line.count'='1');

MSCK REPAIR TABLE atividade2.clientes;
MSCK REPAIR TABLE atividade2.produtos;
MSCK REPAIR TABLE atividade2.pedidos;
