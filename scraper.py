import requests
import feedparser


def get_run(user):
    url = 'https://runalyze.com/athlete/' + user + '/feed'
    response = requests.get(url, verify=False).text
    rss = feedparser.parse(response)
    for post in rss.entries:
        print(post.title + ": " + post.link)


get_run('jkms')
