#!/bin/bash

# please run at the root of project-folder
workdir=$PWD

git fetch
## build frontend
cd $workdir/frontend/desktop
npm run build


## restart backend
# update database struct
docker run -it --rm \
    -v $workdir/backend:/deploy/src/backend \
    -v $workdir/alembic.ini:/deploy/src/alembic.ini \
    -v $workdir/alembic:/deploy/src/alembic \
    --network=deploy_default \
    deploy_backend \
    alembic upgrade head

docker restart sport_meeting_backend

echo Done.
