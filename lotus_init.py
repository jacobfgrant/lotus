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
import re
try:
    import requests
except:
    pip.main(['install', '--upgrade', 'requests'])


def make_headers(auth_token):
    headers = {'content-type':'application/json','Authorization': 'Bearer ' + auth_token}
    return headers


def get_auth_token():
    while True:
        auth_token = getpass.getpass("\nPlease enter your DigitalOcean authorization token:\n")
        
        token_verification = requests.get(url="https://api.digitalocean.com/v2/account", headers=make_headers(auth_token)).text
        
        if token_verification == '{"id":"unauthorized","message":"Unable to authenticate you."}':
            print "\nError: Unable to authenticate. Please try again.\n"
            continue
        else:
            print "Authentication successful.\n"
            break
    
    return auth_token


def get_domain():
    
    # Considering moving this function out of get_domain()
    def valid_domain(domain):
        
        # Valid TLDs. More to be added.
        valid_tlds = [
            'com',
            'org',
            'info',
            'co',
            ]
        
        if len(domain) > 48:
            print "\nError: Domain name too long. Please choose something shorter.\n"
            return False
        
        domains = domain.split('.')
        if domains[-1] not in valid_tlds:
            print "\nError: Not a valid TLD. Please choose another.\n"
            return False
        
        for d in domains[:-1]:
            if d[0] == '-':
                print "\nError: Invalid domain name\nCannot begin with a dash.\nPlease try again.\n"
                return False
            for i in d:
                if not i.isalpha() and i is not '-':
                    print "\n Error: Invalid domain name.\nAlphanumeric characters and dashes only.\nPlease try again.\n"
                    return False
        
        return True
    
        
    while True:
        domain = raw_input("\nPlease enter the domain name you would like to use:\n")
        if valid_domain(domain):
            print "\nSuccess\n"
            break
        else:
            continue
    
    # Tests whether domain has been added to DigitalOcean; otherwise fails
    # To be implemented later
    if False: #Not on DigitalOcean
        print "\nError: Domain not on DigitalOcean."
        print "Please add the domain to DigitalOcean and run this script again."
        exit()
    
    return domain


def get_region():
    regions_dict = {
        "ams1":"Amsterdam 1",
        "ams2":"Amsterdam 2",
        "ams3":"Amsterdam 3",
        "blr1":"Bangalore 1",
        "fra1": "Frankfurt 1",
        "lon1":"London 1",
        "nyc1":"New York City 1",
        "nyc2":"New York City 2",
        "nyc3":"New York City 3",
        "sfo1":"San Francisco 1",
        "sfo2":"San Francisco 2",
        "sgp1":"Singapore 1",
        "tor1":"Toronto 1",
        }
    
    # All regions
    '''
    available_regions = [
        "ams1",
        "ams2",
        "ams3",
        "blr1",
        "fra1",
        "lon1",
        "nyc1",
        "nyc2",
        "nyc3",
        "sfo1",
        "sfo2",
        "sgp1",
        "tor1",
        ]
    '''
    
    # Block storage regions
    available_regions = [
        "fra1",
        "nyc1",
        "sfo2",
        "sgp1",
        ]
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
            print "\nError: Invalid region. Please try again.\n"
            continue
    
    return region


def get_size():
    sizes_dict = {
        "512mb":"0.5 GB RAM / 1 CPU / 20 GB SSD / 1 TB Transfer",
        "1gb":"1 GB RAM / 1 CPU / 30 GB SSD / 2 TB Transfer",
        "2gb":"2 GB RAM / 2 CPU / 40 GB SSD / 3 TB Transfer",
        "4gb":"4 GB RAM / 2 CPU / 60 GB SSD / 4 TB Transfer",
        "8gb":"8 GB RAM / 4 CPU / 80 GB SSD / 5 TB Transfer",
        "16gb":"16 GB RAM / 8 CPU / 160 GB SSD / 6 TB Transfer",
        "m-16gb":"16 GB RAM / 2 CPU / 30 GB SSD / 6 TB Transfer",
        "32gb":"32 GB RAM / 12 CPU / 320 GB SSD / 7 TB Transfer",
        "m-32gb":"32 GB RAM / 4 CPU / 90 GB SSD / 7 TB Transfer",
        "48gb":"48 GB RAM / 16 CPU / 480 GB SSD / 8 TB Transfer",
        "64gb":"64 GB RAM / 20 CPU / 640 GB SSD / 9 TB Transfer",
        "m-64gb":"64 GB RAM / 8 CPU / 200 GB SSD / 8 TB Transfer",
        "m-128gb":"128 GB RAM / 16 CPU / 340 GB SSD / 9 TB Transfer",
        "m-224gb":"224 GB RAM / 32 CPU / 500 GB SSD / 10 TB Transfer",
        }
    
    # All sizes
    '''
    available_sizes = [
        "512mb",
        "1gb",
        "2gb",
        "4gb",
        "8gb",
        "16gb",
        "m-16gb",
        "32gb",
        "m-32gb",
        "48gb",
        "m-64gb",
        "64gb",
        "m-128gb",
        "m-224gb",
        ]
    '''
    
    # For now, only certain sizes will be available
    # Seriously, you don't need 224GB of RAM for munki
    available_sizes = [
        "512mb",
        "1gb",
        ]
    
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
            print "\nError: Invalid size. Please try again.\n"
            continue
    
    return size


#def get_key(auth_token):
def get_key(auth_token):
    
    def get_exisiting_key(auth_token):
        print "\nPlease copy and paste your key's fingerprint."
        print "(This can be found at: https://cloud.digitalocean.com/settings/security)"
        key_fingerprint = raw_input("\nKey Fingerprint:\n\n")
        
        all_keys = requests.get(
            url="https://api.digitalocean.com/v2/account/keys",
            headers=make_headers(auth_token)
            ).text
        
        if key_fingerprint in all_keys:
            print "\nSuccess!\n"
            return key_fingerprint
        else:
            print  "\nError: Key does not exist. Please try again.\n"
            return None
    
    
    def get_new_key(auth_token):
        pub_key = raw_input("\nPlease copy and paste your ssh PUBLIC key\n(NOT your private key!) here:\n\n")
        
        key_name = raw_input("\n\nWhat would you like to call this key?\n")
        
        add_key = requests.post(
            url="https://api.digitalocean.com/v2/account/keys",
            headers=make_headers(auth_token),
            data='{"name":"' + key_name + '","public_key":"' + pub_key + '"}'
            ).text
        
        if 'Key invalid' in add_key:
            print "\nError: Invalid key type. Please try again.\n"
            return None
        
        if 'SSH Key is already in use on your account' in add_key:
            print "\nError: Key already exists."
            print "Please either add this key's fingerprint or add a different key.\n"
            return None
        
        key_fingerprint_re = re.search('"fingerprint":"([0-9a-f:]*)"', add_key)
        key_fingerprint = key_fingerprint_re.groups(1)[0]
        
        if key_fingerprint_re is None:
            print  "\nError: Please try again.\n"
            return None
        
        else:
            print  "\nSuccess!\n"
            return key_fingerprint
    
    
    key_fingerprint_list = []
    while True:
        print "\nWould you like to:\n"
        print "1  :  Use an existing DigitalOcean key"
        print "2  :  Add a new public key to DigitalOcean"
        if len(key_fingerprint_list) > 0:
            print "3  :  Finish adding keys"
        print
        key_choice = raw_input()
        
        
        if key_choice == '1':
            key_fingerprint = get_exisiting_key(auth_token)
            if key_fingerprint is None:
                continue
            else:
                key_fingerprint_list.append(key_fingerprint)
                continue
        
        if key_choice == '2':
            key_fingerprint = get_new_key(auth_token)
            if key_fingerprint is None:
                continue
            else:
                key_fingerprint_list.append(key_fingerprint)
                continue
        
        if key_choice == '3' and len(key_fingerprint_list) > 0:
            break
        
        else:
            print "\nError: Not a valid option.\n\n"
            continue
    
    return key_fingerprint_list


def main():
    
    # Get input from users
    user_input = {}
    user_input['auth_token'] = get_auth_token()
    user_input['domain'] = get_domain()
    user_input['region'] = get_region()
    user_input['size'] = get_size()
    user_input['key_fingerprint_list'] = get_key(user_input['auth_token'])
    
    # Create bootstrap_variables
    bootstrap_variables = []
    bootstrap_variables.append('DO_TOKEN=' + user_input['auth_token'])
    bootstrap_variables.append('DO_DOMAIN=' + user_input['domain'])
    bootstrap_variables.append('DO_REGION=' + user_input['region'])
    bootstrap_variables.append('DO_SIZE=' + user_input['size'])
    bootstrap_variables.append('LOTUS_VERSION=' + lotus_version)
    
    # Get command server cloud-config file
    #digitalocean_user_data = requests.get("https://raw.githubusercontent.com/jacobfgrant/lotus/" + lotus_version + "/server.cloud-config").text
    
    digitalocean_user_data = requests.get("https://github.com/jacobfgrant/lotus/releases/download/v" + lotus_version + "/command-server.cloud-config.yml").text
    
    # Add bootstrap variables to command server cloud-config file
    bootstrap_variables_string = ''
    for bv in bootstrap_variables:
        bootstrap_variables_string = bootstrap_variables_string + bv + '\n      '
    
    digitalocean_user_data = digitalocean_user_data.replace('insert_bootstrap_variables', bootstrap_variables_string)
    digitalocean_user_data = digitalocean_user_data.replace('lotus_release_version', lotus_version)
    
    #api_url = "https://api.digitalocean.com/v2/droplets"
    #api_headers = make_headers(auth_token)
    #api_data = digitalocean_user_data
    
    # Create API data frameworks
    api_data = json.loads(
        """{
            "name":null,
            "region":null,
            "size":null,
            "image":"ubuntu-16-04-x64"
            ,"ssh_keys":null,
            "backups":true,
            "ipv6":true,
            "user_data":null,
            "private_networking":true,
            "volumes":null,
            "tags":["lotus", "command"]
        }"""
        )
    
    # Add user input and data to API data
    api_data['name'] = user_input['domain']
    api_data['region'] = user_input['region']
    api_data['size'] = user_input['size']
    api_data['ssh_keys'] = user_input['key_fingerprint_list']
    api_data['user_data'] = digitalocean_user_data
    
    initialize_lotus_request = requests.post(
        url="https://api.digitalocean.com/v2/droplets",
        headers=make_headers(user_input['auth_token']),
        data=json.dumps(api_data)
        ).text
    
    print "\nRequest:\n"
    print json.dumps(api_data)
    
    print "\n\nReply:\n"
    print initialize_lotus_request
    print


if __name__ == "__main__":
    lotus_version = '0.1.0'
    main()
