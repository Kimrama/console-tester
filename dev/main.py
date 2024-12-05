import os
import sys
import json
import time
from io import StringIO

from rich.console import Console
import keyboard


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
        self.menu_ls = ["TEST", "TEST SET", "ABOUT"]
        self.menu_describe_ls = ["let select file to test", "just see how many test set", "about this program"]
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
            self.render_menu()
        elif self.page == "File" :
            self.render_file()
        elif self.page == "Set" :
            self.render_set()
        elif self.page == "Test" :
            self.start_test()
        elif self.page == "About" :
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
        for testcase in self.set_seleted["testcase"]:
                answer = self.execute_python(testcase["input"]).replace("\n", "")
                print("testcase input:", testcase["input"])
                print("expect output:", testcase["expected_output"])
                print("your answer:", answer, end="")
                if answer == testcase["expected_output"]:
                    console.print("[bold green] PASS[/bold green]")
                    self.score = self.score + 1
                else : console.print("[bold red] FAIL[/bold red]")
                print("-------------------------------------------")
                time.sleep(0.3)

        print("total", self.score)
        print("press any key to go to MENU")

    @staticmethod
    def show_about() :
        console.print("[bold yellow] #About[/bold yellow]")
        console.print("[bold white] Kimrama [/bold white]", "[bold cyan] EDITER [/bold cyan]", "https://github.com/Kimrama")
        console.print("[bold white] tawan123456789 [/bold white]", "[bold cyan] EDITER [/bold cyan]", "https://github.com/tawan123456789")
        console.print("[bold white] Kaka [/bold white]", "[bold spring_green2] TESTER [/bold spring_green2]", "")
        console.print("BACKSPACE (←) // ESC (x)")

    def run(self) :

        self.render()
        keyboard.on_press(self.handle_keyboard_event)

console = Console()
program = Program()

program.run()

try :
    keyboard.wait("esc")
except :
    print("Program close")

