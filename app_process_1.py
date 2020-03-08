"""
*** Duc Dao ***
About This Script:
app process 1 - receive input from app gui system
			  - check for valid input
			  - process some data then save into database
"""

import urllib.request as urq
from bs4 import BeautifulSoup as bs
import sqlite3 as sql
import error_handler as err_h

# --------------------------------------user price--------------------------------------#

def user_price_int(user_price):
	try:
		return int(user_price)
	except Exception as e:
		err_h.error_handler(e)
		return -1

# -----------------------------------------end-----------------------------------------#

def item_name_str(url):
	try:
		web_page = urq.urlopen(url)  # (Open the URL) .urlopen take string or Request obj as it parameter
		content = bs(web_page, 'html.parser')
		if url.find('amazon.com') != -1:  # HTTP Error 503: Service Unavailable (st)
			item_name_str_L = content.find(id="productTitle").get_text().strip()
			content.find(id=["priceblock_ourprice", "priceblock_dealprice", "priceblock_saleprice"]).get_text()
		elif url.find('bhphotovideo.com') != -1:
			item_name_str_L = content.find(class_="title_3bJZzlB3PKkE_8ajs9mroe").get_text().strip()
			content.find(class_=["price_1DPoToKrLP8uWvruGqgtaY"]).get_text()
		elif url.find('bestbuy.com') != -1:  # Operational Time
			item_name_str_L = content.find(class_="heading-5 v-fw-regular").get_text().strip()
			content.find(class_=["priceView-hero-price priceView-customer-price"]).get_text()
		elif url.find('apple.com') != -1:  # HTTP Error 403: Forbidden
			item_name_str_L = content.find(class_="as-productdecision-header").get_text().strip()
			item_name_str_L = item_name_str_L.replace("Buy", "")
			content.find(class_=["as-price-currentprice", "current_price"]).get_text()
		return item_name_str_L
	except Exception as e:
		err_h.error_handler(e)
		return -1

# ---------------------------------------database---------------------------------------#
def process_1(url, user_price, mail_recipient_input):
	save_url_str = url
	save_item_name_str = item_name_str(url)
	if save_item_name_str == -1:
		return -1
	save_user_price_int = user_price_int(user_price)
	if save_user_price_int == -1:
		return -1
	save_recipients_str = mail_recipient_input
	if save_recipients_str.find('@') == -1:
		err_h.error_handler('recipients_err')
		return -1
	conn = sql.connect('tracking_item.db')
	c = conn.cursor()

	try:
		c.execute("""CREATE TABLE tracking_item (
			url_str text,
			item_name_str text, 
			user_price_int integer,
			recipients_str text
			)""")
	except sql.OperationalError:
		pass

	c.execute("""INSERT INTO tracking_item VALUES (:url_str,
	:item_name_str,:user_price_int, :recipients_str)""",
			  {'url_str': save_url_str,
			   'item_name_str': save_item_name_str,
			   'user_price_int': save_user_price_int,
			   'recipients_str': save_recipients_str
			   })

	conn.commit()
	conn.close()
	return 1

# ----------------------------------------end----------------------------------------#
