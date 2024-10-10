from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.1:latest")


# def parse_with_ollama(dom_chunks, parse_description, batch_size=10):
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model

#     parsed_results = []

#     for i in range(0, len(dom_chunks), batch_size):
#         batch_chunks = dom_chunks[i:i+batch_size]
#         combined_chunk = "\n".join(batch_chunks)
#         response = chain.invoke(
#             {"dom_content": chunk, "parse_description": parse_description}
#         )
#         # print(f"Parsed batch: {i} of {len(dom_chunks)}")
#         print(
#             f"Parsed batch: {i // batch_size + 1} of {len(dom_chunks) // batch_size + 1}")
#         parsed_results.append(response)

#     return "\n".join(parsed_results)
def parse_with_ollama(dom_chunks, parse_description, batch_size=10):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i in range(0, len(dom_chunks), batch_size):
        batch_chunks = dom_chunks[i:i+batch_size]
        # Combine chunks into one string
        combined_chunk = "\n".join(batch_chunks)

        # Correcting this reference from 'chunk' to 'combined_chunk'
        response = chain.invoke(
            {"dom_content": combined_chunk, "parse_description": parse_description}
        )

        print(
            f"Parsed batch: {i // batch_size + 1} of {len(dom_chunks) // batch_size + 1}"
        )
        parsed_results.append(response)

    return "\n".join(parsed_results)
