import requests
import urllib
import datetime
import time
status_endpoint = "/status"
headers = {"Content-Type": "application/json"}
server_url = input("Server URL: ")
parsed_url = urllib.parse.urlparse(server_url)
scheme = parsed_url.scheme
netloc = parsed_url.netloc
if scheme == "ss14":
    response = requests.get("http://" + netloc + status_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        name = data.get('name', 'Unknown')
        players = data.get('players', 0)
        soft_max_players = data.get('soft_max_players', 0)
        run_level = data.get('run_level', 0)
        round_start_time = data.get('round_start_time', None)
        if run_level == 1:
            if round_start_time is not None:
                round_start_time = datetime.datetime.fromisoformat(round_start_time)
                round_start_time = round_start_time.replace(tzinfo=None)
                current_time = datetime.datetime.utcnow()
                round_time = current_time - round_start_time
                round_time = str(round_time).split('.')[0]
                print(f"{name}\n{players}/{soft_max_players} players\nRound: in progress, {round_time}")
                while True:
                    current_time = datetime.datetime.utcnow()
                    round_time = current_time - round_start_time
                    round_time = str(round_time).split('.')[0]
                    print("\r", end="")
                    print(f"Round: in progress, {round_time}", end="")
                    time.sleep(1)

            else:
                print(f"Error: round_start_time is None")

        else:
            print(f"{name}\n{players}/{soft_max_players} players\nRound: offline")

    else:
        print(f"Error: {response.status_code}")

else:
    print(f"Invalid URL: {server_url}")
