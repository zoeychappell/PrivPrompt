'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''

import sys


'''
Function that takes in the user input, then cleans the input. 
Parameters: 
    - user_input : The string returned from user_input function. 
Returns: 
    - cleaned_user_input : A nicely formatted string'''
def clean_input():
    # User input gathered.
    # print("Enter your text (Ctrl+Z Enter to finish):")
    # By using sys.stdin.read(), the program can accept multiple lines of input
    user_text = sys.stdin.read() # Note, can introduce character limits here with read(#)
    # Checks for new lines and replaces them with a space.
    cleaned_user_input = user_text.replace("\n", "").replace("\r", "")
    # Turn to lower case for better matching.
    cleaned_user_input.lower()
    # Return the cleaned input and trims whitespace.
    return cleaned_user_input.strip()


def main(): 
    user_input = clean_input()

if __name__ == '__main__':
    main()