import re
# For name recognition
import spacy
# from spacy.pipeline import EntityRuler
# For English word checking
from nltk.corpus import words

'''
This function is the primary sanitization function. 
Parameters: 
    - user_input : A string entered by the user. The prompt. 
Outputs: 
    - dict_email : a dictionary containing the found emails and replacement email
    - dict_ssn : a dictionary containing the found SSNs and replacement SSN
    - dict_name : a dictionary containing the found names and replacement names. 
'''
def sanitize_input(user_input): 

    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") # Matches email addresses 
    EMAIL_PATTERN_2 = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\,[a-zA-Z]{2,}") # Matches email addresses with comma typo

    SSN_PATTERN_1 = re.compile(r"\d{3}-\d{2}-\d{4}") # Matches format ###-##-####
    SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # Matches format ### ## ####
    SSN_PATTERN_3 = re.compile(r"\d{3} \d{2}-\d{4}") # Matches format ### ##-####
    SSN_PATTERN_4 = re.compile(r"\d{3}-\d{2} \d{4}") # Matches format ###-## ####
    SSN_PATTERN_5  = re.compile(r"\d[0-9]{9}")

    DATE_PATTERN_1 = re.compile(r"\d{2}\/\d{2}\/\d{4}") # matches for ##/##/#### ex. 01/03/2024
    DATE_PATTERN_2 = re.compile(r"\d{1}\/\d{1}\/\d{2}") # Matches for #/#/## ex. 1/3/24

    # Matches for #/#/#### ex. 1/3/2024
    # Matches for ##/#/#### ex. 01/3/2024
    # Matches for 
    # do boht month/day/year and day/month/year

    
    dict_email = {}
    dict_ssn = {}
    dict_name = {}

    # #####################
    # Emails
    # #####################

    # Checks the user input for any strings matching the regex pattern. 
    email_matches = EMAIL_PATTERN.findall(user_input) + EMAIL_PATTERN_2.findall(user_input)
    # Initializes an email counter
    email_counter = 1
    # Iterates through found emails
    for e in email_matches:
        # Maps the email to a fake email user#@email.com
        dict_email[e] = f"user{email_counter}@email.com"
        # Replaces the found emails with user#@email.com
        user_input = user_input.replace(e, dict_email[e])
        # Iterate the email counter by one
        email_counter += 1
    
    # #####################
    # SSNs
    # #####################

    # Checks the user input for any strings matching the regex pattern. 
    ssn_matches = SSN_PATTERN_1.findall(user_input) + SSN_PATTERN_2.findall(user_input) + SSN_PATTERN_3.findall(user_input) + SSN_PATTERN_4.findall(user_input)
    # Initialize an ssn counter. 
    s_counter = 1
    # For each match found.
    for s in ssn_matches:
        # Maps the ssn with format XXX-XX-100#
        dict_ssn[s] = f"XXX-XX-{1000+s_counter:04d}"
        # Replaces the found ssns with the XXX-XX-100#
        user_input = user_input.replace(s, dict_ssn[s])
        # Iterates the SSN counter
        s_counter += 1

    # #####################
    # Names
    # #####################

    # Load the English words list (it's a set for fast lookup)
    english_words = set(w.lower() for w in words.words())
    # Load a pre-trained English model (you might need to download it first: python -m spacy download en_core_web_sm)
    nlp = spacy.load("en_core_web_sm")
    # Initialize the NLP
    doc = nlp(user_input)
    # Identify all subjects in the sentence
    sub_toks = [tok for tok in doc if (tok.dep_=="nsubj")]
    # Identify all the entities with PERSON label
    person_names = {ent.text for ent in doc.ents if ent.label_ == "PERSON"}
    # Initialize a name counter
    n_counter = 1
    # For each subject found in the sub_toks
    for subject in sub_toks:
        # Is the subject a person? If no, 
        if subject.text.lower() in english_words:
            continue
        # If yes
        else: 
            # Add the person to the persons_name set.
            person_names.add(subject.text)
    # For each person in the set
    for name in person_names: 
        # Checks for common FPs and removes
        if name == 'Email' or name == 'Volunteer':
            person_names.remove(name)
        # Maps the name to a dummy value = name#
        dict_name[name] = f"name{n_counter}"
        # Replaces the name with the dummy value in the string
        user_input = user_input.replace(name, dict_name[name])
        # Iterates the name counter
        n_counter = n_counter + 1
    print(dict_name)
    return user_input, dict_email, dict_ssn, dict_name


'''
Fail cases found: 
    O'Connor, O'Malley fails
    - o'malley works?
        omalley works
    
    - fails with single names too

    have an issue with not separating names out
    {"george O'malley george omalley": 'name1'}
    {'zoey adam kirby riley caitlin maleah': 'name1'}


    'XXX-XX-1004': 'name11'}

    Russian names fail: 
        Dmitry Иванов

    French names fail
        Léon Dupont

    Japense names normally succeed but wiht a few failures
        Kobayashi Riku

    Chinese names normally succeed but occasionally fail
        Lui Fang
'''

def main(): 
    sanitize_input("Susan Davis recently got married. ")

if __name__ == '__main__':
    main()
