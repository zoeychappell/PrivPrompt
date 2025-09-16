from user_input import clean_input
from sanitize import sanitize_input, fill_data   # 👈 import your sanitizer
from llm_clients.groq_llm_client import groq
from llm_clients.cohere_llm_client import cohere

LIST_OF_LLMS = ["Llama", "Cohere"]

class CLI: 
    def __init__(self):
        self.chosen_llm = None

    def show_help(self):
        print("\033[34m\n=== Help Menu ===")
        print("Available commands at any time:")
        print("  help / h / ?  -> Show this help menu")
        print("  exit / Done   -> Quit the program")
        print("=================\n\033[0m")
    
    def cli(self):
        print("\033[34mWelcome to PrivPrompt!\033[0m \n")

        print("\033[34mAvailable LLMs: \033[0m")
        llm_lookup = {llm.lower(): llm for llm in LIST_OF_LLMS}

        for id, llm in enumerate(LIST_OF_LLMS, start=1):
            print(f"{id}. {llm}")
        
        while not self.chosen_llm:
            llm_choice = input("\n\033[34mWhich LLM would you like to use? (number or name): \033[0m").lower().strip()
             
            if llm_choice in ["help", "h", "?"]:
                self.show_help()
                continue
            
            if llm_choice in llm_lookup:
                self.chosen_llm = llm_choice
            else: 
                print("\033[31mInvalid choice. Please select another LLM. \033[0m")
        
        # === Main loop ===
        while True:
            command = clean_input()

            if command.lower() in ["done", "exit"]:
                print("\033[34mThanks! Goodbye. \033[0m")
                break
            elif command.lower() in ["help", "h", "?"]:
                self.show_help()
                continue

            # 🟢 Sanitize input here
            sanitized_input, dict_email, dict_ssn = sanitize_input(command)

            # === Send to LLM ===
            if self.chosen_llm == "llama":
                response = groq(sanitized_input)   
            elif self.chosen_llm == "cohere":
                response = cohere(sanitized_input)
            else: 
                response = f"Unknown LLM: {self.chosen_llm}"

            # 🟢 Fill back original PII into LLM response
            response = fill_data(dict_email, dict_ssn, response)

            print(f"\033[35m[{self.chosen_llm}]\033[0m \033[34mYou entered:\033[0m {command}")
            print(f"\033[34mLLM Response:\033[0m {response}")


def main():
    cli_instance = CLI()
    cli_instance.cli()

if __name__ == '__main__':
    main()
