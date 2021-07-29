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

	# total CPU and memory
	cpu_core_percents = [0, 0, 0, 0]  # TODO psutil.cpu_percent(interval=None, percpu=True)  # CPU percent since last call
	memory = psutil.virtual_memory()

	# details for processes with highest CPU and memory
	top_cpu_processes = [{"cpu_percent": -1} for _ in range(3)]
	top_memory_processes = [{"memory_used": -1} for _ in range(3)]

	for proc in psutil.process_iter():
		with proc.oneshot():

			will_add_to_cpu_list = True
			for i in range(len(top_cpu_processes)-1, -1, -1):
				if proc.cpu_percent() < top_cpu_processes[i]["cpu_percent"]:
					if i == len(top_cpu_processes) - 1:
						# proc cpu percent is less than all of them so it shouldn't be added to the list
						will_add_to_cpu_list = False
						break
					else:
						# insert the new process into the list and pop out the last process
						top_cpu_processes.insert(i+1, processToDict(proc))
						top_cpu_processes.pop()

			if will_add_to_cpu_list:
				# greater than all of the existing processes in the list
				top_cpu_processes.insert(0, processToDict(proc))
				top_cpu_processes.pop()

	with open("systemload.json", "w") as file:
		json.dump({
			'cpu_core_percents': cpu_core_percents,
			'memory_used': bytes2human(memory.total - memory.available),
			'memory_total': bytes2human(memory.total),
			'memory_percent': memory.percent,
			'top_cpu_processes': top_cpu_processes
		}, file, indent=None, separators=(',', ':'))

	logging.debug("systemload.json updated.")


def processToDict(proc):
	return {
		"pid": proc.pid,
		"name": proc.name(),
		"cpu_percent": proc.cpu_percent(),
		"memory_used": bytes2human(proc.memory_info().rss),
		"memory_used_bytes": proc.memory_info().rss
	}


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
