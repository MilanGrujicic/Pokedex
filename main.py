import requests
import threading
from urllib.request import urlopen
from PIL import ImageTk
from tkinter import *

BACKGROUND_COLOR = "#191919"
ENDPOINT = "https://pokeapi.co/api/v2/pokemon/pikachu"

class Pokedex:
    def __init__(self):
        self.window = Tk()
        self.window.title("Pokedex")
        self.window.config(bg=BACKGROUND_COLOR)

        self.canvas = Canvas(width=850, height=650, bg=BACKGROUND_COLOR)
        pokedex_img = PhotoImage(file="pokedex3.png")
        self.pokedex = self.canvas.create_image(400, 325, image=pokedex_img)
        self.canvas.grid(row=0, column=0)

        self.user_input = Text(bg="#084035", fg="white", height=1, width=31, borderwidth=0)
        self.user_input.place(x=480, y=235)

        self.close_button = Button(text="Search", width=9, height=2, bg="#5fc480", highlightbackground="black", border="2", font=("Helvetica", 17, "bold"),command=self.search_pokemon).place(x=100,y=509)

        self.window.mainloop()

    def search_pokemon(self):
        self.sprite_url = self.get_pokemon_sprite()
        print(self.sprite_url)

    def get_pokemon_sprite(self):
        # self.text = self.user_input.get(1.0, END)
        response = requests.get(url=f"{ENDPOINT}")
        data = response.json()
        sprite = data["sprites"]["front_default"]
        return sprite


if __name__ == "__main__":
    app = Pokedex()
