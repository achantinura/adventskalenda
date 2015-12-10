#!/usr/bin/python
import requests
import os
import time
from pyquery import PyQuery as pq
from config import Config

# call url
def sendreq_get(url):
  r = requests.get(url)
  if r.status_code == 200:
    return pq(r.content)
  else:
    return 'error %s occured' % r.status_code

# fetch data from adventskalender
def adventskalender():
  d = sendreq_get(Config.adventskalender_url)
  tage = d('.tag')

  js = []
  for i in xrange(1, len(tage)):
    day = { 'day': i, 'rewards': [] }
    for line in pq(tage[i]).find('.line'):
      rewards = {}
      rewards['artikel'] = pq(line).find('.artikel').text()
      rewards['losnr'] = pq(line).find('.losnr').text().split(', ')
      rewards['sponsor'] = pq(line).prev('h3').text()
      day['rewards'].append(rewards)
    js.append(day)
  return js
  

if __name__ == '__main__':
  # get all already opened tuerchen from adventskalender
  tuerchen = adventskalender()
  
  # get all familymembers together
  family = Config.jemand.keys()

  messages = []

  # for each member
  for member in family:
    losnr = Config.jemand[member]['losnr']
    telnr = Config.jemand[member]['handynr']
    gewonnen = False

    # check tuerchen
    for tuer in tuerchen:
      tag = tuer['day']
      for reward in tuer['rewards']:
        
        # and if you have a hit
        if losnr in reward['losnr']:
          message = Config.msg % (member, losnr, reward['artikel'], reward['sponsor'])
          messages.append(message)
          gewonnen = True

          # notify the lucky winner 
          os.system(Config.command % (telnr, message.encode('utf-8')))
          time.sleep(2)
    if gewonnen == False:
      message = Config.msg_fail % (member, losnr)
      messages.append(message)

      # notify the poor looser
      os.system(Config.command % (telnr, message.encode('utf-8')))
      time.sleep(2)
