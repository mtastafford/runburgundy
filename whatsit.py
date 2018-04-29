from steem import Steem

import requests
import feedparser

s = Steem()


def get_run(user):
    url = 'https://runalyze.com/athlete/' + user + '/feed'
    response = requests.get(url).text
    rss = feedparser.parse(response)
    response = []
    for post in rss.entries:
        response.append(post.title + ": " + post.link)
    return response


def get_followers(user):
    followers = s.get_followers(user, '', 'blog', 1000)
    users = []
    for follower in followers:
        users.append(follower['follower'])
    return users

followers = get_followers('runburgundy')

for follower in followers:
    with open('post.txt', 'a') as postfile:	
        if follower == 'mstafford':
            newline = (follower + ": " + str(get_run('mtastafford'))+'\n')
            print(newline)
            postfile.write(newline)
        else:
            newline = (follower + ": " + str(get_run(follower))+'\n')
            print(newline)
            postfile.write(newline)
