from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1",
    temperature=0.7
)

response = llm.invoke("Explain transformers in simple terms")

print(response.content)
