from bs4 import BeautifulSoup
import requests
import csv

# Fetch the webpage content
response = requests.get('http://books.toscrape.com/')
response.raise_for_status()  # Ensure the request was successful

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')

# Open a CSV file to write the scraped data
with open('books_scrape.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Price', 'Availability', 'Rating'])  # Column headers

    # Find all product listings
    for book in soup.find_all('article', class_='product_pod'):
        # Extract title from the <a> tag's title attribute
        title = book.find('h3').a['title']

        # Extract price
        price = book.find('p', class_='price_color').text

        # Extract availability status
        availability = book.find('p', class_='instock availability').text.strip()

        # Extract rating from the class of the <p> tag
        rating_class = book.find('p', class_='star-rating')['class']
        rating = rating_class[1] if len(rating_class) > 1 else 'No Rating'

        # Write the data to the CSV file
        csv_writer.writerow([title, price, availability, rating])

print('Books scraping complete. Data saved to books_scrape.csv')
