# Local install of project
> 1. Create conda environment 
> 
> `conda env create -f environment.yml`

Ignore for now. pip later


	
> 2. Install sp

Note that the sp is build not in \sp\build but in \sp lol 
```
rm -r sp
git clone https://github.com/cb-cities/sp.git
cd sp

```

	
> 3. Make some directories 
> 
> `mkdir -p simulation_outputs/link_weights simulation_outputs/log simulation_outputs/network`




# AWS CLI
Problem: Library not loaded: @executable_path/../.Python
install follow (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html)
aws configure 
blablabla

## Push to ECR
Need: 
ID=926340202285
repositoryName=playground
localImage=raw:play

```
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 926340202285.dkr.ecr.us-east-2.amazonaws.com 
```   
```
imageName=runsim:v1
ecrImageTag=runsimV1
repositoryName=playground

docker tag  ${imageName} 926340202285.dkr.ecr.us-east-2.amazonaws.com/${repositoryName}:${ecrImageTag}

docker push 926340202285.dkr.ecr.us-east-2.amazonaws.com/${repositoryName}:${ecrImageTag}    
```

# Build Image
```
$ cd /path/to/python-docker

$ pip3 install Flask
pip3 install -Iv numpy==1.19.4
pip3 install -Iv matplotlib==3.3.1
pip3 install -Iv geopandas==0.8.1
pip3 install scipy
$ pip3 freeze > requirements.txt
$ touch app.py


  - geopandas=0.8.1
  - matplotlib=3.3.1
  - numpy=1.19.4

docker build -f Dockerfile -t raw:play .

```

```
imageName=runsim:v1

docker build -f Dockerfile -t ${imageName} .
docker run -p 9000:8080  ${imageName}

docker run -t ${imageName}

docker exec -it <container-id> sh


curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'


docker container rm $(docker ps -a -q)
docker image rm  ${imageName}


docker commit a898d2b9f1a4 bolinas:test

```

## Mapping template
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

## Test template
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
## Query string
```
vphh=1.5&visitor_cnts=300&player_origin=143&player_destin=193&start_time=100&end_time=900
````
