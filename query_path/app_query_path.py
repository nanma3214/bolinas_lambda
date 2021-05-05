import sys

import os
import query_path


import boto3
import json
from pathlib import Path

def handler(event, context):

    try: 
        write_path = '/tmp'
        
        
        player_origin = int(event["player_origin"])
        player_destin = int(event["player_destin"])
        token = event["token"]

        # Download files from S3
        bucket_name = "bolinas"
        s3_prefix = "player_nodes/" + token + "/"
        client = boto3.client('s3')
        object_lists = client.list_objects(Bucket = bucket_name, Prefix=s3_prefix)

        if 'Contents' not in object_lists:
            raise Exception("Error: no such token.")

        path_list = {} # key = S3path, value = local /tmp path
        for file_info in object_lists['Contents']:
            this_s3_path = file_info['Key']
            this_local_path = this_s3_path.replace(s3_prefix, '/tmp/')
            path_list[this_s3_path] = this_local_path
            Path(this_local_path).parent.mkdir(parents=True, exist_ok=True)
            client.download_file(Bucket = bucket_name, Key = this_s3_path, Filename = this_local_path)

        # Parse out parameters
        para_file = json.load(open(write_path + '/paras.json'))
        token = para_file['token']
        vphh = float(para_file['vphh'])
        visitor_cnts = int(para_file['visitor_cnts'])

        # Iteratively querying path in a 5 min interval
        start_time = 100
        increment = 5*60
        start_node = player_origin
        nodes_dict = {}
        while start_node != player_destin:
            nodes = query_path.query_path(vphh=vphh, visitor_cnts=visitor_cnts, 
                                             player_origin=start_node, player_destin=player_destin, 
                                             start_time=start_time, end_time=start_time+increment,
                                             read_path=write_path)
            nodes_dict[start_time] = nodes
            start_node = nodes[-1]
            start_time += 300

        result = {
            'token': token,
            'nodes_dict' : nodes_dict
        }
        # response = {
        #     'statusCode': 200,
        #     'body': json.dumps(result)
        # }
        return result


    except Exception as e:
        print(e)
        raise e



