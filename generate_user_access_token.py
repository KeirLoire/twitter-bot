import configparser
import tweepy
import webbrowser

def main():
    # Read configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get Authorization URL
    auth = tweepy.OAuth1UserHandler(
        consumer_key = config["twitter"]["consumer_key"],
        consumer_secret = config["twitter"]["consumer_secret"],
        access_token = config["twitter"]["access_token"],
        access_token_secret = config["twitter"]["access_token_secret"],
        callback = config["twitter"]["callback_url"]
    )
    auth_url = auth.get_authorization_url()

    # Get OAuth verifier token
    print("Please authorize and get OAuth verifier token.")
    print("Opening authorization link...")
    webbrowser.open(auth_url, new=0, autoraise=True)

    # Get User Access token
    oauth_token = input("Enter OAuth verifier here:")
    user_access = auth.get_access_token(oauth_token)
    config["twitter_generated"]["user_access_token"] = user_access[0]
    config["twitter_generated"]["user_token_secret"] = user_access[1]

    # Update configuration
    with open("config.ini", "w") as configfile:
        config.write(configfile)

if __name__ == "__main__":
    main()