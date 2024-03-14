# UND Fan ALert

## Introduction
The UND Fan Alert is a Python program designed to check for upcoming hockey games for the University of North Dakota (UND) Fighting Hawks and send push notifications via [NTFY](https://github.com/binwiederhier/ntfy) so you don't miss game time.

## Functionality
- The program fetches the schedule of UND hockey games from a specified URL and stores it locally.
- It checks the schedule daily to determine if there's a game on the current date.
- If a game is found, it sends an alert message containing game details such as opponent, time, and location to the specified NTFY server.

## Dependencies
- Python 3.x
- Requests library for making HTTP requests
- PyYAML library for parsing YAML configuration files
- Schedule library for scheduling tasks
- Logging library for logging messages

## Configuration
- The program's behavior can be configured using a YAML configuration file (`config.yml`).
- Configuration options include:
  - Schedule URL and local file path
  - Messaging server URL and authentication token
  - Logging file path

## Usage
- To use the program, follow these steps:
  1. Ensure all dependencies are installed.
  2. Create a configuration file named `config.yml` with appropriate settings.
  3. Run the main Python script (`und_hockey_alert.py`).

## Future Improvements
- Implement configurable retry logic for failed HTTP requests.
- Enhance alert message formatting and customization options.

## Author
- [Matt Charging (Assimilation)]

## Version History
- [v1.0.0] - [Date]: March 14 2024

## License
- [GPLv2]

## Contact
- For questions or feedback, contact [ mcharging@gmail.com ]