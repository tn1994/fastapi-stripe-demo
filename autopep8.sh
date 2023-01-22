#!/bin/bash
set -eu

#docker-compose run --rm streamlit bash -c 'autopep8 --in-place --recursive --aggressive --aggressive /app/app/'
#docker-compose run --rm streamlit bash -c 'refurb --quiet /app/'

docker-compose run --rm api bash -c '
autopep8 -r -i -a -a /app/;
cd /app/; flake8;
refurb --quiet /app/;
'