# PrivPrompt
This team has the purpose of ensuring data privacy is maintained in LLMs by identifying and obfuscating PII data; including the removal of names, emails, and SSNs from LLM prompts. Leveraging the use of artificial intelligence, we will develop a software called Priv Prompt that is open source and easy to integrate while maintaining utility and accuracy. This software will be a lightweight toolkit and API to preserve privacy of users and accuracy of LLM response. 

This project is completed as part of a bachelor's capstone project at Rochester Institute of Technology. 

We are guided by Faculty advisor Yidan Hu.

# Team Members
Zoey Chappell, Adam Braccia, and Minn Myint

# How to Set Up a dotenv environment 
By using dotenv, API keys can be set as an environment variable and not included directly in the code. 
1. Import dotenv
2. Create a .env file in your environment. 
3. Add an entry in the following format: 
    api_key = "your_api_key"

# To use flask and run front end:
    1. Open Terminal
    2. Go to the location of the /my-flask-app
        cd /Users/adambraccia/Documents/GitHub/PrivPrompt/my-flask-app
    3. Open virtual environment
        python3 -m venv venv
        source venv/bin/activate
    4. install flask and livereload
        pip install flask flask-cors
        pip install livereload 
    5. Run app.py
        python app.py
    5. Open in the browser the IP
        http://127.0.0.1:5001

# How to get a Groq API key

1. Create an groq account and login. 
2. Go to https://console.groq.com/keys and select "Create API Key" in the upper right. 
3. Follow the steps and copy the API key. 

# How to get a Cohere API Key
