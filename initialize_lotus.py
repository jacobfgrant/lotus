#!/usr/bin/env python
#
#
#
# Written by: Jacob F. Grant
# Written: 03/29/2017
# Updated:
#

import json
import getpass
# Add way to pip
import requests


def make_headers(auth_token):
    headers = {'content-type':'application/json','Authorization': 'Bearer ' + auth_token}
    return headers

def get_auth_token():
    while True:
        auth_token = getpass.getpass("\nPlease enter your DigitalOcean authorization token:\n")
        
        token_verification = requests.get("https://api.digitalocean.com/v2/account", headers=make_headers(auth_token)).text
        if token_verification == '{"id":"unauthorized","message":"Unable to authenticate you."}':
            print "Unable to authenticate. Please try again.\n"
            continue
        else:
            print "Authentication successful.\n"
            break
            
    return auth_token


def get_domain():
    
    # Considering moving this function out of get_domain()
    def valid_domain(domain):
        # Valid TLDs. More to be added.
        valid_tlds = ['com', 'org', 'info', 'co']
        
        if len(domain) > 48:
            return False
        
        domains = domain.split('.')
        if domains[-1] not in valid_tlds:
            return False
        
        for d in domains[:-1]:
            if d[0] == '-':
                return False
            for i in d:
                if not i.isalpha() and i is not '-':
                    return False
        
        return True
            
        
    while True:
        domain = raw_input("\nPlease enter the domain name you would like to use:\n")
        if valid_domain(domain):
            print "Invalid domain name. Please try again.\n"
            continue
        # Tests whether domain has been added to DigitalOcean; otherwise fails
        # To be implemented later
        elif False: #Not on DigitalOcean
            print "Domain not on DigitalOcean."
            print "Please add the domain to DigitalOcean and run this script again."
            exit()
        else:
            print "\nSuccess\n"
            break
        
    return domain


def get_region():
    regions_dict = {"ams1":"Amsterdam 1", "ams2":"Amsterdam 2", "ams3":"Amsterdam 3", "blr1":"Bangalore 1", "fra1": "Frankfurt 1", "lon1":"London 1", "nyc1":"New York City 1", "nyc2":"New York City 2", "nyc3":"New York City 3", "sfo1":"San Francisco 1", "sfo2":"San Francisco 2", "sgp1":"Singapore 1", "tor1":"Toronto 1"}
    
    # All regions
    #available_regions = ["ams1", "ams2", "ams3", "blr1", "fra1", "lon1", "nyc1", "nyc2", "nyc3", "sfo1", "sfo2", "sgp1", "tor1"]
    
    # Block storage regions
    available_regions = ["fra1", "nyc1", "sfo2", "sgp1"]
    # For now, only regions with block storage will be made avilable
    
    print "[Region code] : [Region]\n"
    for r in available_regions:
        print r + "  :  " + regions_dict[r]
    
    while True:
        region = raw_input("\nPlease enter the appropriate region code:\n")
        if region in available_regions:
            print "\nSuccess\n"
            break
        else:
            print "Invalid region. Please try again.\n"
            continue
    
    return region


def get_size():
    sizes_dict = {"512mb":"0.5 GB RAM / 1 CPU / 20 GB SSD / 1 TB Transfer", "1gb":"1 GB RAM / 1 CPU / 30 GB SSD / 2 TB Transfer", "2gb":"2 GB RAM / 2 CPU / 40 GB SSD / 3 TB Transfer", "4gb":"4 GB RAM / 2 CPU / 60 GB SSD / 4 TB Transfer", "8gb":"8 GB RAM / 4 CPU / 80 GB SSD / 5 TB Transfer", "16gb":"16 GB RAM / 8 CPU / 160 GB SSD / 6 TB Transfer", "m-16gb":"16 GB RAM / 2 CPU / 30 GB SSD / 6 TB Transfer", "32gb":"32 GB RAM / 12 CPU / 320 GB SSD / 7 TB Transfer", "m-32gb":"32 GB RAM / 4 CPU / 90 GB SSD / 7 TB Transfer", "48gb":"48 GB RAM / 16 CPU / 480 GB SSD / 8 TB Transfer", "64gb":"64 GB RAM / 20 CPU / 640 GB SSD / 9 TB Transfer", "m-64gb":"64 GB RAM / 8 CPU / 200 GB SSD / 8 TB Transfer", "m-128gb":"128 GB RAM / 16 CPU / 340 GB SSD / 9 TB Transfer", "m-224gb":"224 GB RAM / 32 CPU / 500 GB SSD / 10 TB Transfer"}
    
    # All sizes
    #available_sizes = ["512mb", "1gb", "2gb", "4gb", "8gb", "16gb", "m-16gb", "32gb", "m-32gb", "48gb", "m-64gb", "64gb", "m-128gb", "m-224gb"]
    
    # For now, only certain sizes will be available
    # Seriously, you don't need 224GB of RAM for munki
    available_sizes = ["512mb", "1gb"]
    
    def divider(item, item_list):
        div = "  :  "
        space = " " * (len(max(item_list, key=len)) - len(item))
        div = space + div
        return div
    
    print "[Size] : [Specs]\n"
    for s in available_sizes:
        print s + divider(s, available_sizes) + sizes_dict[s]
    
    while True:
        size = raw_input("\nPlease enter the correct size:\n")
        if size in available_sizes:
            print "\nSuccess\n"
            break
        else:
            print "Invalid size. Please try again.\n"
            continue
    
    return size


def main():
    
    # Get input from users
    user_input = {}
    user_input['auth_token'] = get_auth_token()
    user_input['domain'] = get_domain()
    user_input['region'] = get_region()
    user_input['size'] = get_size()
    
    # Create bootstrap_variables
    bootstrap_variables = []
    bootstrap_variables.append('DO_TOKEN=' + user_input['auth_token'])
    bootstrap_variables.append('DO_DOMAIN=' + user_input['domain'])
    bootstrap_variables.append('DO_REGION=' + user_input['region'])
    
    # Get command server cloud-config file
    # FIX URL
    # https://raw.githubusercontent.com/jacobfgrant/lotus/master/server_cloud-config.yml
    cloud_config_file = requests.get("https://raw.githubusercontent.com/jacobfgrant/lotus/version-0.1/server_cloud-config.yml").text
    
    # Add bootstrap_variables to command server cloud-config file
    bootstrap_variables_string = ''
    for bv in bootstrap_variables:
        bootstrap_variables_string = bootstrap_variables_string + bv + '\n      '
    digitalocean_user_data = cloud_config_file.replace('insert_bootstrap_variables', bootstrap_variables_string)
    
    #api_url = "https://api.digitalocean.com/v2/droplets"
    #api_headers = make_headers(auth_token)
    #api_data = digitalocean_user_data
    
    # Create API data basics
    api_data = json.loads('{"name":null,"region":null,"size":null,"image":"ubuntu-16-04-x64","ssh_keys":null,"backups":true,"ipv6":true,"user_data":null,"private_networking":true,"volumes": null,"tags":["lotus", "command"]}')
    
    # Add user input to API data
    api_data['name'] = user_input['domain']
    api_data['region'] = user_input['region']
    api_data['size'] = user_input['size']
    api_data['user_data'] = digitalocean_user_data
    
    initialize_lotus_request = requests.post(url="https://api.digitalocean.com/v2/droplets", headers=make_headers(user_input['auth_token']), data=json.dumps(api_data)).text
    
    print initialize_lotus_request


if __name__ == "__main__":
    main()
