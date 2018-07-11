import datetime
import json
import os

from get_activities import get_runalyze
from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post

blockchain = Blockchain()
members = open('members.json')
members = json.load(members)
stream = map(Post,blockchain.stream(filter_by=['comment']))

def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

post_list = []
post_age = []
while True:
    try:
        for post in stream:
            if post.is_main_post():
            ### IF MEMBER POSTS -- 25% UPVOTE! <-- PERCENTAGE SHOULD BE VARIABLE
            ### IF MEMBER POSTS WITH FITNATION TAG -- 50% UPVOTE! <-- PERCENTAGE SHOULD BE VARIABLE
                author = post["author"]
                title = post["title"]
                tags = ", ".join(post["tags"])                
                if author in members:
                    if 'fitnation' in tags:
                        weight = 50
                    else:
                        weight = 25
                    post.vote(weight, voter = 'runburgundy')
                    print('Hot Damn! Voted on {}s post called *{}*'.format(author, title))
                break
            
            ### IF A MEMBER MENTIONS @RUNBURGUNDY -- 75% UPVOTE, AND RANDO FUNNY COMMENT! <-- PERCENTAGE SHOULD BE VARIABLE
              ### NEED RANDOM COMMENT LIST; GIPHY;
              
            ### IF A MEMBER POSTS WITH RB-RUNALYZE TAG -- 100% UPVOTE AND "PERSONALIZED" / "WAY TO GO ON YOUR xKM RUN" COMMENT! & UPDATE FEED ON BURGUNDY.RUN <-- PERCENTAGE SHOULD BE VARIABLE
            
            
            
            # DO SOMETHNIG
    except Exception as error:
        print(repr(error))
        continue
s = Steem()

