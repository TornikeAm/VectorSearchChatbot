import subprocess

subprocess.run(["python", "-m", "pip", "install", "-r", "requirements.txt"])
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])