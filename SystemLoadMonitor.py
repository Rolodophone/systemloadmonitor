from http.server import SimpleHTTPRequestHandler, HTTPServer
from byte_converter import bytes2human
import psutil
import json
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def updateSystemLoadFile():
	logging.debug("Updating systemload.json.")

	cpu_core_percents = psutil.cpu_percent(interval=None, percpu=True)  # CPU percent since last call

	memory = psutil.virtual_memory()

	with open("systemload.json", "w") as file:
		json.dump({
			'cpu_core_percents': cpu_core_percents,
			'memory_used': bytes2human(memory.total - memory.available),
			'memory_total': bytes2human(memory.total),
			'memory_percent': memory.percent
		}, file, indent=None, separators=(',', ':'))

	logging.debug("systemload.json updated.")


def checkLoadThreadFun():
	while True:
		updateSystemLoadFile()
		time.sleep(0.2)


logging.info("Starting check load thread.")
check_load_thread = threading.Thread(target=checkLoadThreadFun)
check_load_thread.start()

logging.info("Starting server.")
httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
