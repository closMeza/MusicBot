
import tkinter as tk
import sys
from spotify import spotify, Song




class Application(tk.Frame):
   
    # Constructor for our GUI
    

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.spot = spotify()

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
                                 width=25)
        self.textEntry.grid(row = 1, column=0)

        # Search Button
        self.search = tk.Button(self,
                                text="SEARCH",
                                command = self.get_list)
        self.search.grid(row = 1, column=1)

        # ListView 
        self.list_view = tk.Listbox(self,
                                    width=25)
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
        song = Song(input)
       

        self.list_view.insert('end', song.name)
        print(song)

        
        self.textEntry.delete(0, 'end')


def main():
    root = tk.Tk()
    app = Application(master=root)
    root.title("MusicBot")
    root.geometry("300x300")
    app.mainloop()

if __name__ == "__main__":
    main()