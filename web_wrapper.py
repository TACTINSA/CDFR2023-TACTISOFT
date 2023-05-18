#!/usr/bin/env python3
import inspect
import os
import subprocess
import sys
import threading
from typing import Optional

from flask import Flask, json, request, send_from_directory
from flask_cors import CORS

DEFAULT_SCORE = 41  # TODO Default score in case of error

app = Flask(__name__)
CORS(app)

process: Optional[subprocess.Popen] = None


@app.route('/<path:filename>')
def send_report(filename):
    if '.' not in filename:
        if not filename.endswith('/'):
            filename += '/'
        filename += 'index.html'
    print("File :", filename)
    return send_from_directory('web/public', filename)


def run_main_program(args: list):
    global process
    if process is not None:
        kill_main_program()

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    process = subprocess.Popen([sys.executable, path + "/main.py", "--log-level=debug", *args])


def kill_main_program():
    global process
    if process is not None:
        process.kill()
        process = None


def run_main_program_with_strategy(strategy: str):
    run_main_program(["--strategy", strategy])


def run_main_program_with_remote():
    run_main_program(["--server"])


@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    return json.dumps([entry.name[:-3] for entry in os.scandir(path + '/strategies') if not entry.is_dir()])


@app.route('/api/run_strategy', methods=['POST'])
def run_strategy():
    print("run_strategy", request.json)
    run_main_program_with_strategy(request.json["strategy"])
    return json.dumps({"status": "ok"})


@app.route('/api/run_remote', methods=['POST'])
def run_remote():
    print("run_remote")
    run_main_program_with_remote()
    return json.dumps({"status": "ok"})


@app.route('/api/kill', methods=['POST'])
def kill():
    print("kill")
    kill_main_program()
    return json.dumps({"status": "ok"})


@app.route('/api/get_score', methods=['get'])
def get_score():
    if process is not None:
        process.poll()

    score = process.returncode if process else None
    if score is not None:
        score = score - 1000
    if score is not None and not (0 <= score <= 200):
        print("ABC", score)
        score = DEFAULT_SCORE
    print("get_score", score)
    return json.dumps({"status": "ok", "score": score})


def run_web_server():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    os.system("DISPLAY=:0 /usr/bin/chromium-browser --kiosk http://127.0.0.1:5000/embedded/home")

    if process is not None:
        process.kill()
