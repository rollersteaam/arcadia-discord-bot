import os
from chatterbot import conversation

import discord
from dotenv import load_dotenv
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.conversation import Statement

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
chatbot = ChatBot('Arcadia')

lace_commands = [
    "hey",
    "How's it going? Since it seems you're talking to me, I'll now listen to you without having to use bot at the beginning.",

    "let's talk",
    "Okay, I'll start talking to you without you needing to specify that you're talking to me.",

    "stop talking",
    "Aight bro. You'll need to refer to me with 'bot,' as a prefix next time you want to speak with me.",

    "i'm done",
    "Okay, I'll stop talking. Start your message with 'bot,' if you would like to chat again."
]

lace_trainer = ListTrainer(chatbot)

conversation_users = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    messageText: str = message.content

    if not messageText.lower()[0:4] == "bot," and message.author not in conversation_users:
        return

    actualText = messageText.split("bot,")

    if len(actualText) > 1:
        actualText = actualText[1]
    else:
        actualText = actualText[0]

    print(actualText)

    statement: Statement = chatbot.get_response(actualText)

    if statement.text in [lace_commands[1], lace_commands[3]]:
        # Start conversation
        conversation_users[message.author] = True
    elif statement.text in [lace_commands[5], lace_commands[7]]:
        del conversation_users[message.author]

    await message.channel.send(statement)

should_train = input("Should I train? ")

if should_train.lower() == "yes":
    # The bot only needs training once due to its database.
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')
    lace_trainer.train(lace_commands)

print("Connecting to Discord...")

client.run(TOKEN)
