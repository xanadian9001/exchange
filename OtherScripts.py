# Other Useful Scripts to work with the exchange:

# remove a # of item from the player, for when they buy a commodity: ... this is just for proof of concept, btw...
"""
def interact(event):
	# This will use arg 1 (item), 0, and the amount you need to withdraw of arg 1
    if event.player.removeItem("soupamod:goldcoin", 0, 10):
	    event.npc.say("Pass.")
    else:
	    event.npc.say("Fail.")
"""

		
# need to figure out how to :
#	1.  get a dialog selection to toggle between Buy and Sell (or even List)



#	2.  get a dialog selection to determine WHAT commodity the user wants to trade



#	3.  get a value (#) from user to coincide with the buy/sell of a particular commodity



# 	4.  exchange hard game currency (coins) for market value points and vice versa

def interact(event):
	# This will use arg 1 (item), 0, and the amount you need to withdraw of arg 1
    if event.player.removeItem("soupamod:goldcoin", 0, 10):
		# fetch the user's account by loading the whole damn database
		accounts = {}
		with open('D:\data\accounts.csv') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=",")
			for row in reader:
				user = row["user"]
				balance = row["balance"]
				accounts[user] = balance
		if accounts["Bob"] == None: # check to see if the user's even in the database
			accounts["Bob"] = 10
		else: 
			accounts["Bob"] += 10
		# now return the dictionary to the database with the change
		with open('accounts.csv', 'w') as csvfile:
			fieldnames = ["user", "balance"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",")
			writer.writeheader()
			for i in accounts: # loop through each account and write it to the csv
				writer.writerow("user": i, "balance": accounts[i])
	# now go check the actual file & see if it worked
	    event.npc.say("Gold deposited.")
    else:
	    event.npc.say("You don't have enough gold to make the deposit.")
			
