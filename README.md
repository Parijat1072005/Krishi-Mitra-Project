Krishi-Mitra: An Agentic AI Advisor for Indian Agriculture Krishi-Mitra  is an intelligent, conversational AI agent designed to bridge the critical information gap for farmers in India. It acts as a single, reliable point of contact that farmers can consult using simple, natural language to get synthesized insights on weather, real-time market prices, crop advisories, and government schemes.This project leverages a sophisticated agentic AI architecture that is accessible via low-tech channels like SMS, ensuring that even farmers with low digital literacy or intermittent internet can access the data they need to make informed decisions.Key Features Conversational Interface: Understands natural, colloquial, and mixed-language (Hinglish) queries.Multi-Domain Synthesis: Can answer complex questions by combining information from multiple sources in a single response.Tool-Using Agent: Dynamically uses a suite of tools to fetch live data from external APIs (weather, market prices).Grounded in Knowledge: Uses a Retrieval-Augmented Generation (RAG) model with a vector database to answer questions based on a curated knowledge base of official PDF documents.Accessible via SMS: Designed with an SMS-first approach using Twilio to be accessible to the widest possible audience.Architecture Diagram The solution is built on a modern RAG + Tool-Using Agent architecture, ensuring responses are grounded in factual, verifiable data.


        A[Farmer via SMS/WhatsApp]
        B{Flask & Twilio Gateway}
        C{Agent Core (Gemini LLM + LangChain)}
        D[Tool Library]
        E[Live APIs <br> (Weather, Market Prices)]
        F[Vector Database <br> (Schemes, Advisories)]

    A -- Sends Message --> B;
    B -- Passes Query --> C;
    C -- "I need to know the weather and find a scheme." --> D;
    D -- Calls get_weather_forecast --> E;
    D -- Calls find_government_scheme --> F;
    E -- Returns "Rain expected" --> D;
    F -- Returns "PMFBY details" --> D;
    D -- Returns facts to Agent --> C;
    C -- Synthesizes final answer --> B;
    B -- Sends Reply Message --> A;
Technology Stack AI & Machine Learning: LangChain, Google Gemini Pro, LangChain Google GenAI, LangChain ChromaData Handling: ChromaDB (Vector Store), Pandas, PyPDFWeb & API Interaction: Flask, Twilio, Requests, NgrokDevelopment: Python, venv, python-dotenv. 


Setup and Installation: Follow the below steps to get the project running on your local machine.



1. Clone the Repository by using the command 
>>git clone https://github.com/Parijat1072005/krishi-mitra-project.git



2. Go to the project directory
>>cd krishi-mitra-project



3. Create the virtual environment
>>python -m venv venv

4. Activate it (on Windows)
>>.\venv\Scripts\activate



5. Install Dependencies
>>pip install -r requirements.txt



6. Configure Environment Variables i.e Create a file named .env in the root of the project directory and add your API keys in the .env file
>>OPENWEATHER_API_KEY="your_openweathermap_api_key" eg. 9f1f2fc2401501bd67cdc74b2ece13e1

>>DATA_GOV_API_KEY="your_data.gov.in_api_key" eg. 579b464db66ec23bdd0000019a4ac829f2bf414a688ac1d63662bda2

>>GOOGLE_API_KEY="your_google_ai_studio_api_key" #please generate it of your own

>>TWILIO_ACCOUNT_SID="your_twilio_account_sid" #please generate it of your own

>>TWilio_AUTH_TOKEN="your_twilio_auth_token" #please generate it of your own



7. Build the Knowledge BasePlace all your relevant PDF documents (government schemes, advisories, etc.) into the documents folder by just running the script to create the vector database. This only needs to be done once, or whenever you add new documents.
>>python create_vector_db.py


8.How to Run the Project You can run the project in two modes.
A. Developer Mode (Terminal Only)This is the quickest way to test the agent's logic.Make sure your virtual environment is activated.Run the main script:
>>python main.py
The terminal will prompt you to "Ask your question:".


B. SMS Mode (Real User Simulation)This mode allows you to interact with the agent via SMS using Twilio.
Terminal 1: Start the Web Server# Make sure your venv is activated
>>python app.py


Terminal 2: Start Ngrok# This creates a public URL to your local server
>>ngrok http 5000


Configure Twilio: Copy the https://...ngrok-free.app URL from the ngrok terminal and paste it into your Twilio phone number's webhook configuration for incoming messages. Interact: Send an SMS from your verified phone number to your Twilio number.



                                                        krishi-mitra-project structure:

documents/                        # PDFs for the knowledge base are placed here


db/                               # The ChromaDB vector store is saved here


scripts/                          # Utility scripts (e.g., clean_static_data.py)


.env                              # Stores secret API keys (MUST NOT be committed to Git)


.gitignore                        # Specifies files to be ignored by Git


agent.py                          # Contains the core agent logic, tools, and LLM integration


app.py                            # The Flask web server for the SMS interface


config.py                         # Non-secret configuration variables


create_vector_db.py                 # Script to build the knowledge base from PDFs


data_fetchers.py                  # Functions that fetch data from external APIs


main.py                           # The entry point for running the agent in the terminal


requirements.txt                  # Lists all Python dependencies for the project



                                                "Limitations and Future Work"


Known Limitation: There is a known issue with Indian mobile carriers blocking inbound SMS to international Twilio trial numbers. The recommended path forward is to implement the WhatsApp channel, which bypasses these carrier restrictions.


Future Work:Full WhatsApp Integration: Pivot to WhatsApp for a richer, more reliable user experience.**Voice"
