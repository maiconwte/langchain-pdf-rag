import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
   for k in (
        "GOOGLE_EMBEDDING_MODEL",
        "OPENAI_API_KEY",
        "OPENAI_EMBEDDING_MODEL",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
        "PDF_PATH",
        "PGVECTOR_COLLECTION",
        "PGVECTOR_URL"
     ):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))
        store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PGVECTOR_COLLECTION"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )

        documents = store.similarity_search_with_score(question, k=10)

        if not documents:
            return "Não tenho informações necessárias para responder sua pergunta."

        context = ""
        for doc in documents:
            context += doc[0].page_content.strip() + "\n\n"

        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["contexto", "pergunta"]
        )

        model = ChatOpenAI(model="gpt-5-nano", temperature=0.5)

        chain = prompt | model

        response = chain.invoke({"contexto": context, "pergunta": question})

        return response.content.strip()

if __name__ == "__main__":
    search_prompt("Qual o faturamento da empresa Zenith Educação Indústria?")