# main.py
from agent import create_agent

if __name__ == "__main__":
    print("--- Krishi-Mitra AI Agent ---")
    print("Type 'exit' to quit.")

    # Create the agent once
    krishi_agent = create_agent()

    while True:
        user_query = input("\nAsk your question: ")
        if user_query.lower() == 'exit':
            break
        
        if user_query:
            # Let the agent handle the query
            response = krishi_agent.invoke({"input": user_query})
            print("\n🤖 Krishi-Mitra says:")
            print(response['output'])