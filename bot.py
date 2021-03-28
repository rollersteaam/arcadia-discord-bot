import os
from chatterbot import conversation

import discord
from dotenv import load_dotenv
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.conversation import Statement

from bot_modules import tts, commands
from bot_commands import master_command_list, join_channel_command

print("Arcadia starting...")

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

voice_client: discord.VoiceClient = None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: discord.Message):
    global voice_client

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

    command = commands.match(statement.text, master_command_list)

    if command is not None:
        if command == join_channel_command:
            if message.author.voice is None:
                await message.channel.send("No voice state...?")
                return
            
            if message.author.voice.channel is None:
                await message.channel.send("You're not in a channel.")
                return

            voice_channel: discord.VoiceChannel = message.author.voice.channel

            try:
                voice_client = await voice_channel.connect(timeout=5)
            except:
                await message.channel.send("I had issues joining you, sorry. Maybe try again?")
                raise

    if actualText.strip().startswith("say:"):
        newMessage = actualText.split("say:")[1]
        statement.text = newMessage

    await message.channel.send(statement)

    # sapi_stream = tts.Sapi5TTSAudioStream(statement.text)
    tts.say_phrase(statement)

    if voice_client is not None:
        # voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio("local"))

should_train = input("Should I train? (no)")

# Train bot only needs to happen once as training is stored in DB
if should_train.lower() == "yes":
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')

    # Train app-based commands
    commands.extend_with_commands(master_command_list, lace_commands)
    lace_trainer.train(lace_commands)

print("Connecting to Discord...")

client.run(TOKEN)
