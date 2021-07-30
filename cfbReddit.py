import cfbBot
import praw
from config_bot import *

# Reddit stuff
r = praw.Reddit(
    user_agent="cfbBot 0.0.1 by herumph",
    client_id=ID,
    client_secret=SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASS,
)

sub = "cfbsecret"
# sub = "RumphyBot"
subreddit = r.subreddit(sub)
contributors = []

# Fetching arrays
already_done = cfbBot.get_array("already_done")

# Looking at comments
for comment in r.subreddit(sub).comments(limit=25):
    if comment.id not in already_done and str(comment.author) != "cfbBot":
        # marking comment as read if it's a reply
        # this ensures that the PM part does not respond as well
        comment.mark_read()
        already_done.append(comment.id)
        # Making sure the already_done file doesn't get too big.
        del already_done[0]
        cfbBot.write_out("already_done", already_done)

        # Saving comment
        comment_list = str(comment.body)
        comment_list = comment_list.split()

        # passing off to get reply and replying
        reply = cfbBot.call_bot(comment_list, comment.author, contributors)

        if reply == "posted!":
            title = "WHOA!"
            selftext = "he has trouble with the snap!"
            subreddit.submit(title=title, selftext=selftext, send_replies=False)

        if reply != "":
            comment.reply(reply)


# sorting through unread DMs
for pm in r.inbox.unread(limit=25):
    pm.mark_read()
    # only responding to pm's, not comment replies
    if not pm.was_comment:
        body = str(pm.body)
        body = body.split()

        reply = cfbBot.call_bot(body, pm.author, contributors)

    # Responding
    if len(reply) > 1:
        pm.author.message(pm.subject, reply)
