# README File

## Overview

This is a project created for the Python Basics for Market Analysis. It uses Beautiful Soup to scrape [Books to Scrape](https://books.toscrape.com/) and download key datapoints and images.

## Installation

The version of Python installed is 3.10.7 (64-bit)

## Packages

The program uses the following Python packages:
* requests
* csv
* re
* os
* shutil
* time
* BS4

## Virtual Environment

Using a virtual environment allows you to download specific packages for a project. We will use the VEMV module in Python.

1. Create a new folder in your directory
2. Download the following files from this repo into the new folder: books_to_scrape_05.py and requirements.txt
2. In Windows, go to your Command Prompt and use cd to navigate to the newly created folder.
3. To create a virtual environment type the following into the command prompt: python -m venv venv
3. To activate the virtual environment type: venv\Scripts\activate.bat
4. To install the requirements type: pip install -r requirements.txt
To run the script type: python books_to_scrape_05.py
5. To deactivate the environment type: deactivate
6. To delete the environment: rmdir venv /s


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
