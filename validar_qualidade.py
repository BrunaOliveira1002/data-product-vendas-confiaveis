
import duckdb
from pathlib import Path

# Localiza a pasta principal do projeto
projeto = Path(__file__).resolve().parents[2]

# Localiza o arquivo com os dados de vendas

arquivo = Path(__file__).resolve().parent / "vendas.parquet"
# Lê os dados do arquivo Parquet
conexao = duckdb.connect()
vendas = conexao.execute(
    "SELECT * FROM read_parquet(?)",
    [str(arquivo)]
).fetchall()

print("Dados encontrados:")
for venda in vendas:
    print(venda)

# Verifica se existem vendas com valores inválidos

vendas_invalidas = conexao.execute(
    "SELECT * FROM read_parquet(?) WHERE valor <= 0 OR valor IS NULL",
    [str(arquivo)]
).fetchall()

if not vendas_invalidas:
    print("QUALIDADE OK: Todas as vendas possuem valores positivos.")
else:
    print("ATENCAO: Foram encontradas vendas com valores invalidos.")
    print(vendas_invalidas)


# Verifica identificadores de vendas duplicados
duplicados = conexao.execute(
    """
    SELECT id_venda, COUNT(*) AS quantidade
    FROM read_parquet(?)
    GROUP BY id_venda
    HAVING COUNT(*) > 1
    """,
    [str(arquivo)]
).fetchall()

if not duplicados:
    print("QUALIDADE OK: Nenhum ID de venda duplicado.")
else:
    print("ATENCAO: Foram encontrados IDs duplicados.")
    print(duplicados)
# Verifica vendas com identificadores nulos
ids_nulos = conexao.execute(
    """
    SELECT COUNT(*)
    FROM read_parquet(?)
    WHERE id_venda IS NULL
    """,
    [str(arquivo)]
).fetchone()[0]

if ids_nulos == 0:
    print("QUALIDADE OK: Nenhum ID de venda nulo.")
else:
    print(f"ATENCAO: Foram encontrados {ids_nulos} IDs nulos.")

conexao.close()
