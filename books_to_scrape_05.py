#!/usr/bin/env python
# coding: utf-8


# Import Libraries
# This block of code is importing the libraries that will be used.
import requests, csv, re, os, shutil, time
from bs4 import BeautifulSoup


# Starting Timer
# This block is starting a timer.
tic = time.perf_counter()


# Setting Working Directory
# This block is looking for a folder named "Categories" creates one if its not there and sets it as the working directory.
# This folder should be added to the .gitignore file to prevent uploading the files the code creates.
current_folder = os.getcwd()
base_folder = current_folder + '/' + 'Categories'
if os.path.exists(base_folder):
    os.chdir(base_folder)
else:
    os.mkdir(base_folder)
    os.chdir(base_folder)


# Creating Functions that will be used in the program

# Building the Soup
# Input: Book URL
# Output: Book Soup object
# Description: This function intakes the URL for a book and returns a Soup object that will be used by subsequent functions to extract desired data points.
def build_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Getting Title
# Input: Book Soup Object
# Output: String with the Book's title
# Description: This function intakes the Soup object for a book and returns a variable containg the title as a string extracted from the "product_main" html block.
def get_title(soup):
    product_main =soup.find(class_="col-sm-6 product_main")
    title = product_main.h1.string
    return title

# Getting Description
# Input: Book Soup Object
# Output: String with the Book's description
# Description: This function intakes the Soup object for a book and returns a variable containg the description as a string extracted from the "meta" html block.
def get_description(soup):
    description = soup.find('meta', attrs={"name": "description"}).get('content')
    return description

# Importing table that contains multiple data points.
# Input: Book Soup Object
# Output: List with various desired data elements
# Description: This function intakes the Soup object for a book and returns a list which houses several of the desired data elements extracted from the "table" in html.
# Desired data points are:
# [0] universal_product_code
# [2] price_excluding_tax
# [3] price_excluding_tax
# [5] number_available
def get_table(soup):
    data = []
    table = soup.find('table', class_='table-striped')
    rows = table.find_all('tr')
    for row in rows:
        for element in row.find_all('td'):
            data.append(element.string)
    return data

# universal_product_code
# Input: data (list extracted from html with several desired data points)
# Output: String with the Book's UPC
# Description: This function extracts the first entry in the data list, which containes the upc.
def get_upc(data):
    universal_product_code = data[0]
    return universal_product_code

# price_excluding_tax
# Input: data (list extracted from html with several desired data points)
# Output: String with the Book's price_excluding_tax
# Description: This function extracts the third entry in the data list, which containes the price_excluding_tax.
def get_price_excluding_tax(data):
    price_excluding_tax = data[2]
    return price_excluding_tax

# price_including_tax
# Input: data (list extracted from html with several desired data points)
# Output: String with the Book's price_including_tax
# Description: This function extracts the fourth entry in the data list, which containes the price_including_tax.
def get_price_including_tax(data):
    price_including_tax = data[3]
    return price_including_tax

# number_available
# Input: data (list extracted from html with several desired data points)
# Output: String with the Book's number_available
# Description: This function extracts the sixth entry in the data list, which containes the number_available.
def get_number_available(data):
    number_available = data[5]
    return number_available


# category
# Input: Variable containing the Category name
# Output: String with the Book's category
# Description: This function takes the category name from the part of the script that loops through categories and returns it as a string. This function does not actually take the info from the html.
def get_category(soup):
    category = cat_name
    return category

# review rating
# Input: Book Soup Object
# Output: String with the Book's review
# Description: This function intakes the Soup object for a book and returns a variable containg the rating as a string extracted from the "star-rating" html block.
def get_review_rating(soup):
    review_rating = str(soup.find("p", class_="star-rating"))
    temp_list = review_rating.split(' ')
    rating = temp_list[2]
    stars = rating[:-5]
    return stars

# Image URL
# Input: Book Soup Object
# Output: String with the URL to the jpeg image
# Description: This function intakes the Soup object for a book and returns a variable containg the jpg's URL as a string extracted from the "img" html block
def get_image_url(soup):
    url_list = soup.find_all("img")
    image_url = re.sub("\../../","https://books.toscrape.com/", url_list[0]['src'])
    return image_url

# Run functions above
# Input: Url for a book
# Output: Variable containing a list with all the desired datapoints for the book
# Description: This function aggregates the function above, together they create a row to add to the CSV file with a single book's data
def get_row(url):
    soup                   = build_soup(url)
    title                  = get_title(soup)
    description            = get_description(soup)
    data                   = get_table(soup)
    universal_product_code = get_upc(data)
    price_excluding_tax    = get_price_excluding_tax(data)
    price_including_tax    = get_price_including_tax(data)
    number_available       = get_number_available(data)
    category               = get_category(soup)
    review_rating          = get_review_rating(soup)
    image_url              = get_image_url(soup)
    data_row =[title, description, universal_product_code, price_excluding_tax, price_including_tax, number_available, category, review_rating, image_url]
    return data_row

# Image Dowload
# Input: Url for a book's image and its name
# Output: Downloaded jpg into the working evnironment
# Description: Downloads the image for each book
def download_image(url,name):
    filename = url.split("/")[-1]
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)

# Checking for categories with multiple pages and creating a list of all the URLs for the category
# Input: first Url for a Category
# Output: List of all URLs for a category
# Description: This function takes the first URL of a given category and checks to see if there are others by looking for a "next" tag in html. If it does find others it adds them to a list, which is the output of the function
def category_sub_function(category):

    category_sub_list = []
    category_sub_list.append(category)

    # Building the soup
    soup = build_soup(category)
    has_next = soup.find(class_="next")

    # Creating a loop that will continue until it reaches a URL without a "next" section
    i=1
    while has_next != None:
        has_next_str = str(has_next)
        temp_list = has_next_str.split(' ')
        next_page=temp_list[2]
        next_name = re.findall('page.*html', next_page)[0]
        category_sub_list.append(re.sub("index.html",next_name, category))
        soup = build_soup(category_sub_list[i])
        has_next = soup.find(class_="next")
        i = i + 1
    return(category_sub_list)

# Create initial list of book URLs
# Input: Url for a category, if a category has more than 1 url, this function is ran more than once
# Output: List with a URL for each book in that Category URL
# Description: Builds a soup for the page and makes a list of all the book urls in it.
def make_url_list(category):
    # Build the Soup for the Category
    book_soup = build_soup(category)
    # Find all Books URLs. URLs are relative paths, which will need to be subsituted
    book_container = book_soup.find_all('article',{'class': "product_pod"})
    book_url_list.clear()
    for article in book_container:
        for tag in article.find_all('a',{'href': True}, limit=1):
            book_url_list.append(tag['href'])
    # Creating new list with absolute path URLs
    for book in book_url_list:
        absolute_book_url_list.append(re.sub("\../../../","https://books.toscrape.com/catalogue/", book))
    return(absolute_book_url_list)

# Getting Category URLs
# Input: Book's to scrape website URL
# Output: List of URLs for the first page of each category
# Description: The block below will create the list of URLs for each Category

#Making the soup for the main page
main_page = "http://books.toscrape.com/catalogue/category/books_1/index.html"
main_soup = build_soup(main_page)
container = main_soup.find(class_="side_categories")

#Creating list called "url_list" with Soup object
url_list=[]
for tag in container.find_all('a',{'href': True}):
    url_list.append(tag['href'])

# Creating list that contains strings from url_list and adds missing part of https address
full_category_list=[]
for category in url_list:
    # Creating a full url
    full_category_list.append(re.sub("\../","https://books.toscrape.com/catalogue/category/", category))
del full_category_list[0]

# Main Function
# Input: List of Category URLs
# Output: A folder for each Category with a csv file and all the jpg images
# Description: This is the main portion of the script. It all the functions above except for those that are used to create the list with Category urls.

book_url_list=[]
# Start with the category list
for category in full_category_list:
    # Create a Name for the csv file and change working directory
    folder_name = re.search('books/(.+?)/index.html', category).group(1)

    # Changing Working Directory
    os.chdir(base_folder)
    path_name = base_folder + '/' + folder_name
    if os.path.exists(path_name):
        os.chdir(path_name)
    else:
        os.mkdir(path_name)
        os.chdir(path_name)

    # Clear the book url list
    absolute_book_url_list =  []

    # Runs the function to add URLs if the category has more than one page.
    cat_list = category_sub_function(category)
    # Takes the list of urls for the category and loops through them to create a complete list of urls for each book
    for cat in cat_list:
        absolute_book_url_list = make_url_list(cat)

    # Build CSV file name
    cat_name = re.search('books/(.+?)/index.html', category).group(1)
    category_name = re.search('books/(.+?)/index.html', category).group(1) + ".csv"

    # Create header for the csv file
    header = ['title','description','universal_product_code', 'price_excluding_tax', 'price_including_tax', 'number_available', 'category', 'review_rating', 'image_url']
    # Create CSV file
    with open(category_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        #Loop through each Book URL in the category
        for x in absolute_book_url_list:
            # Get the url and run the BS4 and Regex functions to get the data
            url = x
            data_row = get_row(url)
            writer.writerow(data_row)

            #Download Image
            download_image(data_row[8],data_row[0])

    # Print the name of each CSV file as writting it is completed.
    print(category_name)
os.chdir(base_folder)
print('Complete!')

# Stopping Timer
# Stops timer and prints the elapsed time, in minutes rounded to one decimal
toc = time.perf_counter()
print(round((toc-tic)/60,1))
