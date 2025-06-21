# Web-Scraper

To run the above file scraper.py for web scraping in local and performing the parallel exectution across different browsers/OS , execute the following commands in your terminal

python -m pip install browserstack-sdk
browserstack-sdk setup --username "your_username" --key "ypur_passcode"
browserstack-sdk python scraper.py

The username and passcode is generated after signing in on browserstack, you can copy the same from website.