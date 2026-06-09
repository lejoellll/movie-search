from themoviedb import TMDb
import tkinter as tk
from tkinter import Menu, ttk

#Create GUI
def create_menu(parent, T):
    menu = Menu(parent)
    parent.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="Options", menu=filemenu, font=("Arial", 10))
    filemenu.add_command(label="Discover Movies", command=lambda: discover_movie(T))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=parent.quit)

def create_top_frame(parent, T):
    top_frame = tk.Frame(parent)
    top_frame.grid()
    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var, font=("Arial", 10))
    search_entry.grid(row=0, column=0, padx=7)
    button_search = tk.Button(top_frame, text="Search Movie", font=("Arial", 10), command=lambda:search_movie(search_entry, T))
    button_search.grid(row=0, column=1, padx=10)

    return search_entry, button_search

def create_table(parent):
    T = ttk.Treeview(parent, columns=("Column1", "Column2", "Column3"))
    T.heading("#0", text="Title")
    T.heading("Column1", text="Year", anchor="center")
    T.heading("Column2", text="Rating")
    T.heading("Column3", text="Count")

    T.column("#0", width=300)
    T.column("Column1", width=60)
    T.column("Column2", width=60)
    T.column("Column3", width=60)

    T.grid()
    return T

#Discover trending movies
def discover_movie(T):
    for item in T.get_children():
        T.delete(item)
    tmdb = TMDb()
    movies = tmdb.discover().movie(    
        sort_by="vote_average.desc",
        primary_release_date__gte="1997-08-15",
        vote_count__gte=10000,
        vote_average__gte=6.0,
    )
    for movie in movies:
        T.insert(
            "", 
            tk.END, 
            text=(movie.title), 
            values=(movie.year, movie.vote_average, movie.vote_count)
            )

#Search for specific movies
def search_movie(entry, T):
    for item in T.get_children():
        T.delete(item)
    tmdb = TMDb()
    query = entry.get()
    results = tmdb.search().movies(query)
    for item in results:
        movie = tmdb.movie(item.id).details()
        T.insert(
            "", 
            tk.END, 
            text=(movie.title), 
            values=(movie.year, movie.vote_average, movie.vote_count)
            )
    entry.delete(0, tk.END)

#main
def main():
    root = tk.Tk()
    root.title("Movie Search")
    root.geometry()

    T = create_table(root)
    create_menu(root, T)
    create_top_frame(root, T)
    
    tk.mainloop()

if __name__ == "__main__":
    main()





