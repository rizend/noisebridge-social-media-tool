from SocialMediaAction import *



class TwitterAction(SocialMediaAction):
  
  def __init__(self, slack_handle):
    SocialMediaAction.__init__(self, slack_handle)
    self.icon_emoji = ":twitter_icon_emoji:"
  
  def slack_message(self):
    return "A Twitter action has occurred."
  


class Make(TwitterAction):
  
  def __init__(self, slack_handle, content, attachments = []):
    TwitterAction.__init__(self, slack_handle)
    self.content = content
    self.attachments = attachments
    self.tweet_url = None
  
  def slack_message(self):
    return "@here Human friends! " + self.slack_handle + " has posted to our " +\
           "Twitter account! Be sure to share it! :)\nLink: " + self.tweet_url
  
  def handle():
    print("Making a new tweet.")
    self.tweet_url = "TODO"



class Reply(TwitterAction):

  def __init__(self, slack_handle, content, attachments = []):
    TwitterAction.__init__(self, slack_handle)
    self.content = content
    self.attachments = attachments
    self.reply_url = None

  def slack_message(self):
    return "@here Human friends! " + self.slack_handle + " has replied to " +\
           "a tweet via our Twitter account! Be sure to fave it! :)\nLink: " + self.reply_url

  def handle():
    print("Making a new reply.")
    self.reply_url = "TODO"



class Delete(TwitterAction):
  
  def __init__(self, slack_handle, deleted_tweet_url, deleted_tweet_content):
    TwitterAction.__init__(self, slack_handle)
    self.deleted_tweet_url = deleted_tweet_url
    self.deleted_tweet_content = deleted_tweet_content
  
  def slack_message(self):
    return "@here Human friends! " + self.slack_handle + " has deleted a " +\
           "tweet from our Twitter account! I hope you weren't too attached " +\
           "to it!\n Deleted Tweet content: " + self.deleted_tweet_content

  def handle():
    print("Deleting a tweet.")



class Share(TwitterAction):
  
  def __init__(self, slack_handle, shared_tweet_url):
    TwitterAction.__init__(self, slack_handle)
    self.shared_tweet_url = shared_tweet_url
  
  def slack_message(self):
    return "@here Human friends! " + self.slack_handle + " has retweeted a " +\
           "tweet from our Twitter account! Maybe you should RT it too!\n" +\
           "Retweeted tweet: " + self.shared_tweet_url
  
  def handle():
    print("Sharing a tweet.")



class Unshare(TwitterAction):
  
    def __init__(self, slack_handle, unshared_tweet_url):
      TwitterAction.__init__(self, slack_handle)
      self.unshared_tweet_url = unshared_tweet_url

    def slack_message(self):
      return "@here Human friends! " + self.slack_handle + " has undone a " +\
             "retweet from our Twitter account! I hope you weren't too attached " +\
             "to it!\nUnretweeted tweet: " + self.unshared_tweet_url
    
    def handle():
      print("Unsharing a tweet.")