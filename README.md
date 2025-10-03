# 📄 PDF RAG Query System

## Descrição do Projeto

Sistema inteligente de consulta a documentos PDF utilizando **RAG** (Retrieval-Augmented Generation) para fornecer respostas precisas baseadas no conteúdo dos documentos.

## 🛠 Stack

- **Python** - Linguagem principal
- **PDF Loader** - Carregamento e processamento de documentos PDF
- **PostgreSQL + PGVector** - Banco de dados vetorial para armazenamento e busca semântica
- **Docker** - Postgres server
- **LangChain** - Framework para aplicações de LLM
- **OpenAI** - Modelos de linguagem para geração de respostas

## Run Project

### 1. Clone o proejto

```
git clone <repository-url>
cd langchain-pdf-rag
```

### 2. Configure o ambiente python

```
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Adicione a sua `OPENAI_API_KEY` no arquivo `.env`

```
cp .env.example .env
```

### 5. Inicie o banco de dados

```
docker compose up -d
```

### 6. Faça a ingestão do PDF

```
python src/ingest.py
```

### 5. Inicie o chat

```
python src/chat.py
```
