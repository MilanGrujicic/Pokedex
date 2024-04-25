import requests
import threading
from urllib.request import urlopen
from PIL import ImageTk
from tkinter import *

BACKGROUND_COLOR = "#191919"

class Pokedex:
    def __init__(self):
        self.window = Tk()
        self.window.title("Pokedex")
        self.window.config(bg=BACKGROUND_COLOR)

        self.canvas = Canvas(width=850, height=650, bg="black")
        pokedex_img = PhotoImage(file="Pokedex.png")
        self.pokedex = self.canvas.create_image(400, 325, image=pokedex_img)
        self.canvas.grid(row=0, column=0)

        self.user_input = Text(bg="#084035", fg="white", height=1, width=31, borderwidth=0)
        self.user_input.place(x=480, y=235)

        self.close_button = Button(text="Search", width=9, height=2, bg="#5fc480", highlightbackground="black", border="2", font=("Helvetica", 17, "bold"),command=self.search_pokemon).place(x=100,y=509)

        self.window.mainloop()

    def search_pokemon(self):
        pokemon_info = self.sprite_url = self.get_pokemon_info()
        threading.Thread(target=self.getImageFromURL, args=(pokemon_info[-1], self)).start()
        self.imagelab = Label(self.window, text="Loading image from internet ...", width=25, height=5, bg="black", fg="white")
        self.imagelab.place(x=90, y=250)
        self.window.bind("<<ImageLoaded>>", self.on_image_loaded)

    def get_pokemon_info(self):
        pokemon_info = list()
        pokemon_name = self.user_input.get(1.0, END).strip()  # Get and strip the input text
        if not pokemon_name:
            print("Please enter a Pokémon name.")
            return None

        endpoint = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"  # Construct the correct endpoint
        response = requests.get(url=endpoint)

        if response.status_code == 200:
            data = response.json()
            pokemon_info.append(pokemon_name)
            pokemon_info.append(data["id"])
            type = data["types"][0]["type"]["name"]
            type = type.title()
            pokemon_info.append(type)
            pokemon_info.append(data["abilities"][1]["ability"]["name"])
            pokemon_info.append(data["sprites"]["front_default"])
            return pokemon_info
        else:
            print(f"Error fetching Pokémon data: {response.status_code}")
            return None

    def getImageFromURL(self, url, controller):
        try:
            image = ImageTk.PhotoImage(file=urlopen(url))
            # notify controller that image has been downloaded
            controller.image = image
            controller.window.event_generate("<<ImageLoaded>>")
        except Exception as e:
            print(e)

    def on_image_loaded(self, event):
        self.imagelab.config(image=self.image, width=self.image.width(), height=self.image.height())


if __name__ == "__main__":
    app = Pokedex()
