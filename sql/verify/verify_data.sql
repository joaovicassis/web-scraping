-- Verificar contagem de registros
SELECT 'relatorio_operadoras' as tabela, COUNT(*) as total FROM relatorio_operadoras
UNION ALL
SELECT 'dados_demograficos_contabeis' as tabela, COUNT(*) as total FROM dados_demograficos_contabeis;

-- Verificar valores únicos por UF
SELECT 'relatorio_operadoras' as tabela, uf, COUNT(*) as total 
FROM relatorio_operadoras 
GROUP BY uf
ORDER BY uf;

SELECT 'dados_demograficos_contabeis' as tabela, uf, COUNT(*) as total 
FROM dados_demograficos_contabeis 
GROUP BY uf
ORDER BY uf;

-- Verificar valores únicos por modalidade
SELECT 'relatorio_operadoras' as tabela, modalidade, COUNT(*) as total 
FROM relatorio_operadoras 
GROUP BY modalidade
ORDER BY modalidade;

SELECT 'dados_demograficos_contabeis' as tabela, modalidade, COUNT(*) as total 
FROM dados_demograficos_contabeis 
GROUP BY modalidade
ORDER BY modalidade;

-- Verificar registros com dados faltantes
SELECT 'relatorio_operadoras' as tabela, 
       COUNT(*) FILTER (WHERE cnpj IS NULL) as cnpj_nulo,
       COUNT(*) FILTER (WHERE razao_social IS NULL) as razao_social_nula,
       COUNT(*) FILTER (WHERE uf IS NULL) as uf_nula
FROM relatorio_operadoras;

SELECT 'dados_demograficos_contabeis' as tabela,
       COUNT(*) FILTER (WHERE cnpj IS NULL) as cnpj_nulo,
       COUNT(*) FILTER (WHERE razao_social IS NULL) as razao_social_nula,
       COUNT(*) FILTER (WHERE uf IS NULL) as uf_nula
FROM dados_demograficos_contabeis; 