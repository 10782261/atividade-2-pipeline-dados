-- ============================================
-- ATIVIDADE 2 - CAMADA SILVER
-- Tabela fato_vendas
-- ============================================

CREATE EXTERNAL TABLE atividade2.fato_vendas (
    pedido_id INT,
    cliente_id INT,
    nome STRING,
    uf STRING,
    product_id INT,
    descricao STRING,
    categoria STRING,
    quantidade INT,
    preco DOUBLE,
    valor_total DOUBLE
)
STORED AS PARQUET
LOCATION 's3://atividade2-pipeline-mariana10782261-2026/processed/fato_vendas/';
