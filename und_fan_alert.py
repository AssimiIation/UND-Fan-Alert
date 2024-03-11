from datetime import date
import requests, logging, yaml, os, schedule, time

class HockeyGame:
    def __init__(self, date, time, at, opponent, location, ):
        self.date = date
        self.time = time
        self.at = at
        self.opponent = opponent
        self.location = location

    def print_game(self):
        print(f"UND vs { self.opponent } { self.time } @ { self.location }, ")

def load_config(config_file):
    global schedule_url, schedule_filepath, message_server, auth_token, logging_filepath
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        schedule_url = config[0]['schedule']['url']
        schedule_filepath = config[0]['schedule']['filepath']
        message_server = config[1]['messaging']['server']
        auth_token = config[1]['messaging']['token']
        logging_filepath = config[2]['logging']['filepath']
    print("Configuration loaded")

def generate_logfile(log_filepath):
    log_path = './log'
    try:
        os.mkdir(log_path)
        print(f"Log folder created")
    except Exception as e:
        print(f"Log folder exists")

    if not os.path.exists(log_filepath):
        f = open(log_filepath, "a")
        f.close()
        print("Log file generated")
    else:
        print("Log file exists")

def configure_logging(log_filepath):
    generate_logfile(log_filepath)
    logging.basicConfig(filename=log_filepath, filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)

def log(text, log_type='info'):
    print(text)
    if log_type == 'info':
        logging.info(text)
    if log_type == 'error':
        logging.error(text)

def schedule_exists():
    check_for_schedule()
    if os.path.exists(schedule_filepath):
        return True
    else:
        return False

def check_for_schedule():
    schedule = pull_schedule(schedule_url)
    if schedule != None:
        print("Checking for existing schedule...", end=" ")
        if os.path.exists(schedule_filepath):
            print("Found!")
            new = remove_empty_lines(schedule.text)
            with open(schedule_filepath, "r") as f:
                existing = f.read()
            if schedules_match(new, existing):
                log("Schedules are the same, discarding fetched schedule")

            else:
                log("Fetched schedule is newer than existing. Updating existing schedule...")
                write_schedule_to_file(new, schedule_filepath)
        else:
            print("None found")
            write_schedule_to_file(schedule.text, schedule_filepath)

def schedules_match(new, existing):
    if new == existing:
        return True
    else:
        return False
    
def pull_schedule(url):
    print("Attempting to pull schedule...")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    headers = {'User-Agent': user_agent}
    r = requests.get(url, headers=headers)
    if r.ok:
        log(f"Schedule downloaded successfully from: { url }")
        return r
    else:
        log(f"[ERROR] Pulling schedule failed: { r.response }")
        return None

def check_for_game(date):
    print("Checking if there is a game today...", end=" ")
    with open(schedule_filepath, "r") as file:
        lines = file.readlines()
        for line in lines:
            if date in line:
                while line.replace("   ", "  ") != line:
                    line = line.replace("   ", "  ")
                game_data = line.strip().split("  ")
                game = HockeyGame(game_data[0], game_data[1], game_data[2],game_data[3], game_data[4])
                return game
        else:
            return None

def remove_empty_lines(text):
    return os.linesep.join([s for s in text.splitlines() if s])

def write_schedule_to_file(schedule, filepath):
    filename = "schedule.txt"
    schedule_no_lines = remove_empty_lines(schedule)
    with open(filename, "w") as f:
        f.write(schedule_no_lines)
    log(f"Schedule written to '{ filename }' successfully")

def get_alert_time(gametime):
    if gametime[0].isnumeric():
        split_time = gametime.split()
        time = split_time[0][0]
        meridiem = split_time[1].replace('.', '')
        return time+meridiem
    else:
        return "TBD"

def send_game_alert(game):
    global message_server
    message_title = f"UND vs { game.opponent }"
    message = f"Time: {game.time }\nLocation: {game.location}"
    alert_time = get_alert_time(game.time)
    print(f"Alert time: {alert_time}")
    # alert_time = "TBA"
    if alert_time != "TBA":
        requests.post(message_server,
                    data = message, 
                    headers={"Authorization": f"Bearer { auth_token }","Tags": "ice_hockey", "Title": message_title, "At": alert_time})
        log(f"Game alert queued for delivery at { alert_time }: { message_title } { message }")
    else:
        requests.post(message_server,
                    data = message,
                    headers={"Authorization": f"Bearer { auth_token }","Tags": "ice_hockey", "Title": message_title})
        log(f"Game alert sent immediately: { message_title } { message }")

def daily_check():
    log(" -- Starting daily check --")
    if schedule_exists():
        game = check_for_game(today)
        if game != None:
            print("game found!")
            print(f"    UND vs { game.opponent} {game.time } @ { game.location }")
            try:
                send_game_alert(game)
            except Exception as e:
                log(f"[ERROR]: {e}", 'error')
        else:
            log("No game today")
    else:
        log("No schedule found/obtained - aborting")
    log("Finished\n")

schedule_url: str
schedule_filepath: str
message_server: str
auth_token: str
logging_filepath: str

load_config("./config.yml")
configure_logging(logging_filepath)
today = date.today().strftime("%b %-d")

schedule.every().day.at("08:00:00").do(daily_check)
while True:
 
    # Checks whether a scheduled task 
    # is pending to run or not
    schedule.run_pending()
    time.sleep(60)