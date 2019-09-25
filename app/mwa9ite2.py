# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import json
import requests
from time import gmtime, strftime
from Bot import Bot
from ChatLot import ChatLot
from apscheduler.scheduler import Scheduler
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from Model import *
app = Flask(__name__)


cht = ChatLot()


PAT = 'EAAGqXDcG2NQBACQLymj7Y3kqM0nvZCToZCnT6YLERsLGOLKMca0AEKd83zak9JOiOzInvZCMdQgc9x4r5thQYBwDRVfHxh1NaYBr55KNAYnZAg2fCwjVG2iBcNi9bAcsV0pXGrV9fbhcByNLnri26V6XXfedjDWze00WPX3OrAZDZD'
bot = Bot(PAT)


cron = Scheduler(daemon=True)
cron.start()

@cron.interval_schedule(minutes=990)
def job_function():

  bot.send_text_message('1222114411231563','rahi '+strftime("%H:%M", gmtime()))
 
@app.route('/', methods=['GET'])
def handle_verification():
  print ("Handling Verification.")
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me_':
    print ("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print ("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)

    
@app.route('/dataimport', methods=['POST'])
def handle_on_off():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)




@app.route('/', methods=['POST'])
def handle_messages():
  print ("Handling Messages")
  payload = request.get_data()
  print (payload)
  for sender, message in messaging_events(payload):
        print ("Incoming from %s: %s" % (sender, message))
        bot.send_text_message(sender,"ok")
        try:
            rep = cht.get_respond(message.decode("utf-8"))
            if "je suis stupide ne " not in rep :
                process_rep(rep,sender)
            else :
                bot.send_text_message(sender,rep)
        except Exception as e:
            print("respond user")

  return "ok"
def process_rep(rep,sender):
    try:
      data = json.loads(rep)
      print(data)
      bot.send_seen(sender)
      bot.send_text_message(sender,"ok")
      for element in data:
          if element["type"] == 'image':
              bot.send_typing(sender)
              bot.send_image_url(sender, element["rep"])
          elif element["type"] == 'text':
              bot.send_typing(sender)
              bot.send_text_message(sender," 🕌 "+element["rep"]["commune"]+" Wilaya "+element["rep"]["wilaya"]) 
              r = requests.get("http://api.aladhan.com/timingsByCity?city="+element["rep"]["commune"]+"%20"+element["rep"]["wilaya"] +"&country=DZ&method=5")
              data =r.json() 
              bot.send_text_message(sender, u'  الفجر '+data["data"]["timings"]["Fajr"])
              bot.send_typing(sender)
              bot.send_text_message(sender, u'  الشروق '+data["data"]["timings"]["Sunrise"])
              bot.send_typing(sender)
              bot.send_text_message(sender, u'  الظهر '+data["data"]["timings"]["Dhuhr"])
              bot.send_typing(sender)
              bot.send_text_message(sender, u'  العصر '+data["data"]["timings"]["Asr"])
              bot.send_typing(sender)
              bot.send_text_message(sender, u'  المغرب '+data["data"]["timings"]["Maghrib"])
              bot.send_typing(sender)
              bot.send_text_message(sender, u'  العشاء '+data["data"]["timings"]["Isha"])
              bot.send_typing(sender)
          elif element["type"] == 'text_button':
              bot.send_typing(sender)
              bot.send_button_message(sender,element["rep"],element["buttons"]) 
          elif element["type"] == 'text_option':
              bot.send_typing(sender)
              bot.send_message_option(sender,element["rep"],element["options"]) 
          elif element["type"] == 'audio':
              bot.send_typing(sender)
              bot.send_audio_url(sender,element["rep"])
          elif element["type"] == 'video':
              bot.send_typing(sender)
              bot.send_video_url(sender,element["rep"])
          elif element["type"] == 'file':
              bot.send_typing(sender)
              bot.send_file_url(sender,element["rep"])
          elif element["type"] == 'typing':
              bot.send_typing(sender)
          elif element["type"] == 'seen':
              bot.send_seen(sender)
          elif element["type"] == 'check':
              get_respond(sender,element["rep"])
          print (element["type"])
    except Exception as e:
        bot.send_text_message(sender,rep) 
        print('What '+e) 
        pass
def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"

if __name__ == "__main__":
    app.run()