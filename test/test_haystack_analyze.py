
import os
from haystack import Pipeline, Document
from opensearch_haystack  import OpenSearchBM25Retriever
from haystack.components.generators import GPTGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from opensearch_haystack import OpenSearchDocumentStore
from haystack import Document


document_store = OpenSearchDocumentStore(hosts="http://localhost:9200", use_ssl=True,
verify_certs=False, http_auth=("admin", "admin"))


prompt_template = """
Given these documents, answer the question.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Question: {{question}}
Answer:
"""

retriever = OpenSearchBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt_template)
llm = GPTGenerator(api_key=os.environ.get("OPENAI_API_KEY"))
answer_builder = AnswerBuilder()

rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.add_component("answer_builder", answer_builder)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")

rag_pipeline.draw("rag_pipeline.png")

question = "What is the advantage of SSH?"
results = rag_pipeline.run(
    {
        "retriever": {"query": question},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
)

for answer in results["answer_builder"]["answers"]:
    print(answer.data)
