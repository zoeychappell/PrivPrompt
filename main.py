'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''
# Import the required files
from user_input import clean_input
from cli_utility import CLI
from sanitize import sanitize_input
from groq_llm_client import groq
def main():
    # call clean_input 
    cli_instance = CLI()  # Create instance
    user_input = cli_instance.cli() 
    #user_input = clean_input()
    # then feed it into sanitize and store 
    # TRACK what is changed 
    user_input_cleaned = sanitize_input(user_input)
    print(user_input_cleaned)
    # send sanitized content to llm_client and store
    groq(user_input_cleaned)
    # grab the llm response

    # fill in any details if needed

    # ouput the response to the user

if __name__ == '__main__':
    main()
