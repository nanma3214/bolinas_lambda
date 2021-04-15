# Base Image
FROM public.ecr.aws/lambda/python:3.8

# RUN yum install git
RUN yum update -y \
    && yum install -y wget git vim


# Dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# ENV PYTHONPATH "${PYTHONPATH}:${bolinas_root}"

# Clone project files
RUN git clone https://github.com/nanma3214/spatial_queue.git \
    && cd spatial_queue && git checkout master && cd .. \
    && git clone https://github.com/cb-cities/sp.git temp \
    && cd temp && git checkout b094499aab2db7cce3fd449ee1dc88536bab47cf \
    && cd .. \
    && cp -a temp/. spatial_queue/projects/bolinas_civic/sp/. \
    && rm -rf temp \
    && mkdir spatial_queue/projects/bolinas_civic/sp/build \
    && wget --no-check-certificate --content-disposition https://github.com/UCB-CE170a/Fall2020/raw/master/traffic_data/liblsp.so -P ./spatial_queue/projects/bolinas_civic/sp/build 

RUN cp -a ./spatial_queue/projects/bolinas_civic/. .\
    && rm -rf spatial_queue


COPY app.py requirements.txt ./
CMD ["app.handler"]      
