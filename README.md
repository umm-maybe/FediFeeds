# FediFeeds
Bot that scans the public feed of a Mastodon instance and bookmarks toots on topics you specify.

Under the hood, this uses a machine learning model which can classify the probability that a piece of text is on any of a list of topics using a technique called MNLI.  It will run faster on a GPU, but should also work on CPU provided there is sufficient RAM available to load the model.

# How to install
The below instructions assume you have git, Python 3 and Pip already installed.

```
git clone https://github.com/umm-maybe/FediFeeds
python3 -m venv env
source env/bin/activate
pip3 install -Ur requirements.txt
```

# Configuration
Log in to your Mastodon instance, go to Preferences > Development and register an app.  Copy the access token.

Open "config-example.yaml" and and paste the access token from the previous step in the appropriate place on Line 2.  Change line 1 to refer to your Mastodon instance's URL.  Replace the dummy topic keywords in the topic list with the topics that interest you.

The "match_level" parameter sets a probability threshold (between 0 and 1) indicating at what level of relevance you want to bookmark a toot.  For example, 0.60 means that the MNLI model is about 60% sure the toot is on-topic, and it will bookmark said toot if you set a match_level below this number.

Save the edited configuration file as something else, e.g. "my-config.yaml"

# Usage
After configuring the bot, run it at the command line using the following:
`python3 feedwatch.py my-config.yaml`

Run it on a VPS or use tmux if you don't want to leave your terminal open.  Or, you can watch the status messages that the bot will post in the console.

Later, when you login to Mastodon on web or using your favorite mobile client, your bookmarks should contain toots selected for you by your very own machine learning algorithm!

# Caveats
This implementation has no reinforcement learning, meaning there's no way to give input that will affect the results besides the list of topics and relevance threshold.  If you don't like the results, play with these parameters and try again.

