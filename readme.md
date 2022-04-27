In order to make Cylance an effective tool when new and emerging threats are occurring across all tenants within our Multi tenant environment, the need for a scripting function to globally quarantine a hash value associated with a malicious file was identified. 

This script achieves that goal. 

There are some underlying dependencies related to the script →

1. Knowing the SHA256 Hash Value of the file you need to quarantine.
2. Python installed on your machine
3. pip also installed on your machine
4. CyAPI library
5. Cylance multi tenant api key 
6. Creation of a creds.json file in whatever folder the cylance script is being run from


Identifying the Hash Value of the file you need to quarantine →

Open powershell and run the following command to find the SHA256 Hash value of malicious file. 
 Get-Filehash -path c:\your\files\path_and_extension\goes_here -alogrithm SHA256 | fl 

You can also use VirusTotal or other sites to drag and drop the file and retrieve the hash


Installing Python on your machine →

The easiest way to install python on your machine is to follow the directions here: https://www.python.org/


Installing pip on your machine → 

Installing pip is a pretty straightforward process, in depth directions can be found here: https://phoenixnap.com/kb/install-pip-windows


Installing CyAPI → 

Once pip is installed, run the following command: pip install cyapi

Creating Multi Tenant API Key -> 

    1. In the Cylance Multi Tenant, click Settings 
    2. Select Application 
    3. Add a new application with the following permissions (r/w/x)
    4. Save the Credentials Generated


Create a creds.json file →

***THIS FILE MUST BE CREATED IN THE SAME FOLDER THAT THE SCRIPT IS RUN FROM***

Below is a sample of a creds.json file that this script calls for. This format must be strictly adhered to in order
for this script to work

{
    "tid": "",
    "app_id": "<app id here in quotes>,
    "app_secret": "<app secret here in quotes>",
    "region": "US",
    "mtc": "True"
}
