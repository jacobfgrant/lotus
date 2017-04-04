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

echo "Running bootstrap script..."
echo

# Use source and a config file
#source /root/bootstrap.cfg
echo "Reading in bootstrap variables"
source /root/bootstrap_variables
echo

# Install add Ansible repository and install
echo "Adding Ansible to repositories"
apt-add-repository -y ppa:ansible/ansible &> /dev/null && echo "Success" || exit 1
apt-get -qq update
echo

echo "Installing Ansible"
apt-get install -y ansible &> /dev/null && echo "Success" || exit 1
echo

echo "Creating temporary host file"
IPADDR=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')

echo "[command]" >> /etc/ansible/hosts
echo "$IPADDR" >> /etc/ansible/hosts
echo


echo "Downloading Lotus"
wget https://github.com/jacobfgrant/lotus/archive/$LOTUS_VERSION.zip
unzip ./*.zip
mv lotus-* /root/lotus
rm ./*.zip
#chmod 0744 /root/lotus/ansible/*yml
echo


# Create ssh keys for use with Ansible
# REPLACE WITH ANSIBLE IN FUTURE RELEASES
echo "Creating ssh keys"

if [ ! -d /root/.ssh/ ]; then
  mkdir /root/.ssh/
fi
chmod 644 /root/.ssh/
ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
echo


echo "Add ssh key to DigitalOcean"
echo

PUB_KEY=$(cat /root/.ssh/id_rsa.pub)
DO_KEY_NAME='"name":"Lotus Command Server Public Key"'
DO_KEY_PUB='"public_key":"'$PUB_KEY'"'

DO_KEY_ID=$(curl -X POST -H \
"Content-Type: application/json" -H \
"Authorization: Bearer $DO_TOKEN" -d \
"{
    $DO_KEY_NAME,
    $DO_KEY_PUB
}" \
"https://api.digitalocean.com/v2/account/keys" \
| tee -a /var/log/lotus/api_calls.log \
| grep -Po '"id":\K([0-9]*)')

echo -e "\n" | tee -a /var/log/lotus/api_calls.log
echo

sleep 5

# Create munkireport server (droplet)
echo "Building MunkiReport server API call..."
echo

# Create each variable for DigitalOcean API call
DO_API_NAME='"name":"munkireport.'$DO_DOMAIN'"' && echo $DO_API_NAME
DO_API_REGION='"region":"'$DO_REGION'"' && echo $DO_API_REGION
DO_API_SIZE='"size":"'$DO_SIZE'"' && echo $DO_API_SIZE
DO_API_IMAGE='"image":"ubuntu-16-04-x64"' && echo $DO_API_IMAGE
DO_API_SSHKEYS='"ssh_keys":["'$DO_KEY_ID'"]' && echo $DO_API_SSHKEYS
DO_API_BACKUPS='"backups":true' && echo $DO_API_BACKUPS
DO_API_IPV6='"ipv6":true' && echo $DO_API_IPV6
DO_API_PRIVATENETWORKING='"private_networking":true' && echo $DO_API_PRIVATENETWORKING
DO_API_USERDATA='"user_data":"'$(cat /root/lotus/cloud-init/standard.cloud-config.yml)'"' && echo $DO_API_USERDATA
DO_API_MONITORING='"monitoring":true' && echo $DO_API_MONITORING
DO_API_VOLUMES='"volumes":null' && echo $DO_API_VOLUMES
DO_API_TAGS='"tags":["lotus","reporting","munkireport"]' && echo $DO_API_TAGS
echo
echo

# Run API call with set variables
# Adds output to api_calls.log
echo "Creating MunkiReport server..."
echo

curl -X POST -H \
"Content-Type: application/json" -H \
"Authorization: Bearer $DO_TOKEN" -d \
"{
    $DO_API_NAME,
    $DO_API_REGION,
    $DO_API_SIZE,
    $DO_API_IMAGE,
    $DO_API_SSHKEYS,
    $DO_API_BACKUPS,
    $DO_API_IPV6,
    $DO_API_PRIVATENETWORKING,
    $DO_API_USERDATA,
    $DO_API_MONITORING,
    $DO_API_VOLUMES,
    $DO_API_TAGS
}" \
"https://api.digitalocean.com/v2/droplets" \
| tee -a /var/log/lotus/api_calls.log

echo -e "\n" | tee -a /var/log/lotus/api_calls.log
echo


# Create primary munki server (droplet)
echo "Building Munki server API call..."
echo

# Create each variable for DigitalOcean API call
DO_API_NAME='"name":"00-munki.'$DO_DOMAIN'"' && echo $DO_API_NAME
DO_API_REGION='"region":"'$DO_REGION'"' && echo $DO_API_REGION
DO_API_SIZE='"size":"'$DO_SIZE'"' && echo $DO_API_SIZE
DO_API_IMAGE='"image":"ubuntu-16-04-x64"' && echo $DO_API_IMAGE
DO_API_SSHKEYS='"ssh_keys":["'$DO_KEY_ID'"]' && echo $DO_API_SSHKEYS
DO_API_BACKUPS='"backups":true' && echo $DO_API_BACKUPS
DO_API_IPV6='"ipv6":true' && echo $DO_API_IPV6
DO_API_PRIVATENETWORKING='"private_networking":true' && echo $DO_API_PRIVATENETWORKING
DO_API_USERDATA='"user_data":"'$(cat /root/lotus/cloud-init/standard.cloud-config.yml)'"' && echo $DO_API_USERDATA
DO_API_MONITORING='"monitoring":true' && echo $DO_API_MONITORING
DO_API_VOLUMES='"volumes":null' && echo $DO_API_VOLUMES
DO_API_TAGS='"tags":["lotus","munki"]' && echo $DO_API_TAGS
echo
echo

# Run API call with set variables
# Adds output to api_calls.log
echo "Creating Munki server..."
echo

curl -X POST -H \
"Content-Type: application/json" -H \
"Authorization: Bearer $DO_TOKEN" -d \
"{
    $DO_API_NAME,
    $DO_API_REGION,
    $DO_API_SIZE,
    $DO_API_IMAGE,
    $DO_API_SSHKEYS,
    $DO_API_BACKUPS,
    $DO_API_IPV6,
    $DO_API_PRIVATENETWORKING,
    $DO_API_USERDATA,
    $DO_API_MONITORING,
    $DO_API_VOLUMES,
    $DO_API_TAGS
}" \
"https://api.digitalocean.com/v2/droplets" \
| tee -a /var/log/lotus/api_calls.log

echo -e "\n" | tee -a /var/log/lotus/api_calls.log
echo


echo "Modifying cron.d jobs"

echo 'PATH=/usr/bin:/bin:/usr/sbin:/sbin' > /etc/cron.d/cron_bootstrap
echo '@reboot root ansible-playbook /root/lotus/ansible/command.yml --connection=local >> /var/log/lotus/command.log 2>&1' >> /etc/cron.d/cron_bootstrap
chmod 744 /root/lotus/ansible/*.yml
echo


# In future releases, this will be fleshed out
echo "Creating credentials"
echo '[digitalocean]' > /root/.lotus_credentials
echo "auth_token = $DO_TOKEN" >> /root/.lotus_credentials
chmod 400 /root/.lotus_credentials
echo


echo "Deleting bootstrap_variables..."
rm -f /root/bootstrap_variables
echo

echo "Rebooting..."
sleep 10 && reboot
