# -*- coding: UTF-8 -*-
# Author: Alberto Buffolino
# License: GPLv3
import globalPluginHandler
import speech
import config
from globalCommands import commands
# for compatibility
from versionInfo import version_year as mainVersion

def runSilently(func, *args, **kwargs):
	"""run the received func without voice/Braille output"""
	# current speech mode (talk, beep, off)
	curSpeechMode = speech.speechMode if mainVersion<2021 else speech.getState().speechMode
	# current Braille messageTimeout
	curBrailleMsgTimeout = config.conf["braille"]["messageTimeout"]
	# store current config for voice and Braille
	configBackup = {"voice": curSpeechMode, "braille": curBrailleMsgTimeout}
	# turn voice off
	if mainVersion<2021:
		speech.speechMode = speech.speechMode_off
	else:
		speech.setSpeechMode(speech.SpeechMode.off)
	# set Braille messageTimeout to 0 in config cache
	# (avoiding permanent changes)
	config.conf["braille"]._cacheLeaf("messageTimeout", None, 0)
	# run the received func
	try:
		func(*args, **kwargs)
	finally:
		# restore starting speech mode and Braille messageTimeout
		if mainVersion<2021:
			speech.speechMode = configBackup["voice"]
		else:
			speech.setSpeechMode(configBackup["voice"])
		config.conf["braille"]._cacheLeaf("messageTimeout", None, configBackup["braille"])

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def script_poc(self, gesture):
		"""Proof-of-concept to silently invoke default object action"""
		# running directly script_review_activate, from NVDA globalCommands,
		# brings to a undesired "invoke" message; so...
		runSilently(commands.script_review_activate, gesture)
		# Note: gesture is required parameter, but it's substantially a placeholder here
		# because core script does not checks it

	__gestures = { "kb:NVDA+i": "poc" }
