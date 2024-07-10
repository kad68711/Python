import requests
from bs4 import BeautifulSoup


def get_date():
    global date

    date = input(
        "nan ne ii desu ka sono yori YYYY-MM-DD haite imasu:  ")

    return date


def get_song_list():

    URL = f"https://www.billboard.com/charts/hot-100/{date}"

    response = requests.get(url=URL)

    soup = BeautifulSoup(response.text, "html.parser")

    song_names = soup.select("li ul li h3", id="title-of-a-story")

    artist_names = soup.select(
        selector="li ul li span", class_="c-label  a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only ")
    print(artist_names)

    song_list = []
    for song in song_names:
        song_list.append(song.getText().strip())

    artist_list = []
    for artist in artist_names:
        try:
            int(artist.getText())
        except:
            if artist.getText() != "\n\t\n\t-\n":
                artist_list.append(artist.getText().strip())

    list_with_song_and_artist = []

    for i in range(len(artist_list)):
        s_name = song_list[i]
        a_name = artist_list[i]
        both = [s_name, a_name]
        list_with_song_and_artist.append(both)

    print(list_with_song_and_artist)

    return list_with_song_and_artist
