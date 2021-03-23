# Changelog for [cirrus-run]

## v0.4.0 (2021-03-23)

- Added a longer one-time delay to wait out API server errors (see issue #7)
- Added a barebones test suite to (hopefully) eliminate regressions


## v0.3.0 (2020-08-17)

Bugs were fixed, some features were added. Many thanks to [libvirt] team for
their feedback!

- New argument for managing CLI timeout
  *(commit d5ad4bf)*
- Build logs can now be fetched from Cirrus CI and printed to stdout
  *(issue #3)*
- Preempted CI instances do not cause cirrus-run to mistakenly report build
  failure anymore
  *(issue #4)*
- Automatic retries now happen also on API's internal server errors
  *(pull request #6)*

[libvirt]: https://gitlab.com/libvirt/libvirt


## v0.2.0 (2020-02-26)

v0.2.0 is the first cirrus-run release published to PyPI.
Feature set was not modified since the initial release.


## Prior versions (2020-02-13..2020-02-18)

Earlier versions were not tagged and are not available from PyPI. See git
log for the list of changes.

First working version of cirrus-run was released on February 18th, 2020. This
[comment](https://github.com/cirruslabs/cirrus-ci-docs/issues/10#issuecomment-587532447)
marks the event.


[cirrus-run]: https://github.com/sio/cirrus-run
