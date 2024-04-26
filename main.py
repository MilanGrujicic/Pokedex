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

        self.information_display = Frame(self.window, bg="black", width=130, height=150)
        self.information_display.place(x=190, y=220)

        self.pokemon_search = Button(text="Search", width=9, height=2, bg="#5fc480", highlightbackground="black", border="2", font=("Helvetica", 17, "bold"),command=self.search_pokemon).place(x=100,y=509)

        self.made_with_love_by_milan = Label(text="Made with love by Milan Grujicic", bg="black", fg="white", font=("Helvetica", 10, "italic")).place(x=1,y=630)

        self.window.mainloop()

    def search_pokemon(self):
        pokemon_information = self.get_pokemon_information()
        threading.Thread(target=self.getImageFromURL, args=(pokemon_information[-1], self)).start()
        self.imagelab = Label(self.window, text="Loading Pokemon data ...", width=25, height=5, bg="black", fg="white")
        self.imagelab.place(x=90, y=250)
        self.window.bind("<<ImageLoaded>>", self.on_image_loaded)
        self.display_pokemon_information(pokemon_information)

    def get_pokemon_information(self):
        pokemon_information = list()
        pokemon_name = self.user_input.get(1.0, END).strip()  # Get and strip the input text
        if not pokemon_name:
            print("Please enter a Pokémon name.")
            return None

        endpoint = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"  # Construct the correct endpoint
        response = requests.get(url=endpoint)

        if response.status_code == 200:
            data = response.json()
            pokemon_information.append(data["id"])
            pokemon_information.append(pokemon_name)
            pokemon_information.append(data["types"][0]["type"]["name"])
            pokemon_information.append(data["abilities"][1]["ability"]["name"])
            pokemon_information.append(data["sprites"]["front_default"])
            return pokemon_information
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

    def display_pokemon_information(self, list_with_pokemon_information):
        print("display_pokemon_information")

        self.id = Label(self.information_display, text="ID:", bg="black", fg="white")
        self.id.grid(column=0, row=0, pady=5, sticky="e")

        self.pokemon_id = Label(self.information_display, text=list_with_pokemon_information[0], bg="black", fg="white")
        self.pokemon_id.grid(column=1, row=0, pady=5, sticky="w")

        self.name = Label(self.information_display, text="Name:", bg="black", fg="white")
        self.name.grid(column=0, row=1, pady=5, sticky="e")

        self.pokemon_name = Label(self.information_display, text=list_with_pokemon_information[1].title(), bg="black", fg="white",)
        self.pokemon_name.grid(column=1, row=1, pady=5, sticky="w")

        self.type = Label(self.information_display, text="Type:", bg="black", fg="white")
        self.type.grid(column=0, row=2, pady=5, sticky="e")

        self.pokemon_type = Label(self.information_display, text=list_with_pokemon_information[2].title(), bg="black", fg="white")
        self.pokemon_type.grid(column=1, row=2, pady=5, sticky="w")

        self.ability = Label(self.information_display, text="Ability:", bg="black", fg="white")
        self.ability.grid(column=0, row=3, pady=5, sticky="e")

        self.pokemon_type = Label(self.information_display, text=list_with_pokemon_information[3].title(), bg="black", fg="white")
        self.pokemon_type.grid(column=1, row=3, pady=5, sticky="w")

if __name__ == "__main__":
    app = Pokedex()
