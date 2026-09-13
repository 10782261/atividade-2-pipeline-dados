import pandas as pd
import os
from datetime import date

# Data de ingestão
data_ingestao = str(date.today())

# =========================
# CLIENTES
# =========================

clientes = pd.DataFrame([
    {"cliente_id": 1, "nome": "Ana Silva", "uf": "SP"},
    {"cliente_id": 2, "nome": "Bruno Santos", "uf": "RJ"},
    {"cliente_id": 3, "nome": "Carla Oliveira", "uf": "MG"},
    {"cliente_id": 4, "nome": "Daniel Costa", "uf": "PR"},
    {"cliente_id": 5, "nome": "Eduarda Lima", "uf": "SC"},
])

# =========================
# PRODUTOS
# =========================

produtos = pd.DataFrame([
    {"product_id": 101, "descricao": "Notebook", "categoria": "Eletronicos", "preco": 3500.00},
    {"product_id": 102, "descricao": "Mouse", "categoria": "Acessorios", "preco": 120.00},
    {"product_id": 103, "descricao": "Teclado", "categoria": "Acessorios", "preco": 180.00},
    {"product_id": 104, "descricao": "Monitor", "categoria": "Eletronicos", "preco": 900.00},
    {"product_id": 105, "descricao": "Cadeira", "categoria": "Moveis", "preco": 750.00},
])

# =========================
# PEDIDOS
# =========================

pedidos = pd.DataFrame([
    # Registros válidos
    {"pedido_id": 1001, "cliente_id": 1, "product_id": 101, "quantidade": 1},
    {"pedido_id": 1002, "cliente_id": 2, "product_id": 102, "quantidade": 2},
    {"pedido_id": 1003, "cliente_id": 3, "product_id": 103, "quantidade": 1},
    {"pedido_id": 1004, "cliente_id": 4, "product_id": 104, "quantidade": 3},
    {"pedido_id": 1005, "cliente_id": 5, "product_id": 105, "quantidade": 2},

    # Anomalias intencionais
    {"pedido_id": 1006, "cliente_id": 1, "product_id": 101, "quantidade": -2},
    {"pedido_id": 1007, "cliente_id": 2, "product_id": 102, "quantidade": 0},
    {"pedido_id": 1008, "cliente_id": 999, "product_id": 103, "quantidade": 2},
    {"pedido_id": 1009, "cliente_id": 3, "product_id": 999, "quantidade": 1},
    {"pedido_id": 1010, "cliente_id": 888, "product_id": 777, "quantidade": -1},
])

# =========================
# GERAÇÃO DA CAMADA RAW
# =========================

os.makedirs(f"raw/clientes/ingest_date={data_ingestao}", exist_ok=True)
os.makedirs(f"raw/produtos/ingest_date={data_ingestao}", exist_ok=True)
os.makedirs(f"raw/pedidos/ingest_date={data_ingestao}", exist_ok=True)

clientes.to_csv(
    f"raw/clientes/ingest_date={data_ingestao}/clientes.csv",
    index=False
)

produtos.to_csv(
    f"raw/produtos/ingest_date={data_ingestao}/produtos.csv",
    index=False
)

pedidos.to_csv(
    f"raw/pedidos/ingest_date={data_ingestao}/pedidos.csv",
    index=False
)

print("Dados gerados com sucesso!")
print(f"Data de ingestão: {data_ingestao}")
print(f"Clientes: {len(clientes)}")
print(f"Produtos: {len(produtos)}")
print(f"Pedidos: {len(pedidos)}")
