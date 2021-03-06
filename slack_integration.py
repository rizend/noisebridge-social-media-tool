import requests
from flask import Flask, request
import SocialMediaAction
import TwitterService
from secrets import * # includes SLACK_WEBHOOK_URL plus some SLACK_TOKENS



def log_action_to_slack(action):
    payload = {
        "channel": "#hook-testing",
        "username": "social-media-tool",
        "text": action.slack_message(),
        "icon_emoji": action.icon_emoji
    }
    return requests.post(SLACK_WEBHOOK_URL, json=payload)


def log_error_to_slack(err):
    payload = {
        "channel": "#hook-testing",
        "username": "social-media-tool",
        "text": err,
        "icon_emoji": ":vibration_mode:"
    }
    return requests.post(SLACK_WEBHOOK_URL, json=payload)






app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello SMT!"


###
### Services record
###

SERVICES = { \
  "twitter": TwitterService.TwitterService() \
}




###
### Utilities
###


def unknown_social_media_service_error_message(service_name):
  return "There is no social media service named `" + service_name + "`. The known services are: `" + "`, `".join(SERVICES.keys()) + "`."


def split_service(text):
  
  if -1 != text.find(":"):
    
    service_name, rest = text.split(":",1)
    service_name = service_name.strip()
    
    if service_name in SERVICES:
      
      return (None, SERVICES[service_name], rest.strip())
      
    else: return ("UnknownSocialMediaServiceError", None, None)
      
  else: return ("MalformedInputError",None,None)


def split_attachments(text):
  
  if -1 != text.find(";"):
    
    attachments, rest = text.split(";",1)
    
    return (None, map(lambda a: a.strip(), attachments.split(",")), rest.strip())
    
  else: return ("MalformedInputError", None, None)


def split_url(text):
  
  if -1 != text.find(";"):
    
    url, rest = text.split(";",1)
    
    return (None, url.strip(), rest.strip())
    
  else: return ("MalformedInputError", None, None)






###
### Routing
###



MAKE_MALFORMED_ERROR_MESSAGE = "The input you gave is malformed. It should have the format `[service]: [content]"

@app.route("/slack/make", methods=['POST'])
def make():
    
    if request.form['token'] != SLACK_MAKE_TOKEN:
        return ':('
    
    user_id = request.form['user_id']
    
    err, service, content = split_service(request.form['text'])
    
    if "MalformedInputError" == err:
      return MAKE_MALFORMED_ERROR_MESSAGE
    
    if "UnknownSocialMediaServiceError" == err:
      return unknown_social_media_service_error_message(service)
    
    attachments = []
    
    action = SocialMediaAction.Make(service, user_id, content, attachments)
    action.handle()
    
    log_action_to_slack(action)
    
    return ""



MAKE_ATTACHMENTS_MALFORMED_ERROR_MESSAGE = "The input you gave is malformed. It should have the format `[service]: [attachment], ...; [content]"

@app.route("/slack/make-attachments", methods=['POST'])
def make_attachments():

    if request.form['token'] != SLACK_MAKE_ATTACHMENTS_TOKEN:
        return ':('
    
    user_id = request.form['user_id']

    err, service, rest = split_service(request.form['text'])
    
    if "MalformedInputError" == err:
      return MAKE_ATTACHMENTS_MALFORMED_ERROR_MESSAGE
    
    if "UnknownSocialMediaServiceError" == err:
      return unknown_social_media_service_error_message(service)
      
    err, attachments, content = split_attachments(rest)
    
    if "MalformedInputError" == err:
      return MAKE_ATTACHMENTS_MALFORMED_ERROR_MESSAGE
    
    action = SocialMediaAction.Make(service, user_id, content, attachments)
    
    log_action_to_slack(action)
    
    return ""


REPLY_MALFORMED_ERROR_MESSAGE = "The input you gave is malformed. It should have the format `[service]: [url]; [content]"

@app.route("/slack/reply", methods=['POST'])
def reply():

    if request.form['token'] != SLACK_REPLY_TOKEN:
        return ':('
    
    user_id = request.form['user_id']
    
    err, service, rest = split_service(request.form['text'])
    
    if "MalformedInputError" == err:
      return REPLY_MALFORMED_ERROR_MESSAGE
    
    if "UnknownSocialMediaServiceError" == err:
      return unknown_social_media_service_error_message(service)
    
    err, reply_to_url, content = split_url(rest)
    
    if "MalformedInputError" == err:
      return REPLY_MALFORMED_ERROR_MESSAGE
    
    attachments = []
    
    action = SocialMediaAction.Reply(service, user_id, reply_to_url, content, attachments)
    
    log_action_to_slack(action)
    
    return ""



@app.route("/slack/twitter/reply-attachments", methods=['POST'])
def twitter_reply_attachments():

    if request.form['token'] != SLACK_TWITTER_REPLY_ATTACHMENTS_TOKEN:
        return ':('

    user_id = request.form['user_id']
    parts = request.form['text'].split(';',2)
    reply_to_url = parts[0].strip()
    content = parts[2].strip()
    attachments = parts[1].strip().split(',')
    
    action = SocialMediaAction.Reply(Twitter, user_id, reply_to_url, content, attachments)
    
    log_action_to_slack(action)
    return ""



@app.route("/slack/twitter/delete", methods=['POST'])
def twitter_delete():

    if request.form['token'] != SLACK_TWITTER_DELETE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    deleted_tweet_url = request.form['text']
    deleted_tweet_content = ""

    action = SocialMediaAction.Delete(Twitter, user_id, deleted_tweet_url, deleted_tweet_content)

    log_action_to_slack(action)
    return ""



@app.route("/slack/twitter/share", methods=['POST'])
def twitter_share():

    if request.form['token'] != SLACK_TWITTER_SHARE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    shared_tweet_url = request.form['text']

    action = SocialMediaAction.Share(Twitter, user_id, shared_tweet_url)

    log_action_to_slack(action)
    return ""



@app.route("/slack/twitter/unshare", methods=['POST'])
def twitter_unshare():

    if request.form['token'] != SLACK_TWITTER_UNSHARE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    unshared_tweet_url = request.form['text']

    action = SocialMediaAction.Unshare(Twitter, user_id, unshared_tweet_url)

    log_action_to_slack(action)
    return ""



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3115)