import tkinter as tk

# Game class
class TextGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("Text-Based Game")
        
        
        self.game_state = "start"
        
   
        self.label = tk.Label(root, text="Welcome to the adventure game!", width=100, height=10, wraplength=400, font=("Times new roman", 25))
        self.label.pack(padx=20, pady=20)
        
        self.entry = tk.Entry(root, width=40, font =("Times new roman", 18))
        self.entry.pack(padx=20, pady=10)
        
        self.button = tk.Button(root, text="Submit",font = ("Times new roman", 18), command=self.process_input)
        self.button.pack(padx=20, pady=10)
        
    def process_input(self):
        user_input = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        
        if self.game_state == "start":
            self.start_game(user_input)
        elif self.game_state == "forest":
            self.forest_choice(user_input)
        elif self.game_state == "cave":
            self.cave_choice(user_input)
        elif self.game_state == "end":
            self.end_game(user_input)

    def start_game(self, choice):
        if choice in ["start", "begin", "yes"]:
            self.game_state = "forest"
            self.label.config(text="You are in a dark forest. Do you want to go deeper or leave? (Type 'deeper' or 'leave')")
        else:
            self.game_state = "end"
            self.label.config(text="You decided not to start the adventure. Game over! (Type 'restart' to try again)")

    def forest_choice(self, choice):
        if choice == "deeper":
            self.game_state = "cave"
            self.label.config(text="You ventured deeper into the forest and found a cave. Do you want to enter the cave or leave? (Type 'enter' or 'leave')")
        elif choice == "leave":
            self.game_state = "end"
            self.label.config(text="You decided to leave the forest. Game over! (Type 'restart' to try again)")
        else:
            self.label.config(text="Invalid choice. Please type 'deeper' or 'leave'.")

    def cave_choice(self, choice):
        if choice == "enter":
            self.game_state = "end"
            self.label.config(text="You entered the cave and found treasure! Congratulations! (Type 'restart' to play again)")
        elif choice == "leave":
            self.game_state = "forest"
            self.label.config(text="You left the cave and returned to the forest. Do you want to go deeper or leave? (Type 'deeper' or 'leave')")
        else:
            self.label.config(text="Invalid choice. Please type 'enter' or 'leave'.")

    def end_game(self, choice):
        if choice == "restart":
            self.game_state = "start"
            self.label.config(text="Welcome to the adventure game! (Type 'start' to begin your journey)")
        else:
            self.label.config(text="Invalid input. Type 'restart' to play again.")


root = tk.Tk()
game =TextGame(root)

 
root.mainloop()