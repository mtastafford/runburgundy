import requests
import feedparser
import re
import time
from bs4 import BeautifulSoup


#In which we query runalyze for a users' activities by their RSS feed
def get_runalyze(user):
     nbsp_pattern = '\&nbsp;'
     htmltag_pattern = '<[^<]+?>'
     url = 'https://runalyze.com/athlete/' + user + '/feed'
     response = requests.get(url).text
     rss = feedparser.parse(response)
     activity_list = []
     for post in rss.entries:
          what = post['content'][0]['value'][:-1].split('<br>')[:-1]
         #Split the information by '<br>' and omit the last item, Remove html tags ('<[^<]+?>'), replace &nbsp with a space (' '), and then break that into dict entries by splitting the colon (': ') -- in that order
          my_values = dict(re.sub(nbsp_pattern, ' ', re.sub(htmltag_pattern, '', x)).split(': ') for x in post['content'][0]['value'][:-1].split('<br>')[:-1])
          #Lower case all of the keys
          my_values = {key.lower(): value for key, value in my_values.items()}
          #Include the 'published' value
          my_values.update({'published': post['published']})
          #Get calories
          my_values.update([list(reversed(re.sub('<[^<]+?>', '', re.search('<div class="boxed-value">\d* <div class="boxed-value-unit">kcal', requests.get(post['content'][0]['value'][:-1].split('<br>')[-1].split('"')[1]).text).group(0)).split(' ')))])
          #convert dates from strings into actual dates
          my_values['date'] = time.strptime(my_values['date'], '%d.%m.%Y')
          my_values['published'] = time.strptime(my_values['published'], "%a, %d %b %Y %H:%M:%S %z")
          #Add to our list
          activity_list.append(my_values)
     #Sort and return our list
     sorted(activity_list, key=lambda k: k['date']) 
     return activity_list

#In which we query TheCrag for users' recent climbs
def get_thecrag(user):
     base_url = 'https://www.thecrag.com/'
     response = requests.get(base_url + 'climber/' + user).text
     soup = BeautifulSoup(response, 'html.parser')
     user_feed_path = soup.find('a', {'title': 'A feed of recent ascents'}).get('href')
     response = requests.get(base_url + user_feed_path).text
     rss = feedparser.parse(response)
     activity_list = []
     for post in rss.entries:
         soup=BeautifulSoup(post['content'][0]['value'], 'html.parser')
         activity_list.append(soup.find_all('p')[2].get_text())
     return activity_list

print("hello")
print (get_runalyze('mtastafford'))
print (get_thecrag('revengineer'))
