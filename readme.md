# Cloudflare DNS Updater
### What len use it have?
* Update your DNS record on Cloudflare just like [No-ip DUC(Dynamic Update Client)](https://www.noip.com/download?page=win) does.
* Some ISP may provide dynamic IPs, which varies when modem is switched. Running the scirpt after a certain time interval may help you ensure the ip in your DNS record is up-to-dated.
* The scripts uses the public ip of the computer running to update the ip address.
### Usage
1. Configure your data in config.py
    * ZONE_ID: You can find your zone id on Overview tab in Cloudflare.
    * X_AUTH_KEY: You can find the authkey in My Settings -> API Key -> Global API Key
    * X_AUTH_EMAIL: Your Cloudflare login email
    * wanted_type: Condition of filtering, leaving wanted DNS record type only.
    * wanted_name: Same as above, but "name" column this time.
2. Launch main.py, the script will process shits for you.
3. Setup loops to mainting the update yourself zzzzzzzzz.
