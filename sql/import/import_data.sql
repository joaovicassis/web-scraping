-- Importação do arquivo Relatorio_cadop.csv
COPY relatorio_operadoras (
    registro_ans, cnpj, razao_social, nome_fantasia,
    modalidade, logradouro, numero, complemento,
    bairro, cidade, uf, cep, ddd, telefone,
    fax, email, representante, cargo_representante,
    data_registro_ans
)
FROM 'db/datas/relatorio-operadoras/Relatorio_cadop.csv'
WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ';',
    ENCODING 'LATIN1'
);

-- Importação dos arquivos de dados demográficos e contábeis
-- Nota: Para os arquivos ZIP, você precisará primeiro extrair os CSVs
-- e então usar o comando COPY para cada arquivo extraído

-- Exemplo para 1T2024 (após extração)
COPY dados_demograficos_contabeis (
    registro_ans, cnpj, razao_social, nome_fantasia,
    modalidade, logradouro, numero, complemento,
    bairro, cidade, uf, cep, ddd, telefone,
    fax, email, representante, cargo_representante,
    data_registro_ans, periodo, ano, trimestre
)
FROM 'db/datas/demo-contabeis/2024/1T2024.csv'
WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ';',
    ENCODING 'LATIN1'
);

-- Repetir para os outros trimestres (2T2024, 3T2024, 4T2024)
-- Basta copiar e colar o comando acima, alterando o nome do arquivo 