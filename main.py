from tdlib import log
import discord
import game

#----------------------------------------------------------------------------------------------------

client = discord.Client()

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')
	log(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author == client.user: return
	if message.content[0] !='.': return
	command = message.content[1:].split()

	if command[0] == 'help':
		await message.channel.send('''spell [spell (separate words with -)] - provides full description of the spell
search [term] - returns all spells that contain term
class [class] - links to every spell available to that class''')

	elif command[0] == 'class':
		await message.channel.send('http://dnd5e.wikidot.com/spells:'+command[1])

	elif command[0] == 'spell':
		data = neat(command[1].lower())
		info = ''
		for i in data:
			info += i + '\n'
		await message.channel.send(info)
	
	elif command[0] == 'search':
		data = search(command[1])
		info = ''
		for i in data:
			info += i + '\n'
		if info != '':
			await message.channel.send(info)
		else:
			await message.channel.send('no results found - try using **.class**')

	elif command[0] == 'logs':
		if len(command) < 2: command.append(10)
		sendlogs = readlist('log.txt')[0-int(command[1]):]
		messagers = '```'
		for i in sendlogs: messagers += '\n'+i
		messagers += '```'
		await message.channel.send(f'last {int(command[1])} logs:\n{messagers}')

	else: await message.channel.send(f'{command} command not recognised')

#----------------------------------------------------------------------------------------------------

with open(token.txt,'r') as TOKEN:
	client.run(TOKEN)