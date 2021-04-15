import sys
from flask import Flask

import os
import query_path
import run_traffic_simulation

import boto3
import json


def handler(event, context):

    try: 
        home_dir = os.getcwd()
        
        write_path = '/tmp'
        
        vphh = float(event["vphh"])
        visitor_cnts = int(event["visitor_cnts"])

        player_origin = int(event["player_origin"])
        player_destin = int(event["player_destin"])
        start_time = int(event["start_time"])
        end_time = int(event["end_time"])


        run_traffic_simulation.run_traffic_simulation(vphh=vphh, visitor_cnts=visitor_cnts, write_path=write_path)
        
        player_nodes = query_path.query_path(vphh=vphh, visitor_cnts=visitor_cnts, 
                                             player_origin=player_origin, player_destin=player_destin, 
                                             start_time=start_time, end_time=end_time,
                                             read_path=write_path)

        bucket_name = "bolinas"
        file_name = 'player_nodes_{}_{}_{}_{}_{}_{}.json'.format(vphh, visitor_cnts, player_origin, player_destin, start_time, end_time)
        lambda_path = write_path + '/' + file_name
        
        with open(write_path +'/' + file_name, 'w') as outfile:
            json.dump({'nodes': player_nodes}, outfile, indent=2)

        s3_path = "player_nodes/" + file_name
        s3 = boto3.resource("s3")
        
        s3.meta.client.upload_file(lambda_path, bucket_name, s3_path)
        
        result = {
            'nodes' : player_nodes
        }
        response = {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        return response
    except Exception as e:
        print(e)
        raise e



