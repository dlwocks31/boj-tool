import os
import requests
import pickle
import getpass

from bs4 import BeautifulSoup as bs
from xdg import XDG_DATA_HOME

data_dir = XDG_DATA_HOME + '/boj-submit'
boj_url = 'https://www.acmicpc.net'
cookiefile_path = data_dir + '/cookiefile'
sess = requests.Session()


def initialize():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def auth_user(username, password):
    data = {'login_user_id': username,
            'login_password': password,
            'auto_login': 'on'}
    sess.post(boj_url + '/signin', data=data)


def check_login():
    soup = bs(sess.get(boj_url).text, 'html.parser')
    return soup.find('a', {'class': 'username'}) is not None


def save_cookie(session):
    with open(cookiefile_path, 'wb') as f:
        pickle.dump(session.cookies, f)


def login():
    username = input('Username: ')
    password = getpass.getpass()
    auth_user(username, password)
    save_cookie(sess)


if __name__ == '__main__':
    initialize()
    if os.path.isfile(data_dir + '/cookiefile'):
        with open(data_dir + '/cookiefile', 'rb') as f:
            sess.cookies.update(pickle.load(f))
    else:
        login()
    if check_login():
        print('Logged in')
    else:
        print('Login failed')
        os.remove(cookiefile_path)
