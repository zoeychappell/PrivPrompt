'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''
# Import the required files
from user_input import clean_input
from cli_utility import CLI
from sanitize import sanitize_input

def main():
    # call clean_input 
    cli_instance = CLI()  # Create instance
    user_input, response = cli_instance.cli() 
    if not user_input: 
        return


if __name__ == '__main__':
    main()
