from steem import Steem

import requests
import feedparser
import datetime

from datetime import date
today = date.today()
open('post.txt', 'w').close()
postfile = open('post.txt', 'a')
print(today)
postfile.write("Running Log: " + str(today) + ".\n")
postfile.write("running runburgundy fitnation fitness training\n")
postfile.write("## <center>This is one of the first automated posts for the Run Burgundy Decentralized Running Group.</center>\n### <center>We're still figuring some shit out, and aren't ready to go live just yet.</center>\n#### <center>If you're interested in joining, talk to @mstafford.</center>\n\n")
postfile.write("## Below is a summary of the groups runs for " + str(today) + ".\n")
s = Steem()


def get_run(user):
    if user == 'mstafford':
        user = 'mtastafford'
    url = 'https://runalyze.com/athlete/' + user + '/feed'
    response = requests.get(url).text
    rss = feedparser.parse(response)
    response = []
    print(rss)
    #for post in rss.entries:
    #    response.append(post.title + ": " + post.link)
    if len(rss.entries) >= 1:
        response=" posted: " + rss.entries[0]['title'] + " on: " + rss.entries[0]['published']
    return response


def get_follows(user):
    follows = s.get_following(user, 0, 0, 10)
    users = []
    for i in range(len(follows)):
        users.append(follows[i]['following'])
    return users

follows = get_follows('runburgundy')

for follow in follows:
    with open('post.txt', 'a') as postfile:	
        newline = (follow + ": " + str(get_run(follow))+'\n')
        print(newline)
        postfile.write(newline)
#        if follow == 'mstafford':
#            newline = (follow + ": " + str(get_run('mtastafford'))+'\n')
#            print(newline)
#            postfile.write(newline)
#        else:
#            newline = (follow + ": " + str(get_run(follow))+'\n')
#            print(newline)
#            postfile.write(newline)
postfile = open('post.txt', 'a')
postfile.write("## Run Burgundy is a FitNation initiative\n")
postfile.write("Thanks for stopping by, San Diego\n")
