
import duckdb
from pathlib import Path

# Localiza o arquivo Parquet na mesma pasta do programa
arquivo = Path(__file__).resolve().parent / "vendas.parquet"

# Conecta ao DuckDB
conexao = duckdb.connect()

# Verifica se existem vendas com valores invalidos
quantidade_invalidos = conexao.execute(
    """
    SELECT COUNT(*)
    FROM read_parquet(?)
    WHERE valor <= 0 OR valor IS NULL
    """,
    [str(arquivo)]
).fetchone()[0]

if quantidade_invalidos > 0:
    raise ValueError(
        "Consulta bloqueada: existem vendas com valores invalidos."
    )

# Verifica se existem IDs de vendas duplicados
quantidade_duplicados = conexao.execute(
    """
    SELECT COUNT(*)
    FROM (
        SELECT id_venda
        FROM read_parquet(?)
        GROUP BY id_venda
        HAVING COUNT(*) > 1
    )
    """,
    [str(arquivo)]
).fetchone()[0]

if quantidade_duplicados > 0:
    raise ValueError(
        "Consulta bloqueada: existem IDs duplicados."
    )

# Consulta o faturamento total
resultado = conexao.execute(
    """
    SELECT SUM(valor) AS faturamento_total
    FROM read_parquet(?)
    """,
    [str(arquivo)]
).fetchone()

print("Faturamento total: R$", resultado[0])

# Fecha a conexão
conexao.close()
