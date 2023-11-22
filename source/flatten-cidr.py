import argparse
import ipaddress
import sys


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
        if validate_cidr(cidr):
            valid_cidrs.append(cidr)
        else:
            invalid_cidrs.append(cidr)

    if invalid_cidrs:
        print(f"Invalid CIDRs: {invalid_cidrs}", file=sys.stderr)
        sys.exit(1)

    if valid_cidrs:
        normalized_cidrs = [normalize_cidr(cidr) for cidr in valid_cidrs]
        cidr_objects = [ipaddress.ip_network(cidr)
                        for cidr in normalized_cidrs]
        merged_cidrs = ipaddress.collapse_addresses(cidr_objects)
        result = [str(cidr) for cidr in merged_cidrs]
        return result

    return []


def main():
    parser = argparse.ArgumentParser(
        description='Merge and normalize CIDRs from a file')
    parser.add_argument('file_path', type=str,
                        help='Path to the file containing CIDRs')
    parser.add_argument('-i', '--indent', type=int, default=0,
                        help='Number of spaces for indentation')

    args = parser.parse_args()

    with open(args.file_path, 'r') as file:
        cidr_list = [line.strip() for line in file]

    result = merge_and_normalize_cidrs(cidr_list)
    for cidr in result:
        print(' ' * args.indent + cidr)


if __name__ == "__main__":
    main()
