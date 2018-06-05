from steem import Steem
import os
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
from get_activities import get_runalyze, get_thecrag
post_path = '/home/pi/post.txt'

with open('members.json') as f:
    members = json.load(f)
print(members)
s = Steem()
today = date.today()
time_now = time.time()
day_month = time.localtime()[2]
day_week = time.localtime()[6]
time_hours = time.localtime()[3]
time_minutes = time.localtime()[4]
time_seconds = time.localtime()[5]
if day_week == 0:
    week_cutoff = time.localtime(time.mktime(time.localtime()) - 3600*24)
else:
    week_cutoff = time.localtime(time.mktime(time.localtime()) - 3600*24*day_week-time_hours*3600-time_minutes*65-time_seconds)
day_cutoff = time.localtime(time.mktime(time.localtime())- time_hours*3600 - time_minutes*60 - time_seconds - 1)
day_end = time.localtime(time.mktime(time.localtime()) - time_hours*3600 - time_minutes*60 - time_seconds + 3600*24)
dist_pattern = '\d*[\.]*\d*\ km'
dist_table={} #store daily, weekly, and monthly kms for users
dist_table['RB_TOTAL_WEEK']={"weekrun":0,"weekbike":0,"weekother":0,"weekrelative":0}
claimable=s.get_account('runburgundy')["reward_sbd_balance"]
val_pattern = '\d*[\.]\d*'
rewards = re.search(val_pattern, claimable).group(0).split(' ')
rewards = float(rewards[0])

### Post header info.
open(post_path, 'w').close()
postfile = open(post_path, 'a')
postfile.write("Run Burgundy - Decentralized Fitness Group - Activity Log: " + str(today) + ".\n") ### This line is the title of the post
postfile.write("fitnation running cycling hiking fitness\n") ### This line holds the tags
postfile.write("![Run_Burgandy.png](https://steemitimages.com/DQmewBzW8MzewBP3qcUJzNL79hmfzM1qUquedRdSaLX83K4/Run_Burgandy.png)\n") ### This line should be the header image

### Write something to pull custom weekly post from separate text file
postfile.write("## <center>Welcome to Week No. 04, San Diego!</center>\n")
postfile.write("### <center>If you like exercising, earning money, and getting the freshest #fitnation fitness news delivered to your eyeholes -- then I'm afraid you've come to the right place.</center>\n#### <center>We're now accepting members! Lets talk in the discord, or the comments below!</center>\n")
postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("### <center> ... the fitness team had oddly strong hearts.</center>\n How to join our fitness group:\n * Make yourself a (free!) account for athletics tracking at [Runalyze](https://runalyze.com) (open-source running / athletics analytics site);\n * Post some GPS tracked runs/bikes/hikes to your new Runalyze account; \n * Talk to @mstafford or @aussieninja to prove you're real;\n * Vote on these daily posts to increase their rewards;\n * At the end of each week, the SBD rewards get distributed based on kilometres travelled!\n")
postfile.write("## <center>Neato, gang!</center>")

# Gif and rewards summary below
gif = translate('anchorman')
postfile.write("<center>![gif_test]("+gif.media_url+")</center>\n")
postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("#### Current rewards available for last weeks exercises = " + claimable + "!<br>This will be divided up amongst group members based on weekly kilometres ran & cycled!\n") ### Rewards from prev. week
postfile.write("*Note that 1km of running is weighted the same as 3km of cycling!*\n")
postfile.write("## Below is a summary of the groups runs/bikes/hikes as of " + str(today) + ".\n")
postfile.write("*Weekly summary is from Monday->Sunday. Monthly summary is from the 1st to end of month.*\n")

def get_dists():
    run_day = 0.0
    bike_day = 0.0
    other_day = 0.0
    run_week = 0.0 ##cumulative running km's for week
    bike_week = 0.0 ##cumulative biking km's for week
    other_week = 0.0 ##cumulative hiking (other) km's for week
    run_month = 0.0 ##cumulative running km's for month
    bike_month = 0.0 ##cumulative biking km's for month
    other_month = 0.0 ##cumulative hiking (other) km's for month
    for i in range(len(activity_list)):  ## Summing up daily running distance
        if activity_list[i]['published'] >= day_cutoff and activity_list[i]['sport'] == ('Running' or 'Jogging' or 'Walking'): ##if posted since sunday at midnight & Run/Jog/Walk, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            run_day += distance #add activity distance to week total
    for i in range(len(activity_list)):  ## Summing up weekly running distance
        if activity_list[i]['published'] >= week_cutoff and activity_list[i]['published'] <= day_end and activity_list[i]['sport'] == ('Running' or 'Jogging' or 'Walking'): ##if posted since sunday at midnight & Run/Jog/Walk, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            run_week += distance #add activity distance to week total
    for i in range(len(activity_list)):  ## Summing up daily biking distance
        if activity_list[i]['published'] >= day_cutoff and activity_list[i]['sport'] == ('Biking'): ##if posted since sunday at midnight & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            bike_day += distance #add activity distance to day total
    for i in range(len(activity_list)):  ## Summing up weekly biking distance
        if activity_list[i]['published'] >= week_cutoff and activity_list[i]['sport'] == ('Biking'): ##if posted since sunday at midnight & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            bike_week += distance #add activity distance to week total
    for i in range(len(activity_list)):  ## Summing up daily hiking distance
        if activity_list[i]['published'] >= day_cutoff and activity_list[i]['sport'] == ('Other'): ##if posted since sunday at midnight & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            other_day += distance #add activity distance to week total
    for i in range(len(activity_list)):  ## Summing up weekly hiking distance
        if activity_list[i]['published'] >= week_cutoff and activity_list[i]['sport'] == ('Other'): ##if posted since sunday at midnight & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            other_week += distance #add activity distance to week total
    dist_table[follow]={"todayrun":run_day,"weekrun":run_week,"todaybike":bike_day,"weekbike":bike_week,"todayother":other_day,"weekother":other_week}

def get_follows(user): ## Get @runburgundy following list
    follows = s.get_following(user, 0, 0, 10)
    users = []
    for i in range(len(follows)):
        users.append(follows[i]['following'])
    return users

follows = get_follows('runburgundy')

for follow in follows: ##data scrape, weekly totals and write to the post file for each user consecutively.
    print('Scraping data for ' + follow)
    activity_list = get_runalyze(members[follow]['runalyze']) #get user activities
    print('Calculating distances for ' + follow)
    get_dists()
    member_run_week = dist_table[follow]['weekrun']
    member_bike_week = dist_table[follow]['weekbike']
    member_other_week = dist_table[follow]['weekother']
    account_info=s.get_account(follow)
    helper = 0
    postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
    print('Writing post info for ' + follow)
    if len(account_info['json_metadata'])>=5: # Implemented for situations where user hasn't populated profile info
        profile_data = json.loads(account_info['json_metadata'])
        profileImage = profile_data['profile']['profile_image']
        postfile.write("#### !["+follow+"](https://steemitimages.com/0x100/"+profileImage+")")
        postfile.write("Summary for @" + follow +": <hr>\n") #Introduce athlete
    else:
        postfile.write("#### Summary for @" + follow +": <hr>\n") #Introduce athlete
    if len(activity_list)>=1: ## check if there are any activities
        postfile.write("##### Today:\n")
        for i in range(len(activity_list)): 
            if (activity_list[i]['published'] >= day_cutoff) and (activity_list[i]['published'] <= day_end): ##if posted since midnight yesterday, activity counts
                postfile.write("* " + str(activity_list[i]['distance'])+" of " + str(activity_list[i]['sport']) + " for a duration of " + str(activity_list[i]['duration']) + " (hh:mm:ss)!\n")
                helper=1
        if helper == 0:
            postfile.write("* No exercise today -- but there's always tomorrow!\n")
        postfile.write("##### Weekly Summary: ") ### WEEKLY SUMMARY
        if member_run_week > 0:
            postfile.write("Ran " + str(round(member_run_week,2)) + " km!    |    ")
        if member_other_week > 0:
            postfile.write("Hiked / Other'd " + str(round(member_other_week,2)) + " km!    |    ")
        if member_bike_week > 0:
            postfile.write("Biked " + str(round(member_bike_week,2)) + " km!\n")
        if (member_run_week + member_bike_week + member_other_week) <= 0:
            postfile.write("No activities so far this week.\n")
        recent_posts = s.get_blog(follow,-1,50)
        for post in recent_posts:
            json_data = json.loads(post['comment']['json_metadata'])
            if 'fitnation' in json_data['tags']:
                 link = post['comment']['permlink']
                 title = post['comment']['title']
                 postfile.write("\n##### Link to latest #fitnation post: [" + title + "](https://steemit.com/@" + follow + "/" + link + ")<br><br>\n")
                 break
    else:
        postfile.write("YOU HAVEN'T POSTED ANYTHING TO RUNALYZE YET!!\n")

postfile = open(post_path, 'a')
postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("## Run Burgundy is a FitNation initiative\n")
postfile.write("You stay classy, San Diego\n")
postfile.write('<center>[![discord](https://steemitimages.com/0x150/https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2017/12/Discord-Logo-796x396.jpg)](https://discord.gg/QPQBEQV) || <a href="https://runalyze.com/athlete/mtastafford" target="_blank"><img src="https://cdn.runalyze.com/social/v1/signature.png"/></a></center>')
