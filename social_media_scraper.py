from __future__ import division, print_function

import pandas as pd
import pickle
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from stylometry_analysis import StyleFeatures


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def get_posts(code_section, klass):
    return code_section.find_all(class_=klass)


def get_featurized_posts(posts_list):
    # soup = get_soup(url)

    # print(soup)

    # posts_list = get_posts(soup, klass)
    # posts = '|||'.join([post.text for post in posts_list])

    posts = '|||'.join(posts_list)

    # print(get_posts(soup, klass))
    print(len(posts_list))

    stylometry = StyleFeatures(posts)
    # print(stylometry)
    return stylometry


if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = 'https://twitter.com/elonmusk'
    # url = 'https://twitter.com/Miles1Deep'
    # tweet_html_class = "js-tweet-text-container"
    # tweet_html_class = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'
    
    browser.get(url)
    time.sleep(1)

    body = browser.find_element_by_tag_name('body')

    for _ in range(25):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    tweets = browser.find_elements_by_class_name('tweet-text')
    tweets_text = [tweet.text for tweet in tweets]

    features = get_featurized_posts(tweets_text)

    filename = 'Fitted_Model_XGBC_Style'
    loaded_model = pickle.load(open(filename, 'rb'))

    data = pd.DataFrame()
    for feature in features:
        print(features[feature])
        data[feature] = [features[feature]]

    print(data)

    pred = loaded_model.predict(data)

    print(pred)

    retweet_class = 'js-retweet-text'
    # url = 'https://www.facebook.com/...'  
    # fb_html_class = "_5pbx userContent _3ds9 _3576" 
    # fb_html_class = "_5pcr userContentWrapper"

    # featurized_posts = get_featurized_posts(url, fb_html_class)
