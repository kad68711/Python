import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"


response=requests.get(url=URL)

soup=BeautifulSoup(markup=response.text,features="html.parser")

h3_tags=soup.find_all("h3","title")

movie_list=[]
for tag in h3_tags:
    name_with_number=tag.getText()
    movie_list.append(name_with_number)

with open("movies.txt","w",encoding="utf-8") as f:
    for movie in movie_list[::-1]:
        f.write(movie)
        f.write("\n")
    
    



