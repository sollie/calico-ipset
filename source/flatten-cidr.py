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
        print(f"Invalid CIDRs: {invalid_cidrs}")

    if valid_cidrs:
        normalized_cidrs = [normalize_cidr(cidr) for cidr in valid_cidrs]
        cidr_objects = [ipaddress.ip_network(cidr)
                        for cidr in normalized_cidrs]
        merged_cidrs = ipaddress.collapse_addresses(cidr_objects)
        result = [str(cidr) for cidr in merged_cidrs]
        return result

    return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py cidr1 cidr2 cidr3 ...")
        sys.exit(1)

    cidr_list = sys.argv[1:]
    result = merge_and_normalize_cidrs(cidr_list)
    print(result)
