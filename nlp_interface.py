import openai

openai.api_key = 'your-api-key-here'

def query_nlp_model(question: str):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    while True:
        user_query = input("Ask a maintenance question: ")
        if user_query.lower() in ['exit', 'quit']:
            break
        response = query_nlp_model(user_query)
        print(f"Response: {response}")

# Example flow
# if __name__ == "__main__":
#     main()
