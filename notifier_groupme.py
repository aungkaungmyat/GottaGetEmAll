from groupy import Client
import json
import requests

import random
import sys
import time

from hashlib import md5

from camping import SUCCESS_EMOJI

CREDENTIALS_FILE = "groupme_credentials.json"
DELAY_FILE_TEMPLATE = "next_{}.txt"
DELAY_TIME = 1800


with open(CREDENTIALS_FILE) as f:
    groupme_cred= json.load(f)

def create_msg(msg):
    # msg = []
    client = Client.from_token(groupme_cred['access_token_key'])
    messages = client.bots.post(groupme_cred['bot_id'], msg)

    print("The following was messaged: ")
    print()
    print(messages)



first_line = next(sys.stdin)
first_line_hash = md5(first_line.encode("utf-8")).hexdigest()

delay_file = DELAY_FILE_TEMPLATE.format(first_line_hash)
try:
    with open(delay_file, "r") as f:
        call_time = int(f.read().rstrip())
except:
    call_time = 0

if call_time + random.randint(DELAY_TIME-30, DELAY_TIME+30) > int(time.time()):
   print("It is too soon to message again") 
   sys.exit(0)


if "Something went wrong" in first_line:
    create_msg("I'm broken! Please help me, your father Darth Vader.")
    sys.exit()



available_site_strings = []
for line in sys.stdin:
    line = line.strip()
    if SUCCESS_EMOJI in line:
        name = " ".join(line.split(":")[0].split(" ")[1:])
        available = line.split(":")[1][1].split(" ")[0]
        s = "{} site(s) available in {}".format(available, name)
        available_site_strings.append(s)

if available_site_strings:
    msg = "Fellow Darth Vaders!!! "
    msg += first_line.rstrip()
    msg += " 🏕🏕🏕\n"
    msg += "\n".join(available_site_strings)
    msg += "\n" + "🏕" * random.randint(5, 20)  # To avoid duplicate messages.
    create_msg(msg)
    with open(delay_file, "w") as f:
        f.write(str(int(time.time())))
    sys.exit(0)
else:
    print("No campsites available, not messaging 😞")
    sys.exit(1)

