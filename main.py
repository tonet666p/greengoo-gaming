#!/usr/bin/env python

import urllib
import sys
import time
import threading

time_in_list = 300 # 5 minutes
server_ip = "172.16.13.1"
server_port = "5050"

try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk
except:
	pass
	try:
		import gtk
		import gtk.glade
	except:
		sys.exit(1)

class GreenGooMain:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def onButtonPressed(self, button):
		self.help_window.run()
        
	def onDialogExit(self, button):
		self.help_window.hide()

	def onSwitchActivate(self,switch,something):
		if self.connect_switch.get_state():
			request = urllib.urlopen('http://'+server_ip+':'+server_port+'/?action=rem')           
			result = request.readline() 
			if result == 'removed':
				self.status_label.set_text("Desconectado")
				self.missing_time = 1
				
		else:
			if self.auto_disable:
				self.auto_disable = False
			else:
				request = urllib.urlopen('http://'+server_ip+':'+server_port+'/?action=add')           
				result = request.readline()  
				if result == 'added':
					self.status_label.set_text("Conectado")
					self.countdown_thread = threading.Thread(target=self.start_countdown)
					self.countdown_thread.start()

	def start_countdown(self):
		self.missing_time = time_in_list
		while self.missing_time > 0:
			time.sleep(1)
			self.missing_time=self.missing_time-1
			self.countdown_progress.set_text(time.strftime("%M:%S", time.gmtime(self.missing_time)))
			self.countdown_progress.set_fraction(self.missing_time/300.0)
			#print (self.missing_time/300.0)
			#self.countdown_progress.pulse()
		if self.connect_switch.get_state(): # if the switch is activated
			self.auto_disable = True
			self.connect_switch.set_state(False)
		
			

	def __init__(self):
		self.gladefile = "interface.glade"
		self.missing_time = 0
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladefile)
		self.builder.connect_signals(self)
		self.main_window = self.builder.get_object("main_window")
		self.help_window = self.builder.get_object("help_window")
		self.connect_switch = self.builder.get_object("connect_switch")
		self.status_label = self.builder.get_object("status_label")
		self.countdown_progress = self.builder.get_object("countdown_progress")
		#self.countdown_progress.set_pulse_step(1/300)
		#self.countdown_progress.pulse()
		self.auto_disable = False
		
		self.help_window.set_transient_for(self.main_window)
		self.main_window.show()

if __name__ == "__main__":
	main = GreenGooMain()
	Gtk.main()
