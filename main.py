from themoviedb import TMDb
import tkinter as tk
from tkinter import Menu, ttk

#Delete all entries in the table
def reset_all(T):
    for item in T.get_children():
        T.delete(item)

#Create GUI
def create_menu(parent, T):
    menu = Menu(parent)
    parent.config(menu=menu)
    browse_menu = Menu(menu)
    menu.add_cascade(label="Browse", menu=browse_menu, font=("Arial", 10))
    browse_menu.add_command(label="Discover", command=lambda: discover_movie(T))
    browse_menu.add_command(label="Trending Movies", command=lambda: discover_movie(T))
    browse_menu.add_command(label="Top List", command=lambda: discover_movie(T))

    quit_menu = Menu(menu)
    menu.add_cascade(label="Exit", menu=quit_menu, font=("Arial", 10))
    quit_menu.add_command(label="Quit", command=parent.quit)

def create_top_frame(parent, T):
    top_frame = tk.Frame(parent)
    top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    top_frame.grid_columnconfigure(0, weight=1)

    search_frame = tk.Frame(top_frame)
    search_frame.grid(row=0, column=0, sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    action_frame = tk.Frame(top_frame)
    action_frame.grid(row=0, column=1, sticky="e")

    filter_frame = tk.Frame(top_frame)
    filter_frame.grid(row=1, column=0, sticky="w", columnspan=2, pady=2)   

    custom_font = ("Arial", 12)

    search_label = tk.Label(search_frame, text="Search: ", font=custom_font)
    search_label.grid(row=0, column=0, sticky="w")

    search_var = tk.StringVar()

    search_entry = tk.Entry(search_frame, textvariable=search_var, font=custom_font, width=25)
    search_entry.grid(row=0, column=1, sticky="we", padx=(0, 10))

    search_button = tk.Button(action_frame, text="Search", font=custom_font, command=lambda:search_movie(search_entry, T))
    search_button.grid(row=0, column=0, sticky="we", padx=10, ipadx=12)

    reset_button = tk.Button(action_frame, text="Reset", font=custom_font, command=lambda:reset_all(T))
    reset_button.grid(row=0, column=1, sticky="we", padx=7, ipadx=12)

    genre_label = ttk.Label(filter_frame, text="Genre:", font=custom_font)
    genre_label.grid(row=0, column=0, padx=(0, 12), pady=7, sticky="w")

    genre_combobox = ttk.Combobox(
        filter_frame, 
        width=10,
        values=["Action", "Adventure", "Komödie", "Drama", "Thriller", "Horror", "Sci-Fi", "Fantasy", "Romantik", "Krimi", "Western", "Mystery", "Biografie", "Historie", "Musical", "Doku", "Animation", "Family", "Krieg", "Sport"], 
        state="readonly",
        font=custom_font)
    genre_combobox.set("")
    genre_combobox.grid(row=0, column=1, padx=(0, 30), pady=7, sticky="w")

    year_label = ttk.Label(filter_frame, text="Year:", font=custom_font)
    year_label.grid(row=0, column=2, padx=(0, 6), pady=7, sticky="w")

    year_spinbox = ttk.Spinbox(filter_frame, width=7, from_=1950, to=2026, font=custom_font)
    year_spinbox.grid(row=0, column=3, padx=(0, 30), pady=7, ipady=2, sticky="w")

    rating_label = ttk.Label(filter_frame, text="Min. Rating:", font=custom_font)
    rating_label.grid(row=0, column=4, padx=(0, 6), pady=7, sticky="w")

    rating_combobox = ttk.Combobox(
        filter_frame, 
        width=2,
        values=[i for i in range(1, 11)], 
        state="readonly",
        font=custom_font)
    rating_combobox.set("")
    rating_combobox.grid(row=0, column=5, padx=(0, 0), pady=7, sticky="w")

def create_table(parent):
    T = ttk.Treeview(parent, columns=("Year", "Rating", "Count"))
    T.heading("#0", text="Title")
    T.heading("Year", text="Year", anchor="center")
    T.heading("Rating", text="Rating", anchor="center")
    T.heading("Count", text="Count", anchor="center")

    T.column("#0", width=300)
    T.column("Year", width=60, anchor="center")
    T.column("Rating", width=60, anchor="center")
    T.column("Count", width=60, anchor="center")

    T.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    return T

#Discover trending movies
def discover_movie(T):
    reset_all(T)
    tmdb = TMDb()
    movies = tmdb.discover().movie(    
        sort_by="vote_average.desc",
        # primary_release_date__gte="1997-08-15",
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
    reset_all(T)
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
    root.resizable(False, False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)

    T = create_table(root)
    create_menu(root, T)
    create_top_frame(root, T)
    
    root.mainloop()

if __name__ == "__main__":
    main()





