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
    print("Please type your message. Type 'Done' on a new line to finish.")
    lines = []
    for line in sys.stdin:
        # Note for sys.stdin - can introduce character limits
        # Checks if the user enters "done"
        if line.strip().lower() == "done":
            break
        # else, continues
        lines.append(line.rstrip("\n"))

    user_text = " ".join(lines)
    cleaned_user_input = user_text.replace("\n", "").replace("\r", "")
    # Return the cleaned input and trims whitespace.
    return cleaned_user_input.strip()



def main(): 
    user_input = clean_input()

if __name__ == '__main__':
    main()