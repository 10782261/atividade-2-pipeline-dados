# Atividade 2 - Pipeline de Dados com Amazon S3 e Amazon Athena

## 1. Objetivo

Esta atividade tem como objetivo desenvolver um pipeline de dados utilizando Amazon S3 e Amazon Athena, aplicando conceitos de ingestão, qualidade de dados, tratamento de registros inválidos e arquitetura em camadas.

O pipeline foi desenvolvido considerando as camadas Raw, Silver e Gold, além de uma área de quarentena para os registros rejeitados durante as validações de qualidade.

---

## 2. Tecnologias utilizadas

- Python
- Pandas
- PyArrow
- Amazon S3
- Amazon Athena
- SQL
- GitHub

---

## 3. Arquitetura do pipeline

O fluxo de processamento foi estruturado da seguinte forma:

**Dados simulados → RAW → Data Quality → SILVER → GOLD → Amazon Athena**

Os registros considerados inválidos durante a validação de qualidade são direcionados para a área de **Quarantine**.

---

## 4. Geração dos dados

Foram criadas três tabelas de dados simulados:

- Clientes
- Produtos
- Pedidos

Os dados de pedidos foram gerados contendo registros válidos e registros propositalmente inválidos, permitindo testar as regras de qualidade de dados.

Entre as anomalias inseridas estão:

- quantidades menores ou iguais a zero;
- cliente inexistente;
- produto inexistente.

---

## 5. Camada Raw

Os arquivos CSV foram armazenados no Amazon S3 utilizando particionamento por data de ingestão.

Estrutura utilizada:

raw/  
├── clientes/  
│   └── ingest_date=2026-09-13/  
│       └── clientes.csv  
├── produtos/  
│   └── ingest_date=2026-09-13/  
│       └── produtos.csv  
└── pedidos/  
    └── ingest_date=2026-09-13/  
        └── pedidos.csv  

Essa organização facilita a identificação da data de ingestão e a consulta dos dados no Amazon Athena.

---

## 6. Data Quality

Foram aplicadas regras de validação sobre os pedidos.

Um registro é considerado inválido quando:

- quantidade <= 0;
- cliente_id não existe na tabela de clientes;
- product_id não existe na tabela de produtos.

Após a aplicação das regras, foram identificados:

- 10 pedidos no Raw;
- 5 pedidos válidos;
- 5 pedidos rejeitados.

Os registros inválidos foram direcionados para a área de quarentena.

---

## 7. Quarantine

Os registros rejeitados foram armazenados em formato JSON no Amazon S3.

Estrutura:

Dados simulados → RAW → Data Quality → SILVER → GOLD → Amazon Athena

Além dos dados originais, os registros armazenam o motivo da rejeição, permitindo rastrear por que cada pedido foi considerado inválido.

---

## 8. Camada Silver

A camada Silver foi construída utilizando somente os pedidos considerados válidos.

Foi realizado o enriquecimento dos pedidos por meio de JOIN com as tabelas de clientes e produtos.

Foram adicionadas informações como:

- Nome do cliente
- UF
- Descrição do produto
- Categoria
- Preço

Também foi calculado o campo:

`valor_total = quantidade * preco`

O resultado foi armazenado em formato Parquet com compressão Snappy.

Localização no S3:

`processed/fato_vendas/vendas_silver.parquet`

O resultado da camada Silver possui 5 registros válidos e faturamento total de R$ 8.120,00.

---

## 9. Camada Gold

A camada Gold apresenta uma visão agregada para análise dos dados.

Os dados foram agrupados por:

- UF
- Categoria

Foram calculados os seguintes indicadores:

- Quantidade total
- Faturamento total
- Total de pedidos

O resultado foi armazenado em formato Parquet com compressão Snappy.

Localização no S3:

`gold/analytics_vendas/resumo_uf_categoria.parquet`

O faturamento total apresentado na camada Gold é de R$ 8.120,00.

---

## 10. Amazon Athena

O Amazon Athena foi utilizado para consultar e validar as diferentes camadas do pipeline.

Foram criadas tabelas externas para:

- Clientes
- Produtos
- Pedidos
- Pedidos rejeitados
- Fato de vendas (Silver)
- Analytics de vendas (Gold)

Também foram realizadas consultas de auditoria utilizando os metadados:

- `$path`
- `$file_size`

Essas consultas permitiram validar o caminho físico e o tamanho dos arquivos armazenados no Amazon S3.

---

## 11. Reconciliação

Foi realizada uma reconciliação entre os registros do Raw, Silver e Quarantine.

Resultado:

- Total Raw = 10
- Total Silver = 5
- Total rejeitados = 5

A validação demonstra que:

`5 registros válidos + 5 registros rejeitados = 10 registros do Raw`

Dessa forma, os registros foram contabilizados durante o processo de tratamento.

---

## 12. Estrutura do projeto

atividade-2-pipeline-dados/  
├── codigo/  
│   ├── 01_gerar_dados.py  
│   ├── 02_data_quality.py  
│   ├── 03_silver_gold.py  
│   └── requirements.txt  
├── sql/  
│   ├── 01_criar_tabelas_raw.sql  
│   ├── 02_data_quality.sql  
│   ├── 03_quarentena.sql  
│   ├── 04_silver.sql  
│   ├── 05_gold.sql  
│   ├── 06_auditoria_metadados.sql  
│   └── 07_reconciliacao.sql  
├── 01_raw_clientes.png  
├── 02_raw_produtos.png  
├── 03_raw_pedidos.png  
├── 04_data_quality.png  
├── 05_silver.png  
├── 06_path_file_size.png  
└── README.md  

---

## 13. Evidências

As imagens disponíveis neste repositório apresentam evidências das consultas realizadas no Amazon Athena, incluindo:

- Dados das tabelas Raw
- Identificação dos registros rejeitados
- Resultado da camada Silver
- Auditoria de metadados com `$path` e `$file_size`

---

## 14. Como executar

### Geração dos dados

Os dados podem ser gerados utilizando os scripts Python disponíveis na pasta `codigo/`.

1. Executar `01_gerar_dados.py` para gerar os dados de clientes, produtos e pedidos.
2. Executar `02_data_quality.py` para aplicar as regras de qualidade e separar os registros válidos e rejeitados.
3. Executar `03_silver_gold.py` para gerar as camadas Silver e Gold.

### Consultas no Amazon Athena

Após o carregamento dos arquivos no Amazon S3:

1. Criar o banco de dados `atividade2`.
2. Executar os scripts SQL disponíveis na pasta `sql/`.
3. Executar `MSCK REPAIR TABLE` nas tabelas particionadas quando necessário.
4. Consultar as tabelas pelo Amazon Athena.
5. Executar as consultas de auditoria e reconciliação.

---

## 15. Estrutura no Amazon S3

`s3://atividade2-pipeline-mariana10782261-2026/`

- `raw/clientes/ingest_date=2026-09-13/clientes.csv`
- `raw/produtos/ingest_date=2026-09-13/produtos.csv`
- `raw/pedidos/ingest_date=2026-09-13/pedidos.csv`
- `quarantine/pedidos_rejeitados/data=2026-09-13/rejeitados.json`
- `processed/fato_vendas/vendas_silver.parquet`
- `gold/analytics_vendas/resumo_uf_categoria.parquet`
- `athena-results/`

---

## 16. Considerações finais

O projeto permitiu aplicar, na prática, conceitos de Engenharia de Dados, desde a ingestão dos dados até sua disponibilização para análise.

A utilização das camadas Raw, Silver e Gold, juntamente com a área de Quarantine, possibilitou organizar os dados, tratar registros inválidos e manter a rastreabilidade do processo.

As consultas realizadas no Amazon Athena e a reconciliação dos registros também permitiram validar a consistência dos dados processados.
