## Enter the IPV4 subnet here for the WG network
subnetFOUR=10.10.192
## Enter the IPV6 subnet here for the WG network
subnetSIX=fd86:ea04:1111:
# Change this to the file with the public key of the server
# remove the period in front of "./etc/wireguard/publickey" to 
# make it work on the server
serverPubKey=$(cat ./etc/wireguard/publickey)
## Enter the internet address and port here for the WG server
endPoint=1.8.3.2:21223
serverListenPort=21223
wgSrvNum=wg9