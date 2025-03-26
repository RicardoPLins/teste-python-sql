--Queries para criação das duas tabelas
-- tabela para demonstracoes contabeis
CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    data DATE,
    reg_ans INT,
    cd_conta_contabil VARCHAR(20),
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2)
);


-- tabela operadores para o relatorio_cadop.csv
CREATE TABLE operadoras (
	id SERIAL PRIMARY KEY,
    reg_ans INT,
    cnpj VARCHAR(18),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_de_comercializacao INT,
    data_registro_ans DATE
);

-- Queries para fazer a importação dos arquivos que foram corrigidos para as tabelas com o encoding UTF8
COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\1T2023_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\2T2023_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\3T2023_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\4T2023_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\1T2024_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\2T2024_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\3T2024_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:\Program Files\PostgreSQL\16\data\4T2024_corrigido.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';

COPY operadoras(reg_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans)
FROM 'C:\Program Files\PostgreSQL\16\data\relatorio_cadop.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '"';



-- Queries analíticas para responder o que fora pedido
-- Query 1 ---
-- As 10 operadoras com maiores despesas no último trimestre ---

SELECT 
    o.reg_ans,
    o.razao_social,
    SUM(dc.vl_saldo_final) AS total_despesa
FROM 
    demonstracoes_contabeis dc
JOIN 
    operadoras o ON dc.reg_ans = o.reg_ans
WHERE 
    dc.descricao = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
    AND dc.data >= DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '3 months'  -- Início do último trimestre
    AND dc.data < DATE_TRUNC('quarter', CURRENT_DATE)  -- Início do trimestre atual
GROUP BY 
    o.reg_ans, o.razao_social
ORDER BY 
    total_despesa DESC
LIMIT 10;
--- ----

--- Query 2 ---
-- As 10 operadoras com maiores despesas no último ano --
---   ----
SELECT 
    o.reg_ans,
    o.razao_social,
    SUM(dc.vl_saldo_final) AS total_despesa
FROM 
    demonstracoes_contabeis dc
JOIN 
    operadoras o ON dc.reg_ans = o.reg_ans
WHERE 
    dc.descricao = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
    AND dc.data >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'  -- Últimos 12 meses
    AND dc.data < DATE_TRUNC('year', CURRENT_DATE)  -- Até o começo do ano atual
GROUP BY 
    o.reg_ans, o.razao_social
ORDER BY 
    total_despesa DESC
LIMIT 10;
