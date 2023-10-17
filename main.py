from tdlib import log
import discord
import game

#----------------------------------------------------------------------------------------------------


intents = discord.Intents.default() #idk what these two lines do but the docs say you need them now
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')
	log(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	print('seen message!')
	if message.author == client.user: return # if it's the bot's message
	if message.content[0:1] !='.m': return
	command = message.content[3:].split()

	if command[0] == 'help':
		await message.channel.send('''idk lol pester dillon''')
	
	elif command[0] == 'start':
		player1 = message.author
		player2 = command[1] # TODO: see if this can be done by @ing
		print(f'd: player1 = {player1}')
		print(f'd: player2 = {player2}')
		# setup board
	
	elif command[0] == 'place':
		if message.author == player1:
			pass # use game.add where you put in 1
		elif message.author == player2:
			pass # use game.add where you put in 2


	elif command[0] == 'show':
		await message.channel.send('http://dnd5e.wikidot.com/spells:'+command[1])

	else: await message.channel.send(f'{command} command not recognised')

#----------------------------------------------------------------------------------------------------

with open('token.txt','r') as TOKEN:
	client.run(TOKEN.read())