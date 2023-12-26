import os
from transformers import AutoTokenizer
from llama_index import ServiceContext
from llama_index.llms import Replicate
from llama_index import set_global_tokenizer
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.response.notebook_utils import display_source_node

os.environ["REPLICATE_API_TOKEN"] = "YOUR_REPLICATE_API_TOKEN"

documents = SimpleDirectoryReader(input_files=['/Users/balakrishnamaduru/Documents/git/genai_data_injector/tests/resources/raw_data/paul_graham_essay.txt']).load_data()

llama2_7b_chat = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"
llm = Replicate(
    model=llama2_7b_chat,
    temperature=0.01,
    additional_kwargs={"top_p": 1, "max_new_tokens": 300},
)

# set_global_tokenizer(
#     AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode
# )

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model=embed_model
)

index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

# index.storage_context.persist()
# index.vector_store.query()

search_query_retriever = index.as_retriever(service_context=service_context)

search_query_retrieved_nodes = search_query_retriever.retrieve(
    "What happened after the thesis?"
)
print(f"search_query_retrieved_nodes : {search_query_retrieved_nodes}")

for nodes in search_query_retrieved_nodes:
    display_source_node(nodes, source_length=2000)