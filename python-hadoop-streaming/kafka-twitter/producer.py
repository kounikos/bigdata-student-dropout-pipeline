import tweepy
from kafka import KafkaProducer

access_token = "<REDACTED>"
access_token_secret = "<REDACTED>"
api_key = "<REDACTED>"
api_secret = "<REDACTED>"
bearer_token = "<REDACTED>"

# authenticating as my app
# client = tweepy.streamingClient(bearer_token=bearer_token)

# authenticating as myself
# client = tweepy.streamingClient(consumer_key=api_key, consumer_secret=api_secret, access_token=access_token, access_token_secret=access_token_secret)

# filter rules
keywords = '"weather" OR "forecast" OR "temperature" OR "shiny" OR "rainy"'

producer = KafkaProducer(bootstrap_servers="localhost:9092")

topic_name = "twitter_data"

class TwitterStreamer():
    def stream_tweets(self):
        while True:
            stream = tweepy.StreamingClient(bearer_token=bearer_token)
            stream.add_rules(tweepy.StreamRule(keywords))
            stream.filter()
            
class ListenerTS(tweepy.StreamingClient):
    def on_data(self, data):
        producer.send(topic_name, str(data))
        print(data)
        return True

if __name__ == "__main__":
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets()