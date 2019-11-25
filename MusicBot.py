from tkinter import *
from math import *
from spotify import *

Weights = {"energy": .2, "danceability": .5}
SONG_LIST = []
VOTES = []
recommended_songs = []
counter = 0
dislike_counter = 0
searched_song = None
song = None
searched_features = None
WIDTH, HEIGHT = 1000, 550

def main():
    window, background, search_text, song_canvas, scroll_bar, widgets, songs_displayed = create_window(WIDTH, HEIGHT)
    search_text.bind("<Button 1>", search_click(search_text))
    search_text.bind("<Return>", get_search_text(search_text, song_canvas, widgets, songs_displayed))
    background.bind("<Button 1>", background_click(search_text))
    song_canvas.bind("<Button 1>", song_canvas_click(search_text, song_canvas, widgets, songs_displayed))
    window.mainloop()


#Returns variables needed to change the gui in another function
def create_window(width, height):
    window = Tk()
    window.geometry(str(WIDTH) + 'x' + str(HEIGHT))

    background = Canvas(window, width=WIDTH, height=HEIGHT, background='dark blue')
    background.place(x=0, y=0)

    search_message = "Search for song/artist here"
    search_text = Entry(window, width=int(70 * WIDTH / 550 - WIDTH / 50), bd=4)
    search_text.config(highlightbackground='white')
    search_text.insert("0", search_message)
    search_text.place(x=int(70 * WIDTH / 550 - WIDTH / 30), y=30)

    song_canvas = Canvas(window, height = HEIGHT - 200, width = WIDTH - 225)
    song_canvas.place(x = 100, y = 80)      
    song_canvas.config(highlightthickness=0)

    scroll_bar = Scrollbar(window)
    scroll_bar.config(command=song_canvas.yview)                   
    song_canvas.config(yscrollcommand=scroll_bar.set)              
    scroll_bar.pack(side=RIGHT, fill=Y)

    song_canvas.place(x=102, y=77)
    widgets, songs_displayed = [], []
    if len(SONG_LIST) * 45 > HEIGHT - 200:
        widgets.insert(0, song_canvas.create_rectangle(WIDTH - 320, 0, WIDTH - 310, len(SONG_LIST) * 45, fill = "dark blue"))
    else:
        widgets.insert(0, song_canvas.create_rectangle(WIDTH - 320, 0, WIDTH - 310, HEIGHT - 200, fill = "dark blue"))
    add_songs(widgets, song_canvas, SONG_LIST, songs_displayed)
    song_canvas.config(scrollregion=(0,0,0, 45 + len(SONG_LIST) * 45))

    for i in range(0, len(VOTES)):
        widget_num = i * 7 + 1
        vote = VOTES[i]
        if vote == 'Like':
            like(widget_num, song_canvas, widgets, songs_displayed)
        elif vote == 'Dislike':
            dislike(widget_num, song_canvas, widgets, songs_displayed)

    search_button = Button(window, text="Search", command=get_search_text(search_text, song_canvas, widgets, songs_displayed), width= int(WIDTH / 75))
    search_button.place(x=int(WIDTH - WIDTH/4.5), y = 30)

    return window, background, search_text, song_canvas, scroll_bar, widgets, songs_displayed

def get_search_text(search_text, song_canvas, widgets, songs_displayed):
    def fn(*args):
        #temp = search_text.get()
        global searched_song
        global song
        searched_song = search_text.get()
        song = Song(searched_song)
        
        global recommended_songs
        #song_list = song.related_songs
        recommended_songs = song.related_songs #song_list[song.get_genres(song.artist_id)[0]]
        recommend_song(widgets, song_canvas, songs_displayed)
    return fn

def recommend_song(widgets, song_canvas, songs_displayed):
    global counter
    global searched_features

    #save features of the input song into global variable
    searched_features = song.features 

    #temp[0].feature 
    best = None
    
    for match in recommended_songs:
        name = match[0]
        
        #makes it so that it doesnt recommend same song as input
        if name == song.name:
            continue

        features = match[1]
        energy = features['energy']
        dance = features['danceability']

        #calculate range for energy 
        floor_of_energy = searched_features['energy'] - (searched_features['energy'] * Weights['energy'])
        ceiling_of_energy = searched_features['energy'] + (searched_features['energy'] * Weights['energy'])

        #calculate range for danceability
        floor_of_dance = searched_features['danceability'] - (searched_features['danceability'] * Weights['danceability'])
        ceiling_of_dance = searched_features['danceability'] + (searched_features['danceability'] * Weights['danceability'])
        if ((energy > floor_of_energy and energy <ceiling_of_energy) and (dance > floor_of_dance and dance < ceiling_of_dance)):
            best = name
            recommended_songs.remove(match)
            break
        
        #temporary "exception" when AI cant find song with current weights
        #if(best == None):
            #best="enter a new song"

    #push song to GUI for feedback
    add_one_song(widgets, song_canvas, songs_displayed, best)
    if len(recommended_songs) - 1 > counter:
        counter += 1

#Adds Songs and Votes Spaced out by 45 pixels
def add_songs(widgets, canvas, songsArray, songs_displayed):
    for i in range(0, len(songsArray)):
        widgets.insert(i * 7 + 1, canvas.create_text(0, 25 + i * 45, font = "Times 18", text = songsArray[i], anchor=W))
        songs_displayed.append(songsArray[i])
        create_upvote(widgets, canvas, WIDTH - 290, 10 + i * 45, 14, 28)
        create_downvote(widgets, canvas, WIDTH - 250, 10 + i * 45, 14, 28)
        
#Adds one song at a time
#Does nothing if song is already displayed
#Displays Song with current vote if already in global SONG_LIST
#otherwise Adds song to end SONG_LIST and songs_displayed
def add_one_song(widgets, canvas, songs_displayed, song):
    if song in songs_displayed:
        return
    i = (len(widgets) - 1) / 7
    exists = song in SONG_LIST
    widgets.append(canvas.create_text(0, 25 + i * 45, font = "Times 18", text = song, anchor = W))
    
    songs_displayed.append(song)
    create_upvote(widgets, canvas, WIDTH - 290, 10 + i * 45, 14, 28)
    create_downvote(widgets, canvas, WIDTH - 250, 10 + i * 45, 14, 28)
    canvas.config(scrollregion=(0,0,0, 45 + len(SONG_LIST)* 45))
    x1, y1, x2, y2 = canvas.coords(widgets[0])
    y2 += 45
    canvas.coords(widgets[0], x1, y1, x2, y2)

    if not exists:
        SONG_LIST.append(song)
        VOTES.append("None")
    else:
        vote = VOTES[SONG_LIST.index(song)]
        if vote == 'Like':
            like(len(widgets) - 6, canvas, widgets, songs_displayed)
        elif vote == 'Dislike':
            dislike(len(widgets) - 3, canvas, widgets, songs_displayed)

def on_enter(widgets, canvas, songs_displayed, search_text):
    def fn(*args):
        return
    return fn

#Clears canvas of songs and votes
def clear_songs(canvas, widgets, songs_displayed):
    for i in range(0, len(songs_displayed)):
        clear_one_song(widgets, canvas, songs_displayed, songs_displayed[0])

def clear_one_song(widgets, canvas, songs_displayed, song):
    j = songs_displayed.index(song) * 7 + 1
    print(j)
    for i in range(0, 7):
        canvas.delete(widgets[i + j])
    for i in range(0, 7):
        widgets.remove(widgets[j])
    songs_displayed.remove(song)
    print(VOTES)
    canvas.config(scrollregion=(0,0,0, 45 + len(songs_displayed) * 45))

    for i in range(j, len(widgets)):
        canvas.move(widgets[i], 0, -45)

#Creates an upvote on the given canvas with the given x, y coordinates, height, and width and inserts into widgets
def create_upvote(widgets, canvas, x, y, width, height):
    i = int((y - 10) / 45) * 7
    widgets.insert(i + 2, canvas.create_polygon(x, y, x - width/2, y + height/2, x + width/2, y + height/2, fill='white', outline='black', width=3))
    widgets.insert(i + 3, canvas.create_rectangle(x - width/4, y + height/2, x + width/4, y + height, fill='white', outline='black', width=3))
    widgets.insert(i + 4, canvas.create_rectangle(x - width/4 + 2, y + height/2 - 5, x + width/4 - 2, y + height/2 + 5, fill='white', outline='white'))

#Creates a downvote on the given canvas with the given x, y coordinates, height, and width and inserts into widgets
def create_downvote(widgets, canvas, x, y, width, height):
    i = int((y - 10) / 45) * 7
    widgets.insert(i + 5, canvas.create_polygon(x, y + height, x - width/2, y + height/2, x + width/2, y + height/2, fill='white', outline='black', width=3))
    widgets.insert(i + 6, canvas.create_rectangle(x - width/4, y + height/2, x + width/4, y, fill='white', outline='black', width=3))
    widgets.insert(i + 7, canvas.create_rectangle(x - width/4 + 2, y + height/2 - 5, x + width/4 - 2, y + height/2 + 5, fill='white', outline='white'))

#Removes the default search text if clicking on the search text box
def search_click(search_text):
    def fn(*arg):
        if search_text.get()[0:27] == "Search for song/artist here":
            search_text.delete("0", END)
    return fn

#takes away focus from the text box and puts the search message back if nothing is inputed
def background_click(search_text):
    def fn(*arg):
        search_text.master.focus_set()
        if len(search_text.get()) == 0:
            search_text.insert("0", "Search for song/artist here")
    return fn

#Checks where the mouse clicks and finds the widget number associated
#If the widget number is a vote then change the color of that vote
#If the widget number is a song then print whether it is liked or disliked
def song_canvas_click(search_text, canvas, widgets, songs_displayed):
    def fn(event):
        canvas.focus_set()
        if len(search_text.get()) == 0:
            search_text.insert("0", "Search for song/artist here")
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        widget_num, vote = get_widget_num(x, y)
        if widget_num % 7 - 1:
            if (vote == 'like'):
                like(widget_num, canvas, widgets, songs_displayed)
            if (vote == 'dislike'):
                dislike(widget_num, canvas, widgets, songs_displayed)
        else:
            song_num = get_song_num(y)
            print(songs_displayed[song_num - 1] + " Liked = " + str(is_liked(canvas, song_num, widgets)) + " Disliked = " + str(is_disliked(canvas, song_num, widgets)))
    return fn


def get_widget_num(x, y):
    if x > WIDTH - 310:
        return get_vote_num(x, y)
    return 1, "song"

def get_song_num(y):
    temp = (y - 10) % 45
    temp = (ceil((y - temp) / 45) - 1) + 1
    return temp

#Uses the x and y coordinates to find if a vote was clicked
#If a vote is clicked returns a valid widget num > 0 else returns 0
def get_vote_num(x, y):
    temp = (y - 10) % 45
    if x > WIDTH - 295 and x < WIDTH - 285:
        if temp > 0 and temp < 28:
            return (ceil((y - temp) / 45) - 1) * 7 + 2, "like"
    if x > WIDTH - 255 and x < WIDTH - 245:
        if (temp > 0 and temp < 28):
            return (ceil((y - temp) / 45) - 1) * 7 + 5, "dislike"
    return 0, ""

#Returns whether the upvote fill is blue
def is_liked(song_canvas, song_num, widgets):
    return song_canvas.itemcget(widgets[7 * song_num -5], 'fill') == 'blue'

#Returns whether the downvote fill is blue
def is_disliked(song_canvas, song_num, widgets):
    return song_canvas.itemcget(widgets[7 * song_num -2], 'fill') == 'blue'

#Returns whether the VOTE at the song index is Like
def _is_liked(song_name):
    return VOTES[SONG_LIST.index(song_name)] == 'Like'

#Returns whether the VOTE at the song index is Like
def _is_disliked(song_name):
    return VOTES[SONG_LIST.index(song_name)] == 'Dislike'

#sets the like of the song number of the currently displayed songs to the reverse color and the dislike to white
def like(widget_num, canvas, widgets, songs_displayed):
    global VOTES
    white = canvas.itemcget(widgets[widget_num], 'fill') == 'white'
    fill = 'blue' if white else 'white'
    canvas.itemconfig(widgets[widget_num], fill=fill)
    canvas.itemconfig(widgets[widget_num + 1], fill=fill)
    canvas.itemconfig(widgets[widget_num + 2], fill=fill, outline=fill)
    canvas.itemconfig(widgets[widget_num + 3], fill='white')
    canvas.itemconfig(widgets[widget_num + 4], fill='white')
    canvas.itemconfig(widgets[widget_num + 5], fill='white', outline='white')
    
    song_num = SONG_LIST.index(canvas.itemcget(widgets[widget_num - widget_num % 7 + 1], 'text'))
    VOTES[song_num] = 'Like' if white else 'None'
    if (song_num == len(SONG_LIST) - 1):
        recommend_song(widgets, canvas, songs_displayed)
    print(VOTES)


#sets the dislike of the song number of the currently displayed songs to the revers color and the like to white
def dislike(widget_num, canvas, widgets, songs_displayed):
    global VOTES
    global dislike_counter
    white = canvas.itemcget(widgets[widget_num], 'fill') == 'white'
    fill = 'blue' if white else 'white'
    canvas.itemconfig(widgets[widget_num], fill=fill)
    canvas.itemconfig(widgets[widget_num + 1], fill=fill)
    canvas.itemconfig(widgets[widget_num + 2], fill=fill, outline=fill)
    canvas.itemconfig(widgets[widget_num - 3], fill='white')
    canvas.itemconfig(widgets[widget_num - 2], fill='white')
    canvas.itemconfig(widgets[widget_num - 1], fill='white', outline='white')

    dislike_counter += 1

    if dislike_counter < 3:
        Weights['energy'] = (Weights['energy'] +(dislike_counter *.05)) 
        Weights['danceability'] = (Weights['danceability'] -(dislike_counter *.05)) 

    elif dislike_counter == 3:
        Weights['energy'] = .2
        Weights['danceability'] = .5

    elif dislike_counter >= 3:
        Weights['energy'] = (Weights['energy'] -(dislike_counter *.05)) 
        Weights['danceability'] = (Weights['danceability'] +(dislike_counter *.05)) 

    if(Weights['energy'] >= 1 or Weights['energy'] <= 0):
        Weights['energy'] = .2

    if(Weights['danceability'] >= 1 or Weights['danceability'] <= 0):
       Weights['danceability'] = .5

    song_num = SONG_LIST.index(canvas.itemcget(widgets[widget_num - widget_num % 7 + 1], 'text'))
    VOTES[song_num] = 'Dislike' if white else 'None'
    if (song_num == len(SONG_LIST) - 1):
        recommend_song(widgets, canvas, songs_displayed)
    print(VOTES)

main()
