#!/usr/bin/env python3
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import discord
import os

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
step = 0
chat_ids = None

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):    
        global step   
        global chat_ids

        if message.author == client.user:
            return
        if message.channel.id == 840490174684069938 or message.channel.id == 843100497488904272:

            new_user_input_ids = tokenizer.encode(message.content + tokenizer.eos_token, return_tensors='pt')
            print(step)
            print(chat_ids)
            bot_input_ids = torch.cat([chat_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids       
            
            #diversity_penalty (float, optional, defaults to 0.0) – This value is subtracted from a beam’s score if it generates a token same as any beam from other group at a particular time. Note that diversity_penalty is only effective if group beam search is enabled.
            chat_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

            messagebot = tokenizer.decode(chat_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

            tosend = "no comment" if messagebot == "" else messagebot
            await message.channel.send(tosend)
            print('Message from {0.author}: {0.content}'.format(message))
            print('Message from bot {}'.format(tosend))

            # if step < 5:
            #     step += 1
            # else:
            #     step = 0
            #     chat_ids = None

client = MyClient()
client.run('Insert discord token here')
