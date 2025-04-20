# from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama  # pip install llama-index-llms-ollama
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.jinaai import (
    JinaEmbedding,
)  # pip install llama-index-embeddings-jinaai

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# from llama_index.core import PromptTemplate
# import openai # um api key zu prüfen
import os
from dotenv import load_dotenv

load_dotenv()

prompt_sys = 'Beantworte die Frage nur mit dem gegebenen Kontext auf Deutsch, halte die Antwort kurz. Wenn du nicht weiß, dann sag einfach "Ich weiß nicht"'
prompt_sys = 'Answer the question only based on the given context with original sentence(s) in the provided context in German. Keep the answer short. If you dont know the answer, say "I dont know". '
# prompt_few='Some examples are given below. The examples should tell you how the answers look like, but not give you the real answer.\n'
# def fn_few():
#     with open('few_shot1.json', 'r', encoding="utf-8") as file1:
#         dct_few = json.load(file1)
#     str_few=''
#     for key, value in dct_few.items():
#         str_few+=f'Query: {key}\nResponse: {value}\n\n'
#     return str_few.strip()
# prompt_sys+=prompt_few+fn_few()

str_tmpl1 = (
    "Kontextinformationen ist unten.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Angesichts der Kontextinformationen und nicht des Vorwissens, beantworte die Anfrage. "
    "Query: {query_str}\n"
    "Answer: "
)


class Agent:
    def __init__(self, k_top=3):
        """zusammenfassung tool, todos mit few_shot zu optimieren"""
        self.k_top = k_top
        self.index = None
        self.engine = None
        embed_model = JinaEmbedding(
            api_key=os.environ.get("JINA_API"),
            model="jina-embeddings-v2-base-de",
        )  # embed_batch_size=16,
        Settings.embed_model = embed_model
        Settings.llm = Ollama(model="llama3", request_timeout=1200)
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        Settings.system_prompt = prompt_sys

    def valid_api(self, api):
        client = openai.OpenAI(api_key=api)
        try:
            client.models.list()
        except openai.AuthenticationError:
            return False
        else:
            return True

    def init_openai(self, api=""):
        os.environ["OPENAI_API_KEY"] = api
        Settings.llm = OpenAI(temperature=0.2)
        # max_tokens=256 (output), Settings.context_window = 4096, model="gpt-4o"

    def embed(self, dir_pdf, dir_vec):
        documents = SimpleDirectoryReader(
            dir_pdf,
            filename_as_id=True,
        ).load_data()
        self.index = VectorStoreIndex.from_documents(documents=documents)
        self.index.storage_context.persist(persist_dir=dir_vec)

    def reload_index(self, dir_vec):
        storage_context = StorageContext.from_defaults(persist_dir=dir_vec)
        self.index = load_index_from_storage(storage_context)

    def refresh(self, dir_vec, lst_pdf):
        documents = SimpleDirectoryReader(
            input_files=lst_pdf, filename_as_id=True
        ).load_data()
        self.reload_index(dir_vec)
        self.index.refresh(documents)
        self.index.storage_context.persist(persist_dir=dir_vec)

    def qa(self, frage: str):
        retriever = self.index.as_retriever(similarity_top_k=1)
        nodes = retriever.retrieve(frage)
        node0 = nodes[0]
        doc_name = node0.metadata.get("file_name")
        page_nr = node0.metadata.get("page_label")
        text = node0.text
        score = node0.score
        context = {
            "file_name": doc_name,
            "page_nr": page_nr,
            "text": text,
            "score": score,
        }
        return context
        # response = self.engine1.query(frage)

        # self.engine = index.as_query_engine(similarity_top_k=self.k_top)

        # tmpl1 = PromptTemplate(str_tmpl1) # prompt template auf Deutsch
        # self.engine.update_prompts({"response_synthesizer:text_qa_template": tmpl1})

        # retriever = VectorIndexRetriever(
        #     index=index, similarity_top_k=self.k_top
        # )  # try multiple response
        # self.engine1 = RetrieverQueryEngine.from_args(
        #     retriever, response_mode="accumulate"
        # )
