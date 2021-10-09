# Elastic Kubernetes Service

## Install ``eksctl``

```
brew tap weaveworks/tap
```

```
brew install weaveworks/tap/eksctl
```

### Verify the result

```
eksctl
```

```
The official CLI for Amazon EKS

Usage: eksctl [command] [flags]

Commands:
  eksctl anywhere                        EKS anywhere
  eksctl associate                       Associate resources with a cluster
  eksctl completion                      Generates shell completion scripts for bash, zsh or fish
  eksctl create                          Create resource(s)
  eksctl delete                          Delete resource(s)
  eksctl deregister                      Deregister a non-EKS cluster
  eksctl disassociate                    Disassociate resources from a cluster
  eksctl drain                           Drain resource(s)
  eksctl enable                          Enable features in a cluster
  eksctl get                             Get resource(s)
  eksctl help                            Help about any command
  eksctl info                            Output the version of eksctl, kubectl and OS info
  eksctl register                        Register a non-EKS cluster
  eksctl scale                           Scale resources(s)
  eksctl set                             Set values
  eksctl unset                           Unset values
  eksctl update                          Update resource(s)
  eksctl upgrade                         Upgrade resource(s)
  eksctl utils                           Various utils
  eksctl version                         Output the version of eksctl

Common flags:
  -C, --color string   toggle colorized logs (valid options: true, false, fabulous) (default "true")
  -h, --help           help for this command
  -v, --verbose int    set log level, use 0 to silence, 4 for debugging and 5 for debugging with AWS debug logging (default 3)
```
