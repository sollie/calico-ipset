#!/bin/bash

set -e

parse_labels() {
  local labels_string="$1"
  local labels_json="{}"

  IFS=',' read -ra labels <<< "$labels_string"
  for label in "${labels[@]}"; do
    IFS=':' read -r key value <<< "$label"
    labels_json="$labels_json,\"$key\":\"$value\""
  done

  echo "${labels_json:1}"  # Remove leading comma
}

output_option=""
if [ -n "$INPUT_OUTPUT" ]; then
  output_option="--output $INPUT_OUTPUT"
fi

parsed_labels=$(parse_labels "$INPUT_LABELS")

python /script.py \
  --name "$INPUT_NAME" \
  --namespace "$INPUT_NAMESPACE" \
  --labels "$parsed_labels" \
  "$output_option" \
  --file-paths "$INPUT_FILE_PATHS"
