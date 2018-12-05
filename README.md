# Cosine-distance
Install the following modules before you can use the code.
1. argparse
2. re
3. requests
4. bs4
5. googlesearch
6. socket

Use the following commands
1. pip install argparse
3. pip install requests
4. pip install beautifulsoup4
5. pip install google

Usage:


python phishing_url_detector.py --url 'URL'

Methodology

phishing_url_detector.py takes a URL as input, extracts its domain name and makes a Google search with the domain name.

The input URL is the Primary Url while the the top three results from the Google search are the secondary URL.

The Cosine similarity between the Primary and Secondary URLs are calculated with a threshold of 0.5.

If the cosine similarity is < 0.5, then the Primary URL is a phishing URL.

But if the cosine similarity exceeds 0.5, the IP addresses of the primary and secondary URLs are compared. If there is a match, then the Primary URL is not a phishing URL. 

