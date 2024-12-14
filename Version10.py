from tkinter import *
import customtkinter as ct
from PIL import Image, ImageTk
import pygame
import random

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")

# Initialize Pygame mixer for sound effects
pygame.mixer.init()

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Horror Game")
        self.canvas = ct.CTkCanvas(self, width=1920, height=1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.current_scene = "main_menu"
        self.inventory = []
        self.health = 100
        self.show_scene(self.current_scene)

    # Play background music continuously
        self.play_background_music("Q:\\Ibrahim\\Programs\\background_music.mp3")  # Replace with your background music file path

    def play_background_music(self, music_path):
        pygame.mixer.music.load(music_path)  # Load the music
        pygame.mixer.music.set_volume(0.2)  # Set the volume (0.0 to 1.0)
        pygame.mixer.music.play(loops=-1, start=0.0)  # Play the music indefinitely (loops=-1)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((1920, 1080))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(960, 540, image=self.photo, anchor="center")

    def create_canvas_label(self, text, font, y):
        label = ct.CTkLabel(self, text=text, font=font)
        self.canvas.create_window(960, y, window=label)
        return label

    def create_canvas_button(self, text, command, font, y):
        button = ct.CTkButton(self, text=text, command=command, font=font)
        self.canvas.create_window(960, y, window=button)
        return button

    def show_scene(self, scene):
        self.clear_scene()
        if scene == "main_menu":
            self.show_main_menu()
        elif scene == "how_to_play":
            self.show_how_to_play()
        elif scene == "graveyard":
            self.show_graveyard()
        elif scene == "haunted_house":
            self.show_haunted_house()
        elif scene == "abandoned_mine":
            self.show_abandoned_mine()
        elif scene == "final_confrontation":
            self.show_final_confrontation()
        elif scene == "victory":
            self.show_victory()
        elif scene == "game_over":
            self.show_game_over()
        elif scene == "forest":
            self.show_forest()
        elif scene == "old_mansion":
            self.show_old_mansion()

    def clear_scene(self):
        for widget in self.canvas.find_all():
            self.canvas.delete(widget)

    def show_main_menu(self):
        self.load_image("Q:\\Ibrahim\\Programs\\1234.jpg")
        self.create_canvas_label("Welcome to the Horror Game", ("Times new roman", 60, "italic"), 350)
        self.create_canvas_button("How to Play", lambda: self.show_scene("how_to_play"), ("Times new roman", 50), 700)
        self.create_canvas_button("Start Game", lambda: self.show_scene("graveyard"), ("Times new roman", 50), 900)

    def show_how_to_play(self):
        self.load_image("Q:\\Ibrahim\\Programs\\1234.jpg")
        self.create_canvas_label(
            "1. Progress into the game by choosing options.\n"
            "2. Select the action you want to take.\n"
            "3. Complete tasks and escape!",
            ("Times new roman", 40), 350
        )
        self.create_canvas_button("Back", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)

    def show_graveyard(self):
        self.load_image("Q:\\Ibrahim\\Programs\\graveyard.jpg")
        self.create_canvas_label("You are stranded in an abandoned graveyard.\nWhat would you like to do?", ("Times new roman", 40), 350)
        self.create_canvas_button("Search", lambda: self.search_graveyard(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave", lambda: self.leave_graveyard(), ("Times new roman", 50), 900) 

    def search_graveyard(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\graveyard.jpg")
        self.create_canvas_label("You find a rusted key and an old map.\nDo you take them?", ("Times new roman", 40), 350)
        self.create_canvas_button("Take Items", lambda: self.take_items_graveyard(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave Empty-Handed", lambda: self.leave_graveyard(), ("Times new roman", 50), 900)

    def take_items_graveyard(self):
        self.inventory.extend(["key", "map"])
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\graveyard.jpg")
        self.create_canvas_label("You took the key and map.\nThe adventure continues...", ("Times new roman", 40), 350)
        self.create_canvas_button("Continue", lambda: self.show_scene("haunted_house"), ("Times new roman", 50), 900)

    def leave_graveyard(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\graveyard.jpg")
        self.create_canvas_label("You try to leave, but a ghostly figure appears and blocks your path.", ("Times new roman", 40), 350)
        self.create_canvas_button("Fight", lambda: self.fight_ghost(), ("Times new roman", 50), 700)
        self.create_canvas_button("Run", lambda: self.run_from_ghost(), ("Times new roman", 50), 900)

    def fight_ghost(self):
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\fight_sound.mp3").play()  # Play fight sound
        if "key" in self.inventory:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\graveyard.jpg")
            self.create_canvas_label("You use the key to unlock a hidden passage and escape the ghost.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("haunted_house"), ("Times new roman", 50), 900)
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\game_over.jpg")
            self.create_canvas_label("You are defeated by the ghost.", ("Times new roman", 40), 350)
            pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.mp3").play()  # Play game over sound
            self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)

    def run_from_ghost(self):
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\escape_sound.mp3").play()  # Play escape sound
        chance_to_escape = random.randint(1, 3)
        if chance_to_escape == 1:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\graveyard.jpg")
            self.create_canvas_label("You manage to escape the ghost.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("haunted_house"), ("Times new roman", 50), 900)
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\game_over.jpg")
            self.create_canvas_label("You are caught by the ghost.", ("Times new roman", 40), 350)
            pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.mp3").play()  # Play game over sound
            self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)

    def show_haunted_house(self):
        self.load_image("Q:\\Ibrahim\\Programs\\haunted.jpg")
        self.create_canvas_label("You arrive at a creepy old house. Do you enter or leave?", ("Times new roman", 40), 350)
        self.create_canvas_button("Enter House", lambda: self.enter_house(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave House", lambda: self.leave_house(), ("Times new roman", 50), 900)

    def enter_house(self):
        if "map" in self.inventory:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\haunted.jpg")
            self.create_canvas_label("The map guides you through the house. You find a hidden staircase.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("abandoned_mine"), ("Times new roman", 50), 900)
            pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\house_enter_sound.mp3").play()  # House entering sound
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\haunted.jpg")
            self.create_canvas_label("Without the map, you get lost in the house and find yourself trapped.", ("Times new roman", 40), 350)
            self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)

    def leave_house(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\haunted.jpg")
        self.create_canvas_label(
            "You decide to leave the haunted house, but the door slams shut behind you.\n"
            "A ghostly figure appears in front of you, blocking your escape.",("Times new roman", 40), 350
        )
        self.create_canvas_button("Fight Ghost", lambda: self.fight_ghost(), ("Times new roman", 50), 700)
        self.create_canvas_button("Run Away", lambda: self.run_from_ghost(), ("Times new roman", 50), 900)


    def show_abandoned_mine(self):
        self.load_image("Q:\\Ibrahim\\Programs\\mine.jpg")
        self.create_canvas_label("You enter an abandoned mine. The air is thick with dust. What will you do?", ("Times new roman", 40), 350)
        self.create_canvas_button("Search for Items", lambda: self.search_mine(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave Mine", lambda: self.leave_mine(), ("Times new roman", 50), 900)

    def search_mine(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\mine.jpg")
        self.create_canvas_label("You find a pickaxe and a lantern. Do you take them?", ("Times new roman", 40), 350)
        self.create_canvas_button("Take Items", lambda: self.take_mine_items(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave Mine", lambda: self.leave_mine(), ("Times new roman", 50), 900)

    def take_mine_items(self):
        self.inventory.extend(["pickaxe", "lantern"])
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\mine.jpg")
        self.create_canvas_label("You took the pickaxe and lantern. The adventure continues...", ("Times new roman", 40), 350)
        self.create_canvas_button("Continue", lambda: self.show_scene("forest"), ("Times new roman", 50), 900)

    def leave_mine(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\mine.jpg")
        self.create_canvas_label("You decide to leave the mine. As you step outside, the wind picks up and the clouds darken.", ("Times new roman", 40), 350)
        self.create_canvas_button("Continue", lambda: self.show_scene("forest"), ("Times new roman", 50), 700)
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\wind_sound.mp3").play()


    def show_forest(self):
        self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
        self.create_canvas_label("You enter a spooky forest. The trees whisper secrets.\nWhat will you do?", ("Times new roman", 40), 350)
        self.create_canvas_button("Explore the Forest", lambda: self.explore_forest(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave Forest", lambda: self.leave_forest(), ("Times new roman", 50), 900)

    def explore_forest(self):
        chance = random.choice(["item", "enemy", "nothing"])
        if chance == "item":
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
            self.create_canvas_label("You find a magical amulet hidden in the forest.", ("Times new roman", 40), 350)
            self.create_canvas_button("Take Amulet", lambda: self.take_amulet(), ("Times new roman", 50), 700)
            self.create_canvas_button("Leave", lambda: self.leave_forest(), ("Times new roman", 50), 900)
        elif chance == "enemy":
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
            self.create_canvas_label("A wild beast appears! Do you fight or run?", ("Times new roman", 40), 350)
            self.create_canvas_button("Fight", lambda: self.fight_beast(), ("Times new roman", 50), 700)
            self.create_canvas_button("Run", lambda: self.run_from_beast(), ("Times new roman", 50), 900)
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
            self.create_canvas_label("You wander deeper into the forest but find nothing.", ("Times new roman", 40), 350)
            self.create_canvas_button("Leave Forest", lambda: self.leave_forest(), ("Times new roman", 50), 700)

    def take_amulet(self):
        self.inventory.append("amulet")
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
        self.create_canvas_label("You now have the magical amulet. It may come in handy later.", ("Times new roman", 40), 350)
        self.create_canvas_button("Continue", lambda: self.show_scene("old_mansion"), ("Times new roman", 50), 900)

    def fight_beast(self):
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\fight_sound.mp3").play()  # Play fight sound
        if "amulet" in self.inventory:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
            self.create_canvas_label("The amulet gives you strength, and you defeat the beast.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("old_mansion"), ("Times new roman", 50), 900)
        else:
            self.health -= 30  # Deduct health if player fights without amulet
            if self.health <= 0:
                self.clear_scene()
                self.load_image("Q:\\Ibrahim\\Programs\\game_over.jpg")
                self.create_canvas_label("The beast overpowers you. Game over.", ("Times new roman", 40), 350)
                pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.wav").play()  # Play game over sound
                self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)
            else:
                self.clear_scene()
                self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
                self.create_canvas_label(f"You fought the beast but lost some health. Your health: {self.health}", ("Times new roman", 40), 350)
                self.create_canvas_button("Continue", lambda: self.show_scene("forest"), ("Times new roman", 50), 900)


    def run_from_beast(self):
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\escape_sound.mp3").play()  # Escape sound
        chance_to_escape = random.randint(1, 3)
        if chance_to_escape == 1:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
            self.create_canvas_label("You manage to escape the beast.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("old_mansion"), ("Times new roman", 50), 900)
        else:
            self.health -= 20  # Deduct health if caught
            if self.health <= 0:
                self.clear_scene()
                self.load_image("Q:\\Ibrahim\\Programs\\game_over.jpg")
                self.create_canvas_label("The beast catches you and you lose all your health.", ("Times new roman", 40), 350)
                pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.mp3").play()  # Play game over sound
                self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)
            else:
                self.clear_scene()
                self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
                self.create_canvas_label(f"The beast catches you. Your health: {self.health}", ("Times new roman", 40), 350)
                self.create_canvas_button("Continue", lambda: self.show_scene("forest"), ("Times new roman", 50), 900)


    def leave_forest(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\forest.jpg")
        self.create_canvas_label("You decide to leave the forest and return to the path.", ("Times new roman", 40), 350)
        self.create_canvas_button("Continue", lambda: self.show_scene("old_mansion"), ("Times new roman", 50), 900)

    def show_old_mansion(self):
        self.load_image("Q:\\Ibrahim\\Programs\\old_mansion.jpg")
        self.create_canvas_label("You arrive at an old, creepy mansion. Do you enter or leave?", ("Times new roman", 40), 350)
        self.create_canvas_button("Enter Mansion", lambda: self.enter_mansion(), ("Times new roman", 50), 700)
        self.create_canvas_button("Leave Mansion", lambda: self.leave_mansion(), ("Times new roman", 50), 900)

    def enter_mansion(self):
        if "amulet" in self.inventory:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\old_mansion.jpg")
            self.create_canvas_label("The amulet reveals hidden passages inside the mansion.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("final_confrontation"), ("Times new roman", 50), 900)
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\old_mansion.jpg")
            self.create_canvas_label("Without the amulet, the mansion traps you inside.", ("Times new roman", 40), 350)
            self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)

    def leave_mansion(self):
        self.clear_scene()
        self.load_image("Q:\\Ibrahim\\Programs\\old_mansion.jpg")
        self.create_canvas_label("You leave the mansion, but the door slams shut behind you!", ("Times new roman", 40), 350)
        self.create_canvas_button("Continue", lambda: self.show_scene("final_confrontation"), ("Times new roman", 50), 900)

    def show_final_confrontation(self):
        self.load_image("Q:\\Ibrahim\\Programs\\final_battle.jpg")
        self.create_canvas_label(
            "The final confrontation begins! You stand before the dark force that has been haunting you.\n"
            "Do you choose to fight or use a special item?",
            ("Times new roman", 40), 350
        )

        self.create_canvas_button("Fight", lambda: self.fight_dark_force(), ("Times new roman", 50), 700)
        self.create_canvas_button("Use Item", lambda: self.use_special_item(), ("Times new roman", 50), 900)

    def fight_dark_force(self):
        if "pickaxe" in self.inventory and "lantern" in self.inventory:  # Check if the player has special items
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\final_battle_success.jpg")
            self.create_canvas_label("You use the pickaxe and lantern to defeat the dark force!\nVictory is yours!", ("Times new roman", 40), 350)
            self.create_canvas_button("Celebrate Victory", lambda: self.show_scene("victory"), ("Times new roman", 50), 900)
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\final_battle_failure.jpg")
            self.create_canvas_label("You failed to defeat the dark force.\nTry again!", ("Times new roman", 40), 350)
            pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.mp3").play()  # Play failure sound
            self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)

    def use_special_item(self):
        if "lantern" in self.inventory:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\final_battle_lantern.png")
            self.create_canvas_label("The lantern reveals the true form of the dark force!\nYou defeat it with your newfound strength.", ("Times new roman", 40), 350)
            self.create_canvas_button("Continue", lambda: self.show_scene("victory"), ("Times new roman", 50), 900)
        else:
            self.clear_scene()
            self.load_image("Q:\\Ibrahim\\Programs\\final_battle_no_item.jpg")
            self.create_canvas_label("Without the right item, you are overpowered by the dark force.", ("Times new roman", 40), 350)
            pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.mp3").play()  # Play failure sound
            self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 900)


    def show_victory(self):
        self.load_image("Q:\\Ibrahim\\Programs\\victory.jpg")
        self.create_canvas_label("Congratulations! You have defeated the dark force and escaped the nightmare.\nYou are victorious!",("Times new roman", 60, "italic"), 350)
        self.create_canvas_button("Play Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 700)
        self.create_canvas_button("Exit Game", lambda: self.quit(), ("Times new roman", 50), 900)
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\victory_sound.mp3").play()  # Play victory sound


    def show_game_over(self):
        self.load_image("Q:\\Ibrahim\\Programs\\game_over.jpg")
        self.create_canvas_label("Game Over! You have failed in your mission.\nTry again to conquer the darkness!", ("Times new roman", 60, "italic"), 350)
        self.create_canvas_button("Try Again", lambda: self.show_scene("main_menu"), ("Times new roman", 50), 700)
        self.create_canvas_button("Exit Game", lambda: self.quit(), ("Times new roman", 50), 900)
        pygame.mixer.Sound("Q:\\Ibrahim\\Programs\\game_over_sound.mp3").play()  # Play game over sound




if __name__ == "__main__":
    app = App()
    app.mainloop()