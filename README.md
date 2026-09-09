
# Exdis

A Discord bot for remotely executing shell commands.


## Installation & Setup

```
# Make a discord bot with the message content intent and save its token

# Create an acess role for the bot and save its id

# Clone the repository
git clone https://github.com/detoured/Exdis

# Navigate to the Exdis directory
cd Exdis

# Sync uv
uv sync

# Create .env file with the Discord bot token and the acess role id
echo -e "DISCOED_TOKEN={token}\nROLE_ID={id}" > .env

# start the bot
uv run main.py
```

## Usage - In Discord

Create a shell channel (must be sent in a non shell channel):
 ```
 user: !start
Exdis: @user - New shell: ⁠#shell
 ```

Remove & exit a shell channel (must be sent in a shell channel):
 ```
 user: !exit
 ```

 Stop the Exdis bot (must be sent in a non shell channel):
 ```
 user: !stop
 Exdis: Stopping Exdis
 ```

  To execute commands simply send them in a shell channel.

## Acess Role
Those who arent assigned the acess role will not be able to use commands. However, they WILL be able to see shell channels and all of their content

## Disclaimer
This project is intended for educational and authorized use only. Do not use this software to access, control, or interfere with systems, networks, or devices without explicit permission from the owner. I am not responsible for any misuse, damage, or illegal activity resulting from the use of this project. By using this software, you accept full responsibility for ensuring that your use complies with all applicable laws and regulations.



## Acknowledgements

  Inspired by: [kaden-h](https://github.com/kaden-h)
