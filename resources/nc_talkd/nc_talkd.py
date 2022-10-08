# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.

import logging
import string
import sys
import os
import time
import datetime
import traceback
import re
import signal
from optparse import OptionParser
from os.path import join
import json
import argparse
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

def read_socket():
	global talk
	global tps
	global JEEDOM_SOCKET_MESSAGE
	if not JEEDOM_SOCKET_MESSAGE.empty():
		logging.debug("Message received in socket JEEDOM_SOCKET_MESSAGE")
		message = JEEDOM_SOCKET_MESSAGE.get().decode('utf-8')
		message =json.loads(message)
		if message['apikey'] != _apikey:
			logging.error("Invalid apikey from socket : " + str(message))
			return
		try:
			if message['eq_clear'] == "1":
				talk={}
				tps={}
			talk[message['eq_id']]=message['talk_id']
			tps[message['eq_id']]=0
			logging.debug("talk " + talk[message['eq_id']] + " added to " + message['eq_id'])
		except e:
			logging.error('Send command to demon error : '+str(e))

def listen():
	global JEEDOM_COM
	global tps
	jeedom_socket.open()
	try:
		while 1:
			time.sleep(_tps)
			read_socket()
			logging.debug(_url)
			for eq in talk:
				logging.debug(talk[eq])
				headers = {
					'Content-type': 'application/json',
					'OCS-APIRequest': 'true',
					'Accept': 'application/json'
				}
				data = '{"lookIntoFuture":0,"limit":1,"setReadMarker":1}'
				response = requests.get(_url+'/ocs/v2.php/apps/spreed/api/v1/chat/'+talk[eq], headers=headers, data=data,auth = HTTPBasicAuth(_user, _pswd), verify = False)
				if response.ok:
					logging.debug(response.content)
					if len(response.content)>0:
						msg=response.json()["ocs"]["data"][0]['message']
						temps=response.json()["ocs"]["data"][0]['timestamp']
						author=response.json()["ocs"]["data"][0]['actorId']
						if temps != tps[eq]:
							tps[eq]=temps
							logging.debug(temps)
							if (author != _user):
								JEEDOM_COM.send_change_immediate({'eq_id' : eq,'info' : msg,'author' : author,'timestamp':temps})
								logging.debug(msg)
				else:
					logging.debug('Talk ID inconnu')
	except KeyboardInterrupt:
		shutdown()

# ----------------------------------------------------------------------------

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.debug("Shutdown")
	logging.debug("Removing PID file " + str(_pidfile))
	try:
		os.remove(_pidfile)
	except:
		pass
	try:
		jeedom_socket.close()
	except:
		pass
	logging.debug("Exit 0")
	sys.stdout.flush()
	os._exit(0)

# ----------------------------------------------------------------------------

_log_level = "debug"
_socket_port = 52029
_socket_host = 'localhost'
_device = 'auto'
_pidfile = '/tmp/nc_talkd.pid'
_apikey = ''
_callback = ''
_cycle = 0.3
_user = "ncuser"
_pswd = "ncpsw"
_url = "url_nc"
_tps = 5
talk={}
tps={}
parser = argparse.ArgumentParser(
    description='Desmond Daemon for Jeedom plugin')
parser.add_argument("--device", help="Device", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--callback", help="Callback", type=str)
parser.add_argument("--apikey", help="Apikey", type=str)
parser.add_argument("--cycle", help="Cycle to send event", type=str)
parser.add_argument("--pid", help="Pid file", type=str)
parser.add_argument("--socketport", help="Port for service", type=str)
parser.add_argument("--user", help="NextCloud Username", type=str)
parser.add_argument("--pswd", help="NextCloud User Password", type=str)
parser.add_argument("--url", help="NextCloud URL", type=str)
parser.add_argument("--port", help="deamon port", type=str)
parser.add_argument("--tps", help="time base in second", type=str)
args = parser.parse_args()

if args.user:
	_user = args.user
if args.pswd:
	_pswd = args.pswd
if args.url:
	_url = args.url
if args.tps:
	_tps = int(args.tps)
if args.port:
	_socket_port = args.port
if args.device:
	_device = args.device
if args.loglevel:
    _log_level = args.loglevel
if args.callback:
    _callback = args.callback
if args.apikey:
    _apikey = args.apikey
if args.pid:
    _pidfile = args.pid
if args.cycle:
    _cycle = float(args.cycle)
if args.socketport:
	_socketport = args.socketport

_socket_port = int(_socket_port)

jeedom_utils.set_log_level(_log_level)

logging.info('Start demond')
logging.info('Log level : '+str(_log_level))
logging.info('Socket port : '+str(_socket_port))
logging.info('Socket host : '+str(_socket_host))
logging.info('PID file : '+str(_pidfile))
logging.info('Apikey : '+str(_apikey))
logging.info('Device : '+str(_device))
logging.info('User : '+str(_user))
logging.info('Password : '+str(_pswd))
logging.info('URL : '+str(_url))
logging.info('tps : '+str(_tps))

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

try:
	jeedom_utils.write_pid(str(_pidfile))
	JEEDOM_COM=jeedom_com(apikey = _apikey,url = _callback,cycle=_cycle)

	if not JEEDOM_COM.test():
		logging.error('GLOBAL------Network communication issues. Please fix your Jeedom network configuration.')
		shutdown()

	jeedom_socket = jeedom_socket(port=_socket_port,address=_socket_host)
	listen()
except Exception as e:
	logging.error('Fatal error : '+str(e))
	logging.info(traceback.format_exc())
	shutdown()
