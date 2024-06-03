from flask import Flask, request, jsonify
from scraper import scrape
import re

app = Flask(__name__)

# List to store search_links_and_phone_numbers (Link, Phone number) tuples
search_links_and_phone_numbers = []

def run_all_checks(url, phone_number,search_links_and_phone_numbers):
    
    # check that all fields are filled in
    if not url or not phone_number:
        return jsonify({'error': "'url' and 'phone_number' are required fields"}), 400

    # check if US / Canada phone number 
    us_phone_numbers = re.compile(r'^\+1\d{10}$')
    if not bool(us_phone_numbers.match(phone_number)):
        return jsonify({'error': "For now we only accept US phone numbers in +1 format. Must be 11 digits "}), 400
    
    # Check if valid craiglist link 
    if not validate_url(url):
        example_link= "https://boston.craigslist.org/search/sss?query=bicycles#search=1~gallery~0~0"
        return jsonify({'error': f"URL must be from craiglist and contain the word 'query'. For example:  {example_link}"}), 400

    # Check if unique phone and url pair do not exist already 
    pair_exists = is_new_list_in_original([url, phone_number], search_links_and_phone_numbers)
    if pair_exists:
        return jsonify({'error': "This combination of phone and url already exists"}), 400

    # Check that user (phone_number) has less than N queries 
    query_limit=2
    too_many_queries = check_phone_number_instances(phone_number, search_links_and_phone_numbers, limit=query_limit)
    if too_many_queries: 
        return jsonify({'error': f"This number has reached a limit of {query_limit} queries. "}), 400
    
    return {}



def check_phone_number_instances(phone_number, original_list, limit=2):
    count_number_existing = sum(1 for item in original_list if item[1] == phone_number)
    
    return count_number_existing>=limit
    

def is_new_list_in_original(new_list, original_list):
    # check if the query is unique (and not submitted again)
    for item in original_list:
        if item[0] == new_list[0] and item[1] == new_list[1]:
            return True
    return False


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
    
    # run checks to make sure that the new query meets our criterias for input
    response = run_all_checks(url, phone_number,search_links_and_phone_numbers)
    if response:
        return response

    search_links_and_phone_numbers.append((url, phone_number))
    return jsonify(
        {'message': 'Item added successfully', 'search_links_and_phone_numbers': search_links_and_phone_numbers})


# Endpoint to trigger search (TBD logic)
@app.route('/trigger_search', methods=['GET'])
def trigger_search():
    scraping_res = []
    for url, phone_number in search_links_and_phone_numbers:
        print(f'url: {url}, phone_number: {phone_number}')
        scraping_res.append(scrape([url], 5, 0))
        print(scraping_res)
        # todo: here we can trigger the search and send the SMS

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



# Endpoint to delete an item by phone number
@app.route('/delete_search', methods=['DELETE'])
def delete_search():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Exact search query is required'}), 400

    # Find the item with the given phone number
    item_to_delete = None
    for item in search_links_and_phone_numbers:
        if item[0] == url:
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
