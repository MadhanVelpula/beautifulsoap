from bs4 import BeautifulSoup
import requests
import csv

# Fetch the webpage content
source = requests.get('http://coreyms.com').text

# Parse the content with BeautifulSoup
soup = BeautifulSoup(source, 'lxml')

# Open a CSV file to write the scraped data
with open('cms_scrape.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['headline', 'summary', 'video_link'])

    # Loop through articles and extract data
    for article in soup.find_all('article'):
        headline = article.h2.a.text
        summary = article.find('div', class_='entry-content').p.text

        try:
            vid_src = article.find('iframe', class_='youtube-player')['src']
            vid_id = vid_src.split('/')[4].split('?')[0]
            yt_link = f'https://youtube.com/watch?v={vid_id}'
        except Exception as e:
            yt_link = None

        # Write the data to the CSV file
        csv_writer.writerow([headline, summary, yt_link])

print('Scraping complete. Data saved to cms_scrape.csv')
