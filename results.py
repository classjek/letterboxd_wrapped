import requests, sys, webbrowser, bs4
import pickle
from datetime import datetime

class filmObj:
    def __init__(self):
        #film info
        self.slug = ""
        self.name = ""
        self.dir = ""
        self.release = 0
        self.genre = []
        self.theme = []

        # personal info
        self.year = 0
        self.month = ""
        self.day = 0
        self.reviewed = False
        self.liked = False
        self.rating = 0
        self.date = 0
        self.username = ''


if len(sys.argv[1]) < 1:
    print('no username given')
else:
    username = sys.argv[1]


webLink = 'https://letterboxd.com/' + username + '/films/'

def month_to_num(month):
    if month == 'Jan':
        return 1
    if month == 'Feb':
        return 2
    if month == 'Mar':
        return 3
    if month == 'Apr':
        return 4
    if month == 'May':
        return 5
    if month == 'Jun':
        return 6
    if month == 'Jul':
        return 7
    if month == 'Aug':
        return 8
    if month == 'Sep':
        return 9
    if month == 'Oct':
        return 10
    if month == 'Nov':
        return 11
    if month == 'Dec':
        return 12


def getGenres2(webLink, filmObj):

    res = requests.get(webLink)
    filmPage = bs4.BeautifulSoup(res.text, 'html.parser')

    # get genres and themes
    genres = filmPage.find_all(id="tab-genres")
    genThem = genres[0].find_all("p")

    genre = genThem[0].find_all('a')
    for _ in genre:
        genreL = _['href'].split('/')
        filmObj.genre.append(genreL[3])

    theme = genThem[1].find_all('a')
    for _ in theme:
        themeL = _['href'].split('/')
        if themeL[3] != "themes":
            filmObj.theme.append(themeL[3])
    
    #get name, year, director
    header = filmPage.find_all(id="featured-film-header")
    # get that name
    name = header[0].find("h1")
    filmObj.name = (name.text)
    # get that release year
    year = header[0].find('a')
    filmObj.year = year.text
    # get that Director
    dir = header[0].find("span")
    filmObj.dir = dir.text



def getGenres(slug, filmObj):
    
    webLink = 'https://letterboxd.com/' + slug
    res = requests.get(webLink)
    filmPage = bs4.BeautifulSoup(res.text, 'html.parser')

    # get genres and themes
    genres = filmPage.find_all(id="tab-genres")

    if len(genres) > 0:
        genThem = genres[0].find_all("p")

        genre = genThem[0].find_all('a')
        for _ in genre:
            genreL = _['href'].split('/')
            filmObj.genre.append(genreL[3])

        if len(genThem) >= 2:
            theme = genThem[1].find_all('a')
            for _ in theme:
                themeL = _['href'].split('/')
                if themeL[3] != "themes":
                    filmObj.theme.append(themeL[3])

    
    #get director
    header = filmPage.find_all(id="featured-film-header")
    # get that Director
    dir = header[0].find("span")
    filmObj.dir = dir.text



def getFilms(page):
    filmList = []


    webLink = 'https://letterboxd.com/' + page
    
    #try to access webLink
    try:
        res = requests.get(webLink)     
    except requests.exceptions.RequestException as e:
        print(f'There was an error: {e}')
        return

    diaryP = bs4.BeautifulSoup(res.text, 'html.parser')
    films = diaryP.find_all("tr")

    month = ""
    year = ""
    
    # create a film object for each row 
    for row in films[1:]:
        temp = filmObj()
        temp.username= page[:-13]

        #get the month and year
        date = row.find(class_="date")
        if type(date) != bs4.element.Tag: #if no month or year is listed, pull from previous 
            temp.month = month
            temp.year = year
            temp.date = datetime(int(year), month_to_num(month), 1)
        else:
            # get month
            mon = date.find("a")
            temp.month = mon.text
            month = mon.text
            # get day 
            yo = date.find("small")
            temp.year = yo.text
            year = yo.text
            temp.date = datetime(int(year), month_to_num(month), 1)

        #get day watched
        date2 = row.find(class_="td-day diary-day center")
        day = date2.find('a')
        temp.day = day.text
        temp.date = temp.date.replace(day = int(day.text))


        # get name, slug
        filmDetails = row.find(class_="td-film-details")
        details = filmDetails.find("div")
        temp.slug = details['data-film-slug']
        name = filmDetails.find('a')
        temp.name = name.text

        # get release year 
        releasedCenter = row.find(class_="td-released center")
        releaseYr = releasedCenter.find('span')
        temp.release = releaseYr.text


        # get rating and liked
        # rating
        ratingGreen = row.find(class_="td-rating rating-green")
        rating = ratingGreen.find('span')
        temp.rating = rating.text.count('★') + 0.5*(rating.text.count('½'))
        # liked
        diaryLike = row.find(class_="td-like center diary-like")
        liked = diaryLike.find_all('span')
        if len(liked) == 3:
            temp.liked = True

        getGenres(temp.slug, temp)

        filmList.append(temp)
    return filmList


exampleSlug = 'film/the-power-of-the-dog/'
webLink = 'https://letterboxd.com/' + exampleSlug

#getGenres(webLink, powerD)

page = username + '/films/diary/'
myFilms = getFilms(page)

for n in range(2,6):
    page = username + '/films/diary/page/' + str(n) + '/'
    moreFilms = getFilms(page)
    if len(moreFilms) == 0:
        break
    else:
        myFilms = myFilms + moreFilms


with open('my_list.pickle', 'wb') as f:
    #use pickle to serialize my list
    pickle.dump(myFilms, f)
