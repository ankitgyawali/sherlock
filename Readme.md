## sherlock

- Tool to perform port sweep & discover hosts on provided cidr block.
- Performs port scan on specific host.
- Creates a report of discovered hosts & available ports.
- Monitoring & alerting agent for a host & port combination.


## Testing project features

### CLI Commands

Three core scripts:

#### discover.py [Sweep]

Sweeps provided cidr block (default: 127.0.0.1/32) with provided number of threads (default: 256) for provided port to sweep  (default: 80).
CIDR inputs can be comma separated.

- python src/discover.py $cidr $threads $port_to_sweep
    - `python src/discover.py`
    - `python src/discover.py 8.8.8.8/32 32`
    - `python src/discover.py 127.0.0.1/32 32 5000`
    - `python src/discover.py 127.0.0.1,8.8.8.8/32,10.0.20.28 32 5000`

#### scan.py [Scan]

Scans provided host for open ports (default: 127.0.0.1).

- python src/scan.py $host_ip_to_sweep
    - `python src/scan.py`
    - `python src/scan.py 127.0.0.1`
    - `python src/scan.py 8.8.8.8`

#### monitor.py [Monitor]

Monitor provided host for open ports (default: 127.0.0.1) every given interval (default 5 sec).

- python src/monitor.py $host_ip_to_sweep
    - `python src/monitor.py`
    - `python src/monitor.py 127.0.0.1 1`
    - `python src/monitor.py 8.8.8.8 60`

### UI Features

A basic workflow from root page `/` at default port 5000 would look like:

- Step 1: For Option #1 - Enter appropriate CIDR/Thread/Port to sweep. This will take you to a page with discovered "hosts" with open ports.
- Step 2: Page `/discover` can be used to either save report on the backend or perform a full TCP port scan from the list of discovered hosts.
- Step 3: Page `/scan` can further be used to monitor the host for discoverd ports or save report of open ports on the backend.
- Step 4: Back to control center (main page) from `/scan`.
- Step 5: Option #2 - works similarly by redirecting to `/scan` but now the user can explicitly provide a host ip instead of choosing host from list of discovered ips on a cidr block.
- Step 6: Option #2 can also be tested with public ips (at the users own discretion) as long as they are reachable.
- Step 7: The `/scan` page also contains the monitor feature on `/monitor` which compares a trailing value and current value to detect any changes in port. This comparison happens after a call to the backend to get active port which is executed in a `setInterval` on javascript [works differently than backend's `src/monitor.py`].
- Step 8: The `/monitor` page has a "reset alert" buttons which simply hides the red HTML bootstrap div back to green div.
- Step 9: Back to control center (main page) from `/monitor`.
- Step 10: Option #3 - Simply loads any previously saved reports from `/discover` & `/scan` into the UI if any.


## Running project locally

### Running UI as flask app

- From project root install requirements with `pip install -r requirements.txt`.
- Run `python init.py` to start Flask app or `FLASK_APP="init.py" flask run`.

### Running UI via docker

- Pull latest docker image from docker hub [~100mb based on python/alpine].
`docker pull ankitgyawali/sherlock:latest`

- Run docker image bound to your localhost:500
`docker run -d -p 5000:5000 docker.io/ankitgyawali/sherlock:latest`

### Pushing a new image

`docker build -t sherlock .`

`docker tag sherlock ankitgyawali/sherlock:latest`

`docker login`

`docker push ankitgyawali/sherlock:latest`

## Others

### Disabled Pylint(s)

Disabled line too long on - scan.py:
- pylint: disable=C0301

Disabled try catch all exception - discover.py:
- pylint: disable=W0702


### Screenshots

#### CLI

![01-a-discovery.py-Port-sweep.png](/docs/01-cli/01-a-discovery.py-Port-sweep.png?raw=true "01-a-discovery.py-Port-sweep.png")

![01-b-discovery.py-Port-sweep-full-network.png](/docs/01-cli/01-b-discovery.py-Port-sweep-full-network.png?raw=true "01-b-discovery.py-Port-sweep-full-network.png")

![02-b-scan.py-Port-scan.png](/docs/01-cli/02-b-scan.py-Port-scan.png?raw=true "02-b-scan.py-Port-scan.png")

![03-a-monitor.py-Monitor-scan.png](/docs/01-cli/03-a-monitor.py-Monitor-scan.png?raw=true "03-a-monitor.py-Monitor-scan.png")

#### UI

![01-a-Port-sweep-input.png](/docs/02-ui/01-a-Port-sweep-input.png?raw=true "01-a-Port-sweep-input.png")

![01-b-Port-sweep-output.png](/docs/02-ui/01-b-Port-sweep-output.png?raw=true "01-b-Port-sweep-output.png")

![02-a-Port-scan-input.png](/docs/02-ui/02-a-Port-scan-input.png?raw=true "02-a-Port-scan-input.png")

![02-b-Port-scan-output.png](/docs/02-ui/02-b-Port-scan-output.png?raw=true "02-b-Port-scan-output.png")

![02-c-Port-monitor.png](/docs/02-ui/02-c-Port-monitor.png?raw=true "02-c-Port-monitor.png")

![02-d-Port-monitor-alerting.png](/docs/02-ui/02-d-Port-monitor-alerting.png?raw=true "02-d-Port-monitor-alerting.png")

![03-a-Load-Report.png](/docs/02-ui/03-a-Load-Report.png?raw=true "03-a-Load-Report.png")
