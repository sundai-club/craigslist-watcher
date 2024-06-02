import os
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client
from flask import Flask, request, jsonify
from scraper import scrape
import re

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
TWILIO_SID = os.environ.get("TWILIO_SID")

account_sid = TWILIO_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)


app = Flask(__name__)

# List to store search_links_and_phone_numbers (Link, Phone number) tuples
search_links_and_phone_numbers = []


def validate_url(url):
    # check if acceptable search query for craiglist (else the algorithm runs forever)
    pattern = r'^https://\w+\.craigslist\.org/search/.*$'

    passed = True
    if not re.match(pattern, url):
        passed = False
    if 'query' not in url:
        print(f"Wrong url. The url must include 'query' parameter")
        passed = False

    return passed


# Endpoint to add a new item to the list
@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    url = data.get('url')
    phone_number = data.get('phone_number')
    if not url or not phone_number:
        return jsonify({'error': 'URL and phone number are required'}), 400
    if not validate_url(url):
        return jsonify({'error': "URL must be from craigslist and contain the word 'query' "}), 400

    search_links_and_phone_numbers.append((url, phone_number))
    return jsonify(
        {'message': 'Item added successfully', 'search_links_and_phone_numbers': search_links_and_phone_numbers})


# Endpoint to trigger search (TBD logic)
@app.route('/trigger_search', methods=['GET'])
def trigger_search():
    scraping_res = []
    for url, phone_number in search_links_and_phone_numbers:
        print(f'url: {url}, phone_number: {phone_number}')
        curr_res = scrape([url], 0, 60)
        scraping_res.append(curr_res)
        print(f'curr res: {scraping_res}')

        links = []
        for key in curr_res:
            for item in curr_res[key]:
                links.append(item["link"])
        if len(links) > 0:
            print(f'Found new Craigslist items matching your search!\n {links}')
            client.messages.create(
                from_='+18667401602',
                body=f'Found new Craigslist items matching your search!\n {links}',
                to='+18777804236'
            )

    return jsonify({'message': 'Search triggered', 'scraping_res': scraping_res})
    # return jsonify({'message': 'Search triggered', 'search_links_and_phone_numbers': search_links_and_phone_numbers})


# Endpoint to delete an item by phone number
@app.route('/delete_item', methods=['DELETE'])
def delete_item():
    data = request.get_json()
    phone_number = data.get('phone_number')
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    # Find the item with the given phone number
    item_to_delete = None
    for item in search_links_and_phone_numbers:
        if item[1] == phone_number:
            item_to_delete = item
            break

    if item_to_delete:
        search_links_and_phone_numbers.remove(item_to_delete)
        return jsonify(
            {'message': 'Item deleted successfully', 'search_links_and_phone_numbers': search_links_and_phone_numbers})
    else:
        return jsonify({'error': 'Item not found'}), 404


# Endpoint to get the list of search_links_and_phone_numbers (optional for debugging/ as the DATABASE!! :D)
@app.route('/search_links_and_phone_numbers', methods=['GET'])
def get_items():
    return jsonify({'search_links_and_phone_numbers': search_links_and_phone_numbers})


if __name__ == '__main__':
    app.run(debug=True)
