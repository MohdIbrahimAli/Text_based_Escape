from tkinter import *
import customtkinter as ct
from PIL import Image, ImageTk
import pygame

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Horror Game")

        # Create a canvas
        self.canvas = ct.CTkCanvas(self, width=1920, height=1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Initialize main menu
        self.show_main_menu()

    def load_image(self, image_path):
        """Helper function to load and set an image on the canvas."""
        image = Image.open(image_path)
        image = image.resize((1920, 1080))  # Resize the image as needed
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(960, 540, image=self.photo, anchor="center")  # Center the image

    def create_canvas_label(self, text, font, y):
        """Helper to create and place a label on the canvas."""
        label = ct.CTkLabel(self, text=text, font=font)
        self.canvas.create_window(960, y, window=label)
        return label

    def create_canvas_button(self, text, command, font, y):
        """Helper to create and place a button on the canvas."""
        button = ct.CTkButton(self, text=text, command=command, font=font)
        self.canvas.create_window(960, y, window=button)
        return button

    def show_main_menu(self):
        """Display the main menu."""
        # Load main menu background
        self.load_image("Q:\\Ibrahim\\Programs\\1234.jpg")

        # Add main menu label and buttons
        self.label = self.create_canvas_label(
            text="Welcome to the Horror Game", font=("Times new roman", 60, "italic"), y=350
        )
        self.how_to_play_button = self.create_canvas_button(
            text="How to Play", command=self.howtoplay, font=("Times new roman", 50), y=700
        )
        self.start_game_button = self.create_canvas_button(
            text="Start Game", command=self.start_game, font=("Times new roman", 50), y=900
        )

    def hide_main_menu(self):
        """Hide the main menu widgets."""
        self.label.destroy()
        self.how_to_play_button.destroy()
        self.start_game_button.destroy()

    def howtoplay(self):
        """Display instructions on how to play."""
        self.hide_main_menu()

        self.label = self.create_canvas_label(
            text="1. Progress into the game by choosing options.\n"
                 "2. Select the action you want to take.\n"
                 "3. Complete tasks and escape!",
            font=("Times new roman", 40), y=350
        )
        self.back_button = self.create_canvas_button(
            text="Back", command=self.show_main_menu, font=("Times new roman", 50), y=900
        )

    def start_game(self):
        """Start the game, play music, and change the scene."""
        self.hide_main_menu()

        # Play background music
        pygame.mixer.init()
        pygame.mixer.music.load("Q:\\Ibrahim\\Programs\\horrorsound.mp3")
        pygame.mixer.music.play()

        # Update the canvas image
        self.load_image("Q:\\Ibrahim\\Programs\\234.jpg")

        # Add the game label and input
        self.label = self.create_canvas_label(
            text="You are stranded in an abandoned graveyard.\nWhat would you like to do?",
            font=("Times new roman", 40), y=350
        )
        self.entry = ct.CTkEntry(self, font=("Times new roman", 30), width=400, placeholder_text="Type your action...")
        self.canvas.create_window(960, 600, window=self.entry)

        # Add a search button
        self.search_button = self.create_canvas_button(
            text="Search", command=self.searchfirst, font=("Times new roman", 50), y=900
        )

    def searchfirst(self):
        """Handle the first search action."""
        user_input = self.entry.get()  # Get the text from the entry widget
        print(f"Search initiated. User input: {user_input}")

        # Update the scene based on the search
        self.label.configure(
            text="You find a rusted key and an old map.\nDo you take them or keep searching?",
            font=("Times new roman", 40),
        )

        # Update the button behavior
        self.search_button.destroy()
        self.take_items_button = self.create_canvas_button(
            text="Take Key and Map", command=self.take_items, font=("Times new roman", 50), y=900
        )

    def take_items(self):
        """Handle the action of taking items."""
        print("Key and map taken.")
        self.label.configure(
            text="You took the key and map.\nThe adventure continues...",
            font=("Times new roman", 40),
        )

        # Update the button behavior
        self.take_items_button.destroy()
        self.continue_button = self.create_canvas_button(
            text="Continue", command=self.continue_game, font=("Times new roman", 50), y=900
        )

    def continue_game(self):
        """Continue to the next part of the game."""
        print("Continuing the game...")
        self.label.configure(text="To be continued...", font=("Times new roman", 40))
        self.continue_button.destroy()


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
