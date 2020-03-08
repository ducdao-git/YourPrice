"""
*** Duc Dao ***
About This Script:
app price compare - check to sent mail or not
"""

import app_send_email as sMail

def price_compare(price_diff_float_L, url_L, recipients_L):  # need to print out msg dialog in GUI
	if price_diff_float_L < 0:
		print("Please Check Back Latter, The Item Price Still Higher\n")
		return 0
	elif price_diff_float_L >= 0:
		sMail.email_send(url_L, recipients_L)
		print("Item Price is Lower Than Your Wanted Price")
		return -1
	else:
		print("Something Went Wrong")
