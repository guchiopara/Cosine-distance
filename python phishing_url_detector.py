#/usr/bin/env python
from __future__ import print_function
import argparse
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import socket


# Computes the word features.
def word_features(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

#computes the character level cosine distance, based on the word features.
def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]


#Get the google query URLs.
def get_top_k_urls(query ,k=3, tld="com"):
	url_list = []

	try:
		search_list = search(query, tld=tld, num=k)
		for i,entry in enumerate(search_list):
			if(i>=k):
				break
			url_list.append(entry)
	except Exception as e:
		raise Exception(e)
	return url_list

#To extract the domain name from the URL.
def extract_domain_name(url):
	url = url.strip()
	match_token="^(http://|https://)[A-Za-z0-9.-]+(?!.*\|\w*$)"
	domain_name = re.match(match_token, url).group(0).replace(re.match(match_token, url).group(1),'')
	if 'www.' in domain_name:
		domain_name = domain_name.replace('www.','')	
	return domain_name

#Function returning a list of cosine distances.
def get_cosine(primary_url, urllist):
	cosine_dis_list = []
	primary_url_features = word_features(primary_url)
	for secondary_url in urllist:
		secondary_url_features = word_features(secondary_url)
		cur_dis = cosdis(primary_url_features, secondary_url_features)
		cosine_dis_list.append(cur_dis)
	return cosine_dis_list

#Checking if the cosine match is less than 0.5
def check_phising_cosine(coslist):
	for val in coslist:
		if val >= 0.5:
			#print ("Cosine match greater than 0.5")
			return False
	print ("The cosine similarity did not exceed 0.5")
	return True

#Checking the ips for more than 0.5 cosine distance.
def check_phising_ip(primary_url, urllist):
	#getting all the ips attached to the domain name.
	primary_domain_name = extract_domain_name(primary_url)
	#print ("primary_domain_name ", primary_domain_name)
	primary_ip = socket.gethostbyname_ex(primary_domain_name)
	for secondary_url in secondary_url_list:
		secondary_domain_name  =extract_domain_name(secondary_url)
		secondary_ip  = socket.gethostbyname_ex(secondary_domain_name)
		#print ("primary ip", primary_ip," secondary ip ",secondary_ip, "  secondary_url", secondary_url,"  secondary_domain_name" ,secondary_domain_name)
		#Getting the intersection of the ip lists.
		#print ("\nprimary ip list\n", primary_ip[-1],"\n secondary_ip_list", secondary_ip[-1])
		if len(set(primary_ip[-1]).intersection(secondary_ip[-1])): 
			print ("The ips matched.")
			return False
	return True

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", help="The input URL.", required=True, )
	args = parser.parse_args()

	primary_url = args.url
	primary_domain_name = extract_domain_name(args.url)
	secondary_url_list = get_top_k_urls(primary_domain_name)
	cosine_list = get_cosine(primary_url, secondary_url_list)
	is_phising = check_phising_cosine(cosine_list)
	if not is_phising:
		is_phising = check_phising_ip(primary_url, secondary_url_list)
	
	if is_phising:
		print ("\n\nThe url ", primary_url, " is a phising URL.")
	else:
		print ("\n\nThe url ", primary_url, "is not a phising URL.")
