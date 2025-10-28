import sys
#from user_input import clean_input
from sanitize import sanitize_input, fill_in_llm_response
from llm_clients.groq_llm_client import call_groq
from llm_clients.cohere_llm_client import cohere
from llm_clients.google_genai_llm_client import call_genai
from llm_clients.deepseek_llm_client import call_deepseek
from llm_clients.workers_ai_llm_client import call_workers_ai

LIST_OF_LLMS = ["Llama", "Cohere", "Gemini", "Deepseek", "Workers AI"]

class CLI: 
    def __init__(self):
        self.chosen_llm = None

    '''
    Function that takes in the user input, then cleans the input. 
    Parameters: 
        - user_input : The string returned from user_input function. 
    Returns: 
        - cleaned_user_input : A nicely formatted string'''
    def clean_input(self):
        # By using sys.stdin.read(), the program can accept multiple lines of input
        print("\033[1;36mPlease type your message. \033[0m \n" \
        "\033[36mType \033[33m'Done'\033[0m \033[36m on a new line to finish.\n" \
        "Type \033[33m'Exit Program'\033[0m \033[36mor \033[33mCTRL-C\033[0m \033[36m to exit the program.\033[0m")
        lines = []
        # Iterates through each line the user enteres.
        for line in sys.stdin:
            # Note for sys.stdin - can introduce character limits
            # Checks if the user enters "exit program"
            if line.strip().lower() == "exit program":
                return "__EXIT__"
            # User enters 'done' when they want to send the prompt to the LLM
            if line.strip().lower() == "done":
                break

            # Removes the new lines
            lines.append(line.rstrip("\n"))
        # Joins the user input into one big string separated by spaces
        user_text = " ".join(lines)
        # Verifies that all new lines are removed and trims whitespace
        cleaned_user_input = user_text.replace("\n", "").replace("\r", "")
        # Return the cleaned input and trims whitespace.
        return cleaned_user_input.strip()
    
    '''
    This function prints a help menu for the user. 
    Parameters: 
        - self
    Returns: 
        - None
    '''
    def show_help(self):
        print("\033[36m" + "="*40)
        print("                Help Menu")
        print("="*40 + "\033[0m")
        print("\033[34mAvailable commands at any time:\033[0m")
        print("  \033[33mhelp / h / ?\033[0m  -> Show this help menu")
        print("  \033[33mExit Program\033[0m   -> Quit the program")
        print("  \033[33mDone\033[0m   -> Finish the prompt and send it to the LLM")
        print("\033[36m" + "="*40 + "\033[0m")

    '''
    This function is responsible for continuous prompting, printing the program, and controlling the cli. 
    Parameters: 
        - self
    Returns: 
        - None
    '''
    def cli(self):
        # Wraps the entire CLI program in a try statement to accept keyboard shortcuts
        try: 
            print("\n\033[1;34m=== Welcome to PrivPrompt! ===\033[0m\n")

            # Creates a list of available LLMs controlled by the global variable LIST_OF_LLMS
            print("\033[1;34mAvailable LLMs: \033[0m")
            llm_lookup = {llm.lower(): llm for llm in LIST_OF_LLMS}
            # Prints a pretty version of the llm_lookup table to the user
            for id, llm in enumerate(LIST_OF_LLMS, start=1):
                print(f"   \033[36m{id}. {llm}")
            
            while not self.chosen_llm:
                llm_choice = input("\n\033[1;34mWhich LLM would you like to use? (number or name): \033[0m").lower().strip()
                
                if llm_choice in ["help", "h", "?"]:
                    self.show_help()
                    continue
                
                if llm_choice in llm_lookup:
                    self.chosen_llm = llm_choice
                else: 
                    print("\033[1;31m[!] Invalid choice. Please select another LLM.\033[0m")
            
            # === Main loop ===
            while True:
                command = self.clean_input()

                if command == '__EXIT__':
                    print("\n\033[1;32mThanks for using PrivPrompt! Goodbye.\033[0m\n")
                    break
                elif command.lower() in ["help", "h", "?"]:
                    self.show_help()
                    continue

                sanitized_input, dict_email, dict_ssn, dict_name = sanitize_input(command)
                response = "No response"
                # === Send to LLM ===
                if self.chosen_llm == "llama":
                    response = call_groq(sanitized_input)   
                elif self.chosen_llm == "cohere":
                    response = cohere(sanitized_input)
                elif self.chosen_llm == "gemini":
                    response = call_genai(sanitized_input)
                elif self.chosen_llm == "deepseek":
                    response = call_deepseek(sanitized_input)
                elif self.chosen_llm == 'workers ai':
                    response = call_workers_ai(sanitized_input)
                else: 
                    response = f"There was an error."

                filled_in_response = fill_in_llm_response(response, dict_email, dict_ssn, dict_name)
                print("\n" + "\033[35m" + "-"*40 + "\033[0m")
                print(f"\033[35m[{self.chosen_llm.upper()}]\033[0m")
                print(f"\033[34mYou entered:\033[0m {command}")
                print(f"\033[34mSanitized prompt:\033[0m {sanitized_input}")
                print(f"\033[34mOriginal LLM response:\033[0m {filled_in_response}")
                print(f"\033[34mFilled in LLM Response:\033[0m {response}")
                print("\033[35m" + "-"*40 + "\033[0m\n")

        except KeyboardInterrupt: 
            print("\n\033[1;31mProgram interrupted by user. \033[1;32m\nThanks for using PrivPrompt! Goodbye.\033[0m\n")


def main():
    cli_instance = CLI()
    cli_instance.cli()

if __name__ == '__main__':
    main()
