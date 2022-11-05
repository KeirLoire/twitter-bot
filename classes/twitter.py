import tweepy
from classes.openai import Model

class Listener(tweepy.StreamingClient):
    def configure_responder(self, consumer_key, consumer_secret, access_token, access_token_secret, bot_user_id, user_id_to_like):
        self.responder = tweepy.Client(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            access_token = access_token,
            access_token_secret = access_token_secret
        )

        self.bot_user_id = bot_user_id
        self.user_id_to_like = user_id_to_like

    def configure_stream_rules(self, rules):
        existing_rules = self.get_rules().data

        if existing_rules:
            self.delete_rules(existing_rules)

        for rule in rules:
            self.add_rules(tweepy.StreamRule(rule))

    def on_tweet(self, tweet):
        print(tweet.data)
        author = self.responder.get_user(id=tweet.author_id, user_auth=True).data

        # Respond to mentions/replies to you.
        if tweet.entities:
            for mention in tweet.entities["mentions"]:
                if int(mention["id"]) == int(self.bot_user_id):
                    message = f"{author.name}:{tweet.text}"

                    # Get text from quoted/replied tweet
                    if tweet.referenced_tweets:
                        if tweet.referenced_tweets[0].type in ["quoted", "replied_to"]:
                            reference_tweet = self.responder.get_tweet(tweet.referenced_tweets[0].id, user_auth=True, expansions=["author_id"]).data
                            reference_author = self.responder.get_user(id=reference_tweet.author_id, user_auth=True).data

                            message = f"{reference_author.name}:{reference_tweet.text}\n{author.name}:{tweet.text}"

                    response = Model.submit_query(message)
                    self.responder.create_tweet(in_reply_to_tweet_id=tweet.id, text=response)

        # Like tweets of these users
        if(tweet.author_id in self.user_id_to_like):
            # Ignore if it is just a retweet
            if tweet.referenced_tweets:
                if tweet.referenced_tweets[0].type == "retweeted":
                    return

            self.responder.like(tweet.id)

    def on_connection_error(self):
        self.disconnect