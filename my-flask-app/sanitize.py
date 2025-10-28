import re
# For name recognition
import spacy
# from spacy.pipeline import EntityRuler
# For English word checking
from nltk.corpus import words
import unicodedata

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") # Matches email addresses 
EMAIL_PATTERN_2 = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\,[a-zA-Z]{2,}") # Matches email addresses with comma typo

SSN_PATTERN_1 = re.compile(r"\d{3}-\d{2}-\d{4}") # Matches format ###-##-####
SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # Matches format ### ## ####
SSN_PATTERN_3 = re.compile(r"\d{3} \d{2}-\d{4}") # Matches format ### ##-####
SSN_PATTERN_4 = re.compile(r"\d{3}-\d{2} \d{4}") # Matches format ###-## ####
SSN_PATTERN_5  = re.compile(r"\d[0-9]{9}")

DATE_PATTERN_1 = re.compile(r"\d{2}\/\d{2}\/\d{4}") # matches for ##/##/#### ex. 01/03/2024
DATE_PATTERN_2 = re.compile(r"\d{1}\/\d{1}\/\d{2}") # Matches for #/#/## ex. 1/3/24

   
    # TO DOs
    # Matches for #/#/#### ex. 1/3/2024
    # Matches for ##/#/#### ex. 01/3/2024
    # Matches for 
    # do boht month/day/year and day/month/year


def normalize(string):
    string = unicodedata.normalize("NFKC", string)
    return re.sub(r"[^a-zA-Z0-9\s',.@]+", '', string).strip()

def is_token_suffix(string_a, string_b):
    a_tokens = string_a.lower().split()
    b_tokens = string_b.lower().split()
    return len(a_tokens) < len(b_tokens) and a_tokens == b_tokens[-len(a_tokens):]
'''
This function is responsible for only sanitizing names. It is called
in sanitize_input()
Parameters: 
    - user_input : string containing the original prompt
    - dict_email : dictionary of found emails. 
Returns: 
    - user_input : string with the original prompt but no names. 
    - dict_name : dictionary of found names.'''
def sanitize_names(user_input, dict_email):
    sanitized_user_input = user_input
    dict_name = {}

    # Load the English words list (it's a set for fast lookup)
    english_words = set(w.lower() for w in words.words())
    # Load a pre-trained English model (you might need to download it first: python -m spacy download en_core_web_sm)
    nlp = spacy.load("en_core_web_lg")
    # Initialize the NLP
    doc = nlp(user_input)
    # Identify all subjects in the sentence
    sub_toks = [tok for tok in doc if (tok.dep_=="nsubj")]
    # Identify all the entities with PERSON label
    canditates_name = set()
    orig_map = {}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            norm = normalize(ent.text).lower()
            if norm: 
                canditates_name.add(norm)
                orig_map.setdefault(norm, []).append(ent.text)
    PRONOUNS = {
        "i", "me", "my", "mine", "you", "your", "yours", "he", "him", "his",
        "she", "her", "hers", "it", "its", "we", "us", "our", "ours",
        "they", "them", "their", "theirs", "who", "whom"
    }
    # For each subject found in the sub_toks
    for subj in sub_toks:
        if (
            # Check that the word is not a normal english word and not a proper known
            (subj.pos_ != "PROPN" or subj.text.lower() not in english_words)
            # Following three checks for email identification issue.
            and not subj.text in dict_email
            and not EMAIL_PATTERN.match(subj.text)
            and not EMAIL_PATTERN_2.match(subj.text)
            and not subj.text in PRONOUNS
        ):
            norm = normalize(subj.text).lower()
            if norm: 
                canditates_name.add(norm)
                orig_map.setdefault(norm, []).append(subj.text)
    # Note - keeping for now because i might change back to the original (which is commented out.)
    filtered = canditates_name
    #filtered = {name for name in canditates_name
             #   if not any(is_token_suffix(name, other) for other in canditates_name) }

    person_names = set()
    for norm in filtered:
        originals = orig_map.get(norm, [norm])
        chosen = max(originals, key=lambda s: len(s.split()))
        person_names.add(chosen)

    # Remove known False Positives
    cleaned_names = set()
    
    for name in person_names:
        if name.lower() in  {"email", "volunteer"}:
            continue
        if EMAIL_PATTERN.match(name.lower()):
            continue
        if EMAIL_PATTERN_2.match(name.lower()):
            continue
        if any(fake_email in name for fake_email in dict_email.values()):
            continue
        cleaned_names.add(name)
    # Update person_names
    person_names = cleaned_names

    # Initialize a name counter
    n_counter = 1
    # Makes it so the names are sorted by length with longest first. 
    for name in sorted(person_names, key=len, reverse=True):
        # Maps the name to a dummy value = name#
        dict_name[name] = f"name{n_counter}"
        # Replaces the name with the dummy value in the string
        pattern = r"\b" + re.escape(name) + r"\b"
        sanitized_user_input = re.sub(pattern, dict_name[name], user_input)
        # Iterates the name counter
        n_counter = n_counter + 1
    return sanitized_user_input, user_input, dict_name
'''
Sanitizes only the SSNs in the user prompt. 
Parameters: 
    - user_input : string containing the original prompt. 
Returns: 
    - dict_ssn : a dictionary containing found SSNs and the replacements
    - user_input : string containing the original prompt and replacement SSNs. 
'''
def sanitize_ssns(user_input):
    dict_ssn = {}
    sanitized_user_input = user_input
    # Checks the user input for any strings matching the regex pattern. 
    ssn_matches = SSN_PATTERN_1.findall(user_input) + SSN_PATTERN_2.findall(user_input) + SSN_PATTERN_3.findall(user_input) + SSN_PATTERN_4.findall(user_input)
    # Initialize an ssn counter. 
    s_counter = 1
    # For each match found.
    for s in ssn_matches:
        # Maps the ssn with format XXX-XX-100#
        dict_ssn[s] = f"XXX-XX-{1000+s_counter:04d}"
        # Replaces the found ssns with the XXX-XX-100#
        sanitized_user_input, user_input = user_input.replace(s, dict_ssn[s])
        # Iterates the SSN counter
        s_counter += 1
    return sanitized_user_input, user_input, dict_ssn
'''
Sanitizes only the emails in the user prompt. 
Parameters: 
    - user_input : string containing the original prompt. 
Returns: 
    - dict_email : a dictionary containing found emails and the replacements
    - user_input : string containing the original prompt and replacemtn emails. 
'''
def sanitize_emails(user_input):
    sanitized_user_input = user_input
    dict_email = {}
    # Checks the user input for any strings matching the regex pattern. 
    email_matches = EMAIL_PATTERN.findall(user_input) + EMAIL_PATTERN_2.findall(user_input)
    # Initializes an email counter
    email_counter = 1
    # Iterates through found emails
    for e in email_matches:
        # Maps the email to a fake email user#@email.com
        dict_email[e] = f"user{email_counter}@email.com"
        # Replaces the found emails with user#@email.com
        sanitized_user_input = user_input.replace(e, dict_email[e])
        # Iterate the email counter by one
        email_counter += 1
    return sanitized_user_input, user_input, dict_email
'''
This function is the primary sanitization function. 
Parameters: 
    - user_input : A string entered by the user. The prompt. 
Outputs: 
    - dict_email : a dictionary containing the found emails and replacement email
    - dict_ssn : a dictionary containing the found SSNs and replacement SSN
    - dict_name : a dictionary containing the found names and replacement names. 
'''
def fill_in_llm_response(response, dict_email, dict_ssn, dict_name):
    for email, fake_email in dict_email.items(): 
        response = response.replace(fake_email, email)
    for name, fake_name in dict_name.items():
        response = response.replace(fake_name, name)
    for ssn, fake_ssn in dict_ssn.items(): 
        response = response.replace(fake_ssn, ssn)

    return response

def sanitize_input(user_input): 
    user_input = normalize(user_input)

    dict_email = {}
    dict_ssn = {}
    dict_name = {}

    # #####################
    # Emails
    # #####################

    sanitized_email, raw_user_input, dict_email = sanitize_emails(user_input)
    
    # #####################
    # SSNs
    # #####################

    sanitize_ssn, raw_user_input, dict_ssn = sanitize_ssns(sanitized_email)

    # #####################
    # Names
    # #####################

    sanitized_user_input, raw_user_input, dict_name = sanitize_names(sanitize_ssn, dict_email)
    return sanitized_user_input, user_input, dict_email, dict_ssn, dict_name


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
    # out = normalize("Omg, Jerome is a evil genius. He can hide his friend's name using dashes, like -Jerry! Dang, can't believe \Joshua and also /Jerma can hide in plain sight. Even -Thomas can be hidden like /Celia")
    #print (out)
    dict_email = {}
    user_input = "James David and David James are bringing snacks to the party. James promised to bring chips, and David said he'd handle drinks."

    user_input, dict_name = sanitize_names(user_input, dict_email)
    print (user_input)
    #sanitize_input("Susan Davis (Email SDavis@gma.com, SSN 421-37-1396) recently got married.")
    #sanitize_input("James Heard (Email JAHE@gma.com, SSN 559-81-1301) recently got married. How can I congratulate him? I also heard that James has a friend coming over. I think their name was Thomas Conley. Also, James Smith was coming too. Bunch of James coming over, like James Avery. Hope it all goes well!")
if __name__ == '__main__':
    main()
