from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import pandas as pd

#Data Store

names = []
years = []
imdb_ratings = []
metascores = []
votes = []
grosses = []

#URL's parameters

pages_url = [str(i) for i in range(1, 5)]
years_url = [str(i) for i in range(2017, 2018)]

#Monitoring of the loop
start_time = time()
requests = 0

#Loop 2000 - 2017
for year_url in years_url:
    
    #Loop Page1 - 4
    for page_url in pages_url:
        
        #Make a request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url +'&sort=num_votes,desc&page=' + page_url)

        #Pause the loop
        sleep(randint(8,15))

        #Monitor the Requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request: {}; Frequency: {} request/s'.format(requests,requests/elapsed_time))
        clear_output(wait = True)

        #Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
        
        #Break the loop
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break
        
        #Parse the content of the request with BeautifulSoup
        html_soup = BeautifulSoup(response.text, 'html.parser')

        #Select all the 50 movie containers from a single page
        movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

        #For every movie of these 50
        for container in movie_containers:
            if container.find('span', class_='metascore') != None:
                #Movie_name
                name = container.h3.a.text
                names.append(name)
                #Movie_year
                year = container.find('span', class_='lister-item-year text-muted unbold').text
                years.append(year)

                #imdbRate
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                #Metascore
                metascore = int(container.find('span', class_='metascore').text.strip())
                metascores.append(metascore)

                #vote
                V_mod = container.find('span', attrs={'name': 'nv'})
                vote = container.find('span', attrs={'name': 'nv'})['data-value']
                votes.append(vote)

                #gross
                gross = V_mod.find_next_siblings('span', attrs={'name': 'nv'})
                grosses.append(gross)
            else:
                #Movie_name
                name = container.h3.a.text
                names.append(name)
                #Movie_year
                year = container.find(
                    'span', class_='lister-item-year text-muted unbold').text
                years.append(year)

                #imdbRate
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                #Metascore
                metascore = 'N/A'
                metascores.append(metascore)

                #vote
                V_mod = container.find('span', attrs={'name': 'nv'})
                vote = container.find('span', attrs={'name': 'nv'})['data-value']
                votes.append(vote)

                #gross
                gross = 'N/A'
                grosses.append(gross)
            
            
movie_ratings = pd.DataFrame({'movie': names,
                              'year': years,
                        'imdb': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes,
                        'gross':grosses})
print(movie_ratings.info())