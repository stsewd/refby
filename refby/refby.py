import os
import re
from urllib import request

import config
from .errors import PrivateOrInvalidProfileError
from .errors import UserIdNotFoundError

import facebook
from bs4 import BeautifulSoup


_graph = facebook.GraphAPI(config.access_token)


def _get_user_id_from_html(html):
    regex_profile_owner = re.compile(r'"profile_owner":"(\d+)"')
    try:
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find(id="pagelet_timeline_main_column").get('data-gt')
        user_id = re.search(regex_profile_owner, data).group(1)
        return user_id
    except:
        raise UserIdNotFoundError()


def get_user_id(user):
    facebook_url = "http://www.facebook.com/"
    try:
        html = request.urlopen(facebook_url + user)
        user_id = _get_user_id_from_html(html.read())
        return user_id
    except request.HTTPError:
        raise PrivateOrInvalidProfileError(user)


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
        file_name = (
            output
            if os.path.isfile(output)
            else _get_file_name(output, picture)
        )
        _save_image_from_url(picture['url'], file_name)
    else:
        raise OutputDirectoryError(output)
