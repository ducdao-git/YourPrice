"""
*** Duc Dao ***
Notes:
	- Please keep all the py script, picture
	and icon in the dame folder

About This Script: main - display the app
"""
import tkinter as tk
import app_GUI_sys as gSys
import app_GUI_table as gTab

setting_icon_path = "setting_icon.png"
report_icon_path = "report_icon.png"


def app_window_home():
	root_win = tk.Tk()
	root_win.minsize(1072, 603)
	gSys.win_pos(root_win)
	root_win.title("Price Tracking")
	root_win.maxsize(1072, 603)  # problem: auto update table (including text size - not hard code in)
	
	item_id = tk.IntVar()
	
	# button in window
	gSys.add_item(root_win, item_id)
	gSys.edit_item(root_win, item_id)
	gSys.remove_item(root_win, item_id)
	gSys.refresh_table(root_win, item_id)
	
	setting_icon = tk.PhotoImage(file=setting_icon_path).subsample(2, 2)
	gSys.setting(root_win, setting_icon, item_id)
	
	report_icon = tk.PhotoImage(file=report_icon_path).subsample(2, 2)
	gSys.bug_report(root_win, report_icon)
	
	# copyright
	copyright_label = tk.Label(root_win, text='Copyright 2019 D.M. Dao. All rights reserved.', anchor='sw', fg='grey')
	copyright_label.place(relx=0, rely=1, anchor='sw')
	
	# table in window
	gTab.table_frame(root_win, item_id)
	
	# loop
	def loop():
		root_win.destroy()
		app_window_home()
	
	aSecond = 1000  # (ms)
	aMin = aSecond * 60
	root_win.after(aMin * 60, loop)  # refresh_rate
	
	root_win.mainloop()


app_window_home()
