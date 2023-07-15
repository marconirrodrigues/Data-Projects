# Documentação do Projeto

Este projeto é um coletor de dados de notícias e de dados financeiros. Ele coleta notícias do NewsAPI e dados financeiros do Yahoo Finance e armazena esses dados em um banco de dados Postgres.

## Módulos

### database_manager.py

Este módulo contém a classe `DatabaseManager`, que fornece um conjunto de métodos para interagir com um banco de dados PostgreSQL. A classe cria uma conexão com o banco de dados na inicialização e expõe métodos para criar tabelas, inserir dados e fechar a conexão com o banco de dados.

### hashing.py

Este módulo contém a função `calculate_hash`, que calcula um hash SHA-256 para qualquer número de argumentos dados. Essa função é usada para criar IDs únicos para os registros inseridos no banco de dados.

### queries.py

Este módulo contém uma série de consultas SQL que são usadas para criar tabelas e inserir dados nelas. Também contém funções para verificar se um registro já existe na tabela antes de tentar inseri-lo.

### news_data.py

Este módulo contém a classe `NewsAPI`, que é usada para buscar notícias do NewsAPI. A classe usa uma chave de API para autenticar com o NewsAPI e pode buscar notícias de um determinado período passado baseado em uma palavra-chave.

O módulo também contém uma função principal que cria uma instância do `NewsAPI`, busca notícias e insere essas notícias no banco de dados.

### yahoo_finance_data.py

Este módulo contém a classe `FinanceDataFetcher`, que é usada para buscar dados financeiros do Yahoo Finance. A classe usa o pacote `yfinance` para buscar dados financeiros de um determinado ativo financeiro.

O módulo também contém uma função principal que cria uma instância do `FinanceDataFetcher`, baixa dados financeiros e insere esses dados no banco de dados.

## Segurança de Dados

As chaves da API e as credenciais do banco de dados são carregadas a partir de variáveis de ambiente para evitar a exposição de dados sensíveis. Recomenda-se que essas chaves e credenciais sejam armazenadas de forma segura e nunca incluídas diretamente no código.

Os IDs únicos para os registros no banco de dados são criados a partir de um hash SHA-256 dos dados relevantes. Isso aj
