#!/usr/bin/env python3
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import discord

mname = 'facebook/blenderbot-400M-distill'
model = BlenderbotForConditionalGeneration.from_pretrained(mname)
tokenizer = BlenderbotTokenizer.from_pretrained(mname)
memory = ''
step = 0

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):    
        global memory
        global step 

        if message.author == client.user:
            return
        if message.channel.id == 843415631244165120 or message.channel.id == 840490174684069938:

            text = message.content
            #print(text)
            inputs = tokenizer([text], return_tensors='pt')
            reply_ids = model.generate(**inputs)
            reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]


            await message.channel.send(reply)

client = MyClient()
client.run('ODA3MzUzMzcyNzMwNTg5MTg0.YB2waw.EoOqw7Ff2VElUsFw5kp_-xQeCew')