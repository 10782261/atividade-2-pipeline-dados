-- ============================================
-- ATIVIDADE 2 - QUARENTENA
-- Tabela para consulta dos pedidos rejeitados
-- ============================================

CREATE EXTERNAL TABLE atividade2.pedidos_rejeitados (
    pedido_id INT,
    cliente_id INT,
    product_id INT,
    quantidade INT,
    motivo_rejeicao STRING
)
PARTITIONED BY (
    data STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://atividade2-pipeline-mariana10782261-2026/quarantine/pedidos_rejeitados/';
