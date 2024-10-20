
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import json
from joblib import Memory


# model = OllamaLLM(model="llama3.1:latest")


memory = Memory("/tmp/joblib_cache", verbose=0)
# Template for insights generation
# insights_template = ('''
#     "You are a seasoned data analyst tasked with analyzing the following data from the perspective of a {user_role}. Your analysis should provide insightful observations, highlight patterns or correlations, and include actionable suggestions that are directly relevant to a {user_role}."

#     "Data:\n{data}\n\n"
#     "Please adhere to the following guidelines:\n"
#     "1. Generate a concise summary of the data to establish a clear context for the insights.\n"
#     "2. Identify and highlight any noticeable patterns, correlations, or relationships that emerge from the data.\n"
#     "3. Provide actionable suggestions tailored to the needs of a {user_role}, based on your analysis. Recommend steps for improvement, enhancement, or innovation where appropriate.\n"
#     "4. Ensure that your delivery of insights is direct, concise, and devoid of any ambiguity to maintain clarity.\n"
#     "5. Avoid including any extraneous comments or unnecessary explanations beyond the insights directly relevant to the specified {user_role}."
# ''')
insights_template = ('''
"You are an expert data analyst with extensive experience in providing strategic insights. Analyze the following data from the perspective of a {user_role}. Your analysis should offer observations, identify patterns or correlations, and include actionable suggestions directly relevant to this role."

"Data:\n{data}\n\n"

"Please adhere to the following guidelines:\n"
"1. **Executive Summary**: Provide a concise summary of the data, establishing a clear context for your insights.\n"
"2. **Patterns & Relationships**: Identify any noticeable patterns, trends, correlations, or significant relationships in the data.\n"
"3. **Actionable Recommendations**: Suggest specific steps for improvement, optimization, or innovation, tailored to the needs of the {user_role}.\n"
"4. **Data Limitations**: Acknowledge any potential biases or limitations in the data that could affect your analysis.\n"
"5. **Professional Delivery**: Present your insights in a structured, clear, and professional manner. Use appropriate terminology but explain any complex concepts.\n"
"6. **Visualization Suggestions**: Where relevant, propose visualizations (e.g., charts, graphs) that would help communicate key findings.\n"
"7. **Ethical Considerations**: Consider any ethical implications of the data analysis and recommendations.\n"
"8. **Conciseness and Relevance**: Focus on insights directly relevant to the {user_role}, avoiding any extraneous commentary."
''')


model = OllamaLLM(model="llama3.1:latest")


@memory.cache
def generate_llm_insights(parsed_results, user_role):
    # Ensure parsed_results is properly formatted
    if isinstance(parsed_results, (list, dict)):
        # Convert to a well-formatted JSON string
        formatted_data = json.dumps(parsed_results, indent=2)
        data_representation = f"```json\n{formatted_data}\n```"
    elif isinstance(parsed_results, str):
        data_representation = parsed_results
    else:
        raise ValueError("Unsupported data type in parsed_results.")

    prompt = ChatPromptTemplate.from_template(insights_template)

    chain = prompt | model
    # Generate the insights by invoking the chain with the input data
    response = chain.invoke(
        {"data": data_representation, "user_role": user_role})

    print("Generated insights for the provided data and user role")
    return response
