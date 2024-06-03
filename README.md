# craigslist-watcher

**A [Sundai Club](https://sundai.club/) Project**

## Overview

Craigslist Watcher is a Python-based web scraper that monitors Craigslist for new listings matching specified search criteria. When new items are posted, the application sends out SMS notifications to the specified phone numbers using the Twilio API.

## Features

-   Monitor specific Craigslist search URLs for new postings.
-   Send SMS notifications when new items are found.
-   Web interface for adding and managing search URLs and phone numbers.
-   Integrated with Twilio for messaging and Flask for web server capabilities.

## How to Run the Code
### Step 1: Set up Twilio
Create an account at [console.twilio.com](https://console.twilio.com/). Initially, you'll just be able to send messages to a single phone number. After verification, that expands. 
Add the following to .env at the top level of the folder:
- TWILIO_TOKEN=[your twilio api token]
- TWILIO_SID=[your twilio account id]

## Still to do
- Add an endpoint for Twilio, so when a user unsubscribes from Twilio they're also removed from our DB
