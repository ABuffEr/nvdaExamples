# -*- coding: UTF-8 -*-
# Author: Alberto Buffolino
# License: GPLv3
import globalPluginHandler
import api
from subprocess import Popen, PIPE, CREATE_NO_WINDOW as HIDDEN
import ui

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def script_poc(self, gesture):
		"""Proof-of-concept to retrieve command line arguments from foreground application. If this is an editor or viewer, opened starting from a document in explorer, it's very likely that args are or contain the path to the document itself."""
		# useful to obtain processID
		obj = api.getFocusObject()
		# Powershell instructions to run
		psCommand = "Get-CimInstance Win32_Process -Filter \"ProcessId = '{pid}'\" | Select-Object CommandLine -ExpandProperty CommandLine"
		# run Powershell with previous command, hiding console window and catching its output
		ps = Popen(["powershell.exe", psCommand.format(pid=obj.processID)], creationflags=HIDDEN, stdout=PIPE)
		# returned tuple is something like:
		# (b'"path\to\program.exe" "command line args"', None)
		# so get only first item
		res = ps.communicate()[0]
		# convert from bytes to str
		res = res.decode("mbcs")
		# poc could finish here; consider using re module to a better handling of document path
		exePath = obj.appModule.appPath
		# remove exePath from retrieved command line
		# (depending from application, could remain other args, in addition to document path)
		exeArgs = res.split("\"%s\""%exePath, 1)[-1]
		# cleaning from starting spaces and trailing newlines
		exeArgs = exeArgs.strip()
		ui.message("You're opened %s with args %s"%(exePath, exeArgs))

	__gestures = { "kb:NVDA+i": "poc" }
