'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''
import re
'''
This function takes in the user input and finds/replaces sensitive information. 
Parameters: 
    - user_input : a string of the user input.
Returns: 
    - user_input : a string of the user input censored. 
    - dict_email : a dictionary containing PII emails and corresponding censored versions. 
    - dict_ssn : a dictionary containing PII SSNs and corresponding censored versions. 
'''
def sanitize_input(user_input): 
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    SSN_PATTERN_1 = re.compile (r"\d{3}-\d{2}-\d{4}") # ex. 111-12-1234
    SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # ex. 111 12 1234
    SSN_PATTERN_3 = re.compile(r"\d{3}-\d{2} \d{4}") # ex. 111-12 1234
    SSN_PATTERN_4 = re.compile(r"\d{3} \d{2} \d{4}") # ex. 111 12-1234
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
    ssn_matches = SSN_PATTERN_1.findall(user_input) + SSN_PATTERN_2.findall(user_input) + SSN_PATTERN_3.findall(user_input) + SSN_PATTERN_4.findall(user_input)
    # Checks to see if there are any SSN matches
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

    return user_input, dict_email, dict_ssn

'''
This function replaces the LLM output with the  real data (ex. PII)
Parameters: 
    - dict_email : a dictionary containing the PII emails and corresponding matches
    - dict_ssn : a dictionary containing PII SSNs and corresponding sanitized matches
    - llm_output : a string containing the LLM response
Returns: 
    - llm_output : a string containing filled-in LLM response
'''
def fill_data(dict_email, dict_ssn, llm_output):
    # Checks if dict_email has any entries
    if dict_email: 
        for _ in dict_email:
            # In llm_output, replaces censored version with PII
            llm_output = llm_output.replace(dict_email[_], _)
    # Checks if dict_ssn has any entries
    if dict_ssn: 
        for _ in dict_ssn: 
            # In llm_output, replaces censored version with PII
            llm_output = llm_output.replace(dict_ssn[_], _)
    return llm_output

def main(): 
    user_input, dict_email, dict_ssn = sanitize_input("This is a test zoey.chappell@rit.edu, 123 14 1235 and an ssn 123-12-1234")
    llm_output = "Hello person, i see your email is user1@email.com, your ssn is XXX-XX-1001"
    llm_output = fill_data(dict_email, dict_ssn, llm_output)
    print(llm_output)
if __name__ == '__main__':
    main()
