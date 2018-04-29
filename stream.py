from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
from steem.account import Account
import json
import datetime
import os

def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

def create_json():
    user_json = {}
    for user in Account("runburgundy").export()["following"]:
        user_json[user] = {
            "upvote_weight" : 100.0,
            "upvote_limit" : 2,
            "upvote_count" : 0
        }
    print(user_json)
    return user_json

def valid_post(post, user_json):
    title  = post["title"]
    author = post["author"]
    
    if (author in user_json): # and not limit_reached(user_json, author)):
        #user_json[author]["upvote_count"] += 1
        print(post)
        return True
    else:
        return False

def limit_reached(user_json, author):
    if user_json[author]['upvote_limit'] == user_json[author]['upvote_count']:
        return True
    else:
        return False

def run(user_json):
    username = "runburgundy"
    wif = os.environ.get("UNLOCK")
    steem = Steem(wif=wif)
    blockchain = Blockchain()
    stream = map(Post, blockchain.stream(filter_by=["comment"]))

    print("Checking posts on the blockchain!")
    while True:
        try:
            for post in stream:
                title  = post["title"]
                author = post["author"]
                print(author)
                if author in user_json:
#                if valid_post(post, user_json):
                    try:
                        title  = post["title"]
                        author = post["author"]
                        print("Upvoting post {} by {}!".format(title, author))
                        post.upvote(weight=user_json[author]["upvote_weight"],
                            voter=username)
                    except Exception as error:
                        print(repr(error))
                        continue

        except Exception as error:
            print(repr(error))
            continue
#create_json()
run(create_json())



