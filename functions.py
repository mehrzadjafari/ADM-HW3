#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import lxml
import csv
import re
import os
from langdetect import detect



def info_parser(parent_dir, pages = 300, tsv_articles = "tsv_articles" , links = "Links", url = "url"):


    """Extracts books information, check them with langdetect and creates the .tsv files in /tsv_articles.
	All the files and sub-folders (i.e. tsv_folder, links and url.txt) should be stored in parent_dir.

    Args:

	parent_dir (string) : The main path of your working enviorment. All of the folders and files should be here. Example : C:/Users/Desktop/ALGORITHMIC METHODS OF DATA MINING AND LABORATORY/"
        pages (int, optional): Number of pages to parse. Defaults to 300.
	tsv_articles (string, optional) : The name of the folder you are willing to store the .tsv files. Defaults to "tsv_articles"
	links (string, optional) : The name of the main folder you have stored your html files. Defaults to "Links"
	Urls (string, optional) : The name of the text file you have stored your html urls. Defaults to "url"

    Returns:
        .tsv files named article_i.tsv (for each i book in the parent folder)
    """
    
    
    f = open(url + ".txt", "r")
    lines = f.readlines()
    f.close()
    

    tsv_folder = "/" + tsv_articles
    out_path = parent_dir + tsv_folder
    os.makedirs(out_path)
    
    
    
    for j in range(pages):
        
        n = j
        directory = 'Page_' + str(n + 1)
    


    
        for i in range(100):

            Url = lines[i][:-1]
            
            m = i

            file_name = "article_" + str(i+1) + ".html"
            myfile = parent_dir + "/" + links + "/" + directory + "/" + file_name
            soup = BeautifulSoup(open(myfile, 'r', encoding="utf8"), features='lxml')
            
    



            #Book Title
            bookTitle = str(soup.find_all('h1', id = "bookTitle")[0].contents[0]).replace('\n', '').strip()


            lst = soup.find_all('div', {"class": "infoBoxRowTitle"})
            #Book Series
            series_index = False
            for stri in lst:
                if 'Series' in stri:
                    series_index = lst.index(stri)

            bookSeries = ""

            if series_index:

                        bookSeries += str(soup.find_all('div', {"class": "infoBoxRowItem"})[series_index].contents[1]).strip().split(">")[1][:-3]



            #Book Authors
            bookAuthors = str(soup.find_all('a', {"class": "authorName"})[0].contents[0].contents[0])

            #Rating Value
            ratingValue = soup.find_all('span', itemprop = "ratingValue")[0].contents[0].replace('\n', '')

            #Rating Counts
            ratingCount = soup.find_all('a', href="#other_reviews")[0].contents[2].replace('\n', '').strip().split()[0]

            #Review Counts
            reviewCount = soup.find_all('a', href="#other_reviews")[1].contents[2].replace('\n', '').strip().split()[0]



            #Plot

            #first of all, define the full description 
            #(which may contain italics, bolds and preliminar descriptions not related to the plot)
            if len(soup.find_all('div', id="description")[0].contents) <= 3:
                full_descr = soup.find_all('div', id="description")[0].contents[1].contents
            else :
                full_descr = soup.find_all('div', id="description")[0].contents[3].contents

            #if the description begins with this kind of description, remove it
            if len(soup.find_all('div', id="description")[0].contents) > 3 :
                if len(soup.find_all('div', id="description")[0].contents[3].contents) > 2:
                    if "<i>" in str(full_descr[0]):

                        full_descr = full_descr[3:]

            #for every line of the description, add to the list Plot all of the lines except the ones corresponding to the <br/> tags 
            Plot = []

            for q in range(len(full_descr)):
                if str(full_descr[q]) != '<br/>':
                    Plot.append(full_descr[q])


            #for every line of the plot, remove the <i> and </i> tags
            for w in range(len(Plot)):
                if '<i>' in str(Plot[w]):
                    Plot[w] = re.sub(r'<i>', '', str(Plot[w]))
                    Plot[w] = re.sub(r'</i>', '', str(Plot[w]))

            #if the plot begins in bold, remove the <b> tags
            if "<b>" in str(Plot[0]):
                Plot[0] = Plot[0].contents[0]
            
            for u in range(len(Plot)):
                Plot[u] = str(Plot[u])
                
                
            Plot = " ".join(Plot)

            if Plot == [] :
                
                Plot = ""

            #Number of Pages
            NumberofPages = soup.find_all('span', itemprop="numberOfPages")[0].contents[0]

            #Published
            Published = soup.find_all('div', {"class": "row"})[1].contents[0].replace('\n', '').strip().split(" "*8)[1]






            #Finding the position of Characters in "InfoBox" whether it exists or not
            character_index = False

            for stri in lst:
                if 'Characters' in stri:
                    character_index = lst.index(stri)

            #Initiating the characters list
            characters = []

            #If character exists, we will find them up to 5 characters.
            if character_index:

                if int(len(soup.find_all('div', {"class": "infoBoxRowItem"})[character_index].contents)/2) <= 5 :
                    for e in range(int(len(soup.find_all('div', {"class": "infoBoxRowItem"})[character_index].contents)/2)):

                        #Using 2i+1 as each character is on odd index contents
                        characters.append(str(soup.find_all('div', {"class": "infoBoxRowItem"})[character_index].contents[2*e+1]).strip().split(">")[1][:-3])
                else:
                    for e in range(5):
                        characters.append(str(soup.find_all('div', {"class": "infoBoxRowItem"})[character_index].contents[2*e+1]).strip().split(">")[1][:-3])

                characters = ", ".join(characters)

            else :
                characters = ""


            #Setting
            setting = []

            #Finding the index of Setting whether it exists or not !
            setting_index = 0
            for stril in lst:
                if 'Setting' in stril:
                    setting_index = lst.index(stril)

            #Same approach as for characters
            if setting_index > 0:

                for r in range(2):

                    if "</s" in str(soup.find_all('div', {"class": "infoBoxRowItem"})[setting_index].contents[2*r+1]) :
                        temp = re.sub(r'</s', '', str(soup.find_all('div', {"class": "infoBoxRowItem"})[setting_index].contents[2*r+1]))
                        setting.append((str(temp).strip().split(">")[1][:-3]).strip())

                    else:

                        setting.append(str(soup.find_all('div', {"class": "infoBoxRowItem"})[setting_index].contents[2*r+1]).strip().split(">")[1][:-3])




                setting = " ".join(setting)

            else :
                setting = ""


            if detect(Plot) == 'en': 
                
                article_n = str(n*100 + (m + 1))
                out_path_tsv = out_path + "/" + "article_" + article_n + ".tsv"

                with open(out_path_tsv, 'wt', encoding="utf8") as out_file:
                    tsv_writer = csv.writer(out_file, delimiter='\t')
                    tsv_writer.writerow(['bookTitle', 'bookAuthors', 'ratingValue', 'ratingCount', 'reviewCount', 'Plot', 'NumberofPages', 'Published', 'Characters', 'Setting', 'Url'])
                    tsv_writer.writerow([bookTitle, bookSeries, bookAuthors, ratingValue, ratingCount, reviewCount, Plot, NumberofPages, Published, characters, setting, Url])


    out_file.close()
    print("All tsv files generated sucessfully in " + tsv_folder + " directory")
	
def Search_Engine(query = input().split()):
    
    #stem the tokens of the query in order to create a new query: my_query
    my_query = []
    for tok in query:
        my_query.append(ps.stem(tok))

    #create a new dictionary which contains just the keys present in my_query        
    my_invertedId = {}
    for tok in my_query:
        if tok in vocabulary:
            my_invertedId[tok] = my_dict.get(vocabulary[tok])
            
    #if any of the query's tokens is not present into the vocabulary, give an Error Message to the user
        elif tok not in vocabulary:
            print("The query is not present in any plot")
            return([])
      
    #define a list of sets where each set represents the documents that contain each token of the query
    my_sets = []
    for key in my_invertedId:
        my_sets.append(set(my_invertedId[key]))
    result = set()

    for i in range(1, 30001):
        result.add('document_'+str(i))
        
    for my_set in my_sets:
        result = result.intersection(my_set)
    
    if result == set():
        print("The query is not present in any plot")
        return([])
    else:
        return(result)

found = list(Search_Engine())

