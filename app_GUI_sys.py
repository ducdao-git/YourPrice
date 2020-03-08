"""
*** Duc Dao ***
About This Script:
app gui system - create app buttons and its functionality
"""

import tkinter as tk
import app_process_1 as ap1
import app_GUI_table as gTab
import sqlite3 as sql
import webbrowser

def win_pos(master_win):
	sys_width_L = master_win.winfo_screenwidth()
	sys_height_L = master_win.winfo_screenheight()

	master_win.update()
	app_width_L = master_win.winfo_width()
	app_height_L = master_win.winfo_height()

	app_x_pos = int(sys_width_L / 2 - app_width_L / 2)
	app_y_pos = int(sys_height_L / 2 - app_height_L / 2)

	master_win.geometry(f'{app_width_L}x{app_height_L}+{app_x_pos}+{app_y_pos}')
	return {'app_x_pos': app_x_pos, 'app_y_pos': app_y_pos}

def pop_up_transit(self, master_win, title):
	self.lift()
	self.grab_set()
	self.transient(master_win)
	self.title(f'{title}')
	self.resizable(0, 0)

def status_check():
	conn = sql.connect('tracking_item.db')
	c = conn.cursor()
	try:  # tracking_item might not exist
		c.execute("SELECT *,oid FROM tracking_item")
		records = c.fetchall()
		conn.close()
	except sql.OperationalError:
		records = []
	if len(records) == 0:  # tracking_item table exist but have no item
		return 0
	else:
		return 1

def add_item_func(master_win, item_id):
	popup_win = tk.Toplevel()
	pop_up_transit(popup_win, master_win, 'Add Tracking Item')

	def save_input():
		ap1.process_1(str(url_add_input.get()), str(user_price_input.get()), str(recipients_input.get()))

	def another_item():
		try:
			if len(url_add_input.get()) != 0 and len(user_price_input.get()) != 0 and len(recipients_input.get()) != 0:
				save_input()
			else:
				pass
		except Exception as e:
			print(e)
		finally:
			url_add_input.delete(0, 'end')
			user_price_input.delete(0, 'end')
			recipients_input.delete(0, 'end')

	def done(master_win_L, item_id_L):
		try:
			if len(url_add_input.get()) != 0 and len(user_price_input.get()) != 0 and len(recipients_input.get()) != 0:
				save_input()
			else:
				pass
		except Exception as e:
			print(e)
		finally:
			gTab.table_frame(master_win_L, item_id_L)
			popup_win.destroy()

	def entry(text):
		for i in range(3):
			label = tk.Label(popup_win, text=text[i], padx=5, width=15, anchor='se')
			label.grid(row=i, column=0)

	entry(['URL Link', 'Desire Price', 'Recipient Email Add'])

	url_add_input = tk.Entry(popup_win, width=35)
	url_add_input.grid(row=0, column=1, columnspan=2, pady=5)

	user_price_input = tk.Entry(popup_win, width=35)
	user_price_input.grid(row=1, column=1, columnspan=2, pady=5)

	recipients_input = tk.Entry(popup_win, width=35)
	recipients_input.grid(row=2, column=1, columnspan=2, pady=5)

	another_item_btn = tk.Button(popup_win, text='Add Another Item', width=17, command=lambda: another_item())
	another_item_btn.grid(row=3, column=1, pady=5)

	done_btn = tk.Button(popup_win, text='Done', width=17, command=lambda: done(master_win, item_id))
	done_btn.grid(row=3, column=2, pady=5)

	win_pos(popup_win)

# popup_win.protocol("WM_DELETE_WINDOW", lambda: done(master_win, item_id))

def refresh_table_func(master_win, item_id):
	gTab.table_frame(master_win, item_id)

def edit_item_func(master_win, item_id):
	popup_win = tk.Toplevel()
	pop_up_transit(popup_win, master_win, 'Edit Tracking Item')
	status = status_check()
	check = item_id.get()  # check if one item is select

	if status == 1:  # at least 1 tracking item
		if check == -1:
			msg = tk.Label(popup_win, text="""\nPlease Select An Item To Edit
			\n(to select item, please check the box at the beginning of the item line)""")
			msg.grid(ipadx=7, row=0, column=0)
			btn = tk.Button(popup_win, text='Got It!', font='16', command=lambda: popup_win.destroy())
			btn.grid(ipadx=15, pady=7, row=1, column=0)
			win_pos(popup_win)

		else:
			conn = sql.connect('tracking_item.db')
			c = conn.cursor()
			c.execute(f"SELECT *,oid FROM tracking_item WHERE oid = {check}")
			record = c.fetchone()

			# c.execute(f"DELETE FROM tracking_item WHERE oid = {check}")

			def cancel():
				popup_win.destroy()

			def done(master_win_L, item_id_L):
				try:
					if len(user_price_edit.get()) != 0 or len(recipients_edit.get()) != 0:
						conn_L = sql.connect('tracking_item.db')
						c_L = conn_L.cursor()
						if len(user_price_edit.get()) == 0 and len(recipients_edit.get()) != 0:
							del_check = ap1.process_1(record[0], record[2], str(recipients_edit.get()))
						elif len(user_price_edit.get()) != 0 and len(recipients_edit.get()) == 0:
							del_check = ap1.process_1(record[0], str(user_price_edit.get()), record[-2])
						elif len(user_price_edit.get()) != 0 and len(recipients_edit.get()) != 0:
							del_check = ap1.process_1(record[0], str(user_price_edit.get()), str(recipients_edit.get()))

						if del_check == -1:
							pass
						else:
							with conn_L:
								c_L.execute(f"DELETE FROM tracking_item WHERE oid = {check}")
							gTab.table_frame(master_win_L, item_id_L)
					else:
						pass
				except Exception as e:
					print(e)
				finally:
					# conn.close()
					popup_win.destroy()

			def entry(text):
				for i in range(0, 2, 1):
					label = tk.Label(popup_win, text=text[i], padx=5, width=15, anchor='se')
					label.grid(row=i * 2, column=0)

			entry(['Desire Price', 'Recipient Email Add'])

			def show_current_data(current_data):
				for i in range(0, 2, 1):
					label = tk.Label(popup_win, text='Current ' + current_data[i], padx=5, anchor='e')
					label.grid(row=current_data[-1][i], column=0, sticky='we')
					value = tk.Label(popup_win, text=current_data[i + 2], padx=5, anchor='w')
					value.grid(row=current_data[-1][i], column=1, columnspan=2, sticky='we')

			show_current_data(['Desire Price', 'Recipient List', '$ {:,.2f}'.format(record[2]), record[-2], [1, 3]])

			user_price_edit = tk.Entry(popup_win, width=35)
			user_price_edit.grid(row=0, column=1, columnspan=3, pady=5)

			recipients_edit = tk.Entry(popup_win, width=35)
			recipients_edit.grid(row=2, column=1, columnspan=3, pady=5)

			done_btn = tk.Button(popup_win, text='Done', command=lambda: done(master_win, item_id))
			done_btn.grid(row=4, column=1, columnspan=3, sticky='we', padx=10, pady=5)

			cancel_btn = tk.Button(popup_win, text='Cancel', command=cancel)
			cancel_btn.grid(row=4, column=0, columnspan=1, sticky='we', padx=5, pady=5)

			win_pos(popup_win)

	elif status == 0:
		msg = tk.Label(popup_win, text="""\nThere Is No Tracking Item Yet
					\nPlease Add An Item To The Tracking List""")
		msg.grid(ipadx=7, columnspan=5, row=0, column=0)

		def msg_btn():
			add_item_func(master_win, item_id)
			popup_win.destroy()

		add_item_btn = tk.Button(popup_win, text='Add Item', font='16', command=lambda: msg_btn())
		add_item_btn.grid(pady=7, row=1, column=1, sticky='ew')  # ipadx=15,
		quit_btn = tk.Button(popup_win, text='Exit', font='16', command=lambda: popup_win.destroy())
		quit_btn.grid(pady=7, row=1, column=3, sticky='ew')  # ipadx=15,
		win_pos(popup_win)

def remove_item_func(master_win, item_id):  # *********
	popup_win = tk.Toplevel()
	pop_up_transit(popup_win, master_win, 'Remove Tracking Item')
	status = status_check()
	check = item_id.get()  # check if one item is select

	if status == 1:
		if check == -1:
			msg = tk.Label(popup_win, text="""\nPlease Select An Item To Remove
			\n(to select item, please check the box at the beginning of the item line)""")
			msg.grid(ipadx=7, row=0, column=0)
			btn = tk.Button(popup_win, text='Got It!', font='16', command=lambda: popup_win.destroy())
			btn.grid(ipadx=15, pady=7, row=1, column=0)
			win_pos(popup_win)

		else:
			conn = sql.connect('tracking_item.db')
			c = conn.cursor()
			with conn:
				c.execute(f"SELECT *,oid FROM tracking_item WHERE oid = {check}")
				record = c.fetchone()
				item_name = record[1]
				c.execute(f"DELETE FROM tracking_item WHERE oid = {check}")

			msg = tk.Label(popup_win,
						   text="""\nYou Have Delete This Item Off Your Tracking List\n\n{}""".format(item_name))
			msg.grid(ipadx=7, row=0, column=0)
			btn = tk.Button(popup_win, text='Got It!', font='16', command=lambda: popup_win.destroy())
			btn.grid(ipadx=15, pady=7, row=1, column=0)
			conn.close()
			win_pos(popup_win)
			gTab.table_frame(master_win, item_id)

	elif status == 0:
		msg = tk.Label(popup_win, text="""\nThere Is No Tracking Item Yet
					\nPlease Add An Item To The Tracking List""")
		msg.grid(ipadx=7, columnspan=5, row=0, column=0)

		def add_first_item(master_win_L, item_id_L):
			add_item_func(master_win_L, item_id_L)
			popup_win.destroy()

		add_item_btn = tk.Button(popup_win, text='Add Item', font='16',
								 command=lambda: add_first_item(master_win, item_id))
		add_item_btn.grid(pady=7, row=1, column=1, sticky='ew')  # ipadx=15,
		quit_btn = tk.Button(popup_win, text='Exit', font='16', command=lambda: popup_win.destroy())
		quit_btn.grid(pady=7, row=1, column=3, sticky='ew')  # ipadx=15,
		win_pos(popup_win)

def setting_func(master_win, item_id):
	popup_win = tk.Toplevel()
	pop_up_transit(popup_win, master_win, 'Setting')

	def restart_func():
		popup_win_L = tk.Toplevel()
		pop_up_transit(popup_win_L, master_win, 'Setting')

		def table_drop():
			conn = sql.connect('tracking_item.db')
			c = conn.cursor()
			try:  # tracking_item might not exist
				with conn:
					c.execute("Drop Table tracking_item")
				conn.close()
			except sql.OperationalError:
				popup_win.destroy()
				popup_win_L.destroy()
			finally:
				gTab.table_frame(master_win, item_id)
				popup_win_L.destroy()
				popup_win.destroy()

		def msg_destroy():
			popup_win_L.destroy()
			popup_win.destroy()

		msg = tk.Label(popup_win_L,
					   text='Doing This Will Delete All Your Tracking Item \n and Reset The Table to it Default')
		msg.grid(pady=5, padx=5, row=0, column=0, columnspan=2, sticky='ew')
		restart_btn_L = tk.Button(popup_win_L, text='Restart', font='16', width=12, command=table_drop)
		restart_btn_L.grid(pady=5, padx=5, ipadx=7, row=1, column=1, sticky='ew')
		quit_btn_L = tk.Button(popup_win_L, text='Exit', font='16', width=12, command=msg_destroy)
		quit_btn_L.grid(pady=5, padx=5, ipadx=7, row=1, column=0, sticky='ew')
		win_pos(popup_win_L)

	restart_btn = tk.Button(popup_win, text='Restart', font='16', width=12, command=restart_func)
	restart_btn.grid(pady=5, padx=5, row=0, column=1)
	quit_btn = tk.Button(popup_win, text='Exit', font='16', width=12, command=lambda: popup_win.destroy())
	quit_btn.grid(pady=5, padx=5, row=0, column=0)

	win_pos(popup_win)

def bug_report_func():
	webbrowser.open(
		'https://docs.google.com/forms/d/e/1FAIpQLSdlNecMf9HW0--LYt8w5Np2nFhbiInZtZZgHuoRFKNjIBzwgg/viewform?usp=pp_url')

def add_item(master_win, item_id):
	add_item_bt = tk.Button(master_win, text="Add Item", width=15, font="Times 16",
							command=lambda: add_item_func(master_win, item_id))
	add_item_bt.place(bordermode='inside', anchor='center', relx=0.23, rely=0.04)

def edit_item(master_win, item_id):
	edit_item_bt = tk.Button(master_win, text="Edit Item", width=15, font="Times 16",
							 command=lambda: edit_item_func(master_win, item_id))
	edit_item_bt.place(bordermode='outside', anchor='center', relx=0.5, rely=0.04)

def remove_item(master_win, item_id):
	remove_item_bt = tk.Button(master_win, text="Remove Item", width=15, font="Times 16",
							   command=lambda: remove_item_func(master_win, item_id))
	remove_item_bt.place(bordermode='inside', anchor='center', relx=0.77, rely=0.04)

def refresh_table(master_win, item_id):
	refresh_bt = tk.Button(master_win, text="R\ne\nf\nr\ne\ns\nh", font="Times 16",
						   command=lambda: refresh_table_func(master_win, item_id))
	refresh_bt.place(bordermode='inside', anchor='ne', relx=0.05, rely=0.0785)

def setting(master_win, setting_icon, item_id):
	setting_bt = tk.Button(master_win, image=setting_icon, command=lambda: setting_func(master_win, item_id))
	setting_bt.place(anchor='ne', relx=1, rely=0, width=27, heigh=27)
	return setting_bt

def bug_report(master_win, report_icon):
	report_bt = tk.Button(master_win, image=report_icon, command=bug_report_func)
	report_bt.place(anchor='se', relx=1, rely=1, width=27, heigh=27)
