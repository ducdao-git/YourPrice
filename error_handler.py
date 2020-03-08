"""
*** Duc Dao ***
About This Script:
error handler - decide what to do with different errors
"""

import tkinter as tk

def toplevel_win_pos(toplevel_win):
	sys_width_L = toplevel_win.winfo_screenwidth()
	sys_height_L = toplevel_win.winfo_screenheight()

	toplevel_win.update()
	app_width_L = toplevel_win.winfo_width()
	app_height_L = toplevel_win.winfo_height()

	app_x_pos = int(sys_width_L / 2 - app_width_L / 2)
	app_y_pos = int(sys_height_L / 2 - app_height_L / 2)

	toplevel_win.geometry(f'{app_width_L}x{app_height_L}+{app_x_pos}+{app_y_pos}')
	return {'app_x_pos': app_x_pos, 'app_y_pos': app_y_pos}

def pop_up_transit(self):
	self.lift()
	self.grab_set()
	self.title('Error Occurred!')
	self.minsize(400, 200)
	self.resizable(0, 0)

def error_handler(error_code):
	popup_win = tk.Toplevel()
	pop_up_transit(popup_win)

	err = str(error_code)

	# internet errors
	if err.find('503') != -1:
		msg = 'The Service Is Unavailable At The Moment\nPlease Come Back At Another Times'
	elif err.find('unknown url type') != -1:
		msg = 'Please Recheck Your URL Address'
	elif err.find('Errno 8') != -1 or err.find('CERTIFICATE_VERIFY_FAILED') != -1:
		msg = 'Please Recheck Your Internet Connection'
	elif err.find('403') != -1 or err.find("'NoneType' object has no attribute 'get_text'") \
			!= -1 or err.find('403') != -1 or err.find('[Errno 60]') != -1:
		msg = 'This Site Not Supported Yet '

	# price input error
	elif err.find('ValueError') != -1 or err.find('invalid literal for int()') != -1:
		msg = 'Invalid Wanted Price\nPlease Enter Your Desire Price In Whole Number Only\n(Remove "," "$" "." If Have Any)'

	# recipients input error
	elif err.find('recipients_err') != -1:
		msg = 'Invalid Recipients Email Address\nPlease Double Check The Recipients Email Address'

	else:
		msg = err

	err_msg = tk.Button(popup_win, text=msg, font=16, command=lambda: popup_win.destroy())
	err_msg.pack(expand='true', fill='both')

	toplevel_win_pos(popup_win)
