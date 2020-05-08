#!/usr/bin/env python3

#only tested on ubuntu 18.04

import subprocess
import os
import re
import time
import signal

#The URL
URL = '"youtube.com"'
#The path for the temporary profiles
USR_DATA_DIR_PATH = "/tmp/tmpChromiumProfile"
UPDATE_TIME = 5


print("Python display script started")


chromium_flags = ["--noerrdialogs", "--disable-session-crashed-bubble", "--disable-infobars", "--new-window", "--kiosk", "--disable-features=TranslateUI"]


print("Chromium flag:")
for s in chromium_flags: print ("\t"+s)

print("Building Chromium command")

chromium_command = "chromium-browser "
for f in chromium_flags:
	chromium_command += f + " "

#adding the window options and leaving format parameter for later
chromium_command += "--window-position={},{} "
#adding the custom user-data-dir with format parameter
chromium_command += "--user-data-dir={} "
chromium_command += URL

#Clear old directories
os.system("rm -rf " + USR_DATA_DIR_PATH + "*")

print("Chromium command:\n\t{}".format(chromium_command))

print("Getting screen informations")

current_total_screen_res = ""

total_screen_regex = "current \d+ x \d+"
screen_positions_regex = "\d+x\d+\+\d+\+\d+"

chromium_processes = {}

screen_counter = 0

while True:
	print("Getting screen informations")
	xrandr_command = subprocess.Popen("xrandr", stdout=subprocess.PIPE)
	xrandr_out = str(xrandr_command.stdout.read())

	#getting current total screen resolution (all monitors combined)


	total_screen_res = re.search(total_screen_regex, xrandr_out)
	total_screen_res = total_screen_res.group(0).split(" ", 1)[1]


	#check if all windows need to be setup again
	if current_total_screen_res != total_screen_res:
		current_total_screen_res = total_screen_res
		print("Monitor change detected!")
		print("New total screen resolution {}".format(total_screen_res))
		#kill all current chromium sessions
		for id, proc in chromium_processes.items():
			print("Killing old chromium windows - ID {}".format(id))
			os.killpg(os.getpgid(proc.pid), signal.SIGINT)

			tmp_usr_data_dir = USR_DATA_DIR_PATH + str(id)
			print("Deletin temp user data dir - path: {}".format(tmp_usr_data_dir))
			os.system("rm -rf {}".format(tmp_usr_data_dir))

			screen_counter -= 1

		chromium_processes = {}

		screen_positions = re.findall(screen_positions_regex, xrandr_out)

		print("Number of found screens: {}".format(len(screen_positions)))
		#iterate through found screens
		for screen_pos in screen_positions:
			print("Identified screen: {}".format(screen_pos))
			print("Our ID: {}".format(screen_counter))
			offset = screen_pos.split("+")
			offset = (offset[1],offset[2])

			tmp_usr_data_dir = USR_DATA_DIR_PATH + str(screen_counter)
			print("Creating own user data dir - path: {}".format(tmp_usr_data_dir))
			os.system("mkdir {}".format(tmp_usr_data_dir))

			print("Starting chromium on position {}".format(offset))

			tmp_chromium_command = chromium_command.format(offset[0],offset[1],tmp_usr_data_dir)

			print("Using command:\t\n{}".format(tmp_chromium_command))

			chromium_processes[screen_counter] = subprocess.Popen(tmp_chromium_command, stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)
			screen_counter += 1


	time.sleep(UPDATE_TIME)
