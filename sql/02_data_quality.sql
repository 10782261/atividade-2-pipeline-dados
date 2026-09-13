SELECT
    p.pedido_id,
    p.cliente_id,
    p.product_id,
    p.quantidade,

    CONCAT_WS(
        '; ',
        CASE
            WHEN p.quantidade <= 0
            THEN 'quantidade <= 0'
        END,
        CASE
            WHEN c.cliente_id IS NULL
            THEN 'cliente_id inexistente'
        END,
        CASE
            WHEN pr.product_id IS NULL
            THEN 'product_id inexistente'
        END
    ) AS motivo_rejeicao

FROM atividade2.pedidos p

LEFT JOIN atividade2.clientes c
    ON p.cliente_id = c.cliente_id

LEFT JOIN atividade2.produtos pr
    ON p.product_id = pr.product_id

WHERE
    p.quantidade <= 0
    OR c.cliente_id IS NULL
    OR pr.product_id IS NULL;
