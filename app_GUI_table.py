"""
*** Duc Dao ***
About This Script:
app gui table - create and display tracking table
"""

import tkinter as tk
import sqlite3 as sql
import app_process_2 as ap2
import time, webbrowser

def main_frame_config(master_win, self):
	app_width = master_win.winfo_width()
	app_height = master_win.winfo_height()
	self.configure(width=app_width * 0.9, height=app_height * 0.875, bd=5, relief='sunken')
	self.place(relx=0.05, rely=0.08)  # consider using x_pos, y_pos
	self.pack_propagate(0)
	self.grid_propagate(0)
	# main_frame.tk_setPalette()

	self.update()
	main_frame_width = self.winfo_width()
	main_frame_height = self.winfo_height()

	return [main_frame_width, main_frame_height]

def table_cell(main_frame, row, main_frame_width, main_frame_height):
	id_cell = tk.Frame(main_frame, width=main_frame_width / 48, height=main_frame_height / 20)
	id_cell.grid(row=row, column=0)
	id_cell.pack_propagate(0)

	item_name_cell = tk.Frame(main_frame, width=main_frame_width * 401 / 1140 - 3,
							  height=main_frame_height / 20)
	item_name_cell.grid(row=row, column=1)
	item_name_cell.pack_propagate(0)

	item_price_cell = tk.Frame(main_frame, width=main_frame_width * 9 / 76, height=main_frame_height / 20)
	item_price_cell.grid(row=row, column=2)
	item_price_cell.pack_propagate(0)

	user_price_cell = tk.Frame(main_frame, width=main_frame_width * 9 / 76, height=main_frame_height / 20)
	user_price_cell.grid(row=row, column=3)
	user_price_cell.pack_propagate(0)

	price_diff_cell = tk.Frame(main_frame, width=main_frame_width * 9 / 76, height=main_frame_height / 20)
	price_diff_cell.grid(row=row, column=4)
	price_diff_cell.pack_propagate(0)

	recipients_cell = tk.Frame(main_frame, width=main_frame_width / 5, height=main_frame_height / 20)
	recipients_cell.grid(row=row, column=5)
	recipients_cell.pack_propagate(0)

	action_cell = tk.Frame(main_frame, width=main_frame_width / 15, height=main_frame_height / 20)
	action_cell.grid(row=row, column=6)
	action_cell.pack_propagate(0)

	return [id_cell, item_name_cell, item_price_cell, user_price_cell, price_diff_cell,
			recipients_cell, action_cell]

def header_row(cell_lst):
	id_header = tk.Button(cell_lst[0],
						  text='#')  # Checkbutton(id_cell, variable=item_id, onvalue=-1, offvalue=-1)
	id_header.pack(expand='true', fill='both')

	item_name_header = tk.Button(cell_lst[1], text='Item Name')
	item_name_header.pack(expand='true', fill='both')

	item_price_header = tk.Button(cell_lst[2], text='Current Price')
	item_price_header.pack(expand='true', fill='both')

	user_price_header = tk.Button(cell_lst[3], text='Desire Price')
	user_price_header.pack(expand='true', fill='both')

	price_diff_header = tk.Button(cell_lst[4], text='Price Different')
	price_diff_header.pack(expand='true', fill='both')

	recipients_header = tk.Button(cell_lst[5], text='Notification Mail')
	recipients_header.pack(expand='true', fill='both')

	action_header = tk.Button(cell_lst[6], text='Action')
	action_header.pack(expand='true', fill='both')

def item_row(records, row, item_id, cell_lst):
	record = records[row - 1]  # record = [(url, item_name, user_price_int, recipients, oid)]
	process_2 = ap2.process_2(record)
	# process_2 = [item_price_str_L, price_diff_str_L, recipient_lst_L, user_price_str_L]

	id_button = tk.Checkbutton(cell_lst[0], variable=item_id, onvalue=record[-1], offvalue=-1)
	id_button.deselect()
	id_button.pack(expand='true', fill='both')

	if len(record[1]) > 48:
		name_button = tk.Button(cell_lst[1], text=' ' + record[1][0:48] + '...', anchor='w',
								state='disable',
								disabledforeground='black')
	else:
		name_button = tk.Button(cell_lst[1], text=' ' + record[1], anchor='w',
								state='disable',
								disabledforeground='black')
	name_button.pack(expand='true', fill='both')

	iprice_button = tk.Button(cell_lst[2], text=process_2[0], state='disable',
							  disabledforeground='black')
	iprice_button.pack(expand='true', fill='both')

	wprice_button = tk.Button(cell_lst[3], text=process_2[3], state='disable',
							  disabledforeground='black')
	wprice_button.pack(expand='true', fill='both')

	dprice_button = tk.Button(cell_lst[4], text=process_2[1], state='disable',
							  disabledforeground='black')
	dprice_button.pack(expand='true', fill='both')

	if len(process_2[2]) <= 1:
		recipients_button = tk.Button(cell_lst[5], text=' ' + record[-2], anchor='center', state='disable',
									  disabledforeground='black')
	else:
		recipients_button = tk.Button(cell_lst[5], text=' ' + record[-2][0:23] + '...', anchor='w',
									  state='disable',
									  disabledforeground='black')
	recipients_button.pack(expand='true', fill='both')

	if process_2[1].find('-') == -1:
		action_button = tk.Button(cell_lst[6], text='Buy', fg='#00007f', command=lambda: webbrowser.open(record[0]))
		action_button.pack(expand='true', fill='both')
	else:
		action_button = tk.Button(cell_lst[6], text='Wait', fg='#00007f', command=lambda: webbrowser.open(record[0]))
		action_button.pack(expand='true', fill='both')

def table(main_frame, row, main_frame_width_info, records, item_id):
	cell_lst = table_cell(main_frame, row, main_frame_width_info[0], main_frame_width_info[1])
	# cell_lst = [id_cell, item_name_cell, item_price_cell, user_price_cell, price_diff_cell, recipients_cell, action_cell]

	if row == 0:
		header_row(cell_lst)

	elif row < 20:
		item_row(records, row, item_id, cell_lst)

	else:
		print('Continue to Next Page')  # need create next page func

def table_frame(master_win, item_id):
	start_time = time.time()

	# main_frame_2 = tk.Frame(master_win)
	# main_frame_config(master_win, main_frame_2)
	# main_frame_2.lift()

	main_frame = tk.Frame(master_win)
	main_frame_width_info = main_frame_config(master_win, main_frame)
	# main_frame_width_info = [main_frame_width, main_frame_height]

	conn = sql.connect('tracking_item.db')
	c = conn.cursor()

	try:
		with conn:
			c.execute("SELECT *,oid FROM tracking_item")  # tracking_item table might not exist
			records = c.fetchall()

		if len(records) > 0:  # tracking_item table might not have any item
			for row in range(len(records) + 1):
				table(main_frame, row, main_frame_width_info, records, item_id)

		else:
			none_label = tk.Label(main_frame, text='No Tracking Item', font='Times 30 bold')
			none_label.pack(expand='true', fill='both')

	except sql.OperationalError:
		welcome_label = tk.Label(main_frame, text='Welcome to Price Tracking', font='Times 30 bold')
		first_instruction = tk.Label(welcome_label,
									 text='you can add your first tracking item by click on the Add Item button on top')
		first_instruction.pack(side='bottom', pady=main_frame_width_info[1] / 2 - 50)
		welcome_label.pack(expand='true', fill='both')

	print(time.time() - start_time)
	conn.close()
# main_frame_2.destroy()

# main_frame.after(1000 * 10, lambda: table_frame(master_win, item_id))
