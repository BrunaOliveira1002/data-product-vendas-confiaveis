import subprocess
import sys
from pathlib import Path

import duckdb


PROJETO = Path(__file__).resolve().parents[1]


def test_bloqueia_id_nulo(tmp_path):
    # Cria um arquivo Parquet temporario
    arquivo_teste = tmp_path / "vendas.parquet"

    conexao = duckdb.connect()
    conexao.execute(
        """
        COPY (
            SELECT
                CAST(NULL AS INTEGER) AS id_venda,
                'Ana' AS cliente,
                'Notebook' AS produto,
                3500 AS valor
        )
        TO ? (FORMAT PARQUET)
        """.replace("TO ?", f"TO '{arquivo_teste.as_posix()}'")
    )
    conexao.close()

    # Copia o script para a pasta temporaria
    script = tmp_path / "consulta_financeiro.py"
    script.write_bytes(
        (PROJETO / "consulta_financeiro.py").read_bytes()
    )

    # Executa a consulta utilizando os dados de teste
    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )

    # Confirma que a consulta foi bloqueada
    assert resultado.returncode != 0
    assert "IDs nulos" in resultado.stderr

def test_bloqueia_id_duplicado(tmp_path):
    arquivo_teste = tmp_path / "vendas.parquet"

    conexao = duckdb.connect()
    conexao.execute(f"""
        COPY (
            SELECT 1 AS id_venda, 'Ana' AS cliente,
                   'Notebook' AS produto, 3500 AS valor
            UNION ALL
            SELECT 1, 'Bruno', 'Mouse', 80
        )
        TO '{arquivo_teste.as_posix()}'
        (FORMAT PARQUET)
    """)
    conexao.close()

    script = tmp_path / "consulta_financeiro.py"
    script.write_bytes(
        (PROJETO / "consulta_financeiro.py").read_bytes()
    )

    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )

    assert resultado.returncode != 0
    assert "IDs duplicados" in resultado.stderr

def test_bloqueia_valor_negativo(tmp_path):
    arquivo_teste = tmp_path / "vendas.parquet"

    conexao = duckdb.connect()
    conexao.execute(f"""
        COPY (
            SELECT
                1 AS id_venda,
                'Ana' AS cliente,
                'Notebook' AS produto,
                -3500 AS valor
        )
        TO '{arquivo_teste.as_posix()}'
        (FORMAT PARQUET)
    """)
    conexao.close()

    script = tmp_path / "consulta_financeiro.py"
    script.write_bytes(
        (PROJETO / "consulta_financeiro.py").read_bytes()
    )

    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )

    assert resultado.returncode != 0
    assert "valores invalidos" in resultado.stderr

def test_bloqueia_valor_zero(tmp_path):
    arquivo_teste = tmp_path / "vendas.parquet"

    conexao = duckdb.connect()
    conexao.execute(f"""
        COPY (
            SELECT
                1 AS id_venda,
                'Ana' AS cliente,
                'Notebook' AS produto,
                0 AS valor
        )
        TO '{arquivo_teste.as_posix()}'
        (FORMAT PARQUET)
    """)
    conexao.close()

    script = tmp_path / "consulta_financeiro.py"
    script.write_bytes(
        (PROJETO / "consulta_financeiro.py").read_bytes()
    )

    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )

    assert resultado.returncode != 0
    assert "valores invalidos" in resultado.stderr

def test_bloqueia_valor_nulo(tmp_path):
    arquivo_teste = tmp_path / "vendas.parquet"

    conexao = duckdb.connect()
    conexao.execute(f"""
        COPY (
            SELECT
                1 AS id_venda,
                'Ana' AS cliente,
                'Notebook' AS produto,
                CAST(NULL AS INTEGER) AS valor
        )
        TO '{arquivo_teste.as_posix()}'
        (FORMAT PARQUET)
    """)
    conexao.close()

    script = tmp_path / "consulta_financeiro.py"
    script.write_bytes(
        (PROJETO / "consulta_financeiro.py").read_bytes()
    )

    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )

    assert resultado.returncode != 0
    assert "valores invalidos" in resultado.stderr

def test_calcula_faturamento_correto(tmp_path):
    arquivo_teste = tmp_path / "vendas.parquet"

    conexao = duckdb.connect()
    conexao.execute(f"""
        COPY (
            SELECT 1 AS id_venda, 'Ana' AS cliente,
                   'Notebook' AS produto, 3500 AS valor
            UNION ALL
            SELECT 2, 'Bruno', 'Mouse', 80
            UNION ALL
            SELECT 3, 'Carlos', 'Teclado', 150
        )
        TO '{arquivo_teste.as_posix()}'
        (FORMAT PARQUET)
    """)
    conexao.close()

    script = tmp_path / "consulta_financeiro.py"
    script.write_bytes(
        (PROJETO / "consulta_financeiro.py").read_bytes()
    )

    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )

    assert resultado.returncode == 0
    assert "Faturamento total: R$ 3730" in resultado.stdout