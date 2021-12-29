# -*- coding: UTF-8 -*-
# Author: Alberto Buffolino
# License: GPLv3
import globalPluginHandler
import api
from subprocess import Popen, PIPE, CREATE_NO_WINDOW as HIDDEN
import ui

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def script_poc(self, gesture):
		"""Proof of concept to retrieve command line arguments from foreground application. If this is an editor or viewer, opened starting from a document in explorer, it's very likely that args are or contain the path to the document itself."""
		obj = api.getFocusObject()
		psCommand = "Get-CimInstance Win32_Process -Filter \"ProcessId = '{pid}'\" | Select-Object CommandLine -ExpandProperty CommandLine"
		ps = Popen(["powershell.exe", psCommand.format(pid=obj.processID)], creationflags=HIDDEN, stdout=PIPE)
		# tuple like (b'"path\to\program.exe" "command line args"', None)
		res = ps.communicate()[0]
		# convert to str
		res = res.decode("mbcs")
		# poc could finish here; consider using re to a better handling of document path
		exePath = obj.appModule.appPath
		exeArgs = res.split("\"%s\""%exePath, 1)[-1]
		# cleaning from starting spaces and trailing newlines
		exeArgs = exeArgs.strip()
		ui.message("You're opened %s with args %s"%(exePath, exeArgs))

	__gestures = { "kb:NVDA+i": "poc" }
