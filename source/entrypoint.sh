#!/bin/bash

set -e

function convert_to_json() {
  local input_string="$1"

  # Split the string on commas
  IFS=',' read -ra elements <<< "$input_string"

  # Create an associative array to store key-value pairs
  declare -A json_array

  # Process each element and add it to the array
  for element in "${elements[@]}"; do
    IFS=':' read -r key value <<< "$element"
    json_array["$key"]="$value"
  done

  # Convert the associative array to a JSON object
  local json_object=""
  for key in "${!json_array[@]}"; do
    json_object+="\"$key\":\"${json_array[$key]}\","
  done

  # Remove the trailing comma and surround with curly braces
  json_object="{${json_object%,}}"

  echo "$json_object"
}

output_option=""
if [ -n "$INPUT_OUTPUT" ]; then
  output_option="--output=$INPUT_OUTPUT"
fi

parsed_labels=$(convert_to_json "$INPUT_LABELS")

python /app/calico-ipset.py \
  --name="$INPUT_NAME" \
  --namespace="$INPUT_NAMESPACE" \
  --labels="$parsed_labels" \
  "$output_option" \
  "$INPUT_INPUTS"
