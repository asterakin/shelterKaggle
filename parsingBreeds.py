__author__ = 'Stella'

import pandas as pd
from bs4 import BeautifulSoup
import requests
'''
breedGroupMap = {}

url = "https://en.wikipedia.org/wiki/Herding_Group"
# herding group
url = "https://en.wikipedia.org/wiki/Herding_Group"
skip = 2
tableLocation = 0
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[tableLocation]
tds = table.find_all('td')

group ='herding'
herdGroup = []
counter = 0
for td in tds:
    counter = counter + 1
    if counter%skip == 0 :
        a = td.find_all('a')[0]
        breed = a.get_text()
        print(breed)
        herdGroup.append(breed)
        breedGroupMap[breed]=group
    else:
        continue


# sporting group
url = "https://en.wikipedia.org/wiki/Sporting_Group"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[0]
tds = table.find_all('td')
group = 'sport'
temp_sport=[]
counter = 0
for td in tds:
    counter = counter + 1
    if counter%2 == 0 :
        a = td.find_all('a')[0]
        breed = a.get_text()
        temp_sport.append( breed)
        print(breed)
        breedGroupMap[breed]=group
    else:
        continue


# sporting group
url = "https://en.wikipedia.org/wiki/Hound"
group = 'hound'
tableLocation = 2
skip = 2
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[tableLocation]
tds = table.find_all('td')

houndgroup=[]
counter = 0
for td in tds:
    counter = counter + 1
    if counter%skip == 0 :
        a = td.find_all('a')[0]
        breed = a.get_text()
        houndgroup.append( breed)
        print(breed)
        breedGroupMap[breed]=group
    else:
        continue


# working
url = "https://en.wikipedia.org/wiki/Working_Group_(dogs)"
group = 'working'
tableLocation = 0
skip = 1
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[tableLocation]
tds = table.find_all('td')

workgroup=[]
counter = 0
for td in tds:
    counter = counter + 1
    if counter%skip == 0 :
        a = td.find_all('a')
        if a!=[]:
            breed = a[0].get_text()
            workgroup.append( breed)
            print(breed)
            breedGroupMap[breed]=group
    else:
        continue


# toy group
url = "https://en.wikipedia.org/wiki/Toy_Group"
group = 'toy'
tableLocation = 0
skip = 1
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[tableLocation]
tds = table.find_all('td')

toygroup=[]
counter = 0
for td in tds:
    counter = counter + 1
    if counter%skip == 0 :
        a = td.find_all('a')
        if a!=[]:
            breed = a[0].get_text()
            toygroup.append( breed)
            print(breed)
            breedGroupMap[breed]=group
    else:
        continue


url = 'https://en.wikipedia.org/wiki/Terrier_Group'
group = 'terrier'
terriergroup=[]
tableLocation = 0
skip = 1
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
table = soup.find_all('table')[tableLocation]
tds = table.find_all('td')

counter = 0
for td in tds:
    counter = counter + 1
    if counter%skip == 0 :
        a = td.find_all('a')
        if a!=[]:
            breed = a[0].get_text()
            terriergroup.append(breed)
            print(breed)
            breedGroupMap[breed]=group
    else:
        continue '''




breedGroupMap = {}

# herding
url = "https://en.wikipedia.org/wiki/Herding_Group"
tableLocation = 0
groupName = 'herding'
tableLocation = 0
skip = 2
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)


# sporting group
url = "https://en.wikipedia.org/wiki/Hound"
groupName = 'hound'
tableLocation = 2
skip = 2
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)


url = "https://en.wikipedia.org/wiki/Toy_Group"
groupName = 'toy'
tableLocation = 0
skip = 1
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)


url = "https://en.wikipedia.org/wiki/Working_Group_(dogs)"
groupName = 'working'
tableLocation = 0
skip = 1
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)


url = 'https://en.wikipedia.org/wiki/Terrier_Group'
groupName = 'terrier'
terriergroup=[]
tableLocation = 0
skip = 1
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)


url = 'https://en.wikipedia.org/wiki/Sporting_Group'
tableLocation = 0
skip = 2
groupName = 'sport'
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)


url = 'https://en.wikipedia.org/wiki/Non-Sporting_Group'
tableLocation = 0
skip = 2
groupName = 'nonsport'
parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName)



def parseBreedToGroup (url,skip,tableLocation,breedGroupMap,groupName):
    group=[]
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    table = soup.find_all('table')[tableLocation]
    tds = table.find_all('td')

    counter = 0
    for td in tds:
        counter = counter + 1
        if counter%skip == 0 :
            a = td.find_all('a')
            if a!=[]:
                breed = a[0].get_text()
                group.append(breed)
                print(breed)
                breedGroupMap[breed]=groupName
        else:
            continue

    return breedGroupMap