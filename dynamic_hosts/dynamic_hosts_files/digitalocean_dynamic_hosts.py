#!/usr/bin/env python
#
#
#
# Written by: Jacob F. Grant
# Written: 03/27/2017
# Updated:
#

import os
import sys
import json
import ConfigParser
import argparse
# Need to pip install requests (somehow)
import requests

# Import api_functions
sys.path.append('/root/lotus/dynamic_hosts/api_functions/')
from digitalocean_api_functions import *

# Get credentials (DO API token)
config = ConfigParser.ConfigParser()
digitalocean_credentials_config = config.read("/root/.lotus_credentials/digitalocean_credentials")
digitalocean_auth_token = config.get("digitalocean","auth_token")



class DigitalOcean_Inventory(object):
    def __init__(self):
        self.inventory = {}
        self.parse_args()
        #self.list_inventory()
        
        if self.args.list:
            self.inventory = self.list_inventory()
        
        elif self.args.host:
            self.inventory = self.host_inventory()
        
        else:
            self.empty_inventory()
        
        print json.dumps(self.inventory)
    
    
    def list_inventory(self):
        # Rewrite this function
        tag_list = get_tag_list(digitalocean_auth_token)
        # Needs improving; very brittle
        tag_ip_dict = get_tag_ip_dict(digitalocean_auth_token, False)
        
        inventory = {}
        # Add error if tag_list has no elements
        for tag in tag_list:
            inventory[tag] = {'hosts':tag_ip_dict[tag],'vars':{}}
        # Generate non-empty values for thse
        #inventory['_meta'] = {'hostvars':{}}
        
        return inventory
    
    
    def host_inventory(self):
        tag_list = get_tag_list(digitalocean_auth_token)
        # THROW ERROR INSTEAD
        tag = self.args.host
        if tag not in tag_list:
            #return self.empty_inventory()
            #return {'_meta': {'hostvars':{}}}
            return {}
        
        inventory = {}
        tag_ip_dict = get_tag_ip_dict(digitalocean_auth_token, False)
        inventory[tag] = {'hosts':tag_ip_dict[tag],'vars':{}}
        
        return inventory
    
    
    def empty_inventory(self):
        #return {'_meta': {'hostvars':{}}}
        return {}
    
    
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--list", help="", action = 'store_true')
        parser.add_argument("--host", help="", action = 'store')
        self.args = parser.parse_args()
        


if __name__ == "__main__":
    DigitalOcean_Inventory()
