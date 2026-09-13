import pandas as pd
import os

# =========================
# DATA QUALITY
# =========================

# Verifica se as chaves existem nas tabelas dimensionais
pedidos_dq = pedidos.copy()

pedidos_dq["cliente_existe"] = pedidos_dq["cliente_id"].isin(
    clientes["cliente_id"]
)

pedidos_dq["produto_existe"] = pedidos_dq["product_id"].isin(
    produtos["product_id"]
)


# Identifica o motivo da rejeição
def identificar_motivo(row):
    motivos = []

    if row["quantidade"] <= 0:
        motivos.append("quantidade <= 0")

    if not row["cliente_existe"]:
        motivos.append("cliente_id inexistente")

    if not row["produto_existe"]:
        motivos.append("product_id inexistente")

    return "; ".join(motivos)


pedidos_dq["motivo_rejeicao"] = pedidos_dq.apply(
    identificar_motivo,
    axis=1
)


# =========================
# SEPARAÇÃO DOS REGISTROS
# =========================

pedidos_invalidos = pedidos_dq[
    pedidos_dq["motivo_rejeicao"] != ""
].copy()

pedidos_validos = pedidos_dq[
    pedidos_dq["motivo_rejeicao"] == ""
].copy()


# =========================
# QUARENTENA
# =========================

quarentena = pedidos_invalidos[
    [
        "pedido_id",
        "cliente_id",
        "product_id",
        "quantidade",
        "motivo_rejeicao"
    ]
].copy()


os.makedirs(
    "quarantine/pedidos_rejeitados/data=2026-09-13",
    exist_ok=True
)


# JSON no formato NDJSON, compatível com Athena
quarentena.to_json(
    "quarantine/pedidos_rejeitados/data=2026-09-13/rejeitados.json",
    orient="records",
    lines=True,
    force_ascii=False
)


print("Validação concluída!")
print(f"Total de pedidos: {len(pedidos)}")
print(f"Pedidos válidos: {len(pedidos_validos)}")
print(f"Pedidos rejeitados: {len(pedidos_invalidos)}")
