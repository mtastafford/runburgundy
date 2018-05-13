from steem import Steem
import os

steemPostingKey = os.environ.get('steemPostingKey')
steem = Steem(wif=steemPostingKey)

permlink = '@runburgundy/great-odins-raven-we-kinda-broke-something-maybe'

try:
    steem.vote(permlink,100)
    print ("Succesfully upvoted!")
except Exception as e:
    print (repr(e))
