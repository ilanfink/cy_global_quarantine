#Version 1.0, 03.10.22
##NOTES ->

#this is a version of a script to iterate thru a list of tenants from the cylance portal and then
#quarantine a hash value in each tenant

#this code uses some portions from cylance's documentation on configuring a connection to the cylance multi-tenant via
#JWT and built in functions from the CYApi library.

#A goal for the next iteration of this script would be to remove dependency on cyapi library and create functions based
#locally within this script

#The api user must be generated in the multi tenant and passed with the -c flag and the file must be named creds.json
#when this script is run, either in the ide or the cmd line

#Below is a sample of a creds.json file that this script calls for. This format must be strictly adhered to in order
#for this script to work
##{
#    "tid": "",
#    "app_id": "<app id here in quotes>,
#    "app_secret": "<app secret here in quotes>",
#    "region": "US",
#    "mtc": "True"
##}

#Recent updates 3/10/22->
#Added ability to update multiple hash values at once in list format

from __future__ import print_function
import json #json library for JWT token
from cyapi.cyapi import CyAPI #Cylance API Library
import argparse

##Fill the values below to quarantine this file, the reason should be updated with date and reason ->

dat_shas = ["DCF2C7C61DB9E506A01BB3A62591D5A9483B89B3BD75AF04B5FDFEED42E9968E", "A1C9B3EF8A7479BE901F42B364BE1B623634489089754D4B06F424403D040970"] #For multiple values add each in this notation ['value','value2']
dat_list = "quarantine"
dat_reason = "Testing on 3.10.22"

def parse_args():

    regions = []
    regions_help =  "Region the tenant is located: "
    for (k, v) in CyAPI.regions.items():
        regions.append(k)
        regions_help += " {} - {} ".format(k,v['fullname'])

    parser = argparse.ArgumentParser(description='Simple example to build from', add_help=True)
    parser.add_argument('-v', '--verbose', action="count", default=0, dest="debug_level",
                        help='Show process location, comments and api responses')
    parser.add_argument('-tid', '--tid_val', help='Tenant Unique Identifier')
    parser.add_argument('-aid', '--app_id', help='Application Unique Identifier')
    parser.add_argument('-ase', '--app_secret', help='Application Secret')
    parser.add_argument('-c', '--creds_file', dest='creds', help='Path to JSON File with API info provided')
    parser.add_argument('-r', '--region', dest='region', help=regions_help, choices=regions, default='NA')
    parser.add_argument('-m', '--mtc', dest='mtc', help='Indicates API connection via MTC', default=False, action='store_true')

    return parser


args = parse_args().parse_args()

if args.debug_level:
    debug_level = args.debug_level

if args.creds:
    with open(args.creds, 'rb') as f:
        creds = json.loads(f.read())

    if not creds.get('region'):
        creds['region'] = args.region

    if not creds.get('mtc'):
        creds['mtc'] = args.mtc

    API = CyAPI(**creds)

elif args.tid_val and args.app_id and args.app_secret:
    tid_val = args.tid_val
    app_id = args.app_id
    app_secret = args.app_secret
    API = CyAPI(tid_val,app_id,app_secret,args.region,args.mtc)

else:
    print("[-] Must provide valid token information")
    exit(-1)

""" Optional Health Check that the server is up and running
This is a non-authenticated health-check, but returns a
CYApi APIResponse Object
"""

conn_health = API.get_mtc_health_check()
if conn_health.is_success:
    print(conn_health.data)
    print("The MTC API Connection is ready!\n")
else:
    print("MTC API Connection failed health-check.\n\nStatus Code:{}\n{} Exiting..".format(conn_health.status_code,
                                                                                        conn_health.errors))
    exit()


API.create_conn()

tenant_list = []
tenants = API.get_tenants()

tot = 0

print("Collecting Access to {} tenants.".format(len(tenants.data['listData'])))
# Collect the MTC Tenants, for the venueTenantId to call for tenant jwt bearer token.
for t in tenants.data['listData']:
    app = API.get_tenant_app(t['venueTenantId'])
    t['jwt'] = app.data
    tenant_list.append(t)
print("Starting to Iterate through Tenants")
for t in tenant_list:
        tenant_args = {}
        tenant_args['region'] = "NA"
        tenant_args['tenant_app'] = True
        tenant_args['tenant_jwt'] = t['jwt']

        APITenant = CyAPI(**tenant_args)
        APITenant.create_conn()

        threats = APITenant.get_threats()

        for threat in threats.data:

            for dat_sha in dat_shas:
                APITenant.add_to_global_list(dat_list.lower(), dat_reason.lower(), dat_sha.lower())

