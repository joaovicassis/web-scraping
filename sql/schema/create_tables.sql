-- Tabela para dados demográficos e contábeis
CREATE TABLE IF NOT EXISTS dados_demograficos_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    cnpj VARCHAR(14),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE,
    periodo VARCHAR(10), -- Ex: 1T2024, 2T2024, etc.
    ano INTEGER,
    trimestre INTEGER
);

-- Tabela para relatório de operadoras
CREATE TABLE IF NOT EXISTS relatorio_operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    cnpj VARCHAR(14),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

-- Índices para otimização
CREATE INDEX idx_dados_demograficos_registro_ans ON dados_demograficos_contabeis(registro_ans);
CREATE INDEX idx_dados_demograficos_uf ON dados_demograficos_contabeis(uf);
CREATE INDEX idx_dados_demograficos_modalidade ON dados_demograficos_contabeis(modalidade);
CREATE INDEX idx_dados_demograficos_periodo ON dados_demograficos_contabeis(periodo);

CREATE INDEX idx_relatorio_operadoras_registro_ans ON relatorio_operadoras(registro_ans);
CREATE INDEX idx_relatorio_operadoras_uf ON relatorio_operadoras(uf);
CREATE INDEX idx_relatorio_operadoras_modalidade ON relatorio_operadoras(modalidade); 