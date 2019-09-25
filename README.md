Lambda python 3.7 runtime path is:
['/var/task', '/opt/python/lib/python3.7/site-packages', '/opt/python', '/var/runtime', '/var/lang/lib/python37.zip', '/var/lang/lib/python3.7', '/var/lang/lib/python3.7/lib-dynload', '/var/lang/lib/python3.7/site-packages', '/opt/python/lib/python3.7/site-packages', '/opt/python']

If system has python3.7 installed, can do

```
$ pip install --user virutalenv
$ virtualenv --python=python3.7 aws-venv
$ source aws-venv/bin/activate

$ mkdir python
$ pip install -t python/ <packages>			# like pip install -t python/ flask requests
$ zip -r -q aws-packages.zip python/		# zip --recursive --quiet
```

If no python3.7 installed, can use the following

`./pyenv-ubuntu.sh` to get pyenv installed

then do
```
$ pyenv virtualenv 3.7.4 aws-dev
$ pyenv activate aws-dev

# install python packages into python/ folder
$ mkdir python
$ pip install -t ./python <packages>	# like pip install -t /python flask requests

# compress the files into a zip
$ zip -r-q aws-python.zip ./python
```
Upload zip to Lambda layer

Lambda unzips into /opt, hence the /python folder when zipping
