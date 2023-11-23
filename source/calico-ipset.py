# script.py

import argparse
import ipaddress
import os.path
import sys
import yaml


def validate_cidr(cidr):
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def normalize_cidr(cidr):
    cidr_object = ipaddress.ip_network(cidr, strict=False)
    return f"{cidr_object.network_address}/{cidr_object.netmask}"


def merge_and_normalize_cidrs(cidr_list):
    valid_cidrs = []
    invalid_cidrs = []

    for cidr in cidr_list:
        # Ignore lines starting with '#' or '//'
        if not cidr.strip().startswith('#') \
                and not cidr.strip().startswith('//'):
            if validate_cidr(cidr):
                valid_cidrs.append(cidr)
            else:
                invalid_cidrs.append(cidr)

    if invalid_cidrs:
        print(f"Invalid CIDRs: {invalid_cidrs}", file=sys.stderr)
        sys.exit(1)

    if valid_cidrs:
        normalized_cidrs = [normalize_cidr(cidr) for cidr in valid_cidrs]
        cidr_objects = [ipaddress.ip_network(
            cidr) for cidr in normalized_cidrs]
        return [str(cidr) for
                cidr in ipaddress.collapse_addresses(cidr_objects)]

    return []


def generate_calico_manifest(name, namespace, labels, cidrs):
    labels_dict = yaml.safe_load(labels)
    formatted_labels = "\n    ".join(
        [f"{key}: '{value}'" for key, value in labels_dict.items()])

    manifest = f"""apiVersion: crd.projectcalico.org/v1
kind: NetworkSet
metadata:
  name: {name}
  namespace: {namespace}
  labels:
    {formatted_labels}
spec:
  nets:"""""

    for cidr in cidrs:
        manifest += f"\n    - {cidr}"

    return manifest


def process_list(original_list):
    new_list = []

    for item in original_list:
        if len(item) == 0:
            continue
        if isinstance(item, str) and ',' in item:
            split_elements = [elem for elem in item.split(',') if elem.strip()]
            new_list.extend(split_elements)
        elif isinstance(item, list):
            new_list.append(item)
        else:
            new_list.append(item)

    return new_list


def main():
    parser = argparse.ArgumentParser(
        description='Generate Calico manifest for NetworkSet')
    parser.add_argument('files', type=str, nargs='+',
                        help='Paths to the files containing CIDRs')
    parser.add_argument('--name', type=str, required=True,
                        help='Name of the NetworkSet')
    parser.add_argument('--namespace', type=str, required=True,
                        help='Namespace of the NetworkSet')
    parser.add_argument('--labels', type=str, required=True,
                        help='YAML string of labels for the '
                        'NetworkSet in key:value format')
    parser.add_argument('--output', type=str, help='Output file name')

    args = parser.parse_args()

    inputs = process_list(args.files)
    print(f"Inputs: {inputs}")

    if os.path.isdir('/github/workspace'):
        path_prefix = '/github/workspace/'
    else:
        path_prefix = ''

    for i in range(len(inputs)):
        if ' ' in inputs[i]:
            split_elements = [elem for elem in
                              inputs[i].split(' ') if elem.strip()]
            inputs.extend(split_elements)
            inputs.remove(inputs[i])

    for file_path in inputs:
        if not os.path.exists(path_prefix + file_path):
            print(
                f"Error: Input file '{path_prefix + file_path}' "
                "does not exist.",
                file=sys.stderr)
            sys.exit(1)

    cidr_list = []

    for file_path in inputs:
        with open(path_prefix + file_path, 'r') as file:
            # Filter out lines starting with '#' or '//'
            lines = [line.strip() for line in file if not line.strip(
            ).startswith('#') and not line.strip().startswith('//')]
            cidr_list.extend(lines)

    normalized_cidrs = merge_and_normalize_cidrs(cidr_list)
    calico_manifest = generate_calico_manifest(
        args.name, args.namespace, args.labels, normalized_cidrs)

    if args.output:
        with open(path_prefix + args.output, 'w') as output_file:
            output_file.write(calico_manifest)
    else:
        print(calico_manifest)


if __name__ == "__main__":
    main()
