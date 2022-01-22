from bs4 import BeautifulSoup as soup
from openpyxl import Workbook
import requests
import random
import os


class AmazonScrapper:
    def run(self, product="Iphone", pages=1):
        iphone_offers = self.search_product(product, pages)
        self.to_excel(iphone_offers, product=product)

    def get_offers(self, html_page):
        """Extract offers data from amazon website."""
        bs4_page = soup(html_page.content, features="html.parser")

        offers = bs4_page.find_all(attrs={"data-component-type": "s-search-result"})

        def get_offer_data(bs4_offer):
            """Extract name and price data from offers."""
            name = bs4_offer.find("span", class_="a-size-base-plus a-color-base a-text-normal").text

            if bs4_offer.find("span", class_="a-price-whole"):
                price = (
                    bs4_offer.find("span", class_="a-price-whole").text
                    + bs4_offer.find("span", class_="a-price-fraction").text
                )
            else:
                price = 0

            return (name, price)

        offers_list = list(map(get_offer_data, offers))

        return offers_list

    def search_product(self, product, pages):
        """Search the product on the amazon website."""
        offers = []
        for page in range(1, pages + 1):
            url = f"https://www.amazon.com.br/s?k={product}&page={page}"

            html_page = requests.get(url, timeout=3)

            if not html_page:
                print(f"Not able to get any response from '{url}'.")
                continue
            offers += self.get_offers(html_page)
        return offers

    def to_excel(self, list, product):
        """Export the scrapped product list to an excel file."""

        if list == []:
            raise RuntimeError("Nenhuma oferta foi encontrada.")

        if not os.path.isdir("outputs"):
            os.mkdir("outputs")

        workbook = Workbook()
        sheet = workbook.active

        headings = ["ID", "Nome", "Preço"]
        sheet.append(headings)
        for id, item in enumerate(list):
            sheet.append([id, item[0], item[1]])

        hash = random.getrandbits(24)
        workbook.save(f"outputs/amazon_{product}_{hash}.xlsx")
        return True


if __name__ == "__main__":
    amazon = AmazonScrapper()
    amazon.run()
