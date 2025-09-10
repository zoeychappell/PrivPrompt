'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''
import re

def sanitize_input(user_input): 
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    SSN_PATTERN_1 = re.compile (r"\d{3}-\d{2}-\d{4}") # ex. 111-12-1234
    SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # ex. 111 12 1234
    dict_email = {}
    dict_ssn = {}
    '''Email Match'''
    email_matches = EMAIL_PATTERN.findall(user_input)
    # If an email address is found
    if email_matches:
        # Iterate through the email matches
        counter = 1
        for _ in email_matches: 
            # Add the email matches to dict_email and the replacement value
            dict_email[_] = 'user' + str(counter) + '@email.com'
            counter = counter + 1
            # Replace the finding with the replacement. 
            user_input = user_input.replace(_, dict_email[_])
 
    '''SSN Match'''
    ssn_matches = SSN_PATTERN_1.findall(user_input) + SSN_PATTERN_2.findall(user_input)
    if ssn_matches:
        s_counter = 1
        for _ in ssn_matches:
            # Add the SSN and replacement string to the dictionary
            dict_ssn[_] = f"XXX-XX-{1000+s_counter:04d}"
            # Replace the found ssns with XXX-XX-100#
            user_input = user_input.replace(_, dict_ssn[_])
            s_counter = s_counter + 1
    # here for testing       

    '''Name Match'''

    return user_input    

def main(): 
    sanitize_input("This is a test zoey.chappell@rit.edu, anothertest@yahoo.com, 123 14 1235 and an ssn 123-12-1234")

if __name__ == '__main__':
    main()
