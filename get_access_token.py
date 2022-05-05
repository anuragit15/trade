#!/usr/bin/env python3
from alice_blue import *
access_token = AliceBlue.login_and_get_access_token(username='', password='', twoFA='', api_secret='', app_id='')
print(access_token)
with open('access_token', 'w') as file:
    file.write(access_token)
