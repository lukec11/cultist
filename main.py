import slack
import json


with open('config.json') as f:
    config = json.load(f)
    slackToken = config['slackToken']
    legacyToken = config['legacyToken']
    approvedChannel = config['approvedChannel']
    triggerWord = config['triggerWord']
    cults = config['channelList']

slack_client = slack.WebClient(token=legacyToken)


def addToChannel(UID):
    for i in cults:
        try:

            slack_client.conversations_invite(
                token=legacyToken, channel=i, users=UID)
            print(f'Added to {i}!')
        except:
            print(f'Failed to add to {i}!')


def slackReaction(token, channel, ts):
    slack_client.reactions_add(
        token=legacyToken, channel=channel, timestamp=ts, name="heavy_check_mark")


@slack.RTMClient.run_on(event="message")
def on_message(**payload):

    data = payload['data']
    user = data['user']
    message = data['text']
    channel = data['channel']
    ts = data['ts']

    try:
        if message.startswith('!add') and channel == approvedChannel:
            user = (message[len(triggerWord)+1: len(message)]
                    ).replace('<', '').replace('@', '').replace('>', '')

            addToChannel(user)
            slackReaction(legacyToken, channel, ts)
        else:
            print(f'Command not recognized! Text was {message}.')
    except KeyError as k:
        print('Threaded message. Ignore!')
    except BaseException as e:
        print(f'There was a problem! {e}')


rtm_client = slack.RTMClient(token=slackToken)

print('Bot has started!')
rtm_client.start()
