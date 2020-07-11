
from kivymd.app import MDApp
from kivy.lang import Builder 
from kivymd.theming import ThemeManager, ThemableBehavior
from kivy.uix.screenmanager import ScreenManager 
from fbchat import Client 
from fbchat.models import * 
from kivy.properties import ObjectProperty, StringProperty, NumericProperty 
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton 
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import CircularRippleBehavior	
from kivy.uix.image import Image 
import pyperclip
from kivy.uix.image import AsyncImage
from kivymd.uix.list import OneLineAvatarListItem

store = JsonStore("Account.json")
	 	



class Custom_Image_Button(CircularRippleBehavior, ButtonBehavior, Image):
	pass 

class OnlineImage(AsyncImage):
    pass

class ImageButton(CircularRippleBehavior, ButtonBehavior, AsyncImage):
	pass
    
class FB(Client):
	pass 

class Item1(OneLineAvatarListItem):
	pass

class Item2(OneLineAvatarListItem):
	pass


class Yami(ScreenManager):
	default = "User's ID:\n" + "User's name:\n" + "User's profile picture URL:\n" + "User's main URL:"
	user_icon = StringProperty("default.jpg")
	error2 = StringProperty()
	error = StringProperty()
	search = ObjectProperty()
	username = ObjectProperty()
	password = ObjectProperty()
	name = ObjectProperty()
	times = ObjectProperty()
	input_text = ObjectProperty()
	ID = StringProperty(default)
	pic1 = ObjectProperty()
	current_page = NumericProperty(0)





	def login(self):

		try:
			global client 
			client = FB(self.username.text, self.password.text)
			store.put('User_Profile', name = self.username.text, password = self.password.text)
			self.current = "screen2"
			my_user = client.fetchUserInfo(client.uid)[client.uid]
			self.pic1.source = str(my_user.photo)


		except:
			self.show_fail_dialog()

	def show_fail_dialog(self):
		btn = MDFlatButton(text="Try Again")
		btn.bind(on_release=self.close_fail_dialog)
		self.dialog2 = MDDialog(
			text="Incorrect username or password!",
			size_hint=[.7,.7],
			buttons=[
				btn
			],
		)

		self.dialog2.open()

	def close_fail_dialog(self, *args):
		self.dialog2.dismiss()


	def test(self, *args):

		search = str(self.name.text)
		your_text = str(self.text_input.text)

		if len(self.name.text) and len(self.times.text) and len(self.text_input.text) > 0:
			try:
				users = client.searchForUsers(search)
				user = users[0]
				for x in range(int(self.times.text)):
					client.send(Message(text=your_text), thread_id=user.uid)
				self.close()
				self.error = ""

			except:
				self.close()
				self.error = "Warning: wrong name input!"


	def show_dialog(self):
		bt1 = MDFlatButton(text="CANCEL")
		bt2 = MDRaisedButton(text="OK")
		bt1.bind(on_release = self.close)
		bt2.bind(on_release = self.test)
		self.dialog = MDDialog(
		    text="Are you sure?",
		    size_hint = [.7, .7],
		    buttons=[
		        bt1, bt2,
		    ],	
		)
		self.dialog.open()

	def close(self, *args):
		self.dialog.dismiss()


	def fetch_engine(self):
		try:
			self.users = client.searchForUsers(self.search.text)
			user = self.users[0]

			inf = "User's ID: {}".format(user.uid)
			name = "User's name: {}".format(user.name)
			pic = "User's profile picture URL: {}".format(user.photo)
			url = "User's main URL: {}".format(user.url)
			self.ID = "{}\n".format(inf) + "{}\n".format(name) + '{}\n'.format(pic) + '{}\n'.format(url)
			self.user_icon = str(user.photo)
			self.error2 = ""

		except:
			self.error2 = "Warning: wrong name input!"


	def next(self):
		if self.ID != self.default:
			try:
				user = self.users[self.current_page+1]
				self.current_page += 1 
				inf = "User's ID: {}".format(user.uid)
				name = "User's name: {}".format(user.name)
				pic = "User's profile picture URL: {}".format(user.photo)
				url = "User's main URL: {}".format(user.url)
				self.ID = "{}\n".format(inf) + "{}\n".format(name) + '{}\n'.format(pic) + '{}\n'.format(url)
				self.user_icon = str(user.photo)
			except:
				pass

	def back(self):
		if self.current_page > 0:
			user = self.users[self.current_page-1]
			self.current_page -= 1 
			inf = "User's ID: {}".format(user.uid)
			name = "User's name: {}".format(user.name)
			pic = "User's profile picture URL: {}".format(user.photo)
			url = "User's main URL: {}".format(user.url)
			self.ID = "{}\n".format(inf) + "{}\n".format(name) + '{}\n'.format(pic) + '{}\n'.format(url)
			self.user_icon = str(user.photo)


	def copy(self):
		pyperclip.copy(str(self.ID))


	def show_setting(self):

		self.dialog3 = MDDialog(
			title = "Settings",
			type = "simple",
			size_hint = [.7, .7],
			items = [
				Item1(text="Donate"),
				Item2(text="Log Out", on_release=self.log_out),
				],
			)
		self.dialog3.open()

	def log_out(self, *args):
		store.delete('User_Profile')
		root.current = "screen1"
		self.dialog3.dismiss()



class Core(MDApp):

	account_icon = StringProperty() 
          

	def on_start(self):

		if store.exists('User_Profile'): 

			global client 
			client = FB(str(store.get("User_Profile")['name']), str(store.get("User_Profile")['password']))
			root.current = "screen2"

			my_user = client.fetchUserInfo(client.uid)[client.uid]
			self.account_icon = str(my_user.photo)
			
	## Need to update this as well 
	def __init__(self, **kwargs):
		self.title = "Chat Bot"
		self.theme_cls.theme_style = "Dark"
		super().__init__(**kwargs)

	#File's Build System for KV path 
	def build(self):
		global root 
		self.root = root = Builder.load_file("Outlook.kv")




if __name__ == "__main__":
	Core().run()



# Adding more interactive button 
# Learn how to import the program to Mac and IOS 
# Saving enough to publish 
# $PROFIT$
