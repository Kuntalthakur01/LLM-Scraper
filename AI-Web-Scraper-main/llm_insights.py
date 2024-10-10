
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import json
from joblib import Memory

# memory = Memory("/tmp/joblib_cache", verbose=0)

# Template for insights generation
# insights_template = (
#     "You are a data analyst with 20 years of experience tasked with analyzing the following data: {parsed_results}. "
#     "Based on the data provided, please generate insights, highlight patterns or correlations, and offer suggestions where relevant. Follow these guidelines: \n\n"
#     "1. **Generate Insights:** Focus on generating insights that are directly related to the data provided.\n"
#     "2. **Patterns or Correlations:** Identify and highlight any noticeable patterns or correlations.\n"
#     "3. **Suggestions:** Provide actionable suggestions based on the data analysis.\n"
#     "4. **Direct and Concise:** Your response should be direct and concise, without any additional commentary.\n"
#     "5. **No Extra Content:** Include no extraneous text, comments, or explanations."
# )

# model = OllamaLLM(model="llama3.1:latest")


# @memory.cache
# def generate_llm_insights(parsed_results):
#     prompt = ChatPromptTemplate.from_template(insights_template)
#     chain = prompt | model
#     # Convert list of results to string if needed
#     prompt = generate_insights_prompt("\n".join(parsed_results))
#     chain = ChatPromptTemplate.from_template(prompt)

#     # Force all data to be processed as a single batch
#     combined_data = "\n".join(parsed_results)
#     response = chain.invoke({"data": combined_data})
#     print("Generated insights for the single batch")

#     return response


memory = Memory("/tmp/joblib_cache", verbose=0)
# Template for insights generation
insights_template = ('''
    "You are a seasoned data analyst tasked with analyzing the following data. Provide insightful analysis, highlight patterns or correlations, and offer actionable suggestions where relevant.\n\n"
    "Data:\n {data}.\n\n"
    "Please adhere to the following guidelines:\n"
    "Generate a concise summary of the data." then
    "1. Generate insights directly related to the data.\n"
    "2. Identify any noticeable patterns, correlations, or relationships.\n"
    "3. Provide actionable suggestions based on your analysis, recommending steps for improvement or optimization where appropriate. \n"
    "4. Be direct and concise in your delivery of insights to ensure clarity.\n"
    "5. Do not include any additional comments or explanations." '''
                     )


model = OllamaLLM(model="llama3.1:latest")


@memory.cache
def generate_llm_insights(parsed_results):
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
    response = chain.invoke({"data": data_representation})
    print("Generated insights for the provided data")
    return response
