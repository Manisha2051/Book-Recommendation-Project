import pickle as pk
import pandas as pd
from nltk.stem import PorterStemmer
    
similar_books = pk.load(open('Similar_books.pkl','rb'))

porter_stemmer = PorterStemmer()
books = pd.read_csv(r'C:\Users\rajve\Downloads\books_1.Best_Books_Ever.csv.zip')

def recommend(book_name):
    index = books[books['title']==book_name].index
    similar_books_with_index = list(enumerate(similar_books[index][0]))
    our_books = sorted(similar_books_with_index,reverse=True,key=lambda x:x[1])[1:6]
    for index,_ in our_books:
        print(books.iloc[index]['title'])

# title = input('Enter title : ')

recommend('The Hunger Games')