from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import csv
from getpass import getpass
from time import sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd

# list to hold content of tweets
content_list = []
# a set to hold unique "tweet id's" to make sure redundant data is not added to the list
tweet_set = set()

def main(email, password, search, tweet_limit, sleep_time):
    driver = webdriver.Chrome(executable_path="chromedriver")
    # open browser, go to twitter, and login
    start_twitter(email, password, search, sleep_time, driver)
    # scrape tweets and store in dataframe (returned as list)
    df_content = pd.DataFrame(scrape_tweets(tweet_limit, driver), columns=['Name', 'Handle', 'Timestamp', 'Comment', 'Original_Content', 'Replies', 'Retweets', 'Likes'])
    df_html = df_content.to_html()
    df_csv = df_content.to_csv(index=False)
    return df_html, df_csv

# this function will parse out the tweet content and store it in a list (of lists)
def parse_tweets(tweet):
    # if there is no timestamp, then it is a "Promoted" tweet and we don't want it
    try:
        datetime = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    except StaleElementReferenceException:
        return
    
    try:
        tweet_text_list = tweet.text.splitlines()
        u_name = tweet_text_list[0]
        handle = tweet_text_list[1]
        comment = tweet.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        original_content = tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        replies = tweet.find_element_by_xpath('.//div[@data-testid="reply"]').text
        retweets = tweet.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        likes = tweet.find_element_by_xpath('.//div[@data-testid="like"]').text
        tweet_id = u_name + datetime
    except StaleElementReferenceException:
        return
    
    # if "id" not in set, then add tweet to list and "id" to the set
    if not (u_name+datetime) in tweet_set :
        content_list.append([u_name, handle, datetime, comment, original_content, replies, retweets, likes])
        tweet_set.add(u_name+datetime)
    else:
        return


def start_twitter(un, pw, search_val, sleep_time, driver):
    # sleepy time is the pause between actions, increase if needed for slower connection or processing
    sleepy_time = int(sleep_time)

    # open browser and go to twitter
    driver.get("https://www.twitter.com/login")
    # sleep to allow for page loading, may need to increase for slower connections
    sleep(sleepy_time) 

    # find user name input and supply user name
    username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
    username.send_keys(un)
    # get password, find password field, and supply password
    password = driver.find_element_by_xpath('//input[@name = "session[password]"]')
    password.send_keys(pw)
    # "press" the enter key
    password.send_keys(Keys.RETURN)
    sleep(sleepy_time)

    # click the Explore tab
    driver.find_element_by_xpath('//a[@href="/explore"]').click()
    sleep(sleepy_time)

    # enter search term or hashtag
    search_input = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
    search_input.send_keys(search_val)
    search_input.send_keys(Keys.RETURN)
    sleep(sleepy_time)

    # click to Latest tab
    driver.find_element_by_link_text('Latest').click()
    sleep(sleepy_time)

def scrape_tweets(tweet_limit, driver):
    # collect all the tweets on the page
    while len(content_list) <= int(tweet_limit):
        tweets = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        # run them through the parsing filter
        for tweet in tweets:
            parse_tweets(tweet)
            print(len(content_list))
        try:
            driver.execute_script("return arguments[0].scrollIntoView();", tweets[-1])
        except StaleElementReferenceException:
            print(len(content_list) + ' - StaleElementReferenceException')
    return content_list

