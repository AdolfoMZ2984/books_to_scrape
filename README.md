# README File

## Overview

This is a project created for the Python Basics for Market Analysis. It uses Beautiful Soup to scrape [Books to Scrape](https://books.toscrape.com/) and download key datapoints and images.

## Installation

This script was written using Anaconda and Jupyter Notebook, Python 3 (ipykernel). You can download both [Anaconda](https://www.anaconda.com/products/distribution?gclid=Cj0KCQjwyt-ZBhCNARIsAKH1176dQWl6WYnqVvLy0lC4LNAUl-FRbUQFCUnwgK7nSYl-CXcloFMSKkIaAm_zEALw_wcB) and [Jupyter](https://jupyter.org/install).

## Packages

The program uses the following Python packages:
* requests
* csv
* re
* os
* shutil
* time

## Script Overview

The program visits [Books to Scrape](https://books.toscrape.com/) and creates a list of all categories, with their respective URLs. The program subsequently cycles through each Category URL and creates a list of each Book in the category and its URL. The scrips then cycles through each individual Book's page and uses BS4 and Regex to extract the following data points:
1. Title
2. Description
3. Universal Product Code
4. Price excluding Tax
5. Price including Tax
6. Number Available
7. Category
8. Review Rating (Stars)
9. Image URL

As part of the inner loop (for each book) the script also downloads the Book's jpg.

The script relies heavily on functions and while loops to run.

## Outputs

The program creates a folder named 'Catalog', if it doesn't already exist. It then creates a folder for each category in which it subsequently places the downloaded image for each book and a .csv file containing a row for each book in the category. This folder is referenced in this repository's .gitignore to avoid uploading its contents to the remote repository. When the script is done running, the Categories file will be between 40 and 45 MB in size. 
