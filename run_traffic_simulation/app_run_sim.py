import sys

import os
from pathlib import Path
import boto3
import json

import run_traffic_simulation

def handler(event, context):

    try: 
        write_path = '/tmp'
        
        vphh = float(event["vphh"])
        visitor_cnts = int(event["visitor_cnts"])
        token = event["token"]

        with open(write_path +'/paras.json', 'w') as outfile:
            json.dump({'token': token,
                       'vphh': vphh, 
                       'visitor_cnts': visitor_cnts}, outfile, indent=2)

        run_traffic_simulation.run_traffic_simulation(vphh=vphh, visitor_cnts=visitor_cnts, write_path=write_path)
        

        # Grab file paths
        files_to_upload = []
        for path in Path(write_path).rglob('*.json'):
            files_to_upload.append(str(path))
        for path in Path(write_path).rglob('*.csv'):
            files_to_upload.append(str(path))
        for path in Path(write_path).rglob('*.log'):
            files_to_upload.append(str(path))

        # Upload to S3
        s3 = boto3.resource("s3")
        bucket_name = "bolinas"
        for this_file in files_to_upload:
            s3_path = "player_nodes" + this_file.replace(write_path, '/'+token)
            s3.meta.client.upload_file(this_file, bucket_name, s3_path)


        response = {
            'statusCode': 200,
            'message': token + ' files uploaded.'
        }

        return response

    except Exception as e:
        print(e)
        raise e



