from tkinter import *
import customtkinter as ct
from PIL import Image, ImageTk
import pygame
import random
import json
from tkinter import messagebox

# CustomTK and Pygame Initialization
ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")
pygame.mixer.init()

class HorrorGame(ct.CTk):
    def __init__(self):
        super().__init__()
        # Game Configuration
        self.geometry("1920x1080")
        self.title("Horror Game")
        self.canvas = ct.CTkCanvas(self, width=1920, height=1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Game State
        self.current_scene = "main_menu"
        self.inventory = []
        self.health = 100
        self.paused = False

        # Start Game
        self.play_background_music("Resources/background_music.mp3")
        self.show_scene("main_menu")

    # ---------- Utility Methods ----------

    def play_background_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)

    def play_sound(self, sound_path):
        pygame.mixer.Sound(sound_path).play()

    def load_image(self, path):
        img = Image.open(path).resize((1920, 1080))
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(960, 540, image=self.photo, anchor="center")

    def safe_load_image(self, path):
        try:
            self.load_image(path)
        except FileNotFoundError:
            print(f"Error: Image file '{path}' not found.")
            self.load_image("Resources/placeholder.jpg")

    def create_label(self, text, font=("Times New Roman", 40), y=350):
        label = ct.CTkLabel(self, text=text, font=font)
        self.canvas.create_window(960, y, window=label)
        return label

    def create_button(self, text, command, font=("Times New Roman", 50), y=700, x = 960):
        button = ct.CTkButton(self, text=text, command=command, font=font)
        self.canvas.create_window(x, y, window=button)
        return button

    def clear_scene(self):
        self.canvas.delete("all")

    def fade_in(self):
        for i in range(0, 255, 5):
            self.canvas.configure(bg=f"#{i:02x}{i:02x}{i:02x}")
            self.update()
            self.after(10)

    def fade_out(self):
        for i in range(255, 0, -5):
            self.canvas.configure(bg=f"#{i:02x}{i:02x}{i:02x}")
            self.update()
            self.after(10)

    def update_status(self):
        status_text = f"Health: {self.health} | Inventory: {', '.join(self.inventory)}"
        self.status_label = ct.CTkLabel(self, text=status_text, font=("Times New Roman", 20))
        self.canvas.create_window(960, 20, window=self.status_label)

    def toggle_pause(self):
        self.paused = not self.paused
        
        if self.paused:
            self.clear_scene()
            self.create_label("Game Paused", font=("Times New Roman", 60), y=500)
            self.create_button("Resume", command=lambda: self.show_scene(self.current_scene))
        else:
            self.clear_scene()
            self.show_scene(self.current_scene)

    def save_game(self):
    # Save game logic here...
        with open("save_game.json", "w") as file:
            json.dump({"current_scene": self.current_scene, "inventory": self.inventory, "health": self.health}, file)
        messagebox.showinfo("Save Game", "Game has been saved successfully!")

    def load_game(self):
        try:
            with open("save_game.json", "r") as file:
                data = json.load(file)
                self.current_scene = data["current_scene"]
                self.inventory = data["inventory"]
                self.health = data["health"]
            messagebox.showinfo("Load Game", "Game has been loaded successfully!")
            self.show_scene(self.current_scene)
        except FileNotFoundError:
            messagebox.showerror("Load Game", "No saved game file found!")


    def confirm_exit(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.quit()


    # Game Over handler
    def game_over(self, message):
        self.clear_scene()
        self.safe_load_image("Resources/game_over.jpg")
        self.create_label(message)
        self.play_sound("Resources/game_over_sound.mp3")
        self.create_button("Try Again", lambda: self.reset_game())

    # Victory handler
    def show_victory(self):
        self.clear_scene()
        self.safe_load_image("Resources/victory.jpg")
        self.create_label("Congratulations! You have defeated the dark force and escaped the nightmare.\nYou are victorious!")
        self.create_button("Play Again", lambda: self.reset_game())
        self.create_button("Exit Game", lambda: self.quit(), y=800)
        self.play_sound("Resources/victory_sound.mp3")

    def reset_game(self):
        self.inventory = []  # Reset inventory
        self.health = 100    # Reset health to full
        self.show_scene("main_menu")

    def add_universal_buttons(self):
        """Adds Pause, Save, and Load buttons to the current scene."""
        pause_button = ct.CTkButton(self, text="Pause", command=self.toggle_pause, font=("Times New Roman", 20))
        self.canvas.create_window(1800, 100, window=pause_button)  # Position top-right
        
        save_button = ct.CTkButton(self, text="Save", command=self.save_game, font=("Times New Roman", 20))
        self.canvas.create_window(1800, 160, window=save_button)  # Below pause button
        
        load_button = ct.CTkButton(self, text="Load", command=self.load_game, font=("Times New Roman", 20))
        self.canvas.create_window(1800, 220, window=load_button)  # Below save button


    # ---------- Scene Management ----------

    def show_scene(self, scene):
        self.clear_scene()
        SCENES = {
            "main_menu": self.show_main_menu,
            "how_to_play": self.show_how_to_play,
            "graveyard": self.show_graveyard,
            "haunted_house": self.show_haunted_house,
            "abandoned_mine": self.show_abandoned_mine,
            "forest": self.show_forest,
            "old_mansion": self.show_old_mansion,
            "final_confrontation": self.show_final_confrontation,
        }
        SCENES.get(scene, self.show_main_menu)()
        self.update_status()

    # ---------- Scenes ----------

    def show_main_menu(self):
        self.safe_load_image("Resources/1234.jpg")
        self.create_label("Welcome to the Horror Game", font=("Times New Roman", 60, "italic"), y=350)
        self.create_button("How to Play", lambda: self.show_scene("how_to_play"), y=700)
        self.create_button("Start Game", lambda: self.show_scene("graveyard"), y=900)
        self.add_universal_buttons()

    def show_how_to_play(self):
        self.load_image("Resources/1234.jpg")
        instructions = (
            "1. Progress into the game by choosing options.\n"
            "2. Select the action you want to take.\n"
            "3. Complete tasks and escape!"
        )
        self.create_label(instructions)
        self.create_button("Back", lambda: self.show_scene("main_menu"), y=900)

    def show_graveyard(self):
        self.load_image("Resources/graveyard.jpg")
        self.create_label("You are stranded in an abandoned graveyard.")
        self.create_button("Search", self.search_graveyard, y = 600)
        self.create_button("Leave", lambda: self.leave_location("graveyard"))
        self.add_universal_buttons()

    def search_graveyard(self):
        self.clear_scene()
        self.load_image("Resources/graveyard.jpg")
        self.create_label("You find a rusted key and an old map.")
        self.create_button("Take Items", self.take_graveyard_items)
        self.create_button("Leave", lambda: self.leave_location("graveyard"), y = 800)
        self.add_universal_buttons()

    def take_graveyard_items(self):
        self.inventory.extend(["key", "map"])
        self.show_scene("haunted_house")
        self.add_universal_buttons()

    def leave_location(self, location):
        self.clear_scene()
        images = {"graveyard": "Resources/graveyard.jpg"}
        self.load_image(images.get(location, "Resources/graveyard.jpg"))
        self.create_label(f"You try to leave {location}, but a ghost blocks your path.")
        self.create_button("Fight", self.fight_ghost)
        self.create_button("Run", self.run_from_ghost,y=800)
        self.add_universal_buttons()

    def fight_ghost(self):
        self.add_universal_buttons()
        if "key" in self.inventory:
            self.show_scene("haunted_house")
        else:
            self.game_over("The ghost overpowers you. Game Over.")

    def run_from_ghost(self):
        self.add_universal_buttons()
        if random.choice([True, False]):
            self.show_scene("haunted_house")
        else:
            self.game_over("You failed to escape and were caught by the ghost.")

    # ---------- Haunted House ----------

    def show_haunted_house(self):
        self.load_image("Resources/haunted.jpg")
        self.create_label("You arrive at a creepy house.")
        self.create_button("Enter House", self.enter_house)
        self.create_button("Leave House", lambda: self.leave_location("haunted_house"),y=800)
        self.add_universal_buttons()

    def enter_house(self):
        if "map" in self.inventory:
            self.show_scene("abandoned_mine")
        else:
            self.game_over("Without a map, you get lost and trapped inside the house.")

    def show_abandoned_mine(self):
        self.load_image("Resources/mine.jpg")
        self.create_label("You enter an abandoned mine. The air is thick with dust.")
        self.create_button("Search for Items", lambda: self.search_mine())
        self.create_button("Leave Mine", lambda: self.leave_mine(),y=800)
        self.add_universal_buttons()

    def search_mine(self):
        self.clear_scene()
        self.load_image("Resources/mine.jpg")
        self.create_label("You find a pickaxe and a lantern.")
        self.create_button("Take Items", lambda: self.take_mine_items())
        self.create_button("Leave Mine", lambda: self.leave_mine(),y=800)
        self.add_universal_buttons()

    def take_mine_items(self):
        self.clear_scene()
        self.inventory.extend(["pickaxe", "lantern"])
        self.load_image("Resources/mine.jpg")
        self.create_label("You took the pickaxe and lantern. The adventure continues...")
        self.create_button("Continue", lambda: self.show_scene("forest"))
        self.add_universal_buttons()

    def leave_mine(self):
        self.clear_scene()
        self.load_image("Resources/mine.jpg")
        self.create_label("You decide to leave the mine. As you step outside, the wind picks up and the clouds darken.")
        self.create_button("Continue", lambda: self.show_scene("forest"))
        self.play_sound("Resources/wind_sound.mp3")
        self.add_universal_buttons()

    def show_forest(self):
        self.load_image("Resources/forest.jpg")
        self.create_label("You enter a spooky forest. The trees whisper secrets.")
        self.create_button("Explore the Forest", lambda: self.explore_forest())
        self.create_button("Leave Forest", lambda: self.leave_forest(),y=800)
        self.add_universal_buttons()

    def explore_forest(self):
        chance = random.choice(["item", "enemy", "nothing","health"])
        if chance == "item":
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You find a magical amulet hidden in the forest.")
            self.create_button("Take Amulet", lambda: self.take_amulet())
            self.create_button("Leave", lambda: self.leave_forest(),y=800)
            self.add_universal_buttons()

        elif chance == "health":
            self.health = min(self.health + 20, 100)  # Cap at 100
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You found a health potion! Your health is restored by 20.")
            self.create_button("Continue", lambda: self.leave_forest())
            self.add_universal_buttons()

        elif chance == "enemy":
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("A wild beast appears!")
            self.create_button("Fight", lambda: self.fight_beast())
            self.create_button("Run", lambda: self.run_from_beast(),y=800)
            self.add_universal_buttons()

        else:
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You wander deeper into the forest but find nothing.")
            self.create_button("Leave Forest", lambda: self.leave_forest())
            self.add_universal_buttons()

    def take_amulet(self):
        self.inventory.append("amulet")
        self.clear_scene()
        self.load_image("Resources/forest.jpg")
        self.create_label("You now have the magical amulet. It may come in handy later.")
        self.create_button("Continue", lambda: self.show_scene("old_mansion"))
        self.add_universal_buttons()

    def fight_beast(self):
        self.play_sound("Resources/fight_sound.mp3")
        if "amulet" in self.inventory:
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("The amulet gives you strength, and you defeat the beast.")
            self.create_button("Continue", lambda: self.show_scene("old_mansion"))
            self.add_universal_buttons()

        else:
            self.health -= 30
            if self.health <= 0:
                self.clear_scene()
                self.load_image("Resources/game_over.jpg")
                self.create_label("The beast overpowers you. Game over.")
                self.play_sound("Text_based_Escape/Resources/game_over_sound.mp3")
                self.create_button("Continue", lambda: self.show_scene("old_mansion"))
                self.add_universal_buttons()

            else:
                self.clear_scene()
                self.load_image("Resources/forest.jpg")
                self.create_label(f"You fought the beast but lost some health. Your health: {self.health}")
                self.create_button("Continue", lambda: self.show_scene("forest"))
                self.add_universal_buttons()

    def run_from_beast(self):
        self.play_sound("Resources/escape_sound.mp3")
        chance = random.randint(1, 3)
        if chance == 1:
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You manage to escape the beast.")
            self.create_button("Continue", lambda: self.show_scene("old_mansion"))
            self.add_universal_buttons()
        else:
            self.health -= 20  # Deduct health if caught
            if self.health <= 0:
                self.clear_scene()
                self.load_image("Resources/game_over.jpg")
                self.create_label("The beast catches you and you lose all your health.")
                self.play_sound("Resources/game_over_sound.mp3")
                self.create_button("Try Again", lambda: self.reset_game())
            else:
                self.clear_scene()
                self.load_image("Resources/forest.jpg")
                self.create_label(f"The beast catches you. Your health: {self.health}")
                self.create_button("Continue", lambda: self.show_scene("forest"))
                self.add_universal_buttons()


    def leave_forest(self):
        self.clear_scene()
        self.load_image("Resources/forest.jpg")
        self.create_label("You decide to leave the forest and return to the path.")
        self.create_button("Continue", lambda: self.show_scene("old_mansion"))
        self.add_universal_buttons()

    def show_old_mansion(self):
        self.load_image("Resources/old_mansion.jpg")
        self.create_label("You arrive at an old, creepy mansion.")
        self.create_button("Enter Mansion", lambda: self.enter_mansion())
        self.create_button("Leave Mansion", lambda: self.leave_mansion(),y=800)
        self.add_universal_buttons()

    def enter_mansion(self):
        if "amulet" in self.inventory:
            self.clear_scene()
            self.load_image("Resources/old_mansion.jpg")
            self.create_label("The amulet reveals hidden passages inside the mansion.")
            self.create_button("Continue", lambda: self.show_scene("final_confrontation"))
            self.add_universal_buttons()
        else:
            self.clear_scene()
            self.load_image("Resources/old_mansion.jpg")
            self.create_label("Without the amulet, the mansion traps you inside.")
            self.create_button("Try Again", lambda: self.reset_game())
            self.add_universal_buttons()

    def leave_mansion(self):
        self.clear_scene()
        self.load_image("Resources/old_mansion.jpg")
        self.create_label("You leave the mansion, but the door slams shut behind you!")
        self.create_button("Continue", lambda: self.show_scene("final_confrontation"))
        self.add_universal_buttons()

    def show_final_confrontation(self):
        self.load_image("Resources/final_battle.jpg")
        self.create_label(
            "The final confrontation begins! You stand before the dark force that has been haunting you.\n"
            "Do you choose to fight or use a special item?")
        self.create_button("Fight", lambda: self.fight_dark_force())
        self.create_button("Use Item", lambda: self.use_special_item(),y=800)
        self.add_universal_buttons()
    
    def fight_dark_force(self):
        if "pickaxe" in self.inventory and "lantern" in self.inventory:  
            self.clear_scene()
            self.load_image("Resources/final_battle_success.jpg")
            self.create_label("You use the pickaxe and lantern to defeat the dark force!\nVictory is yours!")
            self.create_button("Celebrate Victory", lambda: self.show_victory())
            self.add_universal_buttons()
        else:
            self.clear_scene()
            self.load_image("Resources/final_battle_failure.jpg")
            self.create_label("You failed to defeat the dark force.\nTry again!")
            self.play_sound("Resources/game_over_sound.mp3")
            self.create_button("Try Again", lambda: self.show_scene("main_menu"))
            self.add_universal_buttons()
    
    

    def use_special_item(self):
        if "lantern" in self.inventory:
            self.clear_scene()
            self.load_image("Resources/final_battle_lantern.png")
            self.create_label("The lantern reveals the true form of the dark force!\nYou defeat it with your newfound strength.")
            self.create_button("Continue", lambda: self.show_victory())
        else:
            self.clear_scene()
            self.load_image("Resources/final_battle_no_item.jpg")
            self.create_label("Without the right item, you are overpowered by the dark force.")
            self.play_sound("Resources/game_over_sound.mp3")
            self.create_button("Try Again", lambda: self.reset_game())
            

# ---------- Main Execution ----------

if __name__ == "__main__":
    app = HorrorGame()
    app.protocol("WM_DELETE_WINDOW", app.confirm_exit)
    app.mainloop()
