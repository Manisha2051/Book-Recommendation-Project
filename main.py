import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pickle as pk
import pandas as pd
import requests
from io import BytesIO

# Load data and models
similar_books = pk.load(open('Similar_books.pkl', 'rb'))
books = pd.read_csv(r'C:\Users\rajve\Downloads\books_1.Best_Books_Ever.csv.zip')

def recommend(book_name):
    try:
        index = books[books['title'] == book_name].index[0]  # Get the index value
        similar_books_with_index = list(enumerate(similar_books[index]))
        our_books = sorted(similar_books_with_index, reverse=True, key=lambda x: x[1])[1:6]
        temp = []
        imgs = []
        ratings = []
        publish_dates = []
        
        for idx, _ in our_books:
            temp.append(books.iloc[idx]['title'])
            imgs.append(books.iloc[idx]['coverImg'])
            ratings.append(books.iloc[idx]['rating'])  # Fetch the rating
            publish_dates.append(books.iloc[idx]['publishDate'])  # Fetch the publish date

        for i in range(5):
            # Fetch image from URL
            response = requests.get(imgs[i])
            img_data = response.content
            image = Image.open(BytesIO(img_data)).resize((150, 210))
            image_tk = ImageTk.PhotoImage(image)  # Create a PhotoImage object
            texts[i].config(text=temp[i])
            images[i].config(image=image_tk)
            images[i].image = image_tk  # Keep a reference to avoid garbage collection
            
            # Set Rating and Publish Date
            ratings_texts[i].config(text=f"Rating: {ratings[i]}")
            publish_dates_texts[i].config(text=f"Published: {publish_dates[i]}")
            
    except IndexError:
        messagebox.showwarning("Book Not Found", "The book you searched for is not available.")

def search():
    title = Search.get()
    recommend(title)

def show_menu(event):
    # Display the menu at the mouse position
    menu.post(event.x_root, event.y_root)

root = tk.Tk()
root.title("Book Recommendation System")
root.geometry("1250x700+200+100")
root.config(bg="#4D5656")

# Icon
path = r"C:\Users\rajve\OneDrive\Desktop\Book Recommendation\_icon_image.jpg"
load = Image.open(path)
render = ImageTk.PhotoImage(load)
root.iconphoto(False, render)

# Background image
image = Image.open(r"C:\Users\rajve\OneDrive\Desktop\Book Recommendation\book_image.jpg").resize((1850, 430))
image = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=image)
image_label.pack()
image_label.place(x=0, y=0)

# Heading
heading = Label(root, text="BOOK RECOMMENDATION SYSTEM", font=("Cascadia Code", 30, "bold"), fg="white", bg="black")
heading.place(x=550, y=60)

# Entry box / search section
Search = StringVar()
search_entry = Entry(root, textvariable=Search, width=30, font=("Comic Sans MS", 25), bg="white", fg="black", bd=0)
search_entry.place(x=550, y=172)

# Search Button
Search_Button = tk.Button(root, text="Search", font=("Cooper", 15, "bold"), fg="white", bg="black",
                          borderwidth=5, relief="groove", command=search)
Search_Button.place(x=1070, y=172)

# Setting button
Setting_Button = tk.Button(root, text="Setting", font=("Cooper", 12, "bold"), fg="black", bg="white",
                           borderwidth=2, relief="groove")
Setting_Button.place(x=50, y=30)
Setting_Button.bind('<Button-1>', show_menu)

menu = Menu(root, tearoff=0)  # Menu for search button
check_var = BooleanVar()
menu.add_checkbutton(label="Publish Date", variable=check_var, command=lambda: print(f"Publish Date checked: {check_var.get()}"))

check_var2 = BooleanVar()
menu.add_checkbutton(label="Rating", variable=check_var2, command=lambda: print(f"Rating checked: {check_var2.get()}"))

# Logout button
new_win = tk.Button(root, text="LOGOUT", font=("Cooper", 12, "bold"), fg="black", bg="white", borderwidth=2, relief="groove")
new_win.place(x=1400, y=30)

# Frames for book recommendations
frames = []
texts = []
images = []
rating_frames = []
ratings_texts = []
publish_date_frames = []
publish_dates_texts = []

# Create frames for books, ratings, and publish dates
for i in range(5):
    frame = Frame(root, width=150, height=240, bg="black")   #bg="white"
    frame.place(x=260 + i * 200, y=450)
    frames.append(frame)

    text = Label(frame, text="Book Title", font=("Comic Sans MS", 9), bg="black", fg="white")
    text.place(x=10, y=4)
    texts.append(text)

    image_label = Label(frame)
    image_label.place(x=3, y=30)
    images.append(image_label)

    # Rating Frame
    rating_frame = Frame(root, width=150, height=30, bg="black")
    rating_frame.place(x=260 + i * 200, y=700)
    rating_frames.append(rating_frame)
    
    rating_label = Label(rating_frame, text="Rating: ", font=("Comic Sans MS", 8), bg="black", fg="white")
    rating_label.pack()
    ratings_texts.append(rating_label)
    
    # Publish Date Frame
    publish_date_frame = Frame(root, width=150, height=30, bg="black")
    publish_date_frame.place(x=260 + i * 200, y=740)
    publish_date_frames.append(publish_date_frame)

    publish_date_label = Label(publish_date_frame, text="Published: ", font=("Comic Sans MS", 8), bg="black", fg="white")
    publish_date_label.pack()
    publish_dates_texts.append(publish_date_label)

root.mainloop()

