#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import lxml
import csv
import re
import os
import pandas as pd
from langdetect import detect
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
import json
import re




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
    
    
    
    for j in range(300):
        
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
                    tsv_writer.writerow(['bookTitle', 'bookSeries', 'bookAuthors', 'ratingValue', 'ratingCount', 'reviewCount', 'Plot', 'NumberofPages', 'Published', 'Characters', 'Setting', 'Url'])
                    tsv_writer.writerow([bookTitle, bookSeries, bookAuthors, ratingValue, ratingCount, reviewCount, Plot, NumberofPages, Published, characters, setting, Url])


    out_file.close()

    print("All tsv files generated sucessfully in " + tsv_folder + " directory") 






def create_csv(parent_dir, tsv_folder, export_csv = True):
    
    """
    
    The function reads all .tsv files, combine them into a csv file, and export .csv file into parent directory
    
    Args:
    
    parent_dir (string) : The working directory you are working with
    tsv_folder (string) : The name of the folder that you have stored .tsv files (Attention: It should be in your parent_dir)
    export_csv (Boolean, Optional) : Set to False if you don't want to store the .csv file in your parent_dir. Default set to True
    
    Returns:
    The .csv file of all combined .tsv files
    
    """
    
    
    

    if parent_dir[-1] != '/':
        parent_dir += '/'


    os.chdir(parent_dir + tsv_folder)


    extension = 'tsv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f, delimiter = '\t') for f in all_filenames ])
    combined_csv.reset_index(inplace=True, drop= True)
    print("The csv file has generated! With " + str(len(combined_csv)) + " number of entries.")
    
    if export_csv:
        os.chdir(parent_dir)

        combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
        print("The csv file has been exported to " + parent_dir)
        return combined_csv
    else:
        return combined_csv









def create_dictionary_plot(df, export_json = True):

    """The function pre-processes all the information collected for each book by using nltk library to:
    1. Remove stop words
    2. Remove punctuation
    3. Stemming
    And creates the dictionary file of the Inverted Index 
    

    Args:
    
    df (dataframe) : The dataframe that has been created using 'create_csv' function.
    export_json (Boolean) : Set to False if we don't want to export the .json file in our working directory. Default set True

    Returns:
        The dictionary file of the inverted indexes, and vocabulary.
    
    """
    import nltk
    

    processed_docs = []
    tokenizer = RegexpTokenizer(r"\w+")
    stop_words = set(stopwords.words('english')) 
    ps = PorterStemmer()

    #for every article_i.tsv file, extract the Plot, tokenize it and preprocess it 

    for i in range(len(df)):

        plot = df["Plot"][i]
        tokens = tokenizer.tokenize(plot)
        processed_doc = []
        for token in tokens:
            if (token != 'Plot') & (token != '0') & (not token in stop_words):
                processed_doc.append(ps.stem(token))

        processed_docs.append(processed_doc)


        
    #initialize an empty dictionary
    vocabulary = {}


    #for every document (for every plot in our case)
    for term_id, doc in enumerate(processed_docs,1):

    #for every token in the document
        for tok in doc:

    #if the token is not present in the dictionary yet...
            if tok not in vocabulary:

    #...add it and set term_id as his id
                vocabulary[tok] =  term_id



    #initialize an empty dictionary
    my_dict = {}


    doc_id = 0 
    #for every document (for every plot in our case)
    for n_art, doc in enumerate(processed_docs):
        directory = df["Plot"][n_art]

        #increase the id of the document
        doc_id+=n_art
        n_tok = 0

        #for every token in the document
        for tok in doc:

    #if the id of that specific token is not present in the dictionary yet...
            if vocabulary[tok] not in my_dict:

    #...add it to the dictionary as a key and let document_doc_id be one of its values:
                my_dict[vocabulary[tok]] = ["document_"+str(doc_id)]

    #else, if this token is present in the dictionary but document_doc_id is not one of his values yet...
            elif "document_"+str(doc_id) not in my_dict.get(vocabulary[tok]):

    #append document_doc_id to his values
                my_dict[vocabulary[tok]].append("document_"+str(doc_id))
        
        
    #Exporting the .json file of the dictionary
    if export_json:
        
        dict_file = open("dict_file.json", "w")
        json.dump(my_dict, dict_file)
        dict_file.close()
        dict_file = open("voc_file.json", "w")
        json.dump(vocabulary, dict_file)
        dict_file.close()
        return my_dict, vocabulary
    else:
        return my_dict, vocabulary



    print("All tsv files generated sucessfully in " + tsv_folder + " directory")
	




def Search_Engine(query):
    
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
        found = list(result)

        my_dict1 = {}
        for i in range(1,30001):
            directory = "article_" + str(i) + ".tsv"
            path = functions.os.path.join(parent_dir, directory)
            if functions.os.path.exists(path):
                my_dict1["document_"+str(i)] = "article_"+str(i)


        i = 0
        for item in found:
            directory = my_dict1[item]+".tsv"
            path = functions.os.path.join(parent_dir, directory)
            if i == 0:
                data = functions.pd.read_csv(path, delimiter = '\t', usecols = ['bookTitle', 'Plot', 'Url'])
            else:
                data = data.append(functions.pd.read_csv(path, delimiter = '\t', usecols = ['bookTitle', 'Plot', 'Url']))
               
            data = data.rename(index = {0:'book_'+str(i+1)})
            
            i+=1
                            
        return(data)

