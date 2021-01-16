import pandas as pd
import csv
import os
import re
from nltk.stem.wordnet import WordNetLemmatizer

class DataPreprocessing:
    
    def __init__(self, review):
        self.review = review
        self.REPLACE_URL_WITH_TWO_SPACES = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.REPLACE_WITH_TWO_SPACES = "(\&)|(\%)|(\$)|(\@)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\*)|(–)|([0-9]+)|(<br\s*/><br\s*/>)|(\.)|(\-)|(\/)|(\s+)|(\n)"
        self.REPLACE_WITH_SPACE = "(\s+)"
        self.stopwords =[]
        with open('stopwords.txt', 'r') as stopwords_file:
            for line in stopwords_file:
                stop = line.replace('\n', '')
                self.stopwords.append(stop)
        self.REPLACE_WORDS = "( [a-z]{1,2} )|( [a-z]{20,} )" # 1-2 charactered words & >= 20 charactered words
        self.FINAL = "[^a-z\s]"
        
    def preprocess(self):
        review_nr = self.noise_reduction()
        review_norm = self.normalization(review_nr)
        return review_norm
    
    def noise_reduction(self):
        review_clean = self.review.lower()
        review_clean = " " + review_clean + " "
        review_clean = re.sub(self.REPLACE_URL_WITH_TWO_SPACES, "  ", review_clean)
        review_clean = review_clean.replace("'", "")
        review_clean = re.sub(self.REPLACE_WITH_TWO_SPACES, "  ", review_clean)
        for stopword in self.stopwords:
            review_clean = review_clean.replace(" " + stopword.replace("'","") + " ", "  ")
        review_clean = re.sub(self.REPLACE_WORDS, "  ", review_clean)
        review_clean = re.sub(self.REPLACE_WITH_SPACE, " ", review_clean)
        review_clean = re.sub(self.FINAL, "", review_clean)
        review_clean = review_clean.strip()
        review_words = review_clean.split()
        review_clean = []
        for word in review_words:
            ok = True
            prev = '1'
            prev_count = 0
            for ch in word:
                if ch == prev:
                    prev_count+=1
                else:
                    prev = ch
                    prev_count = 1
                if prev_count >= 3:
                    ok = False
                    break
            if ok:
                review_clean.append(word)
        return " ".join(review_clean)
    
    
    def normalization(self, review_nr):
        lem = WordNetLemmatizer()
        review_words = review_nr.split()
        review_norm = [lem.lemmatize(word) for word in review_words] 
        review_norm = " ".join(review_norm)
        return review_norm