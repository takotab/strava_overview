#! /usr/bin/env bash
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
# docker rmi $(docker images -q)
docker build -t str_over .
# docker run -d --name mycontainer -p 80:80 myimage
docker run -it -p 8080:8080 -e PORT="8080" \
            -e WORKERS_PER_CORE="0.1" str_over
            # -e BIND="0.0.0.0:8080"\
             
            # -v $PWD/shared:app/shared 
            
