#!/usr/bin/env python
# coding: utf-8

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
import json
import re
import os
import glob
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle
nltk.download('stopwords')


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









def create_dictionary_plot(df, export_pickle = False):

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
    import json
    
    #initialize an empty dictionary
    processed_docs = {}

    #initialize a list that will contain the lists of tokens, one per plot 
    tokenizer = RegexpTokenizer(r"\w+")
    stop_words = set(stopwords.words('english')) 
    ps = PorterStemmer()

    #for every article_i.tsv file, extract the Plot, tokenize it and preprocess it 
    for n_art in range(len(df)):
        plot = df['Plot'][n_art]
        tokens = tokenizer.tokenize(plot)
        processed_doc = []
        for token in tokens:
            if (token != 'Plot') & (token != '0') & (not token in stop_words):
                processed_doc.append(ps.stem(token))

        processed_docs['document_'+str(n_art + 1)] = processed_doc


    #initialize an empty dictionary
    vocabulary = {}
    term_id = 1
    #for every document (for every plot in our case)
    for doc in processed_docs.values():

        #for every token in the document
        for tok in doc:

            #if the token is not present in the dictionary yet...
            if tok not in vocabulary:

            #...add it and set term_id as his id
                vocabulary[tok] =  term_id
                term_id += 1


   #initialize an empty dictionary
    inv_index1 = {}


   #for every document (for every plot in our case)
    for doc_id ,doc in enumerate(processed_docs.values()):
        

        #for every token in the document
        for tok in doc:

            #if the id of that specific token is not present in the dictionary yet...
            if vocabulary[tok] not in inv_index1:

            #...add it to the dictionary as a key and let document_doc_id be one of its values:
                inv_index1[vocabulary[tok]] = ["document_"+str(doc_id + 1)]

            #else, if this token is present in the dictionary but document_doc_id is not one of his values yet...
            elif "document_"+str(doc_id + 1) not in inv_index1.get(vocabulary[tok]):

            #append document_doc_id to his values
                inv_index1[vocabulary[tok]].append("document_"+str(doc_id + 1))

        
        
    #Exporting the .pickle file of the dictionaries
    if export_pickle:
        
        dict_file = open("dict_file", "wb")
        pickle.dump(inv_index1, dict_file)
        dict_file.close()
        dict_file = open("voc_file", "wb")
        pickle.dump(vocabulary, dict_file)
        dict_file.close()
        dict_file = open("doc_file", "wb")
        pickle.dump(processed_docs, dict_file)
        dict_file.close()
        return inv_index1, vocabulary, processed_docs
    else:
        return inv_index1, vocabulary, processed_docs



def Search_Engine1(query, df, vocabulary, inv_index1, results = 10):
    
    """
    The function operates as a search engine to iterate into the Plots of book, by query entered by user.
    
    Args:
    query (string) : The query that user enters to search for a book based on information in its plot
    df (dataframe) : The pandas dataframe of .tsv book. For more information check `create_csv` function.
    results (integer) : The number of found results that the user wants to check. Default on 10.
    
    Returns:
    A dataframe of the books found by the query
    
    """
    
    import nltk
    
    #stem the tokens of the query in order to create a new query: my_query
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    queryTokens = tokenizer.tokenize(query)
    
    my_query = []
    for tok in queryTokens:
        my_query.append(ps.stem(tok))

    #create a new dictionary which contains just the keys present in my_query        
    my_invertedId = {}
    for tok in my_query:
        if tok in vocabulary:
            my_invertedId[tok] = inv_index1.get(vocabulary[tok])
            
#if any of the query's tokens is not present into the vocabulary, give an Error Message to the user
    if not my_invertedId:
        return("The query is not present in any plot")
      
    #define a list of sets where each set represents the documents that contain each token of the query
    my_sets = []
    for key in my_invertedId.keys():
        my_sets.append(set(my_invertedId[key]))
    result = set()

    for i in range(len(df)):
        result.add('document_'+str(i + 1))
        
    for my_set in my_sets:
        result = result.intersection(my_set)
    
    if not result:
        return("The query is not present in any plot")
    else:
        found = list(result)
    df = df[["bookTitle", "Plot", "Url"]]
    indexes = []
    for i in range(len(found)):
        num = int(re.findall(r'\d+', found[i])[0])
        ind = num - 1
        indexes.append(ind)
        
    if len(indexes) >= results:
        indexes = indexes[:results]
        return(df.loc[indexes])
        
    else:
        return(df.loc[indexes])
                  



def create_invert_index2(n_docs, inv_index1, processed_docs, export_pickle = True):
    
    """
    The function creates the second inverted index dictionary for search engine.
    
    
    Args:
    
    n_docs (integer): Number of items in our main dataframe of books (i.e. len(df))
    inv_index1 (Dictionary): The first inverted index dictionary, created by create_dictionary_plot function.
    processed_docs (Dictionary): The processed dictionary using plots of books, create by create_dictionary_plot function.
    export_json (Boolean): Set to False if we don't want to export the .json file in our working directory. Default set True.
    
    Returns:
    
    Second inverted index dictionary
    
    """

    #initialize an empty dictionary
    inv_index2 = {}



    #for every term_id belonging to the dictionary my_dict
    for term_id in tqdm(inv_index1):
        line = [term_id, inv_index1[term_id]]
        N = len(inv_index1[term_id]) #number of documents with the term corrisponding to the id term_id

        #for every document that contains that term
        for doc in line[1]:
            tf = processed_docs[doc].count(list(vocabulary.keys())[term_id-1]) #term frequency
            Idf = np.log(n_docs/N) #inverse document frequency
            tfIdf = tf*Idf

            if term_id not in inv_index2:
                inv_index2[term_id] = [(doc,tfIdf)]
            else:
                inv_index2[term_id].append((doc,tfIdf))

    if export_pickle:

      dict_file = open("inv2_file", "wb")
      pickle.dump(inv_index2, dict_file)
      dict_file.close()
      return inv_index2
    else:
           
      return inv_index2
                

def create_similarity_dictionary(inv_index2, export_pickle = True):
    
    """
    The function creates the dictionary for Cosine Similarity search engine.
    
    
    Args:
    
    inv_index2 (Dictionary): The second inverted index dictionary, created by create_invert_index2 function.
    
    Returns:
    
    Cosine Similarity dictionary
    
    """
    
    my_dict = {}
    for i in range(len(df_tsv)):
        my_dict["document_"+str(i + 1)] = i
                
    #initialize an empty dictionary D that will contain for each document the norm of its tfIdf
    dictSimilarity = {}

    #for every document
    for document in tqdm(my_dict):

        for key in inv_index2:

            for doc in inv_index2[key]:

                if doc[0] == document:

                    if document not in dictSimilarity:

                        dictSimilarity[document] = [doc[1]]

                    else:

                        dictSimilarity[document].append(doc[1])  

        if document in dictSimilarity:

            dictSimilarity[document] = np.linalg.norm(dictSimilarity[document])
            
    if export_pickle:
      
      dict_file = open("dictsim_file", "wb")
      pickle.dump(dictSimilarity, dict_file)
      dict_file.close()

      return dictSimilarity
    else:
           
      return dictSimilarity


def Search_Engine2(query, df, inv_index1, inv_index2, dictSimilarity, vocabulary, results = 10):
    
    """
    The function operates as a search engine to iterate into the Plots of book, by query entered by user using new score defined.
    For more info search : Cosine similarity score
    
    Args:
    query (string) : The query that user enters to search for a book based on information in its plot.
    df (dataframe) : The pandas dataframe of .tsv book. For more information check `create_csv` function.
    inv_index1 (dictionary) : The first inverted index dictionary, created by create_dictionary_plot function.
    inv_index2 (dictionary) : The second inverted index dictionary, created by create_invert_index2 function.
    dictSimilarity (dictionary) : The Cosine similarity dictionary, created by create_similarity_dictionary function.
    vocabulary (dictionary) : The vocabulary dictionary, created by create_dictionary_plot function.
    results (integer) : The number of found results that the user wants to check. Default on 10.
    
    Returns:
    A dataframe of the books found by the query based on their similarity to user's query.
    
    """
    
    
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    queryTokens = tokenizer.tokenize(query)
    
    #stem the tokens of the query in order to create a new query: my_query
    my_query = []
    for tok in queryTokens:
        my_query.append(ps.stem(tok))

    #create a new dictionary which contains just the keys present in my_query        
    my_invertedId = {}
    for tok in my_query:
        if tok in vocabulary:
            my_invertedId[tok] = inv_index1.get(vocabulary[tok])

    #if any of the query's tokens is not present into the vocabulary, give an Error Message to the user
        elif tok not in vocabulary:
            return("The query is not present in any plot")
      
    #define a list of sets where each set represents the documents that contain each token of the query
    my_sets = []
    for key in my_invertedId:
        my_sets.append(set(my_invertedId[key]))
    result = set()

    for i in range(len(df)):
        result.add('document_'+str(i + 1))
        
    for my_set in my_sets:
        result = result.intersection(my_set)
    
    if result == set():
        return("The query is not present in any plot")
    else:
        found = list(result)
        
        similarityList = []
        i = 0
        for item in found:
            
            similarity = 0
            for term in my_query:
                
                for doc in inv_index2[vocabulary[term]]:
        
                    if doc[0] == item:
                    
                        if dictSimilarity[item] != 0:

                            similarity += doc[1]/dictSimilarity[item]
                            
            similarity = round(similarity, 2)
            similarityList.append(similarity)
        
    indexes = []
    for i in range(len(similarityList)):
        similarityList[i] = (similarityList[i] - min(similarityList)) / (max(similarityList) - min(similarityList))
        similarityList[i] = round(similarityList[i], 2)
    
    for i in range(len(found)):
        
        num = int(re.findall(r'\d+', found[i])[0])
        
        ind = num - 1
        
        indexes.append(ind)
    
    
    df = df.loc[indexes]
    df["Similarity"] = similarityList
    df.sort_values("Similarity", ascending= False, inplace = True)
    df = df[["bookTitle", "Plot", "Url", "Similarity"]]

        
    if len(indexes) >= results:
        
        return(df[:results])
        
    else:

        return(df)    



def Search_Engine_NewScore(query, df, inv_index1, inv_index2, vocabulary, results = 10):
    
    """
    The function operates as a search engine to iterate into the Plots of book, by query entered by user using new score defined.
    The scoring system works as user enters more information about the publishing year and number of pages of desired book.
    
    Args:
    query (string) : The query that user enters to search for a book based on information in its plot.
    df (dataframe) : The pandas dataframe of .tsv book. For more information check `create_csv` function.
    inv_index1 (dictionary) : The first inverted index dictionary, created by create_dictionary_plot function.
    inv_index2 (dictionary) : The second inverted index dictionary, created by create_invert_index2 function.
    vocabulary (dictionary) : The vocabulary dictionary, created by create_dictionary_plot function.
    results (integer) : The number of found results that the user wants to check. Default on 10.
    
    Returns:
    A dataframe of the books found by the query based on their similarity to user's query and extra values entered by the user.
    
    """
    
    
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    queryTokens = tokenizer.tokenize(query)
    
    #stem the tokens of the query in order to create a new query: my_query
    my_query = []
    for tok in queryTokens:
        my_query.append(ps.stem(tok))

    #create a new dictionary which contains just the keys present in my_query        
    my_invertedId = {}
    for tok in my_query:
        if tok in vocabulary:
            my_invertedId[tok] = inv_index1.get(vocabulary[tok])

    #if any of the query's tokens is not present into the vocabulary, give an Error Message to the user
        elif tok not in vocabulary:
            return("The query is not present in any plot")
      
    #define a list of sets where each set represents the documents that contain each token of the query
    my_sets = []
    for key in my_invertedId:
        my_sets.append(set(my_invertedId[key]))
    result = set()

    for i in range(len(df)):
        result.add('document_'+str(i + 1))
        
    for my_set in my_sets:
        result = result.intersection(my_set)
    
    if result == set():
        return("The query is not present in any plot")
    else:
        found = list(result)
        
    indexes = []        
    for i in range(len(found)):
        
        num = int(re.findall(r'\d+', found[i])[0])
        
        ind = num - 1
        
        indexes.append(ind)        
    
    df = df.loc[indexes]
    df.dropna(subset=['NumberofPages', 'Published'], inplace = True)
    df = df.reset_index()
    df = df.rename(columns={'index': 'book_index'})
    
    user1 = input("Do you want to use our new scoring method? [Y/N] :")
    
    if (user1.lower() == "y") | (user1.lower() == "yes"):
        
        usernum = int(input("How many pages does your desired book have? (approximately) ->"))
        userpub = int(input("What year does the book published? (approximately) ->"))
        

        numdif = []
        pubdif = []
        for i in range(len(df)):

            num = int(re.findall(r'\d+', df["NumberofPages"][i])[0])
            numdif.append(abs(num - usernum))
            pub = int(re.findall(r'\d\d\d\d', df["Published"][i])[0])
            pubdif.append(abs(pub - userpub))
        
        maxnum = max(numdif)
        maxpub = max(pubdif)
        
        similarityList = []
        for i in range(len(df)):
            
            similarity1 = 1 - (numdif[i] / maxnum)
            similarity2 = 1 - (pubdif[i] / maxpub)
            similarity = (similarity1 + similarity2) / 2
            similarityList.append(round(similarity, 2))


        df["Similarity"] = similarityList
        df.sort_values("Similarity", ascending= False, inplace = True)
        df.set_index(["book_index"], inplace = True)
        df = df[["bookTitle", "Plot", "Url", "Similarity"]]
        if len(indexes) >= results:

            return(df[:results])

        else:

            return(df)    
    else:
    
        if len(indexes) >= results:

            return(df[:results])

        else:

            return(df) 
        
        
        
def recur(string_input , n): 
  
    #to read and write a global variable inside a function.
    global max_val 
  
    # if length of array is 1 
    if n == 1 : 
        return 1
  
    # max_ is the length of longest sequence. 
    max_ = 1
  
    #Recursive loop
    for i in range(1, n): 
        result = recur(string_input , i)
              
        if string_input[i-1] < string_input[n-1] and result+1 > max_: 
            max_ = result +1

    # Compare max_ with overall maximum. And update the overall maximum if needed 
    max_val = max(max_val , max_) 
      
    return max_ 
  
    
    
def recur_call(string_input): 
  
    # to allow the access of global variable 
    global max_val 
  
    # lenght of arr 
    len_n = len(string_input) 
  
    # maximum variable holds the result 
    max_val = 1
  
    #Recur will return the maximum length of continous substring
    recur(string_input , len_n) 
  
    return max_val 



def find_longest_subsequence(String_input):
    maximum = []       
   
    for i in range(0,len(String_input)):                #N times
        sequence=[]                                     #O(1)
        first=String_input[i]                           #O(1)
        sequence.append(first) 
        
        for letter in String_input[i+1:]:               #N 

            if alphabet[first] < alphabet[letter]:     #O(1)
                sequence.append(letter)                 #O(1)
                first=letter                            #O(1)

            if len(maximum) <len(sequence):               #O(1)
                maximum=sequence                        #O(1)
                
    return maximum                                    #O(1)
