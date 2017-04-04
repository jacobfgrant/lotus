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
import requests

# Get credentials
lotus_credentials_config = ConfigParser.ConfigParser()
lotus_credentials = lotus_credentials_config.read("/root/.lotus_credentials")

# Get authorization here
# Use lotus_credentials to chose which
api_auth_token = lotus_credentials_config.get("digitalocean","auth_token")

# Import api_functions
# Choose API to import wrappers
# Will use input from lotus_credentials to determine which API
sys.path.append('/etc/ansible/api_functions/')
from digitalocean_api_functions import *



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
        tag_list = get_tag_list(api_auth_token)
        # Needs improving; very brittle
        tag_ip_dict = get_tag_ip_dict(api_auth_token, False)
        
        inventory = {}
        # Add error if tag_list has no elements
        for tag in tag_list:
            inventory[tag] = {'hosts':tag_ip_dict[tag],'vars':{}}
        # Generate non-empty values for thse
        #inventory['_meta'] = {'hostvars':{}}
        
        return inventory
    
    
    def host_inventory(self):
        tag_list = get_tag_list(api_auth_token)
        # THROW ERROR INSTEAD
        tag = self.args.host
        if tag not in tag_list:
            #return self.empty_inventory()
            #return {'_meta': {'hostvars':{}}}
            return {}
        
        inventory = {}
        tag_ip_dict = get_tag_ip_dict(api_auth_token, False)
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
