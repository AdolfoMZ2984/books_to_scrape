# Import Libraries
import requests, csv, re, os, shutil
from bs4 import BeautifulSoup

# Setting Working Directory
#Will change this to use current directory
base_folder = 'C:\\Users\\amora\\OneDrive\\Documents\\Python Scripts\\Categories'
os.chdir(base_folder)

#Creating Functions
# Building the Soup
def build_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Getting Title
def get_title(soup):
    product_main =soup.find(class_="col-sm-6 product_main")
    title = product_main.h1.string
    return title

# Getting Description
def get_description(soup):
    description = soup.find('meta', attrs={"name": "description"}).get('content')
    return description

# Importing table that contains multiple data points.
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
def get_upc(data):
    universal_product_code = data[0]
    return universal_product_code

# price_excluding_tax
def get_price_excluding_tax(data):
    price_excluding_tax = data[2]
    return price_excluding_tax

# price_including_tax
def get_price_including_tax(data):
    price_including_tax = data[3]
    return price_including_tax

# number_available
def get_number_available(data):
    number_available = data[5]
    return number_available

# category
def get_category(soup):
    category = cat_name
    return category

# review rating
def get_review_rating(soup):
    review_rating = str(soup.find("p", class_="star-rating"))
    temp_list = review_rating.split(' ')
    rating = temp_list[2]
    stars = rating[:-5]
    return stars

# Image URL
def get_image_url(soup):
    url_list = soup.find_all("img")
    image_url = re.sub("\../../","https://books.toscrape.com/", url_list[0]['src'])
    return image_url

# This function aggregates the function above, together they create a row to add to the CSV file with a single book's data
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
def download_image(url,name):
    filename = url.split("/")[-1]
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)


#The block below will create the list of URLs for each Category
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

# This is incomplete pending "If Then" for multipage categories

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

    # Build CSV file name
    cat_name = re.search('books/(.+?)/index.html', category).group(1)
    category_name = re.search('books/(.+?)/index.html', category).group(1) + ".csv"

    # Build the Soup for the Category
    book_soup = build_soup(category)

    # Find all Books URLs. URLs are relative paths, which will need to be subsituted
    book_container = book_soup.find_all('article',{'class': "product_pod"})
    book_url_list.clear()
    for article in book_container:
        for tag in article.find_all('a',{'href': True}, limit=1):
            book_url_list.append(tag['href'])
        # Need to add "Next loop"

    # Creating new list with absolute path URLs
    absolute_book_url_list=[]
    for book in book_url_list:
        absolute_book_url_list.append(re.sub("\../../../","https://books.toscrape.com/catalogue/", book))

    # Build Excel File for each Category
    # Change Working Directory

    header = ['title','description','universal_product_code', 'price_excluding_tax', 'price_including_tax', 'number_available', 'category', 'review_rating', 'image_url']
    with open(category_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for x in absolute_book_url_list:
            url = x
            data_row = get_row(url)
            writer.writerow(data_row)

            #Download Image
            download_image(data_row[8],data_row[0])

    # Print the name of each CSV file as writting it is completed.
    print(category_name)
