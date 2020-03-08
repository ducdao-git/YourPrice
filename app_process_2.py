"""
*** Duc Dao ***
About This Script:
app process 2 - take data from database, process
			  - send data to table and compare price
"""

import urllib.request as urq
from bs4 import BeautifulSoup as bs
import app_price_compare as pComp

def extract_info(record):
	url_L = record[0]
	user_price_L = record[-3]
	recipients_L = record[-2]
	return {'url': url_L, 'user_price_int': user_price_L, 'recipients_str': recipients_L}

def mail_recipient_lst(recipients_input):
	recipient_lst_L = str(recipients_input)
	recipient_lst_L = recipient_lst_L.replace(" ", "").split(",")
	return recipient_lst_L

def price_diff_float(item_price_float_L, user_price_L):
	return user_price_L - item_price_float_L

def price_diff_str(price_diff_float_L):
	price_diff_str_L = '$ {:,.2f}'.format(price_diff_float_L)
	return price_diff_str_L

def user_price_str(user_price_L):
	user_price_str_L = user_price_L
	if user_price_str_L == 'None':
		pass
	else:
		user_price_str_L = '$ {:,.2f}'.format(user_price_str_L)
		return user_price_str_L
# --------------------------------------item price--------------------------------------#

def page_content_dic(url):
	try:
		web_page = urq.urlopen(url)  # (Open the URL) .urlopen take string or Request obj as it parameter
		content = bs(web_page, 'html.parser')
		if url.find('amazon.com') != -1:
			item_price_str_L = content.find(id=["priceblock_ourprice", "priceblock_dealprice", "priceblock_saleprice"]).get_text()
		elif url.find('bhphotovideo.com') != -1:
			item_price_str_L = content.find(class_=["price_1DPoToKrLP8uWvruGqgtaY"]).get_text()
		elif url.find('bestbuy.com') != -1:
			item_price_str_L = content.find(class_=["priceView-hero-price priceView-customer-price"]).get_text()
		elif url.find('apple.com') != -1:
			item_price_str_L = content.find(class_=["as-price-currentprice","current_price"]).get_text()
		return item_price_str_L
	except ValueError:
		print('Please Recheck Your URL Link')

def item_price_float(url):
	item_price_str_L = page_content_dic(url)
	item_price_str_L = item_price_str_L.replace(",", "")
	item_price_float_L = float(item_price_str_L[1::])
	return item_price_float_L

def item_price_str(item_price_float_L):
	item_price_str_L = '$ {:,.2f}'.format(item_price_float_L)
	return item_price_str_L

# -----------------------------------------end-----------------------------------------#

def process_2(record):
	info = extract_info(record)
	# print(info['user_price_int'])

	recipient_lst_L = mail_recipient_lst(info['recipients_str'])
	item_price_float_L = item_price_float(info['url'])
	price_diff_float_L = price_diff_float(item_price_float_L, info['user_price_int'])

	pComp.price_compare(price_diff_float_L, info['url'], recipient_lst_L)

	user_price_str_L = user_price_str(info['user_price_int'])
	item_price_str_L = item_price_str(item_price_float_L)
	price_diff_str_L = price_diff_str(price_diff_float_L)
	return [item_price_str_L, price_diff_str_L, recipient_lst_L, user_price_str_L]

# record = (
# 	'https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27/ref=pd_ybh_a_6?_encoding=UTF8&psc=1&refRID=XPFSD1EFDVKMX56HFHTA',
# 	'Raspberry Pi 4 Model B 2019 Quad Core 64 Bit WiFi Bluetooth (2GB)', 50, '$ 50.00',
# 	'ddao23@wooster.edu, samducdao872k1@gmail.com',
# 	2)
# process_2(record)
