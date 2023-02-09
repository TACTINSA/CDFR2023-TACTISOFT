import os
import pathlib
import subprocess
import sys
from typing import Optional

from flask import Flask, json, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

process: Optional[subprocess.Popen] = None


def run_main_program(args: list):
    global process
    if process is not None:
        kill_main_program()
    process = subprocess.Popen([sys.executable, "main.py", "--no-startup", *args])


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
def get_companies():
    return json.dumps([entry.name[:-3] for entry in os.scandir(pathlib.Path(__file__).parent / 'strategies') if not entry.is_dir()])


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


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    if process is not None:
        process.kill()