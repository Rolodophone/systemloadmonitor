from http.server import SimpleHTTPRequestHandler, HTTPServer
from byte_converter import bytes2human
import psutil
import json


def updateSystemLoadFile():
	print("Updating systemload.json.")

	cpu_core_percents = psutil.cpu_percent(interval=None, percpu=True)  # CPU percent since last call
	cpu_total_percent = 0.0

	memory = psutil.virtual_memory()

	with open("systemload.json", "w") as file:
		json.dump({
			'cpu_core_percents': cpu_core_percents,
			'memory_used': bytes2human(memory.total - memory.available),
			'memory_total': bytes2human(memory.total),
			'memory_percent': memory.percent
		}, file, indent=None, separators=(',', ':'))

	print("systemload.json updated.")


class SystemLoadMonitorHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		print("GET request received")
		if self.path == "/systemload.json":
			updateSystemLoadFile()

		return super().do_GET()


httpd = HTTPServer(('', 8000), SystemLoadMonitorHandler)
httpd.serve_forever()
