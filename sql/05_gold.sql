-- ============================================
-- ATIVIDADE 2 - CAMADA GOLD
-- Tabela analytics_vendas
-- ============================================

CREATE EXTERNAL TABLE atividade2.analytics_vendas (
    uf STRING,
    categoria STRING,
    quantidade_total BIGINT,
    faturamento_total DOUBLE,
    total_pedidos BIGINT
)
STORED AS PARQUET
LOCATION 's3://atividade2-pipeline-mariana10782261-2026/gold/analytics_vendas/';
