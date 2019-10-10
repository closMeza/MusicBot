import tkinter as tk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util



class Application(tk.Frame):
   
    # Constructor for our GUI

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.cid = "89ba12dbb318412baa7c3f1c642d17d9"
        self.secret = "47689f35aa354d0dbe06d1b89323561d"


    # this creates all the widgets for our GUI
    def create_widgets(self):

        # value for row on grid
        #r = 0
        
        # Title Label maybe convert to image
        self.header = tk.Label(self,
                             text="Music Bot",
                             font = "28",
                             height=2)
        self.header.grid(row = 0, column = 0)
       
       # textEntry for user input
        self.textEntry = tk.Entry(self,
                                 width=20)
        self.textEntry.grid(row = 1, column=0)

        # Search Button
        self.search = tk.Button(self,
                                text="SEARCH",
                                command = self.get_list)
        self.search.grid(row = 1, column=1)

        # ListView 
        self.list_view = tk.Listbox(self)
        self.list_view.grid(row = 2, column = 0)

        
        #quit button
        self.quit = tk.Button(self, text= "Quit", 
                              fg="red", 
                              command = self.master.destroy)
        self.quit.grid(row = 3, column = 1)

    # this is where we need to map user input to spotify database
    # we need to create a pkg for our AI to proccess input and return
    # list of songs based on genre
    def get_list(self):
        input = self.textEntry.get()
        
        #this needs to be set in init of Application this is the authorizes connection to spotify.
        client_credentials_manager = SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret) 
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        #we need this URI to search items in spotify database.
        URI = 'spotify:track:5bJ1DrEM4hNCafcDd1oxHx'
        result = sp.track(URI)

        #places result of spotify search and places it in list and prints it onto console
        self.list_view.insert(0, result['name'])
        print(result['name'])
        
        self.textEntry.delete(0, 'end')


def main():
    root = tk.Tk()
    app = Application(master=root)
    root.title("MusicBot")
    root.geometry("300x300")
    app.mainloop()

if __name__ == "__main__":
    main()



