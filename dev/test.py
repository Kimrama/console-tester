import os
import sys
import json
import time
from io import StringIO

from rich.console import Console
import keyboard

BANNER = r"""
╔═══════════════════════════════════════════════════════════════════╗
║     ____                      _     _____         _               ║
║    / ___|___  _ __  ___  ___ | | __|_   _|__  ___| |_ ___ _ __    ║
║   | |   / _ \| '_ \/ __|/ _ \| |/ _ \| |/ _ \/ __| __/ _ \ '__|   ║
║   | |__| (_) | | | \__ \ (_) | |  __/| |  __/\__ \ ||  __/ |      ║
║    \____\___/|_| |_|___/\___/|_|\___||_|\___||___/\__\___|_|      ║
║                                                                   ║
║         Kimrama  | tawan123456789 | OkuSan | Archer-SN            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝


"""


class Program :
    def __init__(self) :
        if hasattr(sys, '_MEIPASS'):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.json_file = os.path.join(self.base_dir, 'test_set.json')

        self.page = "Home"

        self.menu_idx = 0
        self.file_idx = 0
        self.set_idx = 0

        self.file_seleted = None
        self.set_seleted = None

        self.file_ls = []
        self.menu_ls = ["TEST", "TEST SET", "CONTRIBUTORS"]
        self.menu_describe_ls = ["Select .py file to test", "Display how many testset available", ""]
        self.set_ls = []

        self.json_file = "test_set.json"

        self.score = 0
    
    def menu_selection_control(self, event) :
        if event.name == "up" and self.menu_idx > 0:
                self.menu_idx -= 1
        if event.name == "down" and self.menu_idx < len(self.menu_ls) - 1:
            self.menu_idx += 1

        if event.name == "enter"  and self.menu_idx == 0:
                self.page = "File"
                self.get_sample_program()

        if event.name == "enter" and self.menu_idx == 1:
            self.page = "Set"
            self.get_test_set()
        
        if event.name == "enter" and self.menu_idx == 2:
            self.page = "About"
    
    def file_selection_control(self, event) :
        if event.name == "up" and self.file_idx > 0:
                self.file_idx -= 1
        if event.name == "down" and self.file_idx < len(self.file_ls) - 1:
            self.file_idx += 1
    
        if event.name == "backspace" :
            self.page = "Home"

        if event.name == "enter" :
            self.get_test_set()
            self.file_seleted = self.file_ls[self.file_idx]

            self.page = "Set"

    def set_selection_control(self, event) :
        if event.name == "up" and self.set_idx > 0:
                self.set_idx -= 1
        if event.name == "down" and self.set_idx < len(self.set_ls) - 1:
            self.set_idx += 1

        if event.name == "backspace" :
            if self.file_seleted :
                self.page = "File"
            else :
                self.page = "Home"
            
        if event.name == "enter" and self.file_seleted :
            self.set_seleted = self.set_ls[self.set_idx]
            self.score = 0
            self.page = "Test"
    
    def about_control(self, event) :
        if event.name == "backspace" : self.page = "Home"

    def handle_keyboard_event(self, event):
        if self.page == "Home" :
            self.menu_selection_control(event)

        elif self.page == "File" :
            self.file_selection_control(event)

        elif self.page == "Set" :
            self.set_selection_control(event)

        elif self.page == "About" :
            self.about_control(event)
        elif self.page == "Test" :
            if event: self.__init__()
        
        self.render()
        

    def render(self) :
        os.system("cls")
        if self.page == "Home" :
            print(BANNER)
            self.render_menu()
        elif self.page == "File" :
            print(BANNER)
            self.render_file()
        elif self.page == "Set" :
            print(BANNER)
            self.render_set()
        elif self.page == "Test" :
            self.start_test()
        elif self.page == "About" :
            print(BANNER)
            self.show_about()
    
    def render_menu(self) :
        console.print(f"[bold yellow] #MENU[/bold yellow]")
        console.print(f"[bold white]-----------------------------------------[/bold white]")
        for menu in self.menu_ls : console.print(f"[[bold cyan]{menu}[/bold cyan]] - {self.menu_describe_ls[self.menu_ls.index(menu)]}") if self.menu_ls.index(menu) == self.menu_idx else console.print(f" {menu}")
        console.print("[bold white]-----------------------------------------[/bold white]")
        console.print("ENTER (↵) // ARROW UP (↑) // ARROW DOWN (↓) // ESC (x)")

    def get_sample_program(self):
        current_folder = self.base_dir
        self.file_ls = [
            file for file in os.listdir(current_folder)
            if os.path.isfile(os.path.join(current_folder, file))  
            and file != os.path.basename(sys.executable)
            and file.endswith(".py")  
    ]
    def render_file(self) :
        console.print(f"[bold yellow] #SELECT FILE TO TEST[/bold yellow]")
        console.print(f"[bold white]-----------------------------------------[/bold white]")
        for file in self.file_ls: console.print(f"[[bold cyan]{file}[/bold cyan]]") if self.file_ls.index(file) == self.file_idx else console.print(f" {file}")
        console.print(f"[bold white]-----------------------------------------[/bold white]")
        console.print("ENTER (↵) // BACKSPACE (←) // ARROW UP (↑) // ARROW DOWN (↓) // ESC (x)")

    def get_test_set(self):
        try:
            with open(self.json_file, 'r', encoding="utf-8") as file:
                self.set_ls = json.load(file)
        except FileNotFoundError:
            print("Error: JSON file not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")

    def render_set(self) :
        console.print(f"[bold yellow] #SELECT TEST SET[/bold yellow]") if self.file_seleted else console.print(f"[bold yellow] #All Test[/bold yellow]")
        console.print(f"[bold white]-----------------------------------------[/bold white]")
        for test in self.set_ls: console.print(f"[[bold cyan]{test["setname"]}[/bold cyan]] - {test["describe"]}") if [entry["setname"] for entry in self.set_ls].index(test["setname"]) == self.set_idx else console.print(f" {test["setname"]}")
        console.print(f"[bold white]-----------------------------------------[/bold white]")
        console.print("ENTER (↵) // BACKSPACE (←) // ARROW UP (↑) // ARROW DOWN (↓) // ESC (x)")
    
    def execute_python(self, input_string):
        file_name = self.file_seleted
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Error: File '{file_name}' not found.")

        with open(file_name, 'r') as file:
            code = file.read()

        output_capture = StringIO()
        sys.stdout = output_capture

        input_iter = iter(input_string.splitlines()) 
        def mock_input(prompt=""):
            print(prompt, end="") 
            return next(input_iter) 

        original_input = __builtins__.input
        __builtins__.input = mock_input

        try:
            exec(code, {})
        except Exception as e:
            print(f"Error occurred during execution: {e}")
        finally:
            __builtins__.input = original_input
            sys.stdout = sys.__stdout__

            captured_output = output_capture.getvalue()
            output_capture.close()
            return captured_output
    
    def start_test(self):
        
        user_file = self.file_seleted
        number_of_testcase = len(self.set_seleted["testcase"])
        
        
        TEST_BANNER = rf"""
        ╔═══════════════════════════════════════════════════════════════════╗
        ║     ____                      _     _____         _               ║
        ║    / ___|___  _ __  ___  ___ | | __|_   _|__  ___| |_ ___ _ __    ║
        ║   | |   / _ \| '_ \/ __|/ _ \| |/ _ \| |/ _ \/ __| __/ _ \ '__|   ║
        ║   | |__| (_) | | | \__ \ (_) | |  __/| |  __/\__ \ ||  __/ |      ║
        ║    \____\___/|_| |_|___/\___/|_|\___||_|\___||___/\__\___|_|      ║
        ║                                                                   ║
        ║         Kimrama  | tawan123456789 | OkuSan | Archer-SN            ║
        ║                                                                   ║
        ╚═══════════════════════════════════════════════════════════════════╝
          
          Selected File:       {user_file}  
                               
          TestName:            {self.set_seleted["setname"]}     
          Description:         {self.set_seleted["describe"]}    
          Number of Testcases: {str(number_of_testcase)}
          
               
        """

        print(TEST_BANNER)    
        
        for i, testcase in enumerate(self.set_seleted["testcase"]):
            try:
                answer = self.execute_python(testcase["input"]).replace("\n", "")
            except UnicodeDecodeError:
                console.print(f"[bold red]Error[/bold red]: UnicodeDecodeError occurred during execution. Please remove non-ASCII characters if any.")
                print("Press any key to go to MENU")
                return
            except Exception as e:
                print(f"Error: {e}")
                
            if answer == testcase["expected_output"]:
                console.print(f"[bold yellow]TESTCASE {i + 1} of {number_of_testcase}[/bold yellow]\t\t[bold green] PASS[/bold green]")
                self.score = self.score + 1
            else : 
                console.print(f"[bold yellow]TESTCASE {i + 1} of {number_of_testcase}[/bold yellow]\t\t[bold red] FAIL[/bold red]")
            
            print("TESTCASE Input: ", testcase["input"])
            print("EXPECTED Output: ", testcase["expected_output"])
            print("Your answer: ", answer, end="")
            
            print()
            
            print("-------------------------------------------")
            time.sleep(0.3)

        console.print("[bold green]TEST FINISHED[/bold green]")
        print(f'Score: {self.score}/{number_of_testcase}')
        print("Press any key to go to MENU")

    @staticmethod
    def show_about() :
        console.print("[bold yellow] # Contributors[/bold yellow]")
        console.print(f"[bold white] {"Kimrama":<15} [/bold white]\t[bold cyan] EDITOR [/bold cyan]\thttps://github.com/Kimrama")
        console.print(f"[bold white] {"tawan123456789":<15} [/bold white]\t[bold cyan] EDITOR [/bold cyan]\thttps://github.com/tawan123456789")
        console.print(f"[bold white] {"OkuSan":<15} [/bold white]\t[bold cyan] EDITOR [/bold cyan]\thttps://github.com/paratpanu18")
        console.print(f"[bold white] {"KaKa":<15} [/bold white]\t[bold cyan] TESTER [/bold cyan]\thttps://github.com/Archer-SN")
        console.print("BACKSPACE (←) // ESC (x)")

    def run(self) :
        self.render()
        keyboard.on_press(self.handle_keyboard_event)

console = Console()
program = Program()

def run_normal():
    program.run()
    try :
        keyboard.wait("esc")
        exit()
    except KeyboardInterrupt:
        print("Ctrl + C detected. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

# User run the program directly without any .py file
# Proceed the program as normal 
if len(sys.argv) == 1:
    run_normal()

elif len(sys.argv) > 2:
    print("Error: Too many arguments.")
    exit(1)
    
else:
    user_file_path = sys.argv[1]
    if not os.path.isfile(user_file_path) or not user_file_path.endswith(".py"):
        print("Error: Provided path is not a valid .py file.")
        exit(1)

    user_file_name = os.path.basename(user_file_path)
    program.file_seleted = user_file_name
    user_file_name = user_file_name.replace(".py", "")  # Remove .py extension
    
    try:
        with open(program.json_file, 'r', encoding="utf-8") as file:
            program.set_ls = json.load(file)
            for test_set in program.set_ls:
                if test_set["setname"] == user_file_name:
                    program.set_seleted = test_set
                    program.start_test()
                    break
            else:
                print(f"Error: Test set '{user_file_name}' not found.")
                print("Please manually select the test set.")
                time.sleep(2)
                program.page = "Set"
                run_normal()
            
    except FileNotFoundError:
        print("Error: Testset file (test_set.json) not found.")

input("Press Enter to exit...")