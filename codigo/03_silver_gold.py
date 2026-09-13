import pandas as pd
import os

# =========================
# CAMADA SILVER
# =========================

# Seleciona somente os campos necessários dos pedidos válidos
colunas_uteis = [
    "pedido_id",
    "cliente_id",
    "product_id",
    "quantidade"
]

df_pedidos_validos = pedidos_validos[colunas_uteis].copy()

# JOIN com a dimensão de clientes
df_silver = df_pedidos_validos.merge(
    clientes[["cliente_id", "nome", "uf"]],
    on="cliente_id",
    how="inner"
)

# JOIN com a dimensão de produtos
df_silver = df_silver.merge(
    produtos[
        ["product_id", "descricao", "categoria", "preco"]
    ],
    on="product_id",
    how="inner"
)

# Cálculo do valor total
df_silver["valor_total"] = (
    df_silver["quantidade"] * df_silver["preco"]
)

# Organização das colunas
df_silver = df_silver[
    [
        "pedido_id",
        "cliente_id",
        "nome",
        "uf",
        "product_id",
        "descricao",
        "categoria",
        "quantidade",
        "preco",
        "valor_total"
    ]
]

# Salva a camada Silver em Parquet com compressão Snappy
os.makedirs("processed/fato_vendas", exist_ok=True)

df_silver.to_parquet(
    "processed/fato_vendas/vendas_silver.parquet",
    index=False,
    compression="snappy"
)


# =========================
# CAMADA GOLD
# =========================

# Agregação por UF e categoria
df_gold = (
    df_silver
    .groupby(
        ["uf", "categoria"],
        as_index=False
    )
    .agg(
        quantidade_total=("quantidade", "sum"),
        faturamento_total=("valor_total", "sum"),
        total_pedidos=("pedido_id", "count")
    )
)

# Ordena pelo maior faturamento
df_gold = df_gold.sort_values(
    by="faturamento_total",
    ascending=False
)

# Salva a camada Gold em Parquet com compressão Snappy
os.makedirs("gold/analytics_vendas", exist_ok=True)

df_gold.to_parquet(
    "gold/analytics_vendas/resumo_uf_categoria.parquet",
    index=False,
    compression="snappy"
)

print("Camadas Silver e Gold criadas com sucesso!")
print(f"Registros Silver: {len(df_silver)}")
print(f"Registros Gold: {len(df_gold)}")
print(
    f"Faturamento total: "
    f"R$ {df_silver['valor_total'].sum():.2f}"
)
