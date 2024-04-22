#Load up the variables used here
# remove the period in front of "./etc/wireguard/publickey" to 
# make it work on the server
source ./etc/wireguard/wg0vars.sh

# Check if the number of arguments is less than 2
if [ $# -lt 2 ]; then
    echo "Usage: $0 <devicename> <last octet of IP>"
    # Read the file line by line
    tail -1 ${wgSrvNum}_ip_list.txt  | awk '{print "Last Assigned IP: "  $3}'
    # Exit the script
    exit 1
fi

# Check if the keys subfolder exists
if [ ! -d "${wgSrvNum}_keys_dir" ]; then
    # If it doesn't exist, create it
    mkdir "${wgSrvNum}_keys_dir"
fi

printf -v filename "%s_%03d_%s_%05d" $wgSrvNum $2 $1 $RANDOM 
mkdir ${wgSrvNum}_keys_dir/$filename
chmod 700 ${wgSrvNum}_keys_dir/$filename
filename=${wgSrvNum}_keys_dir/$filename/$filename

wg genkey > ${filename}.key
wg pubkey < ${filename}.key > ${filename}.pub
wg genpsk > ${filename}.psk

pwpwpw=$(./genSentence.py -l 50 -s -)


echo writing ${filename}.conf
echo "[Interface]" > ${filename}.conf
echo "PrivateKey = $(cat ./${filename}.key) " >> ${filename}.conf
echo "ListenPort = ${serverListenPort}" >> ${filename}.conf
echo "Address = ${subnetFOUR}.${2}/24,${subnetSIX}:${2}/128" >> ${filename}.conf
echo "DNS = 1.1.1.1" >> ${filename}.conf
echo " " >> ${filename}.conf
echo "[Peer]" >> ${filename}.conf
echo "PublicKey = ${serverPubKey} " >> ${filename}.conf
echo "PresharedKey = $(cat ${filename}.psk)" >> ${filename}.conf
echo "AllowedIPs = ::/0, 0.0.0.0/0 " >> ${filename}.conf
echo "Endpoint = ${endPoint} " >> ${filename}.conf

zip --password $pwpwpw ${filename}.zip ${filename}.conf
cat ${filename}.zip | base64 > ${filename}.zip.b64

echo $pwpwpw > ${filename}_zip_pw.txt

echo writing ${filename}_${wgSrvNum}.conf
echo "[Peer]" > ${filename}_${wgSrvNum}.conf
echo "PublicKey = $(cat ${filename}.pub)" >> ${filename}_${wgSrvNum}.conf
echo "PresharedKey = $(cat ${filename}.psk)" >> ${filename}_${wgSrvNum}.conf
echo "AllowedIPs = ${subnetFOUR}.${2}/32" >> ${filename}_${wgSrvNum}.conf
echo " " >> ${filename}_${wgSrvNum}.conf

chmod 600 ${filename}*

echo $(grep AllowedIPs ${filename}_${wgSrvNum}.conf) $(grep PublicKey ${filename}_${wgSrvNum}.conf) ${filename}_${wgSrvNum}.conf  [$pwpwpw] >> ${wgSrvNum}_ip_list.txt
#clear the temp variables
subnetFOUR=
subnetSIX=
serverPubKey=
endPoint=
wgSrvNum=
pwpwpw=
serverListenPort=
shred -u ${filename}.key ${filename}.pub ${filename}.psk