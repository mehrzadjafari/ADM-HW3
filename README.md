# ADM-Homework 3 - Which book would you recommend?

<p align="center"> 
    <img src="https://camo.githubusercontent.com/406644a4e60cd793ef853c47ee30ec2206f3b87081731fb80976824b56417a41/68747470733a2f2f73323938322e7063646e2e636f2f77702d636f6e74656e742f75706c6f6164732f323031352f31322f676f6f6472656164732d65313435373535353432343738302e6a70672e6f7074696d616c2e6a7067" alt="GoodReads">
 </p>


**Goal of the homework**: Build a search engine over the "best books ever" list of [GoodReads](https://www.goodreads.com/). Unless differently specified, all the functions must be implemented from scratch.


## 1. Data collection :

For this homework, there is no provided dataset, but you have to build your own. Your search engine will run on text documents. So, here we detail the procedure to follow for the data collection.

### 1.1. Get the list of books :

We start from the list of books to include in your corpus of documents. In particular, we focus on the  [best books ever list](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1). From this list we want to **collect the url** associated to each book in the list. As you realize, the list is long and splitted in many pages. We ask you to retrieve only the urls of the books listed in the first 300 pages.

The output of this step is a `.txt` file whose single line corresponds to a book's url.


