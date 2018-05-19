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
time_hours = time.localtime()[3]
time_minutes = time.localtime()[4]
time_seconds = time.localtime()[5]
month_cutoff = time.localtime(time.mktime(time.localtime())-3600*24*day_month)
if day_week == 0:
    week_cutoff = time.localtime(time.mktime(time.localtime()) - 3600*24)
else:
    week_cutoff = time.localtime(time.mktime(time.localtime()) - 3600*24*day_week-time_hours*3600-time_minutes*65-time_seconds)
day_cutoff = time.localtime(time.mktime(time.localtime())-3600*24)
dist_pattern = '\d*[\.]*\d*\ km'
dist_table={} #store daily, weekly, and monthly kms for users
dist_table['RB_TOTAL_WEEK']={"weekrun":0,"weekbike":0,"weekother":0,"weekrelative":0}
claimable=s.get_account('runburgundy')["reward_sbd_balance"]
val_pattern = '\d*[\.]\d*'
rewards = re.search(val_pattern, claimable).group(0).split(' ')
rewards = float(rewards[0])

open('/home/mark/post.txt', 'w').close()
postfile = open('/home/mark/post.txt', 'a')
postfile.write("Run Burgundy - Decentralized Fitness Group - Activity Log: " + str(today) + ".\n") ### This line is the title of the post
postfile.write("fitnation running cycling hiking fitness\n") ### This line holds the tags
postfile.write("![Run_Burgandy.png](https://steemitimages.com/DQmewBzW8MzewBP3qcUJzNL79hmfzM1qUquedRdSaLX83K4/Run_Burgandy.png)\n") ### This line should be the header image
postfile.write("## <center>Welcome to Week No. 002, San Diego!</center>\n")
postfile.write("### <center>If you like exercising, earning money, and getting the freshest #fitnation fitness news delivered to your eyeholes -- then I'm afraid you've come to the right place.</center>\n#### <center>We're now accepting members! Lets talk in the discord, or the comments below!</center>\n")
postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("### <center> BY THE POWER OF GREYSKULL!!</center>\n ### <center> We made it to the 2nd week! </center>\n How to join our fitness group:\n * Make yourself a (free!) account for athletics tracking at [Runalyze](https://runalyze.com) (open-source running / athletics analytics site);\n * Post some GPS tracked runs/bikes/hikes to your new Runalyze account; \n * Talk to some people at #FitNation (try the [discord](https://discord.gg/QPQBEQV)) to prove you're real and meet peoples;\n * Vote on these daily posts to increase their rewards;\n * At the end of each week, the SBD rewards get distributed based on kilometres travelled!\n")
postfile.write("### This is still a work in progress, and there are some features to come -- such as:\n")
postfile.write(" * Autovoter if users write a post with #fitnation tag;\n * *Decentralized races*;\n * Leaderboards;\n * Featured users;\n * I'm really just kinda making this up as I go...\n")
gif = translate('anchorman')
postfile.write("<center>![gif_test]("+gif.media_url+")</center>\n")
postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
postfile.write("#### Current rewards available for last weeks exercises = " + claimable + "!<br>This will be divided up amongst group members based on weekly kilometres ran & cycled!\n") ### Rewards from prev. week
postfile.write("*Note that 1km of running is weighted the same as 3km of cycling!*\n")
postfile.write("## Below is a summary of the groups runs/bikes/hikes as of " + str(today) + ".\n")
postfile.write("*Weekly summary is from Monday->Sunday. Monthly summary is from the 1st to end of month.*\n")

def get_activities(user): ## Get activities for individual users from Runalyze.com
    if user == 'mstafford': ## If runalyze account != steemit account, must have database of usernames
        user = 'mtastafford'
    if user == 'phelimint':
        user = 'philb'
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
        if activity_list[i]['published'] >= week_cutoff and activity_list[i]['sport'] == ('Running' or 'Jogging' or 'Walking'): ##if posted since sunday at midnight & Run/Jog/Walk, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            run_week += distance #add activity distance to week total
    for i in range(len(activity_list)): ## Summing up monthly running distance
        if activity_list[i]['published'] >= month_cutoff and activity_list[i]['sport'] == ('Running' or 'Jogging' or 'Walking'): ##if posted since Month 1st @ 0:0:0 & running / jogging / walking ok
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ')## search for distance using regex pattern above. 
            distance = float(distance[0])##change distance string to float
            run_month += distance #add activity distance to month total
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
    for i in range(len(activity_list)): ## Summing up monthly biking distance
        if activity_list[i]['published'] >= month_cutoff and activity_list[i]['sport'] == ('Biking'): ##if posted since Month 1st @ 0:0:0 & biking, activity counts
            distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ') ## search for distance using regex pattern above. 
            distance = float(distance[0]) ##change distance string to float
            bike_month += distance #add activity distance to month total
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
    for i in range(len(activity_list)): ## Summing up monthly hiking distance
        if activity_list[i]['published'] >= month_cutoff and activity_list[i]['sport'] == ('Other'): ##if posted since Month 1st @ 0:0:0 & biking, activity counts
           distance = re.search(dist_pattern, str(activity_list[i]['distance'])).group(0).split(' ') ## search for distance using regex pattern above. 
           distance = float(distance[0]) ##change distance string to float
           other_month += distance #add activity distance to month total
    dist_table[follow]={"todayrun":run_day,"weekrun":run_week,"monthrun":run_month,"todaybike":bike_day,"weekbike":bike_week,"monthbike":bike_month,"todayother":other_day,"weekother":other_week,"monthother":other_month,"weekrelative":0}
    relative = dist_table[follow]['weekrun'] + dist_table[follow]['weekbike']/3
    dist_table[follow]['weekrelative'] += relative
    dist_table['RB_TOTAL_WEEK']['weekrun'] += run_week
    dist_table['RB_TOTAL_WEEK']['weekbike'] += bike_week
    dist_table['RB_TOTAL_WEEK']['weekother'] += other_week
    relative = 0.0
    relative = dist_table['RB_TOTAL_WEEK']['weekrun'] + dist_table['RB_TOTAL_WEEK']['weekbike']/3
    dist_table['RB_TOTAL_WEEK']['weekrelative'] = relative

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

for follow in follows:
    with open('/home/mark/post.txt', 'a') as postfile:
        account_info=s.get_account(follow)
        activity_list = get_activities(follow) #get user activities
        postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")
        print(follow)
        if len(account_info['json_metadata'])>=1:
            profile_data = json.loads(account_info['json_metadata'])
            if profile_data == {}:
                break
            profileImage = profile_data['profile']['profile_image']
            postfile.write("#### !["+follow+"](https://steemitimages.com/0x100/"+profileImage+")")
            postfile.write("Summary for @" + follow +": <hr>\n") #Introduce athlete
        else:
            postfile.write("#### Summary for @" + follow +": <hr>\n") #Introduce athlete
        if len(activity_list)>=1: ## check if there are any activities
            postfile.write("##### Today:\n")
            for i in range(len(activity_list)): 
                if activity_list[i]['published'] >= day_cutoff: ##if posted since midnight yesterday, activity counts
                    postfile.write("* " + str(activity_list[i]['distance'])+" of " + str(activity_list[i]['sport']) + " for a duration of " + str(activity_list[i]['duration']) + " (hh:mm:ss)!\n")
            postfile.write("##### Weekly Summary: ") ### WEEKLY SUMMARY
            if dist_table[follow]['weekrun'] > 0:
                postfile.write("Ran " + str(round(dist_table[follow]['weekrun'],2)) + " km!    |    ")
            else:
                postfile.write("No Running :(    |    ")
            if dist_table[follow]['weekother'] > 0:
                postfile.write("Hiked / Other'd " + str(round(dist_table[follow]['weekother'],2)) + " km!    |    ")
            else:
                postfile.write("No Hiking :(    |    ")
            if dist_table[follow]['weekbike'] > 0:
                postfile.write("Biked " + str(round(dist_table[follow]['weekbike'],2)) + " km!\n")
            else:
                postfile.write("No Biking :( \n")
#            postfile.write("Estimated Payout for the Week = " + str(round((rewards*dist_table[follow]['weekrelative']/dist_table['RB_TOTAL_WEEK']['weekrelative']),3)) +" SBD!\n")
            postfile.write("##### Monthly Summary: ") ### MONTHLY SUMMARY
            if dist_table[follow]['monthrun'] > 0:
                postfile.write("Ran " + str(round(dist_table[follow]['monthrun'],2)) + " km!    |    ")
            else:
                postfile.write("No Running :(    |    ")
            if dist_table[follow]['monthother'] > 0:
                postfile.write("Hiked / Other'd " + str(round(dist_table[follow]['monthother'],2)) + " km!    |    ")
            else:
                postfile.write("No Hiking :(    |    ")
            if dist_table[follow]['monthbike'] > 0:
                postfile.write("Biked " + str(round(dist_table[follow]['monthbike'],2)) + " km!\n")
            else:
                postfile.write("No Biking :(\n")
            recent_posts = s.get_blog(follow,-1,50)
            for post in recent_posts:
                json_data = json.loads(post['comment']['json_metadata'])
                if 'fitnation' in json_data['tags']:
                     link = post['comment']['permlink']
                     title = post['comment']['title']
                     postfile.write("##### Link to latest #fitnation post: [" + title + "](https://steemit.com/@" + follow + "/" + link + ")<br><br>\n")
                     break
        else:
            postfile.write("YOU HAVEN'T POSTED ANYTHING TO RUNALYZE YET!!\n")
            postfile.write("<center>![divider.png](https://steemitimages.com/DQmZMoUJp6VNtbthGnafHXDSYzyXVU5JC3ErFs7qfDEL8QF/divider.png)</center>\n")

postfile = open('/home/mark/post.txt', 'a')
postfile.write("## Run Burgundy is a FitNation initiative\n")
postfile.write("You stay classy, San Diego\n")
postfile.write('<center>[![discord](https://steemitimages.com/0x150/https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2017/12/Discord-Logo-796x396.jpg)](https://discord.gg/QPQBEQV) || <a href="https://runalyze.com/athlete/mtastafford" target="_blank"><img src="https://cdn.runalyze.com/social/v1/signature.png"/></a></center>')
