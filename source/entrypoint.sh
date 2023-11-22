#!/bin/bash

set -e

labels=$(echo "$3" | yq eval-all '.[] | to_entries | map("\(.key)=\(.value)") | join(",")' -)

python -m pip install --upgrade pip
pip install -r /requirements.txt
python /script.py --name "$1" --namespace "$2" --labels "$labels" "${@:4}"
