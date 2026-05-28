# calico-ipset

GitHub Action that generates Calico `NetworkSet` manifests from CIDR files. Reads one or more files containing CIDR ranges, merges and normalizes them, and outputs a Calico-compatible YAML manifest.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | yes | | Name of the `NetworkSet` |
| `namespace` | yes | | Namespace of the `NetworkSet` |
| `labels` | yes | | Labels in `key:value,key:value` format |
| `inputs` | yes | | Space-separated paths to CIDR files |
| `output` | no | stdout | Output file name |
| `minmask` | no | `32` | Minimum network mask for CIDR normalization |
| `apiversion` | no | `projectcalico.org/v3` | Calico API version for the manifest |

## Usage

```yaml
- name: Generate Calico NetworkSet
  uses: sollie/calico-ipset@v1
  with:
    name: my-networkset
    namespace: default
    labels: 'env:prod,app:myapp'
    inputs: cidrs/block1.txt cidrs/block2.txt
    output: networkset.yaml
    minmask: 24
    apiversion: projectcalico.org/v3
```

## License

MIT — see [LICENSE](LICENSE).
