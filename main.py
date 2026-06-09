from themoviedb import TMDb
import tkinter as tk

def discover_movie():
    T.delete("1.0", tk.END)
    tmdb = TMDb()
    movies = tmdb.discover().movie(    
        sort_by="vote_average.desc",
        primary_release_date__gte="1997-08-15",
        vote_count__gte=10000,
        vote_average__gte=6.0,
    )
    for movie in movies:
        T.insert(tk.END,         
        f"{movie.title} ({movie.year})\nIMDb: {movie.vote_average} ({movie.vote_count})\n\n"
        )

def search_movie():
    T.delete("1.0", tk.END)
    tmdb = TMDb()
    query = search_entry.get()
    movies = tmdb.search().movies(query)
    for i in movies:
        movie = tmdb.movie(i.id).details()
        T.insert(tk.END,         
        f"{movie.title} | {movie.year} | Rating: {movie.vote_average} | Votes: {movie.vote_count}\n"
        )
    search_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Movie Search Bar")

T = tk.Text(root, width=75, height=15)
T.pack()

search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var, font=("Arial", 12))
search_entry.pack(side=tk.TOP)

# suggestion_list = tk.Listbox(root, font=("Arial", 12))
# suggestion_list.pack()

button_quit = tk.Button(root, text="Quit", command=root.destroy)
button_quit.pack(side=tk.BOTTOM)

button_discover = tk.Button(root, text="Discover Movies", command=discover_movie)
button_discover.pack(side=tk.BOTTOM)

button_search = tk.Button(root, text="Search Movie", command=search_movie)
button_search.pack(side=tk.TOP)

tk.mainloop()
