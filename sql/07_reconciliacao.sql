-- ============================================
-- ATIVIDADE 2 - RECONCILIAÇÃO DOS DADOS
-- Validação da integridade do pipeline
-- ============================================

SELECT
    (SELECT COUNT(*) FROM atividade2.pedidos) AS total_raw,
    (SELECT COUNT(*) FROM atividade2.fato_vendas) AS total_silver,
    (SELECT COUNT(*) FROM atividade2.pedidos_rejeitados) AS total_rejeitados,
    (SELECT COUNT(*) FROM atividade2.fato_vendas)
      + (SELECT COUNT(*) FROM atividade2.pedidos_rejeitados) AS silver_mais_rejeitados;
