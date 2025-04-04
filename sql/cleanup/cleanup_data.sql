-- Limpeza de dados antes da importação
UPDATE relatorio_operadoras
SET 
    cnpj = REGEXP_REPLACE(cnpj, '[^0-9]', '', 'g'),
    cep = REGEXP_REPLACE(cep, '[^0-9]', '', 'g'),
    telefone = REGEXP_REPLACE(telefone, '[^0-9]', '', 'g'),
    fax = REGEXP_REPLACE(fax, '[^0-9]', '', 'g');

UPDATE dados_demograficos_contabeis
SET 
    cnpj = REGEXP_REPLACE(cnpj, '[^0-9]', '', 'g'),
    cep = REGEXP_REPLACE(cep, '[^0-9]', '', 'g'),
    telefone = REGEXP_REPLACE(telefone, '[^0-9]', '', 'g'),
    fax = REGEXP_REPLACE(fax, '[^0-9]', '', 'g');

-- Padronização de campos de texto
UPDATE relatorio_operadoras
SET 
    uf = UPPER(TRIM(uf)),
    cidade = UPPER(TRIM(cidade)),
    bairro = UPPER(TRIM(bairro));

UPDATE dados_demograficos_contabeis
SET 
    uf = UPPER(TRIM(uf)),
    cidade = UPPER(TRIM(cidade)),
    bairro = UPPER(TRIM(bairro)); 