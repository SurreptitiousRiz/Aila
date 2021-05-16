#!/usr/bin/env python3
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch
import discord
import os

mname = 'facebook/blenderbot-400M-distill'
model = BlenderbotForConditionalGeneration.from_pretrained(mname).to("cuda")
tokenizer = BlenderbotTokenizer.from_pretrained(mname)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):    

        if message.author == client.user:
            return
        if message.channel.id == 840490174684069938 or message.channel.id == 843100497488904272:

            UTTERANCE = message.content
            inputs = tokenizer([UTTERANCE], return_tensors='pt').to("cuda")
            reply_ids = model.generate(**inputs).to("cuda")
            reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
            print(reply)
            await message.channel.send(reply)
            #Add global variable to store conversations, ending it after 5 turns perhaps and printing "moving on"

client = MyClient()
client.run('ODA3MzUzMzcyNzMwNTg5MTg0.YB2waw.EoOqw7Ff2VElUsFw5kp_-xQeCew')