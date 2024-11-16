import json

def convert_llm_response_to_json(llm_response):
    try:
        cleaned_response = llm_response.strip("```json\n").strip("```").replace('\\n', '')
        response = json.loads(cleaned_response)
        return response
    except Exception as e:
        print(f"Error converting response to json: {e}")
        return {}