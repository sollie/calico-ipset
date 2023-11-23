# calico-ipset

Action to create calico ipset manifests

```yaml
inputs:
  name:
    required: true
    description: 'Name of the NetworkSet'
  namespace:
    required: true
    description: 'Namespace of the NetworkSet'
  labels:
    required: true
    description: 'String of labels for the NetworkSet in key:value format'
  inputs:
    required: true
    description: 'Paths to the files containing CIDRs'
  output:
    required: false
    description: 'Output file name (default: stdout)'
```
