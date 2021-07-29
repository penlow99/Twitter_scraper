from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import csv
from getpass import getpass
from time import sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# list to hold content of tweets
content_list = []
# sleep time (in seconds)
sleepy_time = 2
# the number of tweets pulled from the DOM changes when scrolling, this counts the current batch
tweet_count = 0
# the list to hold tweet data
content_list = []
# the total number of tweets to scrape
tweet_limit = 250
# a set to hold unique "tweet id's" to make sure redundant data is not added to the list
tweet_set = set()

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
    
    if not (u_name+datetime) in tweet_set :
        content_list.append([u_name, handle, datetime, comment, original_content, replies, retweets, likes])
        tweet_set.add(u_name+datetime)
    else:
        return

# open browser and go to twitter
driver = webdriver.Chrome(executable_path="/home/patrick/Documents/chromedriver")
driver.get("https://www.twitter.com/login")
# sleep to allow for page loading, may need to increase for slower connections
sleep(sleepy_time) 

# find user name input and supply user name
user = input('What is your login user name or email: ')
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys(user)
# get password, find password field, and supply password
# my_password = getpass()
my_password = 'R?BW9+4)gT~zd?C'
password = driver.find_element_by_xpath('//input[@name = "session[password]"]')
password.send_keys(my_password)
# "press" the enter key
password.send_keys(Keys.RETURN)
sleep(sleepy_time)

# click the Explore tab
driver.find_element_by_xpath('//a[@href="/explore"]').click()
sleep(sleepy_time)
# ask what to search for and enter into field
search_val = input('What would you like to search for: ')
search_input = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
search_input.send_keys(search_val)
search_input.send_keys(Keys.RETURN)
sleep(sleepy_time)

# click to Latest tab
driver.find_element_by_link_text('Latest').click()
sleep(sleepy_time)


# collect all the tweets on the page
while len(content_list) <= tweet_limit:
    tweets = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    # run them through the parsing filter
    for tweet in tweets:
        parse_tweets(tweet)
        tweet_count += 1
        print(len(content_list))
    try:
        driver.execute_script("return arguments[0].scrollIntoView();", tweets[tweet_count-1])
    except StaleElementReferenceException:
        print(len(content_list) + ' - StaleElementReferenceException')
    tweet_count = 0


print(content_list)

