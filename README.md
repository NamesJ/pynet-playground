# pynet-playground

## Setup
```
git clone https://github.com/NamesJ/pynet-playground.git

cd pynet-playground

# Setup and activate virtual environment
# Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\scripts\activate

pip install -r requirements.txt
```

## Running examples (from root of repo)

### Audio server and client
```
# Terminal 1 - server
python -m net.audio.server
```
```
# Terminal 2 - client
python -m net.audio.client
# You should now hear audio from default microphone coming from default speakers
```

### DNS server and client
```
# Terminal 1 - server
python -m net.dns.server
# By default, net.dns.server.DNSServer is created and attempts to load entries
# from a local 'example.dns' file, which is provided in repo
```
```
# Terminal 2 - client
python -m net.dns.client
# Prompt is provided ">>> "
# To lookup IP address associated with name "github.com":
>>> 0 github.com
# To lookup name associated with IP address "140.82.114.4":
>>> 1 140.82.114.4
# To get server status:
>>> 2
```

### DrawApp server and client
```
# Terminal 1 - server
python -m net.drawapp.server
```
```
# Terminal 2 - client
python -m net.drawapp.client
# Prompt is provided ">>> "
# For quick test, enter "get on with it"
>>> get on with it
# For specific shapes, enter canvas method name, args and kwargs
>>> create_oval 50 50 120 210
```

### Proxy server and client, DNS host (target)
For the proxy server, you need to have 2 servers and 1 client (minimum)
```
# Terminal 1 - host server
# Host server (could be any, for this example we need net.dns.server.DNSServer)
# This will be the server that the proxy server forwards client requests to
python -m net.dns.server
```
```
# Terminal 2 - proxy server
python -m net.proxy.server
```
```
# Terminal 3 - proxy client
python -m net.proxy.client
# You should see several log messages showing DNS requests being sent to proxy
# server (with extra info), then forwarded to DNS server, then response taking
# the reverse path.
```
