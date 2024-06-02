# Craigslist scraper endpoint

1. Install the requirements.txt libraries
2. run `python3 app.py` in your local terminal or on your hosted server
3. send a POST request from a client or Postman to `http://127.0.0.1:5000/scrape` (or wherever you host)
4. Include the list of urls to scrape and the time limits (both hour and minute)

Example from Postman on my local device:

Body: `{
    "urls": ["https://boston.craigslist.org/search/sss?postal=02142&query=bicycles&search_distance=0.5#search=1~gallery~0~0", "https://boston.craigslist.org/search/sss?max_price=225&min_price=80&postal=02142&query=bike&search_distance=20#search=1~gallery~0~0"],
    "hour_limit": 0,
    "minute_limit": 60
}`

Response: `{
    "https://boston.craigslist.org/search/sss?max_price=225&min_price=80&postal=02142&query=bike&search_distance=20#search=1~gallery~0~0": [
        {
            "cl_id": "7753144033",
            "link": "https://boston.craigslist.org/gbs/bik/d/boston-raleigh-technium/7753144033.html",
            "location": "boston",
            "screenshot_path": "",
            "time_posted": "33 mins ago",
            "time_scraped": "2024-06-02 16:37:03",
            "title": "RALEIGH TECHNIUM"
        },
        {
            "cl_id": "7753137863",
            "link": "https://boston.craigslist.org/gbs/bik/d/boston-motobicane/7753137863.html",
            "location": "boston",
            "screenshot_path": "",
            "time_posted": "54 mins ago",
            "time_scraped": "2024-06-02 16:37:03",
            "title": "motobicane"
        },
        {
            "cl_id": "7753137517",
            "link": "https://boston.craigslist.org/gbs/bik/d/boston-peugeot/7753137517.html",
            "location": "boston",
            "screenshot_path": "",
            "time_posted": "55 mins ago",
            "time_scraped": "2024-06-02 16:37:03",
            "title": "peugeot"
        },
        {
            "cl_id": "7753130462",
            "link": "https://boston.craigslist.org/gbs/bik/d/cambridge-northwoods-21-spd-aluminum/7753130462.html",
            "location": "Cambridge - near the Alewife train station",
            "screenshot_path": "",
            "time_posted": "59 mins ago",
            "time_scraped": "2024-06-02 16:37:03",
            "title": "Northwoods 21-spd aluminum hybrid commuter bike LGE for 5'8\" to 6'0\""
        }
    ],
    "https://boston.craigslist.org/search/sss?postal=02142&query=bicycles&search_distance=0.5#search=1~gallery~0~0": []
}`
