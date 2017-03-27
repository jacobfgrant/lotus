#!/bin/bash
#
# Bootstraps the Lotus Command Server.
#
# Takes in variables from bootstrap_variables
# Run as root
#
# Built for DigitalOcean
#
# Written by: Jacob F. Grant
# Written: 03/26/2017
# Updated:
#

# Read in and evaluate bootstrap_variables
echo "Reading in bootstrap_variables..." && echo
# Set to bootstrap_variables location
BOOTSTRAP_FILE="/root/bootstrap_variables"
while IFS= read -r BOOTSTRAP_LINE
do
    eval $BOOTSTRAP_LINE
done <"$BOOTSTRAP_FILE"
echo


# Install add Ansible repository and install
apt-get install -yqq software-properties-common
echo "Adding Ansible to repositories"
apt-add-repository -y ppa:ansible/ansible &> /dev/null && echo "Success" || exit 1
apt-get -qq update
echo "Installing Ansible"
apt-get install -y ansible &> /dev/null && echo "Success" || exit 1


# Clone Lotus repo from GitHub
echo "Cloning Lotus repo from GitHub"
git clone https://github.com/jacobfgrant/lotus.git --recursive


# Create munkireport server (droplet)
echo "Building MunkiReport server API call..." && echo

# Create each variable for DigitalOcean API call
DO_API_NAME='"name":"munkireport.'$DO_DOMAIN'"' && echo $DO_API_NAME
DO_API_REGION='"region":"'$DO_REGION'"' && echo $DO_API_REGION
DO_API_SIZE='"size":"512mb"' && echo $DO_API_SIZE
DO_API_IMAGE='"image":"ubuntu-16-04-x64"' && echo $DO_API_IMAGE
DO_API_SSHKEYS='"ssh_keys":null' && echo $DO_API_SSHKEYS
DO_API_BACKUPS='"backups":true' && echo $DO_API_BACKUPS
DO_API_IPV6='"ipv6":true' && echo $DO_API_IPV6
DO_API_PRIVATENETWORKING='"private_networking":true' && echo $DO_API_PRIVATENETWORKING
DO_API_USERDATA='"user_data":"/root/lotus/client_cloud-config.yml"' && echo $DO_API_USERDATA
DO_API_MONITORING='"monitoring":true' && echo $DO_API_MONITORING
DO_API_VOLUMES='"volumes":null' && echo $DO_API_VOLUMES
DO_API_TAGS='"tags":["lotus","reporting","munkireport"]' && echo $DO_API_TAGS

# Run API call with set variables
# Adds output to api_calls.log
echo
echo "Creating MunkiReport server..." && echo
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $DO_TOKEN" -d "{$DO_API_NAME,$DO_API_REGION,$DO_API_SIZE,$DO_API_IMAGE,$DO_API_SSHKEYS,$DO_API_BACKUPS,$DO_API_IPV6,$DO_API_PRIVATENETWORKING,$DO_API_USERDATA,$DO_API_MONITORING,$DO_API_VOLUMES,$DO_API_TAGS}" "https://api.digitalocean.com/v2/droplets" | tee -a /root/api_calls.log
echo


# Create primary munki server (droplet)
echo "Building Munki server API call..." && echo

# Create each variable for DigitalOcean API call
DO_API_NAME='"name":"00-munki.'$DO_DOMAIN'"' && echo $DO_API_NAME
DO_API_REGION='"region":"'$DO_REGION'"' && echo $DO_API_REGION
DO_API_SIZE='"size":"512mb"' && echo $DO_API_SIZE
DO_API_IMAGE='"image":"ubuntu-16-04-x64"' && echo $DO_API_IMAGE
DO_API_SSHKEYS='"ssh_keys":null' && echo $DO_API_SSHKEYS
DO_API_BACKUPS='"backups":true' && echo $DO_API_BACKUPS
DO_API_IPV6='"ipv6":true' && echo $DO_API_IPV6
DO_API_PRIVATENETWORKING='"private_networking":true' && echo $DO_API_PRIVATENETWORKING
DO_API_USERDATA='"user_data":"/root/lotus/client_cloud-config.yml"' && echo $DO_API_USERDATA
DO_API_MONITORING='"monitoring":true' && echo $DO_API_MONITORING
DO_API_VOLUMES='"volumes":null' && echo $DO_API_VOLUMES
DO_API_TAGS='"tags":["lotus","munki"]' && echo $DO_API_TAGS

# Run API call with set variables
# Adds output to api_calls.log
echo
echo "Creating Munki server..." && echo

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $DO_TOKEN" -d "{$DO_API_NAME,$DO_API_REGION,$DO_API_SIZE,$DO_API_IMAGE,$DO_API_SSHKEYS,$DO_API_BACKUPS,$DO_API_IPV6,$DO_API_PRIVATENETWORKING,$DO_API_USERDATA,$DO_API_MONITORING,$DO_API_VOLUMES,$DO_API_TAGS}" "https://api.digitalocean.com/v2/droplets" | tee -a /root/api_calls.log
echo
