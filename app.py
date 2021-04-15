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
        vphh = 1.5
        visitor_cnts = 300

        player_origin, player_destin, start_time, end_time = (143, 193, 100, 900)

        run_traffic_simulation.run_traffic_simulation(vphh=vphh, visitor_cnts=visitor_cnts, write_path=write_path)
        
        player_nodes = query_path.query_path(vphh=vphh, visitor_cnts=visitor_cnts, 
                                             player_origin=player_origin, player_destin=player_destin, 
                                             start_time=start_time, end_time=end_time,
                                             read_path=write_path)

        bucket_name = "bolinas"
        file_name = "my_test_file.csv"
        lambda_path = "/tmp/" + file_name
        s3_path = "output/" + file_name
        os.system('echo testing... >'+lambda_path)
        s3 = boto3.resource("s3")
        
        s3.meta.client.upload_file(lambda_path, bucket_name, file_name)
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






# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello, Docker!'