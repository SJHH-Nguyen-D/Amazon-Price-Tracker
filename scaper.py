from bs4 import BeautifulSoup as bs
import requests, webbrowser, os, re, smtplib, time
import argparse, numpy

URL = "https://www.amazon.ca/ATUP-Compatible-Silicone-Replacement-iWatch/dp/B07P32NJVR?pf_rd_p=9eef0d79-b156-55fc-a14a-f3b6e55f1a29&pf_rd_r=BTWB370GSQR4AGSJW24B&pd_rd_wg=JQX98&ref_=pd_gw_ri&pd_rd_w=8S29L&pd_rd_r=5b5a8218-d05d-4095-929c-df61a4f742b6"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

# parser = argparse.ArgumentParser(
# 	description="Send email when price falls below a certain threshold"
# 	)
# parser.add_argument(
# 	"-e",
# 	"--email",
# 	metavar="N",
# 	type=str,
# 	required=True,
# 	default="",
# 	help="email to send this alert to"
# 	)
# parser.add_argument(
# 	"-u",
# 	"--url",
# 	metavar="N",
# 	type=str,
# 	required=True,
# 	default="",
# 	help="url to the Amazon item of interest"
# 	)
# parser.add_argument(
# 	"-d",
# 	"--discount",
# 	metavar="N",
# 	type=int,
# 	default=0,
# 	help="change the percentage of the item the item should be at"
# 	)
# args = parser.parse_args()

def check_price(url):
	""" get the price of an item on amazon given it's URL """
	page = requests.get(url, headers=headers)
	soup = bs(page.content, "html.parser")

	# get the name of the product
	title = soup.find(id="productTitle").get_text().strip()

	# get the price of the product
	price_range = soup.find(id="priceblock_ourprice").get_text()

	# by default, it prints out the price ranges
	# matches the string pattern of a price into an expression and prints them out
	pattern = re.compile(r"\d*\.\d{2}")
	matches = pattern.finditer(price_range)
	
	converted_prices = [float(i[0]) for i in matches]
	floor_price = converted_prices[0]
	ceiling_price = converted_prices[1]

	print("The price for {} is: {} - {} on Amazon.ca".format(
		title, floor_price, ceiling_price)
	)

	return floor_price, ceiling_price

def thresholder(low_price, high_price):
	""" Takes the median of the price ranges """
	threshold = numpy.median(list([low_price, high_price]))

def send_email(destination_email):
	""" Send a default email to the specified email address when the item price falls below a certain value """

	# if we are using our gmail address
	# we must first set up a connection between gmail and our connection
	server = smtplib.SMTP("smtp.gmail.com", 587)
	# Extended simple email transfer protocol sent by an eamil server to identify itself 
	# when connecting to another email server
	server.ehlo()
	server.starttls()
	server.ehlo()

	password = "kfrrvjzdoopxjscm"
	server.login("dennisnguyendo@gmail.com", password)
	
	subject = "The price fell down!"
	body = "Check the Amazon Link! {}".format(URL)

	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		"dennisnguyendo@gmail.com",
		destination_email,
		msg
		)
	print("The email has been sent!")

	server.quit()


def main():
	# you can also set a schedule for the check_price calls with a while loop
	low_range_price, high_range_price = check_price(URL)
	threshold = thresholder(low_range_price, high_range_price)
	# TODO: threshold function calcultor
	if low_range_price < threshold:
		send_email(destination_email="dennisnguyendo@gmail.com")
	else:
		print("The price has not yet fallen below your desired threshold. Please check again later :)")

"""
Things I want to add to the argparser
* destination email
* Amazon URL
* discount percentage
"""

if __name__ == "__main__":
	main()