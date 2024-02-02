import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def scrape_blog_posts(base_url):
    all_posts = []
    previous_cards = None
    page = 1

    while True:
        page_url = urljoin(base_url, f"p{page}/")
        print(f"Scraping page: {page} - URL: {page_url}")
        response = requests.get(page_url)

        if response.status_code != 200:
            print(f"Error accessing page: {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        cards = soup.find_all('div', class_='card')

        if not cards:
            print(f"No cards found on page: {page}")
            break  # Break the loop if no cards are found on the page

        # Check if the current cards are the same as the previous cards
        if cards == previous_cards:
            print("Reached the end of available pages. Stopping.")
            break

        for card in cards:
            title = card.find('h3').find('a').text.strip()
            post_url = urljoin(base_url, card.find('h3').find('a')['href'])
            description = card.find('div', class_='redactor').text.strip()

            post_data = {
                'title': title,
                'url': post_url,
                'description': description
            }

            all_posts.append(post_data)

        print(f"Processed page: {page}")
        page += 1
        previous_cards = cards  # Update previous cards for the next iteration

    return all_posts

if __name__ == "__main__":
    base_url = "https://www.basketbal.vlaanderen/nieuws/"
    all_blog_posts = scrape_blog_posts(base_url)

    with open('$GITHUB_WORKSPACE/news.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_blog_posts, json_file, ensure_ascii=False, indent=2)

    print("Scraping completed. Data saved to news.json.")
