
# Data Product — Vendas Confiáveis

## Objetivo
Disponibilizar dados de vendas organizados e confiáveis para o departamento Financeiro.

## Responsável pelo produto

Domínio responsável: Departamento de Vendas

Consumidor principal: Departamento Financeiro

## Dados disponibilizados

Arquivo: vendas.parquet

Formato: Parquet

Campos:
- id_venda: identificador único da venda
- cliente: nome do cliente
- produto: nome do produto vendido
- valor: valor da venda em reais

## Regras de qualidade

- O valor da venda deve ser maior que zero.
- Nenhuma venda pode ter valor nulo.
- O identificador da venda não pode ser duplicado.

## Como consumir o Data Product

O departamento Financeiro pode consultar o faturamento
utilizando o arquivo consulta_financeiro.py.

Comando para executar na raiz do projeto:

python consulta_financeiro.py

## Segurança e qualidade

Antes de calcular o faturamento, o programa verifica:

- Se existem vendas com valores inválidos.
- Se existem identificadores de vendas duplicados.

Caso alguma regra seja violada, a consulta é interrompida.

## Resultado esperado

Faturamento total: R$ 3730
