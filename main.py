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
    print("\033[34mDEMO DETAILS: \n This is the original user input:\033[0m \n")
    print(user_input)
    #user_input = clean_input()
    # then feed it into sanitize and store 
    # TRACK what is changed 
    user_input_cleaned, dict_email, dict_ssn = sanitize_input(user_input)
    print ("\033[34mDEMO DETAILS: \n This is the sanitized message:\033[0m \n")
    print(user_input_cleaned)
    # send sanitized content to llm_client and store
    groq(user_input_cleaned)

if __name__ == '__main__':
    main()
