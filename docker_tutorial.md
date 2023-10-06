- STEP 1: how to create a docker image
    - `docker build -t flashi:latest .`

- `docker tag local-image:tagname new-repo:tagname
docker push new-repo:tagname`

- STEP 2: Login to docker using dockerhub credential
    - `docker login -u <username> -p <password>`

- STEP 3: do docker tag
    -  `docker tag flashi:latest tanyajha/flashi:latest`
    -  `docker tag <local repository> <dockerhub repository>`
 
-  STEP 4: do docker push
    -   `docker push <username>/flashi:latest`
