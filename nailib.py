import time # for logs

def log(message, file='log.txt', stamp=True):
	with open(file,'a') as l:
		if stamp == True: l.write('\n' + time.strftime("%d/%m %H:%M:%S ") + message)
		else: l.write('\n' + message)