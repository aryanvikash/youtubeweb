import threading
import subprocess

users ={}
user_time = {}


subprocess.Popen(["gunicorn", "web:app"])



