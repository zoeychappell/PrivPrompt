from user_input import clean_input
from sanitize import sanitize_input
from llm_clients.groq_llm_client import call_groq
from llm_clients.cohere_llm_client import cohere

LIST_OF_LLMS = ["Llama", "Cohere"]

class CLI: 
    def __init__(self):
        self.chosen_llm = None

    def show_help(self):
        print("\033[36m" + "="*40)
        print("                Help Menu")
        print("="*40 + "\033[0m")
        print("\033[34mAvailable commands at any time:\033[0m")
        print("  \033[33mhelp / h / ?\033[0m  -> Show this help menu")
        print("  \033[33mexit / Done\033[0m   -> Quit the program")
        print("\033[36m" + "="*40 + "\033[0m")

    
    def cli(self):
        try: 
            print("\n\033[1;34m=== Welcome to PrivPrompt! ===\033[0m\n")


            print("\033[1;34mAvailable LLMs: \033[0m")
            llm_lookup = {llm.lower(): llm for llm in LIST_OF_LLMS}

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
                command = clean_input()

                if command == '__EXIT__':
                    print("\n\033[1;32mThanks for using PrivPrompt! Goodbye.\033[0m\n")
                    break
                elif command.lower() in ["help", "h", "?"]:
                    self.show_help()
                    continue

                sanitized_input, dict_email, dict_ssn = sanitize_input(command)
                response = "No response"
                # === Send to LLM ===
                if self.chosen_llm == "llama":
                    response = call_groq(sanitized_input)   
                elif self.chosen_llm == "cohere":
                    response = cohere(sanitized_input)
                else: 
                    response = f"There was an error."


                print("\n" + "\033[35m" + "-"*40 + "\033[0m")
                print(f"\033[35m[{self.chosen_llm.upper()}]\033[0m")
                print(f"\033[34mYou entered:\033[0m {command}")
                print(f"\033[34mLLM Response:\033[0m {response}")
                print("\033[35m" + "-"*40 + "\033[0m\n")
        except KeyboardInterrupt: 
            print("\n\033[1;31mProgram interrupted by user. \033[1;32m\nThanks for using PrivPrompt! Goodbye.\033[0m\n")


def main():
    cli_instance = CLI()
    cli_instance.cli()

if __name__ == '__main__':
    main()
