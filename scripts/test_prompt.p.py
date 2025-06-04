from langchain.prompts import PromptTemplate

prompt_template = """Use the following context to answer the question concisely:
{context}
Question: {question}
Helpful Answer:"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
output = prompt.format(context="E-Aadhaar is an electronic form of Aadhaar.", question="What is E-Aadhaar?")
print(output)
