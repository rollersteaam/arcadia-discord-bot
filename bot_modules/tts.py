import os

import comtypes.client
import discord
import pyttsx3
from pyttsx3.drivers import toUtf8, fromUtf8

engine = pyttsx3.init()

voices = engine.getProperty('voices')

print(voices)
engine.setProperty('voice', voices[2].id)

def say_phrase(phrase: str):
    engine.save_to_file(phrase, "local")
    engine.runAndWait()

class Sapi5TTSAudioStream(discord.AudioSource):
    def __init__(self, phrase):
        # Hijack
        tts_service = engine.proxy._driver._tts

        self.stream = comtypes.client.CreateObject('SAPI.SPMemoryStream')

        # Takeover
        temp_stream = tts_service.AudioOutputStream
        tts_service.AudioOutputStream = self.stream
        tts_service.Speak(fromUtf8(toUtf8(phrase)))
        tts_service.AudioOutputStream = temp_stream

    def read(self):
        # stream_bytes = bytearray()
        # self.stream.write(stream_bytes)
        # print(stream_bytes)
        return bytes(self.stream.GetData())