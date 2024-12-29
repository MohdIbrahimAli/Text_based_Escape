from tkinter import *
import customtkinter as ct
from PIL import Image, ImageTk
import pygame
import random
import json
from tkinter import messagebox
import os
from time import sleep

# CustomTK and Pygame Initialization
ct.set_appearance_mode("Dark")  # Set to "Dark" or "Light"
ct.set_default_color_theme("blue")  # Choose a color theme
pygame.mixer.init()

# Constants
RESOURCE_PATH = "Resources/"
DEFAULT_IMAGE = "placeholder.jpg"
DEFAULT_MUSIC_VOLUME = 0.2
FADE_SPEED = 5  # Adjust fade-in/out speed

class HorrorGame(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Horror Game")
        self.geometry("1920x1080")

        # Game State
        self.current_scene = "main_menu"
        self.inventory = []
        self.health = 100
        self.paused = False

        # UI Elements
        self.canvas = ct.CTkCanvas(self, width=1920, height=1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.status_label = ct.CTkLabel(self, text="", font=("blood lust", 28), fg_color="gray")
        self.canvas.create_window(960, 20, window=self.status_label)

        # Start Game
        self.load_background_music(f"{RESOURCE_PATH}background_music.mp3")
        self.fade_in(lambda: self.show_scene("main_menu"))  # Fade-in on game start

    # --- Utility Methods ---

    def load_background_music(self, music_path):
        """Loads background music."""
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(DEFAULT_MUSIC_VOLUME)
            pygame.mixer.music.play(loops=-1)
        except FileNotFoundError:
            print(f"Error: Music file '{music_path}' not found.")

    def play_sound(self, sound_path):
        """Plays a sound effect."""
        try:
            pygame.mixer.Sound(sound_path).play()
        except FileNotFoundError:
            print(f"Error: Sound file '{sound_path}' not found.")

    def load_image(self, path):
        """Loads and displays an image."""
        try:
            img = Image.open(path).resize((1920, 1080))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(960, 540, image=self.photo, anchor="center")
        except FileNotFoundError:
            print(f"Error: Image file '{path}' not found.")
            self.load_image(f"{RESOURCE_PATH}{DEFAULT_IMAGE}")

    def create_label(self, text, font=("blood lust", 55), y=350, fg_color="transparent"):
        """Creates and places a label."""
        label = ct.CTkLabel(self, text=text, font=font, fg_color=fg_color)
        self.canvas.create_window(960, y, window=label)
        return label

    def create_button(self, text, command, font=("blood lust", 50), y=700, x=960, bg_color="#808080", hover_color="#040720"):
        """Creates and places a button with custom colors."""
        button = ct.CTkButton(self, text=text, command=command, font=font, bg_color=bg_color, hover_color=hover_color)
        self.canvas.create_window(x, y, window=button)
        return button

    def clear_scene(self):
        """Clears the current scene."""
        self.canvas.delete("all")

    def fade_in(self, callback):
        """Creates a fade-in effect."""
        for i in range(0, 255, FADE_SPEED):
            self.canvas.configure(bg=f"#{i:02x}{i:02x}{i:02x}")
            self.update()
            sleep(0.01)
        callback()

    def fade_out(self, callback):
        """Creates a fade-out effect."""
        for i in range(255, 0, -FADE_SPEED):
            self.canvas.configure(bg=f"#{i:02x}{i:02x}{i:02x}")
            self.update()
            sleep(0.01)
        callback()

    def update_status(self):
        """Updates the status label."""
        status_text = f"Health: {self.health} | Inventory: {', '.join(self.inventory)}"
        self.status_label = ct.CTkLabel(self, text=status_text, font=("Times New Roman", 20))
        self.canvas.create_window(960, 20, window=self.status_label)

    def toggle_pause(self):
        """Toggles the pause state of the game."""
        self.paused = not self.paused
        if self.paused:
            self.show_pause_menu()
        else:
            self.show_scene(self.current_scene)

    def show_pause_menu(self):
        """Displays the pause menu."""
        self.clear_scene()
        self.load_image("Resources/pause_screen.jpg")
        self.create_label("Game Paused", font=("blood lust", 60), y=350)
        self.create_button("Resume", self.resume_game, y=500)
        self.create_button("Save Game", self.save_game, y=600)
        self.create_button("Load Game", self.load_game, y=700)
        self.create_button("Quit", self.confirm_exit, y=800)

    def resume_game(self):
        """Resumes the game from where it left off."""
        self.paused = False
        self.show_scene(self.current_scene)

    def save_game(self):
        """Saves the game state to a file."""
        game_data = {
            "current_scene": self.current_scene,
            "inventory": self.inventory,
            "health": self.health
        }
        try:
            with open("save_game.json", "w") as file:
                json.dump(game_data, file)
            messagebox.showinfo("Save Game", "Game has been saved successfully!")
        except IOError:
            print("Error: Could not save the game.")

    def load_game(self):
        """Loads the game state from a file."""
        try:
            with open("save_game.json", "r") as file:
                data = json.load(file)
                self.current_scene = data["current_scene"]
                self.inventory = data["inventory"]
                self.health = data["health"]
            messagebox.showinfo("Load Game", "Game has been loaded successfully!")
            self.show_scene(self.current_scene)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Load Game", "No saved game file found!")

    def confirm_exit(self):
        """Confirms before quitting the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.quit()

    # --- Game Over/Victory Handlers ---

    def game_over(self, message):
        self.clear_scene()
        self.load_image("Resources/game_over.jpg")
        self.create_label(message, fg_color="red")
        self.play_sound("Resources/game_over_sound.mp3")
        self.create_button("Try Again", self.reset_game)

    def show_victory(self):
        self.clear_scene()
        self.load_image("Resources/victory.jpg")
        self.create_label("Congratulations! You have defeated the dark force and escaped the nightmare.\nYou are victorious!")
        self.create_button("Play Again", self.reset_game, bg_color="#2C3539")
        self.create_button("Exit Game", self.quit, y=800, bg_color="red", hover_color="darkred")
        self.play_sound("Resources/victory_sound.mp3")

    def reset_game(self):
        """Resets the game state and transitions smoothly back to the main menu."""
        self.inventory = []
        self.health = 100
        self.current_scene = "main_menu"
        self.fade_in(lambda: self.show_scene("main_menu"))

    def add_universal_buttons(self):
        """Add Pause, Save, and Load buttons to the current scene."""
        pause_button = ct.CTkButton(self, text="Pause", command=self.toggle_pause, font=("blood lust", 20))
        self.canvas.create_window(1800, 100, window=pause_button)

        save_button = ct.CTkButton(self, text="Save", command=self.save_game, font=("blood lust", 20))
        self.canvas.create_window(1800, 160, window=save_button)

        load_button = ct.CTkButton(self, text="Load", command=self.load_game, font=("blood lust", 20))
        self.canvas.create_window(1800, 220, window=load_button)

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
        self.load_image("Resources/1234.jpg")
        self.create_label("Welcome to the Horror Game", font=("blood lust", 70, "italic"), y=350)
        self.create_button("How to Play", lambda: self.show_scene("how_to_play"), y=700)
        self.create_button("Start Game", lambda: self.show_scene("graveyard"), y=800)
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
        self.create_button("Search for anything", self.search_graveyard, y=600)
        self.create_button("Leave graveyard", lambda: self.leave_location("graveyard"))
        self.current_scene = "graveyard"
        self.add_universal_buttons()

    def search_graveyard(self):
        self.clear_scene()
        self.load_image("Resources/graveyard.jpg")
        self.create_label("You find a rusted key and an old map.")
        self.create_button("Take them", self.take_graveyard_items)
        self.create_button("Leave", lambda: self.leave_location("graveyard"), y=800)
        self.add_universal_buttons()

    def take_graveyard_items(self):
        self.inventory.extend(["key", "map"])
        self.show_scene("haunted_house")

    def leave_location(self, location):
        self.clear_scene()
        images = {"graveyard": "Resources/graveyard.jpg"}
        self.load_image(images.get(location, "Resources/graveyard.jpg"))
        self.create_label(f"You try to leave {location}, but a ghost blocks your path.")
        self.create_button("Fight", self.fight_ghost)
        self.create_button("Run", self.run_from_ghost, y=800)
        self.add_universal_buttons()

    def fight_ghost(self):
        self.clear_scene()
        self.load_image("Resources/graveyard.jpg")
        self.create_label("You try to fight the ghost, but it's too powerful.")
        self.create_label("But you some how manage to escape.")
        if "key" in self.inventory:
            self.after(3000, lambda: self.show_scene("haunted_house"))
        else:
            self.game_over("The ghost overpowers you. Game Over.")

    def run_from_ghost(self):
        if random.choice([True, False]):
            self.show_scene("haunted_house")
        else:
            self.game_over("You failed to escape and were caught by the ghost.")

    def show_haunted_house(self):
        self.load_image("Resources/haunted.jpg")
        self.create_label("You arrive at a creepy house.")
        self.create_button("Enter House", self.enter_house)
        self.create_button("Leave House", lambda: self.leave_location("haunted_house"), y=800)
        self.current_scene = "haunted_house"
        self.add_universal_buttons()

    def enter_house(self):
        if "map" in self.inventory:
            self.show_scene("abandoned_mine")
        else:
            self.game_over("Without a map, you get lost and trapped inside the house.")

    def show_abandoned_mine(self):
        self.load_image("Resources/mine.jpg")
        self.create_label("You enter an abandoned mine. The air is thick with dust.")
        self.create_button("Search for Items", self.search_mine)
        self.create_button("Leave Mine", self.leave_mine, y=800)
        self.current_scene = "abandoned_mine"
        self.add_universal_buttons()

    def search_mine(self):
        self.clear_scene()
        self.load_image("Resources/mine.jpg")
        self.create_label("You find a pickaxe and a lantern.")
        self.create_button("Take Items", self.take_mine_items)
        self.create_button("Leave Mine", self.leave_mine, y=800)
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
        self.create_label("You enter a spooky forest. The trees are whispering some secrets.")
        self.create_button("Explore the Forest", self.explore_forest)
        self.create_button("Leave Forest", self.leave_forest, y=800)
        self.current_scene = "forest"
        self.add_universal_buttons()

    def explore_forest(self):
        chance = random.choice(["item", "enemy", "nothing", "health"])
        if chance == "item":
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You find a magical amulet hidden in the forest.")
            self.create_button("Take Amulet", self.take_amulet)
            self.create_button("Leave", self.leave_forest, y=800)
            self.add_universal_buttons()

        elif chance == "health":
            self.health = min(self.health + 20, 100)  # Cap at 100
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You found a health potion! Your health is restored by 20.")
            self.create_button("Continue", self.leave_forest)
            self.add_universal_buttons()

        elif chance == "enemy":
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("A wild beast appears!")
            self.create_button("Fight", self.fight_beast)
            self.create_button("Run", self.run_from_beast, y=800)
            self.add_universal_buttons()

        else:
            self.clear_scene()
            self.load_image("Resources/forest.jpg")
            self.create_label("You wander deeper into the forest but find nothing.")
            self.create_button("Leave Forest", self.leave_forest)
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
                self.play_sound("Resources/game_over_sound.mp3")
                self.create_button("Try Again", self.reset_game)
                self.add_universal_buttons()
            else:
                self.clear_scene()
                self.load_image("Resources/forest.jpg")
                self.create_label(f"You fought the beast but lost some health. Your health: {self.health}")
                self.create_button("Continue", self.show_scene("forest"))
                self.add_universal_buttons()

    def run_from_beast(self):
        self.clear_scene()
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
                self.create_button("Try Again", self.reset_game)
                self.add_universal_buttons()
            else:
                self.clear_scene()
                self.load_image("Resources/forest.jpg")
                self.create_label(f"The beast catches you. Your health: {self.health}")
                self.create_button("Continue", self.show_scene("forest"))
                self.add_universal_buttons()

    def leave_forest(self):
        self.clear_scene()
        self.load_image("Resources/forest.jpg")
        self.create_label("You decide to leave the forest and return to the path.")
        self.create_button("Continue", lambda: self.show_scene("old_mansion"))
        self.add_universal_buttons()

    def show_old_mansion(self):
        self.clear_scene()
        self.load_image("Resources/old_mansion.jpg")
        self.create_label("You arrive at an old, Haunted mansion.")
        self.create_button("Enter Mansion", self.enter_mansion)
        self.create_button("Leave Mansion", self.leave_mansion, y=800)
        self.current_scene = "old_mansion"
        self.add_universal_buttons()

    def enter_mansion(self):
        if "amulet" in self.inventory :
            self.clear_scene()
            self.load_image("Resources/old_mansion.jpg")
            self.create_label("The amulet reveals hidden passages inside the mansion.")
            self.create_button("Continue", lambda: self.show_scene("final_confrontation"))
            self.add_universal_buttons()
        else:
            self.clear_scene()
            self.load_image("Resources/old_mansion.jpg")
            self.create_label("Without the amulet, the mansion traps you inside.")
            self.create_button("play again", self.reset_game)
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
            "The final confrontation begins! \nYou stand before the dark force that has been haunting you.\n"
            "Do you choose to fight or use a special item?")
        self.create_button("Fight", self.fight_dark_force)
        self.create_button("Use Item", self.use_special_item, y=800)
        self.add_universal_buttons()
    
    def fight_dark_force(self):
        """Enhanced fight mechanics for the final confrontation."""
        self.clear_scene()
        self.load_image("Resources/final_battle.jpg")
        self.create_label("The dark force attacks! Prepare for battle.", font=("blood lust", 40), y=100)
        
        # Initial battle state
        player_health = self.health
        enemy_health = 150
        player_stamina = 50

        def player_turn():
            """Handles player's turn in the fight."""
            self.clear_scene()
            self.load_image("Resources/final_battle.jpg")
            self.create_label(f"Your Health: {player_health} | Stamina: {player_stamina}\nEnemy Health: {enemy_health}", font=("blood lust", 30), y=100)
            
            self.create_button("Attack", lambda: player_attack(), y=600)
            self.create_button("Defend", lambda: player_defend(), y=700)
            self.create_button("Use Item", lambda: player_use_item(), y=800)

        def enemy_turn():
            """Handles enemy's turn in the fight."""
            nonlocal player_health, enemy_health
            self.clear_scene()
            damage = random.randint(10, 30)
            player_health -= damage
            self.create_label(f"The dark force attacks! You take {damage} damage.\nYour Health: {player_health}", font=("blood lust", 30), y=100)
            
            if player_health <= 0:
                self.game_over("You were defeated by the dark force.")
            else:
                self.create_button("Next Turn", player_turn, y=800)

        def player_attack():
            """Player's attack move."""
            nonlocal enemy_health, player_stamina
            if player_stamina >= 10:
                damage = random.randint(15, 30)
                enemy_health -= damage
                player_stamina -= 10
                self.create_label(f"You attack the dark force, dealing {damage} damage!\nEnemy Health: {enemy_health}", font=("blood lust", 30), y=100)
            else:
                self.create_label("You are too tired to attack! Regain stamina by defending.", font=("blood lust", 30), y=100)
            
            if enemy_health <= 0:
                self.show_victory()
            else:
                self.create_button("Enemy's Turn", enemy_turn, y=800)

        def player_defend():
            """Player's defensive move."""
            nonlocal player_stamina
            stamina_gain = random.randint(10, 20)
            player_stamina += stamina_gain
            self.create_label(f"You defend and regain {stamina_gain} stamina!\nStamina: {player_stamina}", font=("blood lust", 30), y=100)
            self.create_button("Enemy's Turn", enemy_turn, y=800)

        def player_use_item():
            """Player uses an item from the inventory."""
            nonlocal player_health, enemy_health
            if "amulet" in self.inventory:
                effect = random.choice(["heal", "damage"])
                if effect == "heal":
                    heal_amount = random.randint(20, 40)
                    player_health += heal_amount
                    self.create_label(f"The amulet heals you for {heal_amount} health!\nYour Health: {player_health}", font=("blood lust", 30), y=100)
                else:
                    damage = random.randint(30, 50)
                    enemy_health -= damage
                    self.create_label(f"The amulet emits a blinding light, dealing {damage} damage to the enemy!\nEnemy Health: {enemy_health}", font=("blood lust", 30), y=100)
                self.inventory.remove("amulet")
            else:
                self.create_label("You have no items to use!", font=("blood lust", 30), y=100)
            
            if enemy_health <= 0:
                self.show_victory()
            else:
                self.create_button("Enemy's Turn", enemy_turn, y=800)

        player_turn()

    
    def use_special_item(self):
        if "lantern" in self.inventory:
            self.clear_scene()
            self.load_image("Resources/final_battle_lantern.png")
            self.create_label("The lantern reveals the true form of the dark force!\nYou defeat it with your newfound strength.")
            self.create_button("Continue", self.show_victory)
            self.add_universal_buttons()
        else:
            self.clear_scene()
            self.load_image("Resources/final_battle_failure.jpg")
            self.create_label("You have no special item to use! The dark force overpowers you.\nTry again!")
            self.play_sound("Resources/game_over_sound.mp3")
            self.create_button("Try Again", self.reset_game)
            self.add_universal_buttons()

# ---------- Main Execution ----------

if __name__ == "__main__":
    app = HorrorGame()
    app.protocol("WM_DELETE_WINDOW", app.confirm_exit)
    app.mainloop()