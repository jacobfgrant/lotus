#!/usr/bin/env python
#
#
#
#
#
#
# Written by: Jacob F. Grant
# Written: 03/27/2017
# Updated:
#

import sys
import json
import requests


def make_headers(auth_token):
    # Add error if fails
    headers = {'content-type':'application/json','Authorization': 'Bearer ' + auth_token}
    return headers


def get_id_list(auth_token):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = make_headers(auth_token)
    request_json = json.loads(requests.get(url, headers=headers).text)
    
    id_list = []
    for droplet in request_json['droplets']:
        id_list.append(droplet['id'])
            
    return id_list


def get_id_dict(auth_token):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = make_headers(auth_token)
    request_json = json.loads(requests.get(url, headers=headers).text)
    
    id_dict = {}
    for droplet in request_json['droplets']:
        id_dict[droplet['id']] = droplet
            
    return id_dict


def get_tag_list(auth_token, include_empty_tags=False):
    # Returns a list of tags
    url = "https://api.digitalocean.com/v2/tags"
    headers = make_headers(auth_token)
    request_json = json.loads(requests.get(url, headers=headers).text)
    
    tag_list = []
    for tag in request_json['tags']:
        if tag['resources']['droplets']['count'] == 0:
            if include_empty_tags == False:
                continue
        tag_list.append(tag['name'])
            
    return tag_list


def get_tag_dict(auth_token):
    # Returns a dictionary
    url = "https://api.digitalocean.com/v2/droplets?tag_name="
    headers = make_headers(auth_token)
    
    tag_list = get_tag_list(auth_token, False)
    tag_dict = {}
    for tag in tag_list:
        tag_url = url + tag
        tag_dict[tag] = json.loads(requests.get(tag_url, headers=headers).text)
    
    return tag_dict


def get_tag_ip_dict(auth_token, get_public_ip=True):
    # Outputs a dictionary of lists
    tag_dict = get_tag_dict(auth_token)
    
    ip_dict = {}
    for tag in tag_dict:
        ip_dict[tag] = []
        for droplet in tag_dict[tag]['droplets']:
            for ipv4_network in droplet['networks']['v4']:
                if ipv4_network['type'] == 'public' and get_public_ip == True:
                    ip_dict[tag].append(ipv4_network['ip_address'])
                # Add error if no private ip address
                if ipv4_network['type'] == 'private' and get_public_ip == False:
                    ip_dict[tag].append(ipv4_network['ip_address'])
    
    return ip_dict


if __name__ == "__main__":
    main()
