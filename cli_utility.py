
from user_input import clean_input
LIST_OF_LLMS = ["groq"]

class CLI: 
    def __init__(self):
        self.chosen_llm = None
    '''
    Shows a help menu. 
    '''
    def show_help(self):
        """Print the help guide."""
        print("\033[34m\n=== Help Menu ===")
        print("Available commands at any time:")
        print("  help / h / ?  -> Show this help menu")
        print("  exit / Done   -> Quit the program")
        print("=================\n\033[0m")
    
    def cli(self):
        print("\033[34mWelcome to PrivPompt!\033[0m \n")

        print("\033[34mAvailable LLMs: \033[0m")
        for id, llm in enumerate(LIST_OF_LLMS, start = 1):
            print(f"{id}. {llm}")
        
            llm_choice = input("\n\033[34mWhich LLM would you like to use? (number or name): \033[0m").strip()
             
            if llm_choice.lower() in ["help", "h", "?"]:
                self.show_help()
                continue
            
            elif (llm_choice.lower() in LIST_OF_LLMS):
                self.chosen_llm = llm_choice
            else: 
                print("\033[31mInvalid choice. Please select another LLM. \033[0m")
        command = clean_input()

        if command.lower() in ["done", "exit"]:
            print("\033[34mThanks! Goodbye. \033[0m")
            # need to close gracefully here
        elif command.lower() in ["help", "h", "?"]:
            self.show_help()
            
        else: 
            print(f"\033[35m[{self.chosen_llm}]\033[0m \033[34mYou entered \033[0m {command}")

        return command
    
def main():
    cli_instance = CLI()
    cli_instance.cli()

if __name__ == '__main__':
    main()
