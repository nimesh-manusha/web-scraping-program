import requests
from bs4 import BeautifulSoup
import csv

# Base URL for books listing
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# List to store book details
books_data = []

# Loop through multiple pages (scraping first 5 pages)
for page in range(1, 6):
    url = BASE_URL.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all book containers
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        stock = book.find("p", class_="instock availability").text.strip()

        books_data.append([title, price, stock])

# Save data to a CSV file
csv_filename = "books_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Stock Availability"])
    writer.writerows(books_data)

print(f"Scraped data saved to {csv_filename}")
