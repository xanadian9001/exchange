# Pyrix Spleef Challenge
# This starts a spleef-like event centered at x_c, y, z_c.  You can change those variable to whatever
# you want, wherever you plan on having the center of the board.  This script will do one of four things.
# The first 3 will start happening once just 1 player is within range.  The fourth one will occur when
# at least 1 player is just out of range of the board.
# 1.  Place 9 blocks of magma that will inflict some damage
# 2.  Begin an event where some "warning blocks" are placed, and in 100 "ticks," those blocks are removed
#	  completely, causing the player to fall (if he didn't move off of the warning blocks in time)
# 3.  Repair (maybe) some of the "damaged" board.
# 4.  Repair *all* the holes (where there is minecraft:air) to "reset" the board.  The magma stays.
# Note that the locations of events 1-3 are random.  You could easily change it so that the "warning blocks"
# are placed UNDER some random player, but I didn't do that here.

import math
import time
from random import randint
import collections

global x
global y
global z
global id
global x_t
global z_t
global event_thingie
global rebuild_complete

y = 66 # the height of the spleef board
x_c = 100 # defines center
z_c = 100 # defines center
max_r = 50 # maximum radius from center
x = 100
z = 100
x_t = 100
z_t = 100
id = 600 # if you're combining this with the Wall-O-Fire, you better not have this at 0 or there will be a conflict
event_thingie = {} # a dictionary of lists for id, x, and z (I hope)
rebuild_complete = False

def init(event):
	event.npc.timers.clear()

def timer(event):
	
	if event.id == 0 or event.id == 1: # keep the event.id == 1 if you're using rotating_fire_beam.py
		#result = "Timer ID is " + str(id) + " with coordinates x = " + str(x) + ", z = " + str(z) + " at time " + str(time.clock())
		#event.npc.say(result)
		dummy = True
	#elif event.id == id: # sometimes *this* triggers....
		#x_t = event_thingie[id][0]
		#z_t = event_thingie[id][1]
		#command2 = "execute @s " + str(x_t) + " " + str(y) + " " + str(z_t) + " fill " + str(x_t - 1) + " " + str(y) + " " + str(z_t - 1) + " " + str(x_t + 1) + " " + str(y) + " " + str(z_t + 1 ) + " minecraft:air"
		#event.npc.executeCommand(command2)
		# garbage collection
		#del event_thingie[event.id]
	else: # and sometimes *this* triggers, even when event.id == id.  no idea why.
		x_t = event_thingie[event.id][0]
		z_t = event_thingie[event.id][1]
		coin_toss = event_thingie[event.id][2]
		command2 = "execute @s " + str(x_t) + " " + str(y) + " " + str(z_t) + " fill " + str(x_t - 1) + " " + str(y) + " " + str(z_t - 1) + " " + str(x_t + 1) + " " + str(y) + " " + str(z_t + 1 ) + " minecraft:air"
		event.npc.executeCommand(command2)
		command = "execute @s "  + str(x_c) + " " + str(y) + " " + str(z_c) + " playsound minecraft:block.gravel.break master @a "+ str(x) + " " + str(y + 0.75) + " " + str(z) +" 1 0.5"
		event.npc.executeCommand(command)
		if coin_toss == 1: # this can be used if you want 2 different outcomes
			event.npc.say("HEADS")
		elif coin_toss == 0:
			event.npc.say("TAILS")
		else:
			event.npc.say("I lost my coin!  :(")
		# garbage collection
		del event_thingie[event.id]


def tick(event):
	global event_thingie
	global id
	global rebuild_complete
	if event.npc.world.getClosestEntity(event.npc.getPos(), 49, 1) != None: #someone is nearby, let's do some nasty shit
		rebuild_complete = False
		d_10 = randint(0,10)
		#event.npc.say(str(d_10))
		# every tick, whether we need it or not, let's calculate where the ...event... will happen:
		r = randint(3,48) # how far out is this going to happen
		a = randint(0,359) # at what angle from center
		# now for some ...*gulp*... trigonometry.  what is new X and new Y?
		radians = math.radians(a)
		x = int(math.cos(radians) * r) + x_c
		z = int(math.sin(radians) * r) + z_c
		location = "x = " + str(x) + ", z = " + str(z)
		if d_10 == 0 or d_10 == 1: # magma blocks
			command = "execute @s " + str(x_c) + " " + str(y) + " " + str(z_c) + " fill " + str(x - 1) + " " + str(y) + " " + str(z - 1) + " " + str(x + 1) + " " + str(y) + " " + str(z + 1 ) + " minecraft:magma"
			event.npc.executeCommand(command)
			command = "execute @s "  + str(x_c) + " " + str(y) + " " + str(z_c) + " playsound minecraft:block.lava.ambient master @a "+ str(x) + " " + str(y + 0.75) + " " + str(z) +" 1 1"
			event.npc.executeCommand(command)
		elif d_10 == 2: # open holes
			command = "execute @s " + str(x_c) + " " + str(y) + " " + str(z_c) + " fill " + str(x - 1) + " " + str(y) + " " + str(z - 1) + " " + str(x + 1) + " " + str(y) + " " + str(z + 1 ) + " minecraft:wool 14"
			event.npc.executeCommand(command)
			command = "execute @s " + str(x_c) + " " + str(y) + " " + str(z_c) + " particle fallingdust " + str(x) + " " + str(y + 0.75) + " " + str(z) + " 0.75 0.5 0.75 0.02 25"
			event.npc.executeCommand(command)
			command = "execute @s "  + str(x_c) + " " + str(y) + " " + str(z_c) + " playsound minecraft:weather.rain master @a "+ str(x) + " " + str(y + 0.75) + " " + str(z) +" 1 0.5"
			event.npc.executeCommand(command)
			id = int(time.clock())+600 # it's actually the "time", but I'm using it as a unique identifier for this particular object
			event.npc.timers.forceStart(id,100,False)
			# flip a coin ... testing to see if I can have multiple delayed events w/o it being a pain in the ass to code
			coin = randint(0,1)
			event_list = [x, z, coin]
			event_thingie[id] = event_list
		elif d_10 == 3 or d_10 == 4 or d_10 == 5 or d_10 == 6: # replace land
			command = "execute @s " + str(x_c) + " " + str(y) + " " + str(z_c) + " fill " + str(x - 1) + " " + str(y) + " " + str(z - 1) + " " + str(x + 1) + " " + str(y) + " " + str(z + 1 ) + " minecraft:obsidian"
			event.npc.executeCommand(command)
		else:
			dummy = True
	elif event.npc.world.getClosestEntity(event.npc.getPos(), 70, 1) != None: #someone is getting closer...or maybe moving out of the 50m range?...
		# this routine is for cleanup.  It's a *bit* laggy.  Just FYI.
		# do a nested for loop that replaces all the holes with something solid
		if rebuild_complete == False:
			for this_x in range(-50,50):
				for this_z in range(-50,50):
					h = math.sqrt(this_x ** 2 + this_z ** 2)
					if h < 50:
						event.npc.getWorld().setBlock(this_x+x_c, y, this_z+x_c, "minecraft:obsidian", 0)
						#command = "execute @s ~ ~ ~ setblock " + str(int(x_this + x_c)) + " " + str(y) + " " + str(int(z_this + z_c)) + " minecraft:obsidian 1 keep"
						#event.npc.executeCommand(command)
			rebuild_complete = True
		#report = "execute @s ~ ~ ~ tell xanadian Out of range."
		#event.npc.executeCommand(report)
	else:
		dummy = True
