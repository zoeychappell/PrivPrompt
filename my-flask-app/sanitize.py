import re
# for name recognition
import spacy
from spacy.pipeline import EntityRuler
# For human name recognition
import stanza
from nltk.corpus import words
'''
This function will take in a filepath, try to open it, and 
add the contents of the file to a list. 
Parameters: 
    filepath (str) : Path to the file with the names
Returns: 
    names_list (list) : The new list with all the names
'''
def open_file(filepath):
    names_list = []
    try: 
        with open(filepath, mode = 'r') as file:
            for lines in file: 
               line = lines.rstrip()
               names_list.append(line)
        file.close()
    except FileNotFoundError as fnfe:
        print("The file is not found. ")
    return names_list

def sanitize_input(user_input): 


    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") # Matches email addresses 
    SSN_PATTERN_1 = re.compile(r"\d{3}-\d{2}-\d{4}") # Matches format ###-##-####
    SSN_PATTERN_2 = re.compile(r"\d{3} \d{2} \d{4}") # Matches format ### ## ####
    SSN_PATTERN_3 = re.compile(r"\d{3} \d{2}-\d{4}") # Matches format ### ##-####
    SSN_PATTERN_4 = re.compile(r"\d{3}-\d{2} \d{4}") # Matches format ###-## ####
    SSN_PATTERN_5  = re.compile(r"\d[0-9]{9}")
    dict_email = {}
    dict_ssn = {}
    dict_name = {}

    # #####################
    # Emails
    # #####################

    email_matches = EMAIL_PATTERN.findall(user_input)
    counter = 1
    for e in email_matches:
        dict_email[e] = f"user{counter}@email.com"
        user_input = user_input.replace(e, dict_email[e])
        counter += 1
    
    # #####################
    # SSNs
    # #####################

    ssn_matches = SSN_PATTERN_1.findall(user_input) + SSN_PATTERN_2.findall(user_input) + SSN_PATTERN_3.findall(user_input) + SSN_PATTERN_4.findall(user_input)
    s_counter = 1
    for s in ssn_matches:
        dict_ssn[s] = f"XXX-XX-{1000+s_counter:04d}"
        user_input = user_input.replace(s, dict_ssn[s])
        s_counter += 1

    # #####################
    # Names
    # #####################

    # Load the English words list (it's a set for fast lookup)
    english_words = set(w.lower() for w in words.words())
    # Load a pre-trained English model (you might need to download it first: python -m spacy download en_core_web_sm)
    nlp = spacy.load("en_core_web_sm")
    # ruler = nlp.add_pipe('entity_ruler', before="ner")
    # names_list = open_file('data/female_lower.txt')
    #names_list = open_file('data/male_lower.txt')
    #patterns = [{"label": "PERSON", "pattern": name} for name in names_list]
    #ruler.add_patterns(patterns)

    # Note: spacy has a displaCy visualizer 
    text = user_input
    doc = nlp(text)
    sub_toks = [tok for tok in doc if (tok.dep_=="nsubj")]
    person_names = {ent.text for ent in doc.ents if ent.label_ == "PERSON"}
    '''for ent in doc.ents:
        if ent.label_ == "PERSON":
            person_names.append(ent.text)'''
    n_counter = 1
    for subject in sub_toks:
        # Is the subject a person? If no, 
        if subject.text.lower() in english_words:
            continue
        # If yes
        else: 
            person_names.add(subject.text)
    for n in person_names: 
        if n == 'Email' or n == 'Volunteer':
            person_names.remove(n)
        dict_name[n] = f"name{n_counter}"
        user_input = user_input.replace(n, dict_name[n])
        n_counter = n_counter + 1
    
        '''
    Note from zoey: 
    I'm currently testing out solutions for name recognition. 
    Stanza is slower and tends seems to be about the same as spaCy
    so i'm not sold yet 
    --------------------------
    nlp_stanza = stanza.Pipeline('en')
    doc_stanza = nlp_stanza("Zoey Is A Person, so is Barack Obama")
    print(doc_stanza.entities)
    '''
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
    sanitize_input("zoey is my friend")
    sanitize_input("john is my buddy. ")
    sanitize_input("apple is my friend")

if __name__ == '__main__':
    main()
