## sherlock

- A tool to discover hosts on local network cidrs.
- TCP port scan provided host.
- Create a report of discovered hosts & available ports.
- Monitoring and alerting agent on host & port combination.

### Testing from Command Line directly

Three main drivers

- python src/discover.py $cidr $threads
    - python src/discover.py 10.0.20.0/24 256


### Docker build 

`docker build --tag sherlock .`


### Disabled Pylint(s)

Needed to disable line too long - scan.py
- pylint: disable=C0301

Needed to try catch all exception - discover.py:
- pylint: disable=W0702


### Things left to do

- Docker
- Documentation/Demo for usage
- Prep for submission