import os
import json
from urllib import request

import config

import facebook
from bs4 import BeautifulSoup


_graph = facebook.GraphAPI(config.access_token)


def search_facebook(query, search_type='user'):
    return _graph.get_object("search", q=query, type=search_type)


def get_user_id(user):
    # TODO 404 private profile
    facebook_url = "http://www.facebook.com/"
    html = request.urlopen(facebook_url + user)
    soup = BeautifulSoup(html.read(), 'html.parser')
    div = soup.find(id="pagelet_timeline_main_column")
    data = json.loads(div.get('data-gt'))  # TODO regex
    return data['profile_owner']


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
