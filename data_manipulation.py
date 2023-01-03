import pickle
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class filmObj:
    def __init__(self):
        #film info
        self.slug = ""
        self.name = ""
        self.release = 0
        self.genre = []
        self.theme = []

        # personal info
        self.year = 0
        self.month = ""
        self.day = 0
        self.dir = ""
        self.liked = False
        self.rating = 0
        self.date= 0
        self.username = ''

class yourData:
    def __init__(self):
        self.movieDay = 0
        self.numMovieDay = 0
        self.username = ''


with open('my_list.pickle', 'rb') as f:
    # use pickle module to deserialize list
    myFilms = pickle.load(f)

tupFilms = []
for _ in myFilms:
    temp = []
    temp.extend([_.name, _.slug, _.dir, _.release, _.year, _.date])
    tupFilms.append(temp)


film_df = pd.DataFrame(tupFilms, columns=['name', 'slug', 'director', 'release year', 'year watched', 'date watched'])
#film_df.set_index('name', inplace=True)


#dir_counts = film_df['name'].value_counts()
#print(dir_counts.head(10))

nicole = yourData()

yo_df = film_df['date watched'].value_counts()
#print(yo_df.head(1))
nicole.movieDay = yo_df.index[0]
nicole.numMovieDay = yo_df.iloc[0]
nicole.username = myFilms[0].username

print(nicole.username, "on", nicole.movieDay.strftime('%Y-%m-%d'), 'you watched', nicole.numMovieDay, 'movies' )