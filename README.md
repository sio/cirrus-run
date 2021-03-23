# Command line tool to execute jobs in Cirrus CI

## Project status

Beta software. Adopted by several third parties to build their CI pipelines.
Breaking changes in new releases are possible. Recommended to pin to specific
version when using in production.


## Overview

cirrus-run is a CLI application that allows you to execute builds in
CirrusCI.

It uses local YAML files for build configuration, but requires a reference to
GitHub repo and branch to assign ownership of the build. The build itself may
have no relation to the specified GitHub repo. This enables integration with
other source code hosting platforms, [e.g. with GitLab][blog]: you can trigger
CirrusCI builds by executing cirrus-run in GitLab CI

[blog]: https://potyarkin.ml/posts/2020/cirrus-ci-integration-for-gitlab-projects/



## Installation

cirrus-run can be installed with pip:

```
pip install cirrus-run
```

Latest development versions are also installable:

```
pip install "https://github.com/sio/cirrus-run/tarball/master#egg=cirrus-run"
```

You can also run it in Docker:
[potyarkin/cirrus-run](https://hub.docker.com/r/potyarkin/cirrus-run).
This image is especially useful for integrating with other CI platforms.


## Usage

```
usage: cirrus-run [-h] [--token TOKEN] [--github REPO] [--branch BRANCH] [-v]
                  [--timeout MINUTES]
                  [--show-build-log {failure,always,never}]
                  [CONFIG]

Execute CI jobs in CirrusCI

positional arguments:
  CONFIG                Path to YAML configuration file or Jinja2 template for
                        such file. Filenames ending with .j2 or .jinja2 are
                        assumed to provide the templates. All environment
                        variables are available inside these templates.
                        Default value: $CIRRUS_CONFIG or .cirrus.yml or
                        .cirrus.yml.j2

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Access token for CirrusCI API. Recommended and more
                        secure way of providing the token is via environment
                        variable. Default value: $CIRRUS_API_TOKEN
  --github REPO         GitHub repo id that will own the build
                        ("owner/reponame"). This repo may have no relation to
                        the CI job being executed. It may even be empty.
                        Default value: $CIRRUS_GITHUB_REPO
  --branch BRANCH       GitHub repo branch that will own the build. This
                        branch may have no relation to the CI job being
                        executed. Default value: $CIRRUS_GITHUB_BRANCH or
                        master
  -v, --verbose         Increase output verbosity. Repeating this argument
                        multiple times increases verbosity level even further.
  --timeout MINUTES     Timeout (in minutes) before assuming that the build
                        has hanged and that API responses are unreliable.
                        Default value: $CIRRUS_TIMEOUT or 120
  --show-build-log {failure,always,never}
                        Specify whether to print the build log to stdout after
                        completing CI run. Default value:
                        $CIRRUS_SHOW_BUILD_LOG or "failure"
```


## Support and contributing

If you need help with using cirrus-run, please create
**[an issue](https://github.com/sio/cirrus-run/issues)**. Issues are also the
primary venue for reporting bugs and posting feature requests. General
discussion related to this project is also acceptable and very welcome!

In case you wish to contribute code or documentation, feel free to open **[a
pull request](https://github.com/sio/cirrus-run/pulls)**. That would certainly
make my day!

I'm open to dialog and I promise to behave responsibly and treat all
contributors with respect. Please try to do the same, and treat others the way
you want to be treated.

If for some reason you'd rather not use the issue tracker, contacting me via
email is OK too. Please use a descriptive subject line to enhance visibility
of your message. Also please keep in mind that public discussion channels are
preferable because that way many other people may benefit from reading past
conversations. My email is visible under the GitHub profile and in the commit
log.


## License and copyright

Copyright 2020-2021 Vitaly Potyarkin

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use these files except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
