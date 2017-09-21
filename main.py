# *-* encoding: utf-8 *-*

import configparser
import datetime
import gi
import locale
import os
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

APPNAME = "Quit Smoking"
APPVERSION = "0.0.1"
LOGOFILE = ""
MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""
# locale.setlocale(locale.LC_TIME, locale.getdefaultlocale()[0])
# TO BE FIXED

class NewData(Gtk.Assistant):
	def __init__(self):
		Gtk.Assistant.__init__(self)
		self.set_title("New Data")
		# self.set_default_size(400, -1)
		self.connect("cancel", self.on_cancel_clicked)
		self.connect("close", self.on_close_clicked)
		self.connect("apply", self.on_apply_clicked)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_default_size(800, 600)

		################################ PAGE 1 ######################################################
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.append_page(box)
		self.set_page_type(box, Gtk.AssistantPageType.INTRO)
		self.set_page_title(box, "Introduction")
		label = Gtk.Label(label="""
Welcome to """ + APPNAME + """, an app that helps you to quit smoking!

The app will ask you some data, such as costs and time of last cigarette, in order to work. Data inserted are saved only on your device so your privacy is respected.

Press \"Continue\" to go on.""")
		label.set_line_wrap(True)
		box.pack_start(label, True, True, 0)
		self.set_page_complete(box, True)
		
		################################ PAGE 2 ######################################################
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.append_page(box)
		self.set_page_type(box, Gtk.AssistantPageType.CONTENT) # Gtk.AssistantPageType.PROGRESS
		self.set_page_title(box, "Settings")
		label = Gtk.Label(label="Let's define some data the program needs to know in order to work.")
		label.set_line_wrap(True)
		box.pack_start(label, True, True, 0)
		
		listbox = Gtk.ListBox()		# TODO: Not sure if it is the correct choice?
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		hbox.pack_start(vbox, True, True, 0)
		
		label = Gtk.Label("Last cigarette", xalign=0)
		vbox.pack_start(label, True, True, 0)
		self.calendar = Gtk.Calendar()
		hbox.pack_start(self.calendar, False, True, 0)

		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		hbox.pack_start(vbox, True, True, 0)

		label = Gtk.Label("Duration", xalign=0)
		vbox.pack_start(label, True, True, 0)
		
		ad = Gtk.Adjustment(1, 1, 1000, 1, 0, 0)
		self.duration = Gtk.SpinButton(adjustment=ad, climb_rate=1, digits=0)
		self.duration.set_hexpand(True)
		hbox.pack_start(self.duration, False, True, 0)
		
		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		hbox.pack_start(vbox, True, True, 0)

		label = Gtk.Label("Number of smoked cigarettes in a day", xalign=0)
		vbox.pack_start(label, True, True, 0)
		
		ad = Gtk.Adjustment(1, 1, 1000, 1, 0, 0)
		self.number = Gtk.SpinButton(adjustment=ad, climb_rate=1, digits=0)
		self.number.set_hexpand(True)
		hbox.pack_start(self.number, False, True, 0)
		
		listbox.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		hbox.pack_start(vbox, True, True, 0)

		label = Gtk.Label("Cost per cigarette", xalign=0)
		vbox.pack_start(label, True, True, 0)
		
		ad = Gtk.Adjustment(0.01, 0.01, 10, 0.01, 0, 0)
		self.cost = Gtk.SpinButton(adjustment=ad, climb_rate=0.01, digits=2)
		self.cost.set_hexpand(True)
		hbox.pack_start(self.cost, False, True, 0)
		
		listbox.add(row)
		
		box.add(listbox)
		self.set_page_complete(box, True)
		
		################################ PAGE 3 ######################################################
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.append_page(box)
		self.set_page_type(box, Gtk.AssistantPageType.CONTENT)
		self.set_page_title(box, "Goals")
		label = Gtk.Label(label="You can add some goals. You define the target of saved money and some information, so that you will be informed when you saved that amount of money and you can do whatever you want with them. You can donate them to non-profit associations: make this world a better place!")
		label.set_line_wrap(True)
		box.pack_start(label, True, True, 0)
		self.set_page_complete(box, True)
		
		# TODO: goals. Array of arrays: [Name, Saved euros]

		################################ PAGE 4 ######################################################
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.append_page(box)
		self.set_page_type(box, Gtk.AssistantPageType.CONFIRM)
		self.set_page_title(box, "Confirm")
		label = Gtk.Label(label="Do you confirm that the data you inserted are correct? You can go back and change them before confirming.")
		label.set_line_wrap(True)
		box.pack_start(label, True, True, 0)
		self.set_page_complete(box, True)

		################################ PAGE 5 ######################################################
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.append_page(box)
		self.set_page_type(box, Gtk.AssistantPageType.SUMMARY)
		self.set_page_title(box, "Summary")
		label = Gtk.Label(label="A 'Summary' should be set as the final page of the Assistant if used however this depends on the purpose of your Assistant. It provides information on the changes that have been made during the configuration or details of what the user should do next. On this page only a Close button is displayed. Once at the Summary page, the user cannot return to any other page.")
		label.set_line_wrap(True)
		box.pack_start(label, True, True, 0)
		self.set_page_complete(box, True)

	def on_apply_clicked(self, *args):
		self.date = self.calendar.get_date()
		self.costpercig = self.cost.get_value()
		self.timespent = self.duration.get_value_as_int()
		self.cigsperday = self.number.get_value_as_int()

	def on_close_clicked(self, *args):
		self.destroy()

	def on_cancel_clicked(self, *args):
		self.destroy()

	def on_complete_toggled(self, checkbutton):
		self.set_page_complete(self.complete, checkbutton.get_active())
		
class Window(Gtk.ApplicationWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.set_default_size(800, 600)
		self.set_position(Gtk.WindowPosition.CENTER)

		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = APPNAME
		self.set_titlebar(hb)
	
		button = Gtk.Button()
		button.add(Gtk.Image.new_from_icon_name("document-new", Gtk.IconSize.BUTTON))
		button.connect("clicked", self.on_new_clicked)
		hb.pack_start(button)

		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")

		self.add(self.box)
		# self.connect("delete-event", quit_app)
		
		if os.path.isfile('cards.xml') == True:
			config = configparser.ConfigParser()
			conf = config.read("quit_smoking.conf")
		
		self.date = datetime.date(2016, 2, 5)
		self.costpercig = 0.25
		self.timespent = 10
		self.cigsperday = 4
		label = Gtk.Label(label="Stop smoking at " + str(self.date))
		#label.set_line_wrap(True)
		self.box.pack_start(label, True, True, 0)
		days = (datetime.date.today() - self.date).days
		if days == 1:
			label = Gtk.Label(label="Not smoking since " + str(days) + " day")
		else:
			label = Gtk.Label(label="Not smoking since " + str(days) + " days")
		#label.set_line_wrap(True)
		self.box.pack_start(label, True, True, 0)

		if self.cigsperday*days == 1:
			label = Gtk.Label(label="Saved " + str(self.cigsperday*days) + " cigarette")
		else:
			label = Gtk.Label(label="Saved " + str(self.cigsperday*days) + " cigarettes")
			
		#label.set_line_wrap(True)
		self.box.pack_start(label, True, True, 0)

		label = Gtk.Label(label="Saved " + str(self.cigsperday*days*self.costpercig) + " euros")	# TODO: Internationalization
		#label.set_line_wrap(True)
		self.box.pack_start(label, True, True, 0)

		if self.timespent*self.cigsperday*days == 1:
			label = Gtk.Label(label="Saved " + str(self.timespent*self.cigsperday*days) + " minute")
		else:
			label = Gtk.Label(label="Saved " + str(self.timespent*self.cigsperday*days) + " minutes")
		#label.set_line_wrap(True)
		self.box.pack_start(label, True, True, 0)
		
		## HEALTH:
		# Blood pressure (20 min)
		# Carbon monoxide (8 h)
		# Heart attack (1 d)
		# Sense of smell (2 d)
		# Breathing (3 d)
		# Nicotine withdrawal (1 w)
		# Capacity (3 m)
		# Lung hairs (9 m)
		# Coronary arteries (1 y)
		# Heart attack (2 y)
		# Stroke (5 y)
		# Lung cancer (10 y)
		# Heart attack (15 y)
		
		
	def on_new_clicked(self, button):
		newdata = NewData()
		response = newdata.show_all()
		print("Response: " + str(response))
		if response == Gtk.ResponseType.APPLY:
			children = self.box.get_children()
			print(children[0].get_label())
			children[0].set_label("Stop smoking at " + str(self.date))
			print(children[0].get_label())
			days = (datetime.date.today() - self.date).days
			print(children[1].get_label())
			if days == 1:
				children[1].set_label("Not smoking since " + str(days) + " day")
			else:
				children[1].set_label("Not smoking since " + str(days) + " days")
			print(children[1].get_label())
			print(children[2].get_label())
			if self.cigsperday*days == 1:
				children[2].set_label("Saved " + str(self.cigsperday*days) + " cigarette")
			else:
				children[2].set_label("Saved " + str(self.cigsperday*days) + " cigarettes")
		
			print(children[2].get_label())
			print(children[3].get_label())
			children[3].set_label("Saved " + str(self.cigsperday*days*self.costpercig) + " euros")
			print(children[3].get_label())
			print(children[4].get_label())
			if self.timespent*self.cigsperday*days == 1:
				children[4].set_label("Saved " + str(self.timespent*self.cigsperday*days) + " minute")
			else:
				children[4].set_label("Saved " + str(self.timespent*self.cigsperday*days) + " minutes")
			print(children[4].get_label())
			
class Application(Gtk.Application):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, application_id="org.gnome.quitsmoking",
			flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
			**kwargs)
		self.window = None
	
	def do_startup(self):
		Gtk.Application.do_startup(self)

		action = Gio.SimpleAction.new("about", None)
		action.connect("activate", self.on_about)
		self.add_action(action)

		action = Gio.SimpleAction.new("quit", None)
		action.connect("activate", self.on_quit)
		self.add_action(action)

		builder = Gtk.Builder.new_from_string(MENU_XML, -1)
		self.set_app_menu(builder.get_object("app-menu"))

	def do_activate(self):
		if not self.window:
			self.window = Window(application=self, title=APPNAME)
			self.window.connect("delete-event", self.on_quit)
			self.window.show_all()
		self.window.present()

	def do_command_line(self, command_line):
		options = command_line.get_options_dict()

		if options.contains("help") or options.contains("h"):
			print("Help to be created")

		elif options.contains("version") or options.contains("v"):
			print(APPVERSION)
		else:
			pass
		self.activate()
		return 0

	def on_about(self, action, param):
		aboutdialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
		aboutdialog.set_program_name(APPNAME)
		aboutdialog.set_version(APPVERSION)
		aboutdialog.set_copyright(u"Copyright \xc2\xa9 2017 Michael Moroni")
		aboutdialog.set_license_type(Gtk.License.GPL_3_0)		
		aboutdialog.set_authors(["Michael Moroni"])
		aboutdialog.set_documenters(["Michael Moroni"])
		aboutdialog.set_website("http://github.com/airon90/gnome-smoking")
		aboutdialog.set_website_label("GitHub repository")
		aboutdialog.set_title("")
		aboutdialog.set_comments("Stop smoking right now with this app. Reach the goals, save money and live better!")
		aboutdialog.set_translator_credits("""
		Esperanto: Michael Moroni\n
		Italian: Michael Moroni
		""")
		# aboutdialog.set_logo(LOGOFILE)
		aboutdialog.connect("response", self.on_close)
		aboutdialog.present()

	def on_close(self, action, parameter):
		action.destroy()

	def on_quit(self, action, parameter):
		Gtk.main_quit()

if __name__ == "__main__":
	app = Application()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)
