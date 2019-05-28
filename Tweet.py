# simple tweet class

import pandas as pd
import numpy as np
import re
import emoji

class Tweet:
    # initialize lazy-by-default instance
    # id and fit on init optional
    def __init__(self, text, tweetid="Undefined", fit_it=False):
        self.tweetid_ = tweetid
        self.text_ = text
        if fit_it == True:
            self.fit()
        else:
            self.is_fit_ = False

    # fit calls all methods, setting all attributes
    def fit(self):
        if self.is_fit_ == True:  # avoid refitting
            print(f"Tweet \'{self.tweetid_}\' already fit!")
        else:
            self.find_hashtags()  # make a list of hashtags
            self.find_handles()  # ...
            self.find_urls()
            self.find_emojis()
            self.clean()
            self.is_fit_ = True

    # make a list of hashtags
    def find_hashtags(self):
        hashtags = []
        try:
            hashtags.extend(re.findall(r"#\w+", self.text_))
        except:
            pass
        self.hashtags_ = hashtags

    # list of handles
    def find_handles(self):
        handles = []
        try:
            handles.extend(re.findall(r"@\w+", self.text_))
        except:
            pass
        self.handles_ = handles

    # list of urls
    def find_urls(self):
        urls = []
        # source: https://www.geeksforgeeks.org/python-check-url-string/
        urls = re.findall(r"https?://t\.co/\S+", self.text_)
        self.urls_ = urls

    # list of emojis
    def find_emojis(self):
        emojis = []
        try:
            emojis.extend(re.findall(emoji.get_emoji_regexp(), self.text_))
        except:
            pass
        self.emojis_ = emojis
        self.demojis_ = [emoji.demojize(e) for e in emojis]
        
    # simple status report
    def show_attributes(self):
        for k,v in sorted(vars(self).items()):
            print(f"{k}: {v}", end='\n')
        print()

    # remove special elements and provide as .text_clean_
    # indicate whether elements are woven into text (just in a word order sense for now)
    def clean(self):
        clean_text = {}
        split_text = dict(enumerate(self.text_.split()))
        special_elements = self.hashtags_ + self.handles_ + self.urls_ + self.emojis_
        for index, term in split_text.items():
            if term not in special_elements:
                clean_text.update({index: term})
        self.text_clean_ = " ".join(clean_text.values())

        # also check if any non-text elements are interwoven with text
        self.is_complex_ = False
        start_clean_text = min(clean_text.keys())
        end_clean_text = max(clean_text.keys())
        for index, term in split_text.items():
            if term in special_elements and index in range(start_clean_text, end_clean_text):
                self.is_complex_ = True
                break