import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
import os
import shutil
import sys


class ReviewDl:
    
    def __init__(self, url):
        self.url = url
        
    def down(self, name = ""):
        review_link = self.url
        paginationKey = ""
        num_reviews = 0
        cwd = os.getcwd()
        #if (index != 49): continue #uncomment line to test only 1 movie (0 - 249)
        try:
            with open("DNN_input_files/input2-%s.txt" % name, "w") as f:
#                 writer = csv.writer(f, dialect='myDialect')
#                 writer.writerow(['username', 'rating', 'helpful', 'total', 'date', 'title', 'review'])
#                 print ('Scraping movie : ' + row['name'])
                review_list = []
                while True:
                    page = requests.get((review_link + paginationKey), headers = {"Accept-Language": "en-US, en;q=0.5"})
                    soup = BeautifulSoup(page.content, 'html.parser')
                    review_containers = soup.find_all('div', 'review-container')
                    review_data = []
                    for review_container in review_containers:
                        rating = review_container.find('span', 'rating-other-user-rating')
                        if rating is not None:
                            rating = int(rating.span.contents[0])
                        else:
                            rating = 'Null'
                        title = review_container.find('a', 'title')
                        if title is not None:
                            title = str(title.contents[0])
                        else:
                            title = 'Null'
                        username = review_container.find('span', 'display-name-link')
                        if username is not None:
                            username = str(username.a.contents[0])
                        else:
                            username = 'Null'
                        date = review_container.find('span', 'review-date')
                        if date is not None:
                            date = str(date.contents[0])
                        else:
                            date = 'Null'
                        review = review_container.find('div', 'content')
                        if review is not None:
                            parsed_review = ''
                            for content in review.div.contents:
                                parsed_review += str(content)
                            review = parsed_review
                        else:
                            review = 'Null'
                        helpful = review_container.find('div', 'actions')
                        total = None
                        if helpful is not None:
                            wordlist = str(helpful.contents[0]).split(' out of ')
                            helpful = int(wordlist[0].strip().replace(',', ''))
                            total = int(wordlist[1].split(' ')[0].replace(',', ''))
                        else:
                            helpful = 'Null'
                            total = 'Null'
#                         review_data = [username, rating, helpful, total, date, title, review]
                        review_list.append(review)
                        num_reviews += 1
                    load_more_data = soup.find('div', 'load-more-data')
                    if load_more_data is not None:
                        paginationKey = str(load_more_data['data-key'])
                    else:
                        # Beautifulsoup breaks for "#&#@!" in a review in Pulp Fiction no idea why
                        # No paginationKey obtained so forcefully try from page response if available
                        paginationKey = None
                        con = str(page.content)
                        if (con.find('div class="load-more-data"') != -1):
                            paginationKey = con.split('<div class="load-more-data" data-key="')[1]
                            paginationKey = paginationKey.split('"')[0]
                            #print (paginationKey)
                        if paginationKey is None:
                            break
                
                    if(num_reviews%100==0):
                        print("%s number of reviews scraped"%str(num_reviews))
                    
                f.write(" ".join(review_list))
        except Exception as e:
            print (e)
            f.close()
            if os.path.exists(cwd + "DNN_input_files/input2-%s.txt" % name):
                os.remove(cwd + "DNN_input_files/input2-%s.txt" % name)
                print ('Removed input2.txt')
            sys.exit(0)    
    
