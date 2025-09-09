'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''
import re

def sanitize(user_input): 
    dict_email = {}
    # Search for emails
    matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", user_input)
    # If an email address is found
    if matches:
        # Iterate through the email matches
        for _ in matches: 
            counter = 1
            # Add the email matches to dict_email and the replacement value
            dict_email[_] = 'user' + str(counter) + '@email.com'
            counter += 1
            # Replace the finding with the replacement. 
            user_input = re.sub(_, dict_email[_], user_input)
    else: 
        print("no emails found.")
    print (user_input)
    

def main(): 
    sanitize("This is a test zoey.chappell@rit.edu")

if __name__ == '__main__':
    main()
