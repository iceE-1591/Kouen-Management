import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN        = os.environ.get("TOKEN")
GUILD_ID     = os.environ.get("GUILD_ID")
CHANNEL_ID   = os.environ.get("CHANNEL_ID")
MESSAGE_ID   = os.environ.get("MESSAGE_ID")
ROLE_ID      = os.environ.get("ROLE_ID")
ARCHIVE_ID   = os.environ.get("ARCHIVE_ID")
VC_ID        = os.environ.get("VC_ID")
SANKA_ID     = os.environ.get("SANKA_ID")
KIKISEN_ID   = os.environ.get("KIKISEN_ID")
DELETE_ID    = os.environ.get("DELETE_ID")
DELETE_ID_ID = os.environ.get("DELETE_ID_ID")