#Library used (tkinter, pygame, mutagen)
import time
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import Button, Frame, Label, Listbox, Menu, filedialog
from tkinter import PhotoImage
from tkinter.constants import ACTIVE, ANCHOR, BOTTOM, E, END, GROOVE, HORIZONTAL, X
from pygame import mixer
from mutagen.mp3 import MP3

#________________MAIN WINDOW DIMENSION_____________
body = tk.Tk()
body.title("Spotiplay")
body.geometry("400x430")
body.config(bg = '#E4EFE7')

# initialize pygame mixer
pygame.init()
mixer.init()

#________________MAIN FUNCTION_____________________


#Adding single/multiple tracks function
def add_track():

    #Opening files in directory
    tracks = filedialog.askopenfilenames(initialdir = 'tracks/', title = "Select a Track", filetypes=(("mp3 Files", "*.mp3"),))
    #Loop statement to remove the directory info.
    for track in tracks:
        track = track.replace("C:/Users/Nero/music-player/tracks/","")
        track = track.replace(".mp3", "")
        music_box.insert(END, track)

    # for track in tracks:
    #   music_box.insert(END,track)

#Removing single/multiple tracks function
def remove_track():

    #Calling for stop function
    stop()
    #Removing single track
    music_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def remove_tracks():

    #Calling for stop function
    stop()
    #Removing multiple tracks
    music_box.delete(0,END)
    pygame.mixer.music.stop()

#Play Function
def play():

    #calling global stopped for preventing slider to stop while the track is playing
    global stopped
    stopped = False

    #Getting the title of the song and directory of the mp3
    tracks = music_box.get(ACTIVE)
    tracks = f'C:/Users/Nero/music-player/tracks/{tracks}.mp3'
    # trackdir = os.path.dirname('C:/Users/Nero/music player/tracks')
    # trackpath = os.path.join(trackdir,".mp3")

    #Playing the track
    pygame.mixer.music.load(tracks)
    pygame.mixer.music.play(loops=0)

    #Calling of track_time function
    track_time()

    # position = int(length_track)
    # track_slide.config(to=position, value=0)
    
    # curr_volume = pygame.mixer.music.get_volume
    # track_slide_label.config(text=curr_volume*100)

#Pause Function
global paused
paused = False

def pause(is_paused):

    global paused
    paused=is_paused

    #If else statement for pausing and unpausing a track
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
    
#Stop Function
global stopped
stopped = False

def stop():

    #Reset the slider and time stat bar
    time_bar.config(text='')
    track_slide.config(value=0)

    #Stop track from playing
    pygame.mixer.music.stop()
    music_box.selection_clear(ACTIVE)

    time_bar.config(text='')

    #Global variable for stop to stop the slider on moving when it is stopped
    global stopped
    stopped = True

#Skip Function
def skip():

    #Reset the slider and time stat bar
    time_bar.config(text='')
    track_slide.config(value=0)
    #Getting the current posision number of the current track
    next = music_box.curselection()
    #Adding 1 to the current track and prepare to skip the track
    next = next[0]+1
    #Getting the title of the current next track
    track = music_box.get(next)
    track = f'C:/Users/Nero/music-player/tracks/{track}.mp3'
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(loops=0)

    #Navigation of the bar if it has been skipped
    music_box.selection_clear(0,END)
    music_box.activate(next)
    music_box.selection_set(next, last=None)

#Previous Function
def prevs():

    #Reset the slider and time stat bar
    time_bar.config(text='')
    track_slide.config(value=0)
    #Getting the current posision number of the current track
    back = music_box.curselection()
    #Subtracting 1 to the current track and the track should have been previous
    back = back[0]-1
    #Getting the title of the current previous track
    track = music_box.get(back)
    track = f'C:/Users/Nero/music-player/tracks/{track}.mp3'
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(loops=0)

    #Navigation of the bar if it has been Previous
    music_box.selection_clear(0,END)
    music_box.activate(back)
    music_box.selection_set(back, last=None)


#Track time Function
def track_time():

    #if statement for slider for getting 2x faster
    if stopped:
        return

    #Getting the Current track time
    curr_time = pygame.mixer.music.get_pos()/1000

    #label to get the data
    #track_slide_label.config(text=f'Slider:{int(track_slide.get())} and track_pos:{int(curr_time)}')

    #Converting track length to time format
    current_converted_track = time.strftime('%M:%S', time.gmtime(curr_time))

    #Getting the title of the current next track
    track = music_box.get(ACTIVE)
    track = f'C:/Users/Nero/music-player/tracks/{track}.mp3'
    load_track = MP3 (track)
    global length_track
    length_track = load_track.info.length
    #Song time converted to time format
    current_length_track = time.strftime('%M:%S', time.gmtime(length_track))
    
    #if statement for updating the slider while the track is playing
    #increase the curr time by 1 sec
    curr_time +=1
    if int(track_slide.get()) == int(length_track):
        time_bar.config(text=f'{current_length_track}')
    
    elif paused:
        pass

    elif int(track_slide.get()) == int(curr_time):
        #Slider position update
        position = int(length_track)
        track_slide.config(to=position, value=int(curr_time))

    else: 
        #Slider position update
        position = int(length_track)
        track_slide.config(to=position, value=int(track_slide.get))

        #Track time converted to time format
        current_length_track = time.strftime('%M:%S', time.gmtime(int(track_slide.get())))
        #Track time in time bar
        time_bar.config(text=f'Time: {current_converted_track}')

        time_nav = int(track_slide.get())+1
        track_slide.config(value=time_nav)


    #Song time in time bar
    #time_bar.config(text=f'{current_length_track}')
    #The slider position value of the current playing track
    #track_slide.config(value=int(curr_time))

    # curr_time_label = Label(body, text=int(curr_time))
    # curr_time_label.pack(pady=10)

    #Track slider position
    
    #Play time of the track
    time_bar.after(1000, track_time)


#Track navigator slider
def t_slider():
    #track_slide_label.config(text=f'{int(track_slide.get())} of {int({length_track})}')
    
    track = music_box.get(ACTIVE)
    track = f'C:/Users/Nero/music-player/tracks/{track}.mp3'
    
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(loops=0, start=int(track_slide.get()))


#Track Volume Function
def t_vol():
    pygame.mixer.music.set_volume(vol_slider.get())
    # curr_volume = pygame.mixer.music.get_volume
    # track_slide_label.config(text=curr_volume*100)


#________________MAIN GUI_____________________

#Frame
main_frame = Frame(body)
main_frame.pack(pady=30)

#Music Box, the list of the music that has been import
music_box = Listbox(main_frame, bg="#FAF1E6", fg="#064420", width=55)
music_box.grid(row=0, column=0)

#Music track navigator slider
track_slide = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command = t_slider, length=330)
track_slide.grid(row=1, column=0, pady=20)
# track_slide_label = Label(body, text="0")
# track_slide_label.pack(pady=10)

#Configuration of the Buttons
controls_frame = Frame(main_frame, bg="#E4EFE7")
controls_frame.grid(row=2,column=0, pady=10)

#Volume control frame
vol_frame = ttk.LabelFrame(main_frame)
vol_frame.grid(row=3, column=0)

#Volume Slider
vol_slider = ttk.Scale(vol_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command = t_vol, length=100)
vol_slider.pack(pady=5)

#Image of the Buttons
prev_bt = PhotoImage(file='gui/prev.png')
pause_bt = PhotoImage(file='gui/pause.png')
play_bt = PhotoImage(file='gui/play.png')
stop_bt = PhotoImage(file='gui/stop.png')
skip_bt = PhotoImage(file='gui/skip.png')

#Controls of the buttons
prev_control = Button(controls_frame, image = prev_bt, borderwidth=0, command= prevs)
prev_control.grid(row=0, column=0, padx=5)
pause_control = Button(controls_frame, image = pause_bt, borderwidth=0, command = lambda: pause(paused))
pause_control.grid(row=0, column=1, padx=5)
play_control = Button(controls_frame, image = play_bt, borderwidth=0, command = play)
play_control.grid(row=0, column=2, padx=5)
stop_control = Button(controls_frame, image = stop_bt, borderwidth=0, command = stop)
stop_control.grid(row=0, column=3, padx=5)
skip_control = Button(controls_frame, image = skip_bt, borderwidth=0, command= skip)
skip_control.grid(row=0, column=4, padx=5)

#Menu
main_menu = Menu(body)
body.config(menu = main_menu)

#Selecting/Importing a track from Menu
menu_add_track = Menu(main_menu)
main_menu.add_cascade(label = "Add", menu = menu_add_track)
#Selecting a file to be imported in the music box
menu_add_track.add_command(label= "Import File", command = add_track)

#Removing a track form the menu
menu_remove_track = Menu(main_menu)
main_menu.add_cascade(label = "Remove", menu = menu_remove_track)
#Selecting a file to be removed in the music box
menu_remove_track.add_command(label= "Remove", command = remove_track)
menu_remove_track.add_command(label= "Remove All Track", command = remove_tracks)

#Track time status
time_bar = Label(body, text='', bd=1, relief=GROOVE, anchor=E)
time_bar.pack(fill=X, side=BOTTOM, ipady=2)


body.mainloop()

