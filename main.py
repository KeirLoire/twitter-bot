import configparser
import json
from classes.twitter import Listener
from classes.openai import Model

def main():
    # Get configuration values
    config = configparser.RawConfigParser()
    config.read('config.ini')

    # Configure OpenAI model
    Model.set_api_key(config["openai"]["api_key"])

    # Configure Twitter Stream Listener
    listener = Listener(config["twitter"]["bearer_token"])
    listener.configure_stream_rules(json.loads(config["twitter_targets"]["stream_rules"]))

    # Configure Twitter Sender
    listener.configure_responder(
        config["twitter"]["consumer_key"],
        config["twitter"]["consumer_secret"],
        config["twitter_generated"]["bot_access_token"],
        config["twitter_generated"]["bot_token_secret"],
        config["twitter_targets"]["bot_user_id"],
        json.loads(config["twitter_targets"]["user_id_to_like"]),
    )

    # Start Stream Listener
    listener.filter(expansions=["author_id", "in_reply_to_user_id", "entities.mentions.username", "referenced_tweets.id.author_id"])

if __name__ == "__main__":
    main()