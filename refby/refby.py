import os
import json
from urllib import request

import config

import facebook
from bs4 import BeautifulSoup


_graph = facebook.GraphAPI(config.access_token)


def search_facebook(query, search_type='user'):
    return _graph.get_object("search", q=query, type=search_type)


def _get_user_id_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find(id="pagelet_timeline_main_column").get('data-gt')
    data = json.loads(data)  # TODO regex {"profile_owner":"id_numer","ref":"timeline:timeline"}
    return data['profile_owner']


def get_user_id(user):
    # TODO 404 private profile
    facebook_url = "http://www.facebook.com/"
    html = request.urlopen(facebook_url + user)
    user_id = _get_user_id_from_html(html.read())
    return user_id


def get_profile(user_id):
    profile = _graph.get_object(user_id)
    return profile


def get_profile_picture(user_id):
    profile = get_profile(user_id)
    picture = _graph.get_connections(profile['id'], 'picture', type='large', fileld={'url'})
    picture['user'] = profile
    return picture


def _save_to_file(image, file_name):
    with open(file_name, 'wb') as output:
        output.write(image.read())


def _save_image_from_url(url, file_name):
    with request.urlopen(url) as image:
        _save_to_file(image, file_name)


def _get_file_name(output, picture):
    user_name = picture['user']['name']
    user_id = picture['user']['id']
    file_extension = ".jpg"
    file_name = os.path.join(output, user_name + " (" + user_id + ")" + file_extension)
    return file_name


def download_profile_picture(user_id, output):
    if os.path.exists(output):
        picture = get_profile_picture(user_id)
        file_name = output if os.path.isfile(output) else _get_file_name(output, picture)
        _save_image_from_url(picture['url'], file_name)
    else:
        raise Exception("Output directory doesn't exists: " + output)
