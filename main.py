import discord
import os
import sys
import json
import time
import random
import requests
import pytz
from datetime import datetime

# Importing Settings
settingU = json.load(open('settings.json'))
jtopy = json.dumps(settingU)
setting = json.loads(jtopy)
token = setting['token']
channelid = setting['channelID']
apikey = setting["APIkey"]
webhookID = setting["webhookID"]

client = discord.Client()

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	f = open("anomaly.txt", "a+")
	channel = await client.fetch_channel(channelid)
	webhook = await client.fetch_webhook(webhookID)
	await webhook.send(content="Starting AutoFish")
	while True:
		print("Fishing")
		await channel.send("ff")
		
		time.sleep(1)
		tz_NY = pytz.timezone('America/New_York')
		datetime_NY = datetime.now(tz_NY)
		ctime = datetime_NY.strftime("%H:%M:%S")
		
		async for message in channel.history(limit=1):
			if len(message.embeds) == 1:
				print("1 Embed")
			elif len(message.embeds) == 2:
				print("2 Embeds")
				ecount = 0
				f.write("---------------------------------\n" + ctime + "\n")
				f.write("2 Embeds Detected\n")
				for embed in message.embeds:
					ecount += 1
					f.write(f"""Embed {ecount}:
Title: {embed.title}
Description: {embed.description}
""")
				f.write("\n\n")
				f.flush()
			else:
				print(str(len(message.embeds)) + "Embeds")
				ecount = 0
				f.write("---------------------------------\n" + ctime + "\n")
				f.write("Random Embeds Detected")
				for embed in message.embeds:
					ecount += 1
					f.write(f"""Embed {ecount}:
Title: {embed.title}
Description: {embed.description}
""")
				f.write("\n\n")
				f.flush()
			

			for embed in message.embeds:
				#print(f"""Title: {embed.title}
#Description: {embed.description}
#""")
				if "you caught" in str(embed.title).lower():
					print(f"{ctime} | Caught Something!\n")
					await webhook.send(content="Success")
				elif "anti-bot" in str(embed.title).lower():
					print(f"{ctime} | Captcha Detected, Pausing\n")
					await webhook.send(content="@everyone CAPTCHA DETECTED, PAUSING")
					input("Press Enter to Continue")
				else:
					f.write(f"""{ctime} \nTitle: {embed.title}
Description: {embed.description}
""")
					f.write("\n\n")
					f.flush()
		
		time.sleep(random.uniform(1.5, 2))
		

client.run(token, bot=False)
