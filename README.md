# Alanytics 2

Real time data for editorial sites. A rewrite of https://github.com/gamernetwork/alanytics (node and cronjob based analysis).

Use FluxDB, Kapacitor, asyncio, aiohttp

## Requirements and setup

### Install fluxdb (nightly build) and kapacitor

```
wget https://s3.amazonaws.com/influxdb/influxdb_nightly_amd64.deb
sudo dpkg -i influxdb_nightly_amd64.deb
```

Need FluxDB nightly in order to benefit from this change https://github.com/influxdata/influxdb/pull/6510
which means you can take the `last()` val in InfluxQL from a set and get a timestamp.

### Install Kapacitor (current release)

```
wget https://s3.amazonaws.com/kapacitor/kapacitor_0.12.0-1_amd64.deb
sudo dpkg -i influxdb_0.12.2-1_amd64.deb
```

### Checkout code

```
git clone git@github.com/gamernetwork/alanytics2/
```

### Install python gubs

We need a nice shiny new python to get decent asyncio. We'll use pyenv to slot different python installations on this box.

#### Install python 3.5.1

```
# Get pyenv
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
# set up environment using bashrc
# you can use bash_profile if you want, I don't care
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc 
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc 
echo 'eval "$(pyenv init -)"' >> ~/.bashrc 
# restart env
exec bash
# use pyenv to install python 3.5.1
pyenv install 3.5.1
# or wherever you've installed it
cd alanytics-python/
# set this project to use python 3.5.1
pyenv local 3.5.1
# check it's worked
python -V
```

There should be a `.python-version` file in current dir too.

#### Install alanytics python deps

Note: python3 ships with py**v**env (note: 'v') for virtualenvs.

```
cd alanytics
pyvenv env
env/bin/pip install -r requirements.txt
```

Run collector

```
env/bin/python -m aiohttp.web -H `hostname` -P 8081 alan.app:init
```

Define Kapacitor pipeline

```
kapacitor define -name top_arts -tick top_arts.tick -type stream -dbrp alan_raw_hits.oneday
kapacitor enable top_arts
```


