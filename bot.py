import praw
import os
import datetime

now = datetime.datetime.now()
filename = "champions.txt"

# Use simple text file storage for champion names
if not os.path.isfile(filename):
    champion_names = []
else:
    with open(filename, "r") as f:
        champion_names = f.read()
        champion_names = champion_names.split("\n")

        # remove errant entries
        champion_names = list(filter(None, champion_names))

# get the relevant subreddits
reddit = praw.Reddit("bot1")
all_sub = reddit.subreddit("all")
champion_sub = reddit.subreddit("ChampionsOfReddit")

# find today's "Champion of Reddit", avoiding users who have been championed already
for post in all_sub.top(time_filter="day", limit=10):
    if post.author not in champion_names:

        # add the name to the champion names file
        champion_names.append(post.author.name)
        with open(filename, "w") as f:
            for name in champion_names:
                f.write(name + "\n")

        # post the new champion's information to r/ChampionsOfReddit
        champion_sub.submit(
            post.author.name,
            selftext="u/" + post.author.name +
                     " became a Champion of Reddit on this day, " +
                     now.strftime("%Y-%m-%d") +
                     ", bringing to us this masterpiece:\n\n\"[" +
                     post.title + "](https://www.reddit.com/r/" +
                     post.subreddit.display_name +
                     "/comments/" + post.id + ").\""
        )
        
        # leave a comment on the new champion's "winning" post, letting them know they have been recorded
        post.reply(
            "#Praise be to the newest Champion of Reddit, u/" +
            post.author.name +
            "!\n\n[Let us not forget the Champions of yore...](https://www.reddit.com/r/ChampionsOfReddit/)"
        )

        break
