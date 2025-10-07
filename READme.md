# PrivPrompt
This team has the purpose of ensuring data privacy is maintained in LLMs by identifying and obfuscating PII data; including the removal of names, emails, and SSNs from LLM prompts. Leveraging the use of artificial intelligence, we will develop a software called Priv Prompt that is open source and easy to integrate while maintaining utility and accuracy. This software will be a lightweight toolkit and API to preserve privacy of users and accuracy of LLM response. 

This project is completed as part of a bachelor's capstone project at Rochester Institute of Technology. 

We are guided by Faculty advisor Yidan Hu.

# Team Members
Zoey Chappell, Adam Braccia, and Minn Myint

# Download all dependencies
1. run the command 'pip install -r requirements.txt'

# How to Set Up a dotenv environment 
By using dotenv, API keys can be set as an environment variable and not included directly in the code. 
1. Import dotenv
2. Create a file names '.env' in the root directory. .env 
3. Add an entry in the following format: 
    api_key = "your_api_key"
    NOTE: Each LLM has a specific naming scheme that the API key should follow. 

# To use flask and run front end:

    1. Open Terminal
    2. Go to the location of the /my-flask-app
        cd /Users/adambraccia/Documents/GitHub/PrivPrompt/my-flask-app
    3. Open virtual environment
        python3 -m venv venv
        source venv/bin/activate
    4. install flask and livereload and others
        pip install flask flask-cors
        pip install livereload
        pip install spacy
        python -m spacy download en_core_web_sm
        pip install groq
        pip install python-dotenv


    5. Run app.py
        python app.py
    5. Open in the browser the IP
        http://127.0.0.1:5001

# How to get a Groq API key

1. Create an groq account and login. 
2. Go to https://console.groq.com/keys and select "Create API Key" in the upper right. 
3. Follow the steps and copy the API key. 

# How to get a Cohere API key
1. Go to https://dashboard.cohere.com/welcome/login and create a new account. 
2. Navigate to the API Keys button in the left menu
3. Make a new TRIAL KEY - NOT the production key
4. Add the api key to your .env file by following the dotenv instructions.
5. IMPORTANT: Make sure to follow the naming scheme 
		COHERE_API_KEY=’<your key>’

# How to get a Google AI Stuido API Key
1. Go to https://aistudio.google.com/prompts/new_chat and create an account. 
2. Select “Get API Key” in the bottom left. 
3. Create a new project by selecting "Project" from the menu on the left. 
4. Select "Create a new project" in the upper right and follow steps. 
5. Select "Api keys" in the menu on the left. 
6. Select "Create API Key" in the upper right. 
7. Name your key and select the appropriate project. 
8. Add the API key to your .env file by following the dotenv instructions. 
9. IMPORTANT: Make sure to follow the naming scheme
    GEMINI_API_KEY='<your key>'

# How to get a Deepseek API Key
Note:  This is not actually communicating with Deepseek but is going through OpenRouter. 
1. Go to https://openrouter.ai/models
2. Find Deepseek V3.1 (Free). 
    NOTE: it must be this specific version
3. Select Deepseek and it will bring you to this page. 
4. Scroll down until you find Create API Key. 
5. Select it and it will bring you to this page. 
6. Select Create API Key and follow the prompts. 
7. Name the key and the other options are optional. 
8. Copy the api key
9. Add the api key to your .env file by following the dotenv instructions.
    Make sure to follow the naming scheme 
		DEEPSEEK_API_KEY=’<your key>’

