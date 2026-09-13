-- ============================================
-- ATIVIDADE 2 - AUDITORIA DE METADADOS
-- ============================================

SELECT
    pedido_id,
    uf,
    categoria,
    valor_total,
    "$path",
    "$file_size"
FROM atividade2.fato_vendas;
