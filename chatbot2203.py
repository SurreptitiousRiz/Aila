#!/usr/bin/env python3
import datetime
from aiohttp import content_disposition_filename
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import discord
import os
import sys

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
step = 0
chat_history_ids = None
chat_history = []
channel_id = ''
token = ''

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    
    def torch_delete(tensor, indices):
        mask = torch.ones(tensor.numel(), dtype=torch.bool)
        mask[indices] = False
        return tensor[mask]

    async def on_message(self, message):    
        global step   
        global chat_history_ids
        global chat_history

        if message.author == client.user:
            return
        if message.channel.id == channel_id:
            try:
                with torch.no_grad():

                    input_ids = tokenizer.encode(message.content + tokenizer.eos_token, return_tensors='pt')

                    if chat_history_ids is not None:
                        input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
                                       
                    chat_history_ids = model.generate(
                        input_ids,
                        do_sample=True, 
                        max_length=1000, 
                        top_k=50, 
                        top_p=0.95,
                        temperature=0.7,
                        pad_token_id=tokenizer.eos_token_id
                    )

                    output = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
                    print(chat_history_ids)

                    tosend = "no comment" if output == "" else output
                    await message.channel.send(tosend)
                    step += 1
                    if step > 2:
                        chat_history_ids = None
                        step = 0
                   
            except:
                print(sys.exc_info()[0])
                with torch.no_grad():
                    
                    tosend = "Try again."
                    await message.channel.send(tosend)
                    step = 0
                    chat_history_ids = None

client = MyClient()
client.run(token)
