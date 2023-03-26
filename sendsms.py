# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from tkinter import *
from threading import *
import threading
import random
import time
import pyautogui
import pandas
from PIL import ImageTk, Image
import tkinter.font as tkFont

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']='AC19c46e7522c3f20d9596b27a86541280'
auth_token = os.environ['TWILIO_AUTH_TOKEN']='bc564634327878a7e5a5f9a16cd2321e'
client = Client(account_sid, auth_token)

# name = input('Welcome to Helpify, what\'s you name? ')
#phone = input('What is your phone number? ')

mental_health = ['Your present circumstances don’t determine where you go; they merely determine where you start." — Nido Qubein', "You got this - keep up the hard work!", "Don't forget to take a break, fresh air heals all!", "You don’t have to control your thoughts. You just have to stop letting them control you.\" — Dan Millman",
                    ]
twilio_number = '+14406888960'
physical_health = ["Make sure to get active today! Whether that be the gym, a run or a walk!", "Don't forget to eat today", "Don't stare at your screen all day - make sure to take a break and talk with friends, enjoy the weather, or make some food!"]

mental_health_resource_links_url = ["https://www.nimh.nih.gov/health/find-help",
                                "https://988lifeline.org/",
                                "https://us.movember.com/"]
mental_health_resource_links_names = ["National Institue of Mental Health",
                                      "988 Suicide and Crisis Hotline",
                                      "Movember Foundation"]
mental_health_resource_links = zip(mental_health_resource_links_url, mental_health_resource_links_names)
physical_health_resource_links_url = ["http://webmd.com/",
                                      "https://www.myplate.gov/",
                                      "https://www.healthline.com/nutrition/how-to-start-exercising"]
physical_health_resource_links_names = ["WebMD",
                                        "MyPlate",
                                        "Beginner's Guide to Exercise"]

quotesData = pandas.read_csv("Quotes.csv")
x1 = random.randrange(40)

mental_messages = ["hope you're doing okay", "you matter", "keep going!", "today is a new day"]
physical_messages = ["you're looking good today", "get that workout in!", "hope your diet is going well!"]


response_questions = ["How are you feeling today?", "Enjoy today, are you excited for tommorow?", "Have you eaten today?"]
#Have you eaten today? If you would like some recipes I can send you some?!?

questionsData = ["How are feeling today? Really. Both physically and mentally.",
                 "What's taking up most of your headspace right now?",
                 "What was your last full meal, and have you been drinking enough water?",
                 "How have you been sleeping?",
                 "Have you been doing physical activities lately?",
                 "What did you do today that made you feel good?",
                 "What's something you're looking forward to in the next few days?",
                 "What are you grateful for right now?"]

zipCode = "What is your zip code by the way?"

# question = "Have you eaten today? If you would like some recipes I can send you some?!? (Just say 'recipes' followed by which meal and I'll get right on it!)"
# question2 = "Tell me how your day is going!"
# message = client.messages \
#                 .create(
#                      body= name +  ", " + question2,
#                      from_='+14406888960',
#                      to='+12072740647'
#                  )



window = Tk()
username = StringVar()
number = StringVar()
user_opt_mental = IntVar()
user_opt_physical = IntVar()
frequency_level = StringVar(value="Low")
window_quit_flag = threading.Event()
window_width_factor = .67
window_height_factor = .67
window_bg = 'lightblue'
width, height = pyautogui.size()
width *= window_width_factor
height *= window_height_factor
width_as_int = int(width)
height_as_int = int(height)
icon_photo = PhotoImage(file="icon_logo.png")
#bg_photo = Image.open('background.jpg')
#bg_photo = bg_photo.resize((width_as_int, height_as_int), Image.LANCZOS)
#bg_label = Label(window, image=bg_photo)

# app specific details
app_name = "SoulSupport"
app_font = tkFont.Font(family="Frutiger", size="48", weight="bold")
standard_info_font = ('Arial 18')
link_font = tkFont.Font(family="Frutiger", size="16", weight="bold", underline=True)

# for when the user has logged in
login_app_font = tkFont.Font(family="Frutiger", size="24", weight="bold")


def create_window():
    window.title(app_name)    
    window.geometry(str(width_as_int) + "x" + str(height_as_int))
    window.configure(bg=window_bg)
    posRight = int(window.winfo_screenwidth()*(1-window_width_factor) / 2)
    posDown = int(window.winfo_screenheight()*(1-window_height_factor) / 3)
    window.geometry("+{}+{}".format(posRight, posDown))
    window.protocol("WM_DELETE_WINDOW", window_quit)
    window.columnconfigure(0, weight=1)
    window.wm_iconphoto(False, icon_photo)

    home_screen()

    window.mainloop()

def home_screen():
    for widget in window.winfo_children():
        if(widget is not bg_label):
            widget.destroy()

    # reset username and number
    username.set("")
    number.set("")

    # top of the window, APP NAME
    app_name_frame = Frame(window,bg=window_bg)
    app_name_label = Label(app_name_frame, font=app_font, text=app_name, bg=window_bg,justify=CENTER)
    app_name_label.grid(row=0, rowspan=2, ipadx=width_as_int/4)
    app_name_frame.grid(row=0,column=0, pady=height_as_int/6)

    # register button
    buttons_frame = Frame(window, bg=window_bg)
    button_font = ("Arial 16")
    register_button = Button(buttons_frame, text="Register", font=button_font, command=user_register, width=18, height=2)
    register_button.grid(row=0, column=0, padx=10)

    # sign in button
    sign_in_button = Button(buttons_frame, text="Sign In", font=button_font, command=user_sign_in, width=18, height=2)
    sign_in_button.grid(row=0, column=1, padx=10)

    buttons_frame.grid(row=1)
def user_register():

    for widget in window.winfo_children():
        widget.destroy()

    width, height = window.winfo_width(), window.winfo_height()

     # top of the window, APP NAME
    app_name_frame = Frame(window,bg=window_bg)
    app_name_label = Label(app_name_frame, font=app_font, text=app_name, bg=window_bg,justify=CENTER)
    app_name_label.grid(row=0, rowspan=2, ipadx=width/4)
    app_name_frame.grid(row=0,column=0, pady=height/8)


    # center of the window, USER INFO
    info_frame = Frame(window, bg=window_bg)
    info_font = ('Arial 18')
    name_label = Label(info_frame, text="Name: ", bg=window_bg, font=info_font)
    name_entry = Entry(info_frame, textvariable= username, font=info_font)
    number_label = Label(info_frame, text="Number: ", bg=window_bg, font=info_font)
    number_entry = Entry(info_frame, textvariable= number, font=info_font)

    name_label.grid(row=1, column=0,pady=10)
    name_entry.grid(row=1, column=1, pady=10)
    number_label.grid(row=2, column=0, pady=10)
    number_entry.grid(row=2, column=1, pady=10)
    
    info_frame.grid(row=1)

    # text me button
    ###############
    #
    # CURRENTLY TESTING USER_ASK_CATEGORIES
    #
    ##############
    button_frame = Frame(window, bg=window_bg)
    button_font = ("Arial 16")
    text_me_button = Button(button_frame, text="Text me", font=button_font, command=text_user, width=18, height=2)
    text_me_button.grid(row=0)

    # back button
    back_button = Button(button_frame, text="Back", font=button_font, command=home_screen, width=18, height=2)
    back_button.grid(row=0, column=1, padx=30)

    button_frame.grid(row=2, pady=30)


    # notify user of what sign up is
    inform_user_frame = Frame(window, bg=window_bg)
    inform_user_font = ('Arial 16')
    inform_user_label = Label(inform_user_frame, text="* By clicking 'Text Me', you will be texted a welcome message", 
                              font = inform_user_font, wraplength=width*3/7, bg=window_bg)
    inform_user_label.grid(row=0)
    inform_user_frame.grid(row=3)


    window.columnconfigure(0, weight=1)

def user_sign_in():
    for widget in window.winfo_children():
        widget.destroy()

    width, height = window.winfo_width(), window.winfo_height()

     # top of the window, APP NAME
    app_name_frame = Frame(window,bg=window_bg)
    app_name_label = Label(app_name_frame, font=app_font, text=app_name, bg=window_bg,justify=CENTER)
    app_name_label.grid(row=0, rowspan=2, ipadx=width/4)
    app_name_frame.grid(row=0,column=0, pady=height/8)


    # center of the window, USER INFO
    info_frame = Frame(window, bg=window_bg)
    info_font = ('Arial 18')
    name_label = Label(info_frame, text="Name: ", bg=window_bg, font=info_font)
    name_entry = Entry(info_frame, textvariable= username, font=info_font)
    number_label = Label(info_frame, text="Number: ", bg=window_bg, font=info_font)
    number_entry = Entry(info_frame, textvariable= number, font=info_font)

    name_label.grid(row=1, column=0,pady=10)
    name_entry.grid(row=1, column=1, pady=10)
    number_label.grid(row=2, column=0, pady=10)
    number_entry.grid(row=2, column=1, pady=10)
    
    info_frame.grid(row=1)

    # text me button
    button_frame = Frame(window, bg=window_bg)
    button_font = ("Arial 16")
    text_me_button = Button(button_frame, text="Sign In", font=button_font, command=validate_user_sign_in, width=18, height=2)
    text_me_button.grid(row=0)

    # back button
    back_button = Button(button_frame, text="Back", font=button_font, command=home_screen, width=18, height=2)
    back_button.grid(row=0, column=1, padx=30)

    button_frame.grid(row=2, pady=30)

    window.columnconfigure(0, weight=1)

def validate_user_sign_in():
    number_valid = validate_user_number()
    if(not number_valid):
        popup_invalid_number()
        return
    user_home_screen()

def user_home_screen():
    for widget in window.winfo_children():
        widget.destroy()

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=0)
    width, height = window.winfo_width(), window.winfo_height()

    # top of the window, APP NAME
    app_name_frame = Frame(window,bg=window_bg)
    app_name_label = Label(app_name_frame, font=login_app_font, text=app_name, bg=window_bg,justify=CENTER)
    app_name_label.grid(row=0, rowspan=2, ipadx=width/4)
    app_name_frame.grid(row=0,column=0, pady=height/20)

    # welcome user
    welcome_user_frame = Frame(window, bg=window_bg)
    welcome_font = ('Arial 28')
    welcome_user_label = Label(welcome_user_frame, text="We are so glad you are here with us today,", font=welcome_font, bg=window_bg, wraplength=width*3/5)
    welcome_user_label.grid(row=0, pady=10)
    username_font = tkFont.Font(family="Courier", size="42")
    username_font.configure(slant="italic")
    user_name_label = Label(welcome_user_frame, text=username.get(), font=username_font, bg=window_bg)
    user_name_label.grid(row=1)
    welcome_user_frame.grid(row=1, pady=50)

    # buttons for settings, resources, logout to home screen
    # settings button
    button_frame = Frame(window, bg=window_bg)
    button_font = ("Arial 16")
    # settings_button = Button(button_frame, text="Settings", font=button_font, command=user_settings, width=16, height=2)
    # settings_button.grid(row=0)

    #resources button
    resources_button = Button(button_frame, text="Resources", font=button_font, command=show_resources, width=16, height=2)
    resources_button.grid(row=0, column=1, padx=30)

    # logout button
    back_button = Button(button_frame, text="Logout", font=button_font, command=home_screen, width=16, height=2)
    back_button.grid(row=0, column=2)

    button_frame.grid(row=2, pady=30)

def show_resources():
    for widget in window.winfo_children():
        widget.destroy()

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)


    mental_resources_frame = Frame(window, bg=window_bg)
    mental_resources_frame.columnconfigure(0, weight=1)
    # LABEL
    mental_resources_main_label = Label(mental_resources_frame, text="Mental Health Resources:", font=standard_info_font, bg=window_bg)
    mental_resources_main_label.pack()
    # LINKS
    # have to hardcode for now
    mlink1 = Label(mental_resources_frame, text=mental_health_resource_links_names[0], bg=window_bg, cursor="hand2", font=link_font)
    mlink1.pack(pady=20)
    mlink1.bind("<Button-1>", lambda e:
                link_user(mental_health_resource_links_url[0]))
    mlink2 = Label(mental_resources_frame, text=mental_health_resource_links_names[1], bg=window_bg, cursor="hand2", font=link_font)
    mlink2.pack()
    mlink2.bind("<Button-1>", lambda e:
                link_user(mental_health_resource_links_url[1]))
    mlink3 = Label(mental_resources_frame, text=mental_health_resource_links_names[2], bg=window_bg, cursor="hand2", font=link_font)
    mlink3.pack(pady=20)
    mlink3.bind("<Button-1>", lambda e:
                link_user(mental_health_resource_links_url[2]))
    mental_resources_frame.grid(row=0, column=0, pady=75)

    health_resources_frame = Frame(window, bg=window_bg)
    health_resources_frame.columnconfigure(0, weight=1)
    # LABEL
    health_resources_main_label = Label(health_resources_frame, text="Physical Health Resources:", font=standard_info_font, bg=window_bg)
    health_resources_main_label.pack()
    # LINKS
    hlink1 = Label(health_resources_frame, text=physical_health_resource_links_names[0], bg=window_bg, cursor="hand2", font=link_font)
    hlink1.pack(pady=20)
    hlink1.bind("<Button-1>", lambda e:
                link_user(physical_health_resource_links_url[0]))
    hlink2 = Label(health_resources_frame, text=physical_health_resource_links_names[1], bg=window_bg, cursor="hand2", font=link_font)
    hlink2.pack()
    hlink2.bind("<Button-1>", lambda e:
                link_user(physical_health_resource_links_url[1]))
    hlink3 = Label(health_resources_frame, text=physical_health_resource_links_names[2], bg=window_bg, cursor="hand2", font=link_font)
    hlink3.pack(pady=20)
    hlink3.bind("<Button-1>", lambda e:
                link_user(physical_health_resource_links_url[2]))
    health_resources_frame.grid(row=0, column=1)

    # back button
    button_frame = Frame(window, bg=window_bg)
    button_font = ("Arial 16")
    text_me_button = Button(button_frame, text="Back", font=button_font, command=user_home_screen, width=16, height=2)
    text_me_button.grid(row=1)
    button_frame.grid(row=1, columnspan=2, pady=50)

def link_user(url):
    webbrowser.open_new_tab(url)

def user_settings():
    pass

def popup_invalid_number():
        popup = Tk()
        popup.geometry("250x150")
        posRight = int(window.winfo_screenwidth()/ 3)
        posDown = int(window.winfo_screenheight() / 3)
        popup.geometry("+{}+{}".format(posRight, posDown))
        popup.wm_title("Invalid Number")
        error_label = Label(popup, text="Invalid number, please re-enter")
        error_label.pack()
        error_button = Button(popup, text="Okay", command=popup.destroy)
        error_button.pack()
        popup.mainloop()

def text_user():
    number_valid = validate_user_number()
    if(not number_valid):
        popup_invalid_number()
        return

    message = client.messages.create(
        to ="+1" + number.get(),
        from_ = twilio_number,
        body = "Hello " + username.get() + ", thank you for signing up, please send your zip code!"
    )
    print(message.account_sid)

    ask_user_for_text_categories()

def validate_user_number():
    user_number_json = client.lookups.v2.phone_numbers('+1' + number.get()).fetch()
    return user_number_json.valid

def ask_user_for_text_categories():
     for widget in window.winfo_children():
        widget.destroy()
     ask_user_frame = Frame(window, bg=window_bg)
     ask_label = Label(ask_user_frame, text="Which type of messages would you like to recieve?", bg=window_bg, font=standard_info_font)   
     ask_label.grid(row=0)
     ask_user_frame.grid(row=0, pady=60)

     checkbox_frame = Frame(window, bg=window_bg)
     mental_button = Checkbutton(checkbox_frame, text="Mental health", variable=user_opt_mental, onvalue=1, offvalue=0, 
                                font=standard_info_font, bg=window_bg, height=4, bd=5)
     physical_button = Checkbutton(checkbox_frame, text="Physical health", variable=user_opt_physical, onvalue=1, offvalue=0, 
                                  font=standard_info_font, bg=window_bg, height=4, bd=5)
     mental_button.grid(row=0, column=0, padx= 15)
     physical_button.grid(row=0, column=1)
     checkbox_frame.grid(row=1, pady=30)

     text_button = Frame(window, bg=window_bg)
     button_font = ('Arial 16')
     random_texts_button = Button(text_button, text="Confirm Settings", command=ask_user_for_daily_frequency, width=20, height=2, font=button_font)
     random_texts_button.grid(row=0)
     text_button.grid(row=2)

    # notify user that they can change these later
    # inform_user_frame = Frame(window, bg=window_bg)
    # inform_user_font = ('Arial 16')
    # inform_user_label = Label(inform_user_frame, text="* You can change these at a later time", 
    #                           font

def random_text_user():
     for widget in window.winfo_children():
          widget.destroy()


          ask_user_frame = Frame(window, bg=window_bg)
          ask_label = Label(ask_user_frame, text="Which type of messages would you like to recieve?", bg=window_bg, font=standard_info_font)   
          ask_label.grid(row=0)
          ask_user_frame.grid(row=0, pady=60)

          checkbox_frame = Frame(window, bg=window_bg)
          mental_button = Checkbutton(checkbox_frame, text="Mental health", variable=user_opt_mental, onvalue=1, offvalue=0, 
                                          font=standard_info_font, bg=window_bg, height=4, bd=5)
          physical_button = Checkbutton(checkbox_frame, text="Physical health", variable=user_opt_physical, onvalue=1, offvalue=0, 
                                            font=standard_info_font, bg=window_bg, height=4, bd=5)
          mental_button.grid(row=0, column=0, padx= 15)
          physical_button.grid(row=0, column=1)
          checkbox_frame.grid(row=1, pady=30)

          text_button = Frame(window, bg=window_bg)
          button_font = ('Arial 16')
          random_texts_button = Button(text_button, text="Confirm Settings", command=random_text_user, width=20, height=2, font=button_font)
          random_texts_button.grid(row=0)
          text_button.grid(row=2)

         
def thread_helper(time_to_sleep):
    if(user_opt_mental.get() == 0 and user_opt_physical.get() == 0):
        return
    messages_to_send = []
    if(user_opt_mental.get() == 1):
        messages_to_send.append(random.choice(quotesData.values.tolist()))
    if(user_opt_physical.get() == 1):
          messages_to_send.extend(questionsData)
    while not window_quit_flag.is_set():
        message_to_send = random.choice(messages_to_send)
        message = client.messages.create(
            to ="+1" + number.get(),
            from_ = twilio_number,
            body = message_to_send
        )
        print(message.account_sid)
        for i in range(time_to_sleep):
            time.sleep(1)
            if window_quit_flag.is_set():
                return
        

def ask_user_for_daily_frequency():
    for widget in window.winfo_children():
        widget.destroy()


    width, height = window.winfo_width(), window.winfo_height()
    ask_user_frame = Frame(window, bg=window_bg)
    ask_label = Label(ask_user_frame, text="How frequent would you like to recieve messages?", bg=window_bg, font=standard_info_font,
                      wraplength=width*3/5)   
    ask_label.pack(pady=20)

    # create the radio buttons and associate each with a value
    low_rb = Radiobutton(ask_user_frame, text="Low", variable=frequency_level, value="Low", bg="lightblue", font=standard_info_font)
    low_rb.pack()

    moderate_rb = Radiobutton(ask_user_frame, text="Moderate", variable=frequency_level, value="Moderate", bg="lightblue", font=standard_info_font)
    moderate_rb.pack()

    high_rb = Radiobutton(ask_user_frame, text="High", variable=frequency_level, value="High", bg="lightblue", font=standard_info_font)
    high_rb.pack()

    # pack the frame to add it to the window
    ask_user_frame.pack(pady=60)

    button_frame = Frame(ask_user_frame, bg=window_bg)
    button_font = ('Arial 16')
    confirm_button = Button(button_frame, text="Confirm", command=confirm_user_frequency, width=20, height=2, font=button_font)
    confirm_button.pack(pady=30)
    button_frame.pack()

def confirm_user_frequency():
    # for demo purposes
     time_to_wait = 0
     if "Low" in frequency_level.get():
            time_to_wait = 60
     elif "Moderate" in frequency_level.get():
            time_to_wait = 30
     elif "High" in frequency_level.get():
            time_to_wait = 15
     else:
            time_to_wait = 60

     thread = Thread(target=thread_helper, args=(time_to_wait,))
     thread.start()
    

     user_home_screen()

def window_quit():
    window_quit_flag.set()
    window.destroy()

def main():
    create_window()



if __name__ == "__main__":
    main()
