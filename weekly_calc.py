from steem import Steem
import requests
import feedparser
import datetime
import re
import time
from datetime import date
import math
import json
import giphypop
from giphypop import translate

s = Steem()
today = date.today()
time_now = time.time()
day_month = time.localtime()[2]
day_week = time.localtime()[6]
month_cutoff = time.localtime(time.mktime(time.localtime())-3600*24*day_month)
week_cutoff = time.localtime(time.mktime(time.localtime()) - 3600*24*6)
last_week_end = week_cutoff
last_week_pretty = str(week_cutoff[0]) + "-" + str(week_cutoff[1]) + "-" + str(week_cutoff[2]-1)
last_week_start = time.localtime(time.mktime(time.localtime()) - 3600*24*7*2)
    
print("Week Start = " + str(last_week_start) + " and Week End = " + str(last_week_end))
day_cutoff = time.localtime(time.mktime(time.localtime())-3600*24)
dist_pattern = '\d*[\.]*\d*\ km'
dist_table={} #store daily, weekly, and monthly kms for users
dist_table['RB_TOTAL_WEEK']={"weekrun":0,"weekbike":0,"weekother":0,"weekrelative":0}
claimable=s.get_account('runburgundy')["reward_sbd_balance"]
val_pattern = '\d*[\.]\d*'
rewards = re.search(val_pattern, claimable).group(0).split(' ')
rewards = float(rewards[0])

open('/home/mark/reward_post.txt', 'w').close()
postfile = open('/home/mark/reward_post.txt', 'a')
postfile.write("Run Burgundy - Decentralized Fitness Group - REWARD TIME!: " + str(today) + ".\n") ### This line is the title of the post
postfile.write("running runburgundy fitnation fitness training\n") ### This line holds the tags
postfile.write("![Run_Burgandy.png](https://steemitimages.com/DQmewBzW8MzewBP3qcUJzNL79hmfzM1qUquedRdSaLX83K4/Run_Burgandy.png)\n") ### This line should be the header image
postfile.write("## <center>*I love rewards. Rewards rewards rewards. Here they come now -- over to my wallet.*</center>\n")
postfile.write("https://www.youtube.com/watch?v=V7Tf43WMhUg \n")
postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("### <center> This is officialy **THE FIRST** reward payout for the Run Burgundy Fitness Group!</center>\n * See some of the daily updates for a breakdown of how this works!\n * Runalyze *How To* post coming soon!\n")


postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("#### Current Rewards Available so far for Last Week = " + claimable + "!<br>This will be divided up amongst group members based on weekly kilometres ran & cycled!\n") ### Rewards from prev. week
postfile.write("*Note that 1km of running is weighted the same as 3km of cycling!*\n")
postfile.write("## Below is a summary of the groups runs/bikes/hikes for the week ending: " + last_week_pretty + "\n")

def get_activities(user): ## Get activities for individual users from Runalyze.com
    if user == 'mstafford': ## If runalyze account != steemit account, must have database of usernames
        user = 'mtastafford'
    url = 'https://runalyze.com/athlete/' + user + '/feed' ##RSS feed url
    response = requests.get(url).text
    rss = feedparser.parse(response)  ## Parse RSS feed
    activity_list = []
    for post in rss.entries:
        my_values = dict(re.sub('\&nbsp;', ' ', re.sub('<[^<]+?>', '', x)).split(': ') for x in post['content'][0]['value'][:-1].split('<br>')[:5]) ## Remove "<b>" and remove "\&nbsp" from activity description and add to dict
        my_values = {key.lower(): value for key, value in my_values.items()}
        my_values.update({'published': post['published']})
        my_values['date'] = time.strptime(my_values['date'], '%d.%m.%Y')
        my_values['published'] = time.strptime(my_values['published'], "%a, %d %b %Y %H:%M:%S %z")
        activity_list.append(my_values) ## add cleaned up information to list
        sorted(activity_list, key=lambda k: k['date'])
    return activity_list

def get_dists():
    run_dist = 0.0
    bike_dist = 0.0
    other_dist = 0.0
    for i in range(len(activity_list)):  ## Summing up daily running distance
        if activity_list[i]['published'] >= last_week_start and activity_list[i]['published'] <= last_week_end and activity_list[i]['sport'] == ('Running' or 'Jogging' or 'Walking'): ##if posted since sunday at midnight & Run/Jog/Walk, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            run_dist += distance #add activity distance to week total

    for i in range(len(activity_list)):  ## Summing up daily biking distance
        if activity_list[i]['published'] >= last_week_start and activity_list[i]['published'] <= last_week_end and activity_list[i]['sport'] == ('Biking'): ##if posted since sunday at midnight & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            bike_dist += distance #add activity distance to day total

    for i in range(len(activity_list)):  ## Summing up daily hiking distance
        if activity_list[i]['published'] >= last_week_start and activity_list[i]['published'] <= last_week_end and activity_list[i]['sport'] == ('Other'): ##if posted since sunday at midnight & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            other_dist += distance #add activity distance to week total

    dist_table[follow]={"running":round(run_dist,2),"biking":round(bike_dist,2),"hiking":round(other_dist,2),"weekrelative":0}
    relative = round(dist_table[follow]['running'] + dist_table[follow]['biking']/3,2)
    dist_table[follow]['weekrelative'] += round(relative,2)
    dist_table['RB_TOTAL_WEEK']['weekrun'] += round(run_dist,2)
    dist_table['RB_TOTAL_WEEK']['weekbike'] += round(bike_dist,2)
    dist_table['RB_TOTAL_WEEK']['weekother'] += round(other_dist,2)
    relative = 0.0
    relative = round(dist_table['RB_TOTAL_WEEK']['weekrun'] + dist_table['RB_TOTAL_WEEK']['weekbike']/3,2)
    dist_table['RB_TOTAL_WEEK']['weekrelative'] = round(relative,2)
    print(dist_table)

def get_follows(user): ## Get @runburgundy following list
    follows = s.get_following(user, 0, 0, 10)
    users = []
    for i in range(len(follows)):
        users.append(follows[i]['following'])
    return users

follows = get_follows('runburgundy')
for follow in follows: ##initial scrape and weekly / monthly totals
    activity_list = get_activities(follow) #get user activities
    get_dists()

postfile.write("## Total KM's Ran: " + str(dist_table['RB_TOTAL_WEEK']['weekrun']) + "\n")
postfile.write("## Total KM's Biked: " + str(dist_table['RB_TOTAL_WEEK']['weekbike']) + "\n")
postfile.write("## Total Weighted KM's: " + str(dist_table['RB_TOTAL_WEEK']['weekrelative']) + "\n")

for follow in follows:
    with open('/home/mark/reward_post.txt', 'a') as postfile:
        account_info=s.get_account(follow)
        activity_list = get_activities(follow) #get user activities
        postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
        if len(account_info['json_metadata'])>=1:
            profile_data = json.loads(account_info['json_metadata'])
            profileImage = profile_data['profile']['profile_image']
            postfile.write("#### !["+follow+"](https://steemitimages.com/0x100/"+profileImage+")")
            postfile.write("Summary for @" + follow +": <hr>\n") #Introduce athlete
        else:
            postfile.write("#### Summary for @" + follow +": <hr>\n") #Introduce athlete
        if len(activity_list)>=1: ## check if there are any activities
            postfile.write("##### Weekly Distances: ")
            if dist_table[follow]['running'] > 0:
                postfile.write("Ran " + str(dist_table[follow]['running']) + " km!    |    ")
            else:
                postfile.write("No Running :(    |    ")
            if dist_table[follow]['hiking'] > 0:
                postfile.write("Hiked / Other'd " + str(dist_table[follow]['hiking'] > 0) + " km!    |    ")
            else:
                postfile.write("No Hiking :(    |    ")
            if dist_table[follow]['biking'] > 0:
                postfile.write("Biked " + str(dist_table[follow]['biking']) + " km!\n")
            else:
                postfile.write("No Biking :( \n")
            postfile.write("#### Weighted Km's = " + str(dist_table[follow]['weekrelative']) + "!\n")
            share = round((dist_table[follow]['weekrelative'])/(dist_table['RB_TOTAL_WEEK']['weekrelative'])*float(rewards),3)
            postfile.write("#### Reward earned = " + str(dist_table[follow]['weekrelative']) + " / " + str(dist_table['RB_TOTAL_WEEK']['weekrelative']) + " x " + str(rewards) + " SBD = " + str(share) + " SBD!\n")
        else:
            postfile.write("YOU HAVEN'T POSTED ANYTHING TO RUNALYZE YET!!\n")
            postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")

postfile = open('/home/mark/reward_post.txt', 'a')
postfile.write("## Run Burgundy is a FitNation initiative\n")
postfile.write("You stay classy, San Diego\n")
postfile.write('<center>[![discord](https://steemitimages.com/0x150/https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2017/12/Discord-Logo-796x396.jpg)](https://discord.gg/QPQBEQV) || <a href="https://runalyze.com/athlete/mtastafford" target="_blank"><img src="https://cdn.runalyze.com/social/v1/signature.png"/></a></center>')

#gif = translate('anchorman')
#postfile.write("<center>![gif_test]("+gif.url+")</center>")
