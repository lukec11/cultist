import slack
import json
import os


config = os.environ
slackToken = config['slackToken']
legacyToken = config['legacyToken']
approvedChannel = config['approvedChannel']
triggerWord = config['triggerWord']

with open('cults.json') as f:
    cults = json.load(f)

# Initialize slack as a web client
slack_client = slack.WebClient(token=legacyToken)


def addToChannel(UID):  # Function to add user (UID) to all channels in 'cults' list
    for i in cults:
        try:
            slack_client.conversations_invite(
                token=legacyToken, channel=i, users=UID)
            print(f'Added to {i}!')
        except:
            print(f'Failed to add to {i}!')


def slackReaction(token, channel, ts):  # Function to add check mark reaction
    slack_client.reactions_add(
        token=legacyToken, channel=channel, timestamp=ts, name="heavy_check_mark")


@slack.RTMClient.run_on(event="message")  # Runs RTM to listen for new messages
def on_message(**payload):
    data = payload['data']

    user = data['user']  # User who posted the message
    message = data['text']  # Message text itself
    channel = data['channel']  # Channel the message was posted in
    ts = data['ts']  # Timestamp of the message

    try:
        if message.startswith('!add') and channel == approvedChannel:
            user = (message[len(triggerWord)+1: len(message)]
                    ).replace('<', '').replace('@', '').replace('>', '')  # Strips unnecessary characters from UID

            addToChannel(user)
            slackReaction(legacyToken, channel, ts)
        else:
            # Check for non-commands in the command channel
            print(f'Command not recognized! Text was {message}.')
    except KeyError as k:  # Check for slack threaded messages
        print('Threaded message. Ignore!')
    except BaseException as e:  # Check for any other problem
        print(f'There was a problem! {e}')


# Run the program
rtm_client = slack.RTMClient(token=slackToken)
print('Bot has started!')
rtm_client.start()
