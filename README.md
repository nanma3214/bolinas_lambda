# bolinas_lambda
Integration of [Bolinas traffic simulation](https://github.com/cb-cities/spatial_queue/tree/master/projects/bolinas_civic) with AWS Lambda for the Bolinas Resilience game developed on Unity.

&nbsp;

## Project Map

![alt text](https://github.com/nanma3214/bolinas_lambda/blob/main/project_map.jpg?raw=true)


## In This Repository
```
bolinas_lambda
│   README.md
│   project_map.jpg
└─── run_traffic_similation
│   │   app_run_sim.py
│   │   Dockerfile.runsim
│   │   requirements.txt
└─── query_path
│   │   app_query_path.py
│   │   Dockerfile.query
│   │   requirements.txt
└─── outdated (intended for run & query the simulation together)
│   │   app.py
│   │   Dockerfile
│   │   requirements.txt
```
&nbsp;


## Project Overview
Three components for this project:

**Unity** &leftarrow; Amazon API Gateway &rightarrow; **AWS Lambda** &leftarrow; AWS SDK for Python (Boto3)&rightarrow; **AWS S3(Simple Cloud Storage)**

&nbsp;


## API Gateway

API resource structure (current stage v1-4):
```
test_bolinas
└─── async (outdated)
│   │   GET
└─── invoke-sim (for Lambda function invoke_sim)
│   │   GET
└─── query-path (for Lambda function query-path)
│   │   GET
└─── store-ans (for Lambda function store-ans)
│   │   POST
└─── sync (outdated)
│   │   GET
```
&nbsp;


## AWS Lambda Structure

The Bolinas traffic simulation is breaken down into two stages at AWS Lambda:

1. Run traffic simulation
   
    Execute [run_traffic_simulation.py](https://github.com/cb-cities/spatial_queue/blob/master/projects/bolinas_civic/run_traffic_simulation.py).

    Two AWS Lambda functions are responsible for this stage:

      * invoke_simulation: code can be accessed from AWS Lambda directly
      * run_traffic_simulation: is built as a container from `/run_traffic_simulation/Dockerfile.runsim` 

     
2. Query path

    Execute [query_path.py](https://github.com/cb-cities/spatial_queue/blob/master/projects/bolinas_civic/query_path.py).

    One AWS Lambda function is responsible for this stage:
    
    * query_path: is built as a container from `/query_path/Dockerfile.query`

The Unity game makes two API `GET` request through API Gateway to invoke these two stages.

&nbsp;


## Dockers

### Generate `requirements.txt`
This step is skipped unless building dockers from scratch.
```
cd /path/to/python-docker

pip3 install -Iv numpy==1.19.4
pip3 install -Iv matplotlib==3.3.1
pip3 install -Iv geopandas==0.8.1
pip3 install scipy

pip3 freeze > requirements.txt
touch app.py
```
&nbsp;

### Build Docker images
Give the docker a name and a tag and set to `$imageName`. Here the docker name is `query` and the tag is `v1.21`.

```
imageName=query:v1.21
docker build -f Dockerfile -t ${imageName} .
```

&nbsp;

### Test Docker images locally

Run dockers locally:
```
docker run -p 9000:8080  ${imageName}
```

Execute the running docker in shell(get the `container-id` by `docker ps -a`):
```
docker exec -it <container-id> sh
```

Simulate the Lambda environment (read more on [here](https://docs.aws.amazon.com/lambda/latest/dg/images-test.html)):
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

Commit Docker image:
```
docker commit <container-id> <imagename:tag>
```

Remove a Docker image:
```
docker image rm  ${imageName}
```

Remove all Docker image:
```
docker container rm $(docker ps -a -q)
```

&nbsp;

### Push Docker image to Amazon Elastic Container Registry (ACR)

First, install AWS CLI command line tool following [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html). 
&nbsp;


Log in to AWS through AWS CLI. Need AWS account ID and region (such as `us-east-2`).

```
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-2.amazonaws.com 
```   

Lastly, set up the local Docker image name `$imageName`, the image name on ECR `$ecrImageTag`, and the ECR repository name `$repositoryName`. For example, 

```
imageName=query:v1.21
ecrImageTag=queryV1.21
repositoryName=playground
```
Tag the local image and upload to ECR.
```
docker tag  ${imageName} <account-id>.dkr.ecr.us-east-2.amazonaws.com/${repositoryName}:${ecrImageTag}

docker push <account-id>.dkr.ecr.us-east-2.amazonaws.com/${repositoryName}:${ecrImageTag}    
```
&nbsp;

### Other things that might be useful
#### AWS Lambda Test Template
```
{
  "vphh": "1.5",
  "visitor_cnts": "300",
  "player_origin": "143",
  "player_destin": "193",
  "start_time": "100",
  "end_time": "900"
}
```

#### API Gateway Header Mapping Template
```
{
     "vphh": "$input.params('vphh')",
     "visitor_cnts": "$input.params('visitor_cnts')",
     "player_origin": "$input.params('player_origin')",
     "player_destin": "$input.params('player_destin')",
     "start_time": "$input.params('start_time')",
     "end_time": "$input.params('end_time')"
}
```

#### API Gateway Parameter Test
```
vphh=1.5&visitor_cnts=300&player_origin=143&player_destin=193&start_time=100&end_time=900
````
