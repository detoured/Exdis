from dotenv import load_dotenv
import os
import sys

def get_token():
    load_dotenv()
    try:
        token = os.getenv('DISCOED_TOKEN')
    except:
        print("Exdis cannot be used without assigning a Discord bot token to the .env file")
        sys.exit(1)

    return token

def get_perm_role_id():
    load_dotenv()
    try:
        perm_role_id = os.getenv('ROLE_ID')
    except:
        print("Exdis cannot be used without assigning an access role id to the .env file")
        sys.exit(1)

    return perm_role_id

def get_non_role_view():
    load_dotenv()
    try:
         match os.getenv('NON_ACCESS_ROLE_VIEW_PERM').lower():
            case "true":
                 non_role_view = True
                 return non_role_view
            case "false":
                 non_role_view = False
                 return non_role_view
    except:
        non_role_view = False

    return non_role_view