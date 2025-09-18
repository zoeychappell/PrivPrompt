import re
# for name recognition
import spacy

def sanitize_input(user_input): 
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") # Matches email addresses 
    SSN_PATTERN_1 = re.compile(r"\d{3}-\d{2}-\d{4}") # Matches format ###-##-####
    SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # Matches format ### ## ####
    SSN_PATTERN_3 = re.compile(r"\d{3} \d{2}-\d{4}") # Matches format ### ##-####
    SSN_PATTERN_4 = re.compile(r"\d{3}-\d{2} \d{4}") # Matches format ###-## ####
    dict_email = {}
    dict_ssn = {}
    dict_name = {}

    # Emails
    email_matches = EMAIL_PATTERN.findall(user_input)
    counter = 1
    for e in email_matches:
        dict_email[e] = f"user{counter}@email.com"
        user_input = user_input.replace(e, dict_email[e])
        counter += 1

    # SSNs
    ssn_matches = SSN_PATTERN_1.findall(user_input) + SSN_PATTERN_2.findall(user_input) + SSN_PATTERN_3.findall(user_input) + SSN_PATTERN_4.findall(user_input)
    s_counter = 1
    for s in ssn_matches:
        dict_ssn[s] = f"XXX-XX-{1000+s_counter:04d}"
        user_input = user_input.replace(s, dict_ssn[s])
        s_counter += 1

    # Names
    # Load a pre-trained English model (you might need to download it first: python -m spacy download en_core_web_sm)
    nlp = spacy.load("en_core_web_sm")

    text = user_input
    doc = nlp(text)

    person_names = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person_names.append(ent.text)
    n_counter = 1
    for n in person_names: 
        dict_name[n] = f"name{n_counter}"
        user_input = user_input.replace(n, dict_name[n])
        n_counter = n_counter + 1
    print(dict_name)
    return user_input, dict_email, dict_ssn, dict_name


