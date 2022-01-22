# Amazon Offer Scrapper

## What Is This?

This is a simple python script that can be used to search offers of products on amazon website and export to a .xlsx file.

## How To Use This

1. Clone this repository.
2. Create the enviroment `python -m venv env`.
3. Run `pip install -r requirements.txt` to install dependencies.
4. Run `python amazon_scrapper.py`.
5. The .xlsx files are saved in `/outputs` folder.
6. The product and pages can be configured on the `run` method of AmazonScrapper `class`.
   (Default `product="Iphone` and `pages=1` )
