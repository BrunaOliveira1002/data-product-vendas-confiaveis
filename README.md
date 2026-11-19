# Data Product — Vendas Confiáveis

## Objetivo

Disponibilizar dados de vendas organizados, validados e confiáveis para o Departamento Financeiro, permitindo o cálculo do faturamento com verificações de qualidade dos dados.

## Responsável pelo produto

- **Domínio responsável:** Departamento de Vendas
- **Consumidor principal:** Departamento Financeiro

## Tecnologias utilizadas

- Python
- SQL
- DuckDB
- Apache Parquet
- Pytest
- Git e GitHub

## Dados disponibilizados

**Arquivo:** `vendas.parquet`

**Formato:** Apache Parquet

### Estrutura dos dados

| Campo | Tipo | Descrição |
|---|---|---|
| id_venda | INTEGER | Identificador único da venda |
| cliente | VARCHAR | Nome do cliente |
| produto | VARCHAR | Nome do produto vendido |
| valor | DECIMAL(12,2) | Valor da venda em reais, com duas casas decimais |

O tipo DECIMAL(12,2) permite representar valores monetários com centavos, evitando imprecisões típicas de números de ponto flutuante.

## Regras de qualidade

O Data Product possui quatro regras principais:

1. O valor da venda deve ser maior que zero.
2. O valor da venda não pode ser nulo.
3. O identificador da venda não pode ser duplicado.
4. O identificador da venda não pode ser nulo.

Caso alguma dessas regras seja violada, a consulta financeira é bloqueada.

## Como validar a qualidade dos dados

Execute o seguinte comando na pasta principal do Data Product:

```bash
python validar_qualidade.py
```

O programa verifica:

- Valores financeiros negativos, iguais a zero ou nulos.
- Identificadores de vendas duplicados.
- Identificadores de vendas nulos.

O validador apresenta mensagens informativas e alertas quando identifica inconsistências.

Esse script funciona como um relatório de qualidade e não interrompe automaticamente a execução.

## Como consumir o Data Product

O Departamento Financeiro pode consultar o faturamento utilizando o script `consulta_financeiro.py`.

Execute:

```bash
python consulta_financeiro.py
```

Antes de calcular o faturamento, o programa verifica se os dados atendem às regras de qualidade.

Caso encontre valores inválidos, IDs duplicados ou IDs nulos, a consulta é interrompida por uma exceção ValueError.

## Segurança e qualidade

O Data Product utiliza validações preventivas para evitar o consumo de dados inconsistentes.

As verificações implementadas incluem:

- Identificação de valores financeiros negativos.
- Bloqueio de valores iguais a zero.
- Bloqueio de valores financeiros nulos.
- Identificação de IDs duplicados.
- Bloqueio de IDs nulos.
- Interrupção do cálculo financeiro quando uma regra é violada.

Essas verificações contribuem para a integridade e a confiabilidade das informações utilizadas pelo Departamento Financeiro.

## Testes automatizados

O projeto utiliza Pytest para testar automaticamente as regras de qualidade e o cálculo do faturamento.

### Como executar os testes

Na pasta principal do Data Product, execute:

```bash
python -m pytest tests/ -v
```

### Cenários testados

| Teste | Resultado |
|---|---|
| Bloqueio de identificador nulo | Aprovado |
| Bloqueio de identificador duplicado | Aprovado |
| Bloqueio de valor negativo | Aprovado |
| Bloqueio de valor igual a zero | Aprovado |
| Bloqueio de valor nulo | Aprovado |
| Cálculo correto do faturamento | Aprovado |

Resultado da última execução:

```text
6 passed in 15.78s
```

Os testes automatizados utilizam arquivos Parquet temporários, preservando o arquivo original de vendas.

### Testes com valores decimais

Também foram realizados testes manuais para verificar o funcionamento do tipo DECIMAL(12,2).

Exemplo:

| Produto | Valor |
|---|---|
| Produto A | R$ 149,90 |
| Produto B | R$ 80,50 |
| Total | R$ 230,40 |

Resultado obtido:

```text
Faturamento total: R$ 230.40
```

O resultado confirmou que a consulta consegue trabalhar com valores monetários contendo centavos.

## Resultado esperado

Com os dados originais, a consulta financeira retorna:

```text
Faturamento total: R$ 3730.00
```

O conjunto de dados contém três vendas válidas:

| ID | Cliente | Produto | Valor |
|---|---|---|---|
| 1 | Ana | Notebook | R$ 3.500,00 |
| 2 | Bruno | Mouse | R$ 80,00 |
| 3 | Carlos | Teclado | R$ 150,00 |

**Faturamento total: R$ 3.730,00**

## Melhorias implementadas

- Inclusão da verificação de identificadores nulos.
- Atualização da consulta financeira para bloquear IDs nulos.
- Atualização do relatório de qualidade.
- Implementação de seis testes automatizados com Pytest.
- Conversão do campo financeiro para DECIMAL(12,2).
- Validação do cálculo de faturamento com centavos.
- Atualização da documentação técnica.
- Configuração do .gitignore para ignorar arquivos temporários e backups.

## Próximas melhorias

- Ampliar a cobertura dos testes automatizados.
- Implementar validação explícita do esquema e dos tipos de dados.
- Melhorar o tratamento de erros.
- Adicionar verificações específicas para arquivos vazios.
- Evoluir os mecanismos de monitoramento da qualidade dos dados.

## Considerações finais

O Data Product — Vendas Confiáveis demonstra a aplicação prática de conceitos de Engenharia de Dados, qualidade de dados, Python, SQL e DuckDB.

O projeto utiliza verificações de qualidade antes do consumo das informações financeiras, contribuindo para a identificação de inconsistências e a prevenção de cálculos sobre dados inválidos.

A implementação de testes automatizados, o uso de tipos financeiros precisos e a documentação das regras de qualidade tornam o produto mais confiável, testável e fácil de manter.

O projeto permanece aberto a melhorias contínuas, seguindo práticas de desenvolvimento e Engenharia de Dados.