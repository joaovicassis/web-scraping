# Sistema de Web Scaping para busca de operadoras de saúde

Este projeto é um sistema completo para coleta, processamento e busca de dados de operadoras de saúde. O sistema consiste em um web scraper para coletar dados da ANS, um processador para extrair informações de PDFs, um banco de dados PostgreSQL para armazenamento, e uma API REST com interface web para busca textual.

## 🚀 Funcionalidades

### Backend
- **Web Scraping**: Coleta automática de dados da ANS
- **Processamento de PDFs**: Extração estruturada de dados de documentos PDF
- **Banco de Dados**: Armazenamento em PostgreSQL com índices otimizados
- **API REST**: Endpoints para busca textual com filtros e paginação
- **Testes Unitários**: Cobertura de testes para garantir qualidade do código

### Frontend
- **Interface Moderna**: Desenvolvida com Vue.js 3 e Bootstrap 5
- **Busca em Tempo Real**: Atualização automática dos resultados
- **Filtros Avançados**: Por UF e modalidade
- **Paginação**: Navegação intuitiva entre resultados
- **Responsividade**: Interface adaptável a diferentes dispositivos

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- NPM ou Yarn

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/operadoras-search.git
cd operadoras-search
```

### 2. Configuração do Ambiente Python
```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados
```bash
# Crie um banco de dados PostgreSQL
createdb operadoras_db

# Configure a variável de ambiente
# Windows
set DATABASE_URL=postgresql://usuario:senha@localhost:5432/operadoras_db
# Linux/Mac
export DATABASE_URL=postgresql://usuario:senha@localhost:5432/operadoras_db
```

### 4. Configuração do Frontend
```bash
# Entre no diretório do frontend
cd frontend-vue

# Instale as dependências
npm install

# Configure as variáveis de ambiente
# Crie um arquivo .env
echo "VITE_API_URL=http://localhost:8000" > .env
```

## 🚀 Executando o Projeto

### 1. Inicialize o Banco de Dados
```bash
# Na raiz do projeto
python src/database.py
```

### 2. Execute o Web Scraping e Processamento
```bash
# Na raiz do projeto
python main.py
```

### 3. Inicie a API
```bash
# Na raiz do projeto
python src/api.py
```

### 4. Inicie o Frontend
```bash
# Em outro terminal, na pasta frontend-vue
npm run dev
```

Acesse a aplicação em:
- Frontend: http://localhost:8080
- API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs

## 📚 Documentação da API

### Endpoints

#### GET /
Retorna informações básicas sobre a API.

**Resposta**:
```json
{
  "message": "API de Busca de Operadoras",
  "version": "1.0.0",
  "endpoints": {
    "/search": "Busca textual em operadoras",
    "/health": "Verificação de saúde da API"
  }
}
```

#### GET /health
Verifica o status da API e conexão com o banco de dados.

**Resposta**:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### GET /search
Realiza busca textual em operadoras.

**Parâmetros**:
- `query` (string, obrigatório): Termo de busca
- `limit` (integer, opcional, padrão=10): Número máximo de resultados
- `offset` (integer, opcional, padrão=0): Número de resultados para pular
- `uf` (string, opcional): Filtrar por UF
- `modalidade` (string, opcional): Filtrar por modalidade

**Resposta**:
```json
[
  {
    "registro_ans": "123456",
    "cnpj": "12345678901234",
    "razao_social": "OPERADORA EXEMPLO",
    "nome_fantasia": "OPERADORA",
    "modalidade": "OPERADORA",
    "cidade": "SÃO PAULO",
    "uf": "SP",
    "bairro": "CENTRO"
  },
  // ... mais resultados
]
```

## 🧪 Testes

### Testes de Configuração
```bash
python src/test_setup.py
```

### Testes da API
```bash
pytest src/test_api.py
```

## 📁 Estrutura do Projeto

```
operadoras-search/
├── src/
│   ├── api.py              # API FastAPI
│   ├── crawler.py          # Web scraper
│   ├── processor.py        # Processador de PDFs
│   ├── database.py         # Gerenciador do banco de dados
│   ├── test_api.py         # Testes da API
│   └── test_setup.py       # Testes de configuração
├── sql/
│   ├── schema/
│   │   └── create_tables.sql
│   ├── import/
│   │   └── import_data.sql
│   ├── cleanup/
│   │   └── cleanup_data.sql
│   └── verify/
│       └── verify_data.sql
├── frontend-vue/
│   ├── src/
│   │   ├── components/
│   │   │   └── SearchForm.vue
│   │   ├── views/
│   │   │   └── HomeView.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── assets/
│   │   │   └── main.css
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── db/
│   └── datas/
│       ├── demo-contabeis/
│       └── relatorio-operadoras/
├── main.py
└── requirements.txt
```

## 🔒 Segurança

- Credenciais do banco de dados são gerenciadas via variáveis de ambiente
- API implementa CORS para controle de acesso
- Dados sensíveis são tratados de forma segura
- Validação de entrada em todos os endpoints

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- BeautifulSoup4
- PyPDF2
- Pandas
- Pytest

### Frontend
- Vue.js 3
- Vue Router
- Pinia
- Axios
- Bootstrap 5
- Vite


## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
