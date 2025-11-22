import re
# For name recognition
import spacy
# from spacy.pipeline import EntityRuler
# For English word checking
from nltk.corpus import words
import unicodedata
import sys

# ---------------- REGEX DEFINITIONS ----------------

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") # Matches email addresses 
EMAIL_PATTERN_2 = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\,[a-zA-Z]{2,}") # Matches email addresses with comma typo

SSN_PATTERN_1 = re.compile(r"\d{3}-\d{2}-\d{4}") # Matches format ###-##-####
SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # Matches format ### ## ####
SSN_PATTERN_3 = re.compile(r"\d{3} \d{2}-\d{4}") # Matches format ### ##-####
SSN_PATTERN_4 = re.compile(r"\d{3}-\d{2} \d{4}") # Matches format ###-## ####
SSN_PATTERN_5  = re.compile(r"\d{9}") # Matches for #########

DATE_PATTERN_1 = re.compile(r"\d{2}\/\d{2}\/\d{4}") # matches for ##/##/#### ex. 01/03/2024
DATE_PATTERN_2 = re.compile(r"\d{1}\/\d{1}\/\d{2}") # Matches for #/#/## ex. 1/3/24

PHONE_PATTERN_1 = re.compile (r"\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}") # matches 1231231234
PHONE_PATTERN_2 = re.compile(r"\+([1-9]\d{0,2})[-.\s]?\(?\d{1,3}\)?([-.\s]?\d{1,3}){2,3}") # matches phone numbers with extensions

BIRTHDAY_PATTERN_1 = re.compile(r"(?:\d{1}|\d{2}|\d{4})[-\\/](?:\d{1}|\d{2}|\d{4})[-\\/](?:\d{1}|\d{2}|\d{4})") 
# Above matches format: 
# ##/##/#### or ##\##\#### or ##-##-#### or ####-##-## or ####/##/## or ####\##\##
MONTH = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
SEP = r"[ \-\\/]+"   
BIRTHDAY_PATTERN_2 = re.compile(rf"{MONTH}{SEP}\d{1,2}{SEP}\d{2,4}") # Matches Jan 11 2003, January 11 2003, January 1 03
BIRTHDAY_PATTERN_3 = re.compile(rf"\d{{1,2}}{SEP}{MONTH}{SEP}\d{{2,4}}") # Matches day month year format


# ---------------- Global Parameters ----------------

NLP = None
ENGLISH_WORDS = None

# ---------------- Helper Functions ----------------

'''
This function will lacy load spaCy models for use in name sanitization. 
Parameters: 
    - None
Returns: 
    - NLP 
'''
def get_nlp():
    # Tells the function that NLP is a global variable, not function scope variable
    global NLP
    # If NLP is none
    if NLP is None: 
        # Try to download spaCy large model
        try: 
            NLP = spacy.load("en_core_web_lg")
        # If error, try and download spaCy small model
        except OSError:
            NLP = spacy.load("en_core_web_sm")
    return NLP
'''
This function will lacy load NLTK words for use in name sanitization. 
Parameters: 
    - None
Returns: 
    - ENGGLISH_WORDS 
'''
def get_english_words():
    # Establishes the scope of ENGLISH WORDS
    global ENGLISH_WORDS
    if ENGLISH_WORDS is None: 
        try:
            ENGLISH_WORDS = set(w.lower() for w in words.words())
        # Catches if NLTK words is not downloaded correctly and generates an error
        except LookupError:
            raise RuntimeError(
                "❌ NLTK English word list not found. Please run:\n"
                "    >>> import nltk\n"
                "    >>> nltk.download('words')\n"
                "and then restart your application.")
        # Catch all for if errors appear
        except Exception as e: 
            raise RuntimeError(f"Unexpected error loading NLTK words: {e}")
    return ENGLISH_WORDS

'''
Function to remove strange characters, whitespace, etc in string. 
Parameters: 
    - string : the string with potentially weird characters
Returns: 
    - string : the string with removed weird characters
'''
def normalize(string):
    string = unicodedata.normalize("NFKC", string)
    return re.sub(r"[^\w\s',.@]", '', string, flags=re.UNICODE).strip()



def is_token_suffix(string_a, string_b):
    a_tokens = string_a.lower().split()
    b_tokens = string_b.lower().split()
    return len(a_tokens) < len(b_tokens) and a_tokens == b_tokens[-len(a_tokens):]

# ---------------- Primary Sanitization Functions ----------------

'''
This function is responsible for only sanitizing names. It is called
in sanitize_input()
Parameters: 
    - user_input : string containing the original prompt
    - dict_email : dictionary of found emails. 
Returns: 
    - sanitized_user_input : string containing the original prompt and replacement phone numbers. 
    - user_input : string containing original user input
    - dict_name : dictionary of found names.'''
def sanitize_names(user_input, dict_email):
    sanitized_user_input = user_input
    dict_name = {}
    # Load a pre-trained English model (you might need to download it first: python -m spacy download en_core_web_sm)

    nlp = get_nlp()
    # Load the English words list (it's a set for fast lookup)

    english_words = get_english_words()  
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
            (subj.pos_ != "PROPN" and subj.text.lower() not in english_words)
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
        if name.lower() in  {"email", "volunteer", "name"}:
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
        sanitized_user_input = re.sub(pattern, dict_name[name], sanitized_user_input)
        # Iterates the name counter
        n_counter = n_counter + 1
    return sanitized_user_input, user_input, dict_name
'''
Sanitizes only the SSNs in the user prompt. 
Parameters: 
    - user_input : string containing the original prompt. 
Returns: 
    - dict_ssn : a dictionary containing found SSNs and the replacements
    - sanitized_user_input : string containing the original prompt and replacement phone numbers. 
    - user_input : string containing original user input

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
        sanitized_user_input = sanitized_user_input.replace(s, dict_ssn[s])
        # Iterates the SSN counter
        s_counter += 1
    return sanitized_user_input, user_input, dict_ssn
'''
Sanitizes only the emails in the user prompt. 
Parameters: 
    - user_input : string containing the original prompt. 
Returns: 
    - dict_email : a dictionary containing found emails and the replacements
    - sanitized_user_input : string containing the original prompt and replacement phone numbers. 
    - user_input : string containing original user input

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
        sanitized_user_input = sanitized_user_input.replace(e, dict_email[e])
        # Iterate the email counter by one
        email_counter += 1
    return sanitized_user_input, user_input, dict_email

'''
Fills in the LLM response with the original data. 
Paramters: 
    - response : string containing the LLM response
    - dict_email : a dictionary containing the found emails and replacement email.
    - dict_ssn : a dictionary containing the found SSNs and replacement SSN.
    - dict_name : a dictionary containing the found names and replacement names. 
    - dict_phone : a dictionary containing the found phone numbers and replacement phone numbers.
Outputs: 
    - response : String of LLM response with replacement values replaced with original values. '''
def fill_in_llm_response(response, dict_email, dict_ssn, dict_name, dict_phone):
    # Replaces fake emails with the given email
    for email, fake_email in dict_email.items(): 
        response = response.replace(fake_email, email)
    # Replaces fake names with the given names
    for name, fake_name in dict_name.items():
        # checks for exact matches
        response = response.replace(fake_name, name)
        # Checks for capitlized variant. 
        response = response.replace(str.capitalize(fake_name), str.capitalize(name))
    # Replaces fake SSNs with the given SSNs
    for ssn, fake_ssn in dict_ssn.items(): 
        response = response.replace(fake_ssn, ssn)
    # Replaces fake phone numbers with the given phone numbers
    for phone, fake_phone in dict_phone.items():
        response = response.replace(fake_phone, phone)
    return response

'''
Sanitizes only the phone numbers in the user prompt. 
Parameters: 
    - user_input : string containing the original prompt. 
Returns: 
    - dict_phone : a dictionary containing found phone numbers and the replacements
    - sanitized_user_input : string containing the original prompt and replacement phone numbers. 
    - user_input : string containing original user input

 '''
def sanitize_phonenumbers(user_input):
    # Initialize a dictionary for found and replacement numbers
    dict_phone = {}
    # Rename variable
    sanitized_user_input = user_input
    # Search for phone numbers that match the REGEX patterns
    phone_matches = PHONE_PATTERN_1.findall(user_input) + PHONE_PATTERN_2.findall(user_input)
    phone_counter = 1
    # Iterate through matches
    for phone in phone_matches: 
        # Replaces matches with a fake number
        dict_phone[phone] = f"(111)111-111{phone_counter}"
        # Rewrites sanitized input with the replacement string
        sanitized_user_input = user_input.replace(phone, dict_phone[phone])
        phone_counter = phone_counter + 1
    return sanitized_user_input, user_input, dict_phone

'''
This function is the primary sanitization function. 
Parameters: 
    - user_input : A string entered by the user. The prompt. 
Outputs: 
    - dict_email : a dictionary containing the found emails and replacement email.
    - dict_ssn : a dictionary containing the found SSNs and replacement SSN.
    - dict_name : a dictionary containing the found names and replacement names. 
    - dict_phone : a dictionary containing the found phone numbers and replacement phone numbers.
'''

def choose_sanitize_word(sanitized_user_input, user_input,
                         dict_email, dict_ssn, dict_name, dict_phone,
                         flask_choices=None):
    # Helper function to process a single dictionary
    def process_dict(label, data_dict):
        # Local to the inner function 
        nonlocal sanitized_user_input

        for original, replacement in list(data_dict.items()):
            # For Flask implementation
            if flask_choices is not None: 
                user_wants = flask_choices.get(original, True)
            
            # For CLI implementation
            elif sys.stdin.isatty():
                print(f"\nDetected {label}: \033[33m{original}\033[0m")
                print(f"Suggested replacement → {replacement}")
                # Get the user answer
                choice = input("Sanitize this? (yes/no): ").strip().lower()
                user_wants = (choice == "yes")
            # Default case = Sanitize all
            else: 
                user_wants = True
            
            # Apply user_wants
            if not user_wants: 
                # remove the dummy value, restore original 
                sanitized_user_input = sanitized_user_input.replace(replacement, original)
                del data_dict[original]     # Remove from dictionary
        return data_dict
    # process each data category
    dict_email = process_dict("email", dict_email)
    dict_ssn = process_dict("SSN", dict_ssn)
    dict_name = process_dict("name", dict_name)
    dict_phone = process_dict("phone number", dict_phone)
    return sanitized_user_input, dict_email, dict_ssn, dict_name, dict_phone


def sanitize_input(user_input): 
    user_input = normalize(user_input)


    # #####################
    # Emails
    # #####################

    sanitized_email, raw_user_input, dict_email = sanitize_emails(user_input)
    
    # #####################
    # SSNs
    # #####################

    sanitized_ssn, raw_user_input, dict_ssn = sanitize_ssns(sanitized_email)

    # #####################
    # Names
    # #####################

    sanitized_names, raw_user_input, dict_name = sanitize_names(sanitized_ssn, dict_email)
    
    # #####################
    # Phones
    # #####################
    
    sanitized_user_input, raw_user_input, dict_phone = sanitize_phonenumbers(sanitized_names)
    sanitized_user_input, dict_email, dict_ssn, dict_name, dict_phone = choose_sanitize_word(
        sanitized_user_input,
        user_input,
        dict_email,
        dict_ssn,
        dict_name,
        dict_phone
    )
    return sanitized_user_input, user_input, dict_email, dict_ssn, dict_name, dict_phone

