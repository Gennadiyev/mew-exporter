'''mewpy/api.py

The low-level API of the mewpy package.
'''

from typing import Union
from copy import deepcopy
import requests

def login(phone: Union[str, int], password: str) -> dict:
    '''Login to Mew.

    @param phone: The phone number of the user.
    @type phone: str or int
    @param password: The password of the user.
    @type password: str
    @return: The login response.
    '''
    url = 'https://api.mew.fun/api/v2/auth/login'
    data = {
        'phone': str(phone),
        'password': str(password)
    }
    # Post data as json
    req_login = requests.post(url, json=data)
    return req_login.json()

def get_all_user_thoughts(user_id: str, token: str) -> dict:
    '''Get all thoughts created by user.

    @param user_id: The Mew user ID.
    @type user_id: str
    @param token: The Mew token.
    @type token: str
    @return: The thoughts response.
    '''
    # Send first request
    url = 'https://api.mew.fun/api/v1/users/{}/timeline'.format(user_id)
    headers = {
        'authorization': f'Bearer {token}',
        'accept': 'application/json text/plain */*',
        'referer': 'https://mew.fun/'
    }
    params = {
        'limit': 20,
        'media': False
    }
    first_req = requests.get(url, headers=headers, params=params)
    first_req_json = first_req.json()
    # Assert request successful
    assert "entries" in first_req_json and "objects" in first_req_json and "pagination" in first_req_json, "The first request to get thoughts failed with response: {}".format(first_req_json)
    # Construct result dict
    result = {}
    result["entries"] = first_req_json.get("entries", [])
    result["objects"] = first_req_json.get("objects", {"embeds":{},"media":{},"topics":{},"users":{}})
    # Get pagination
    pagination = first_req_json.get("pagination", False)
    while pagination:
        params["before"] = pagination
        req = requests.get(url, headers=headers, params=params)
        req_result = req.json()
        result["entries"] += req_result.get("entries", [])
        result["objects"]["embeds"].update(req_result.get("objects", {}).get("embeds", {}))
        result["objects"]["media"].update(req_result.get("objects", {}).get("media", {}))
        result["objects"]["topics"].update(req_result.get("objects", {}).get("topics", {}))
        result["objects"]["users"].update(req_result.get("objects", {}).get("users", {}))
        pagination = req_result.get("pagination", False)
    return result

def get_node_info(node_id: str, extra_headers: dict = {}) -> dict:
    '''Get node info.
    
    @param node_id: The node id.
    @type node_id: str
    @param extra_headers: Extra headers to be sent. Optional.
    @type extra_headers: dict
    @return: The node info response.
    '''
    url = 'https://api.mew.fun/api/v1/nodes/{}'.format(node_id)
    req_node_info = requests.get(url, headers=extra_headers)
    return req_node_info.json()
