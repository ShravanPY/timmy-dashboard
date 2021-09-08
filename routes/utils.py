import quart
import os
import requests

app = quart.Quart("")
token = os.getenv('token')
ri = os.getenv('ri')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
