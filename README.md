Lambda python 3.7 runtime path is:
['/var/task', '/opt/python/lib/python3.7/site-packages', '/opt/python', '/var/runtime', '/var/lang/lib/python37.zip', '/var/lang/lib/python3.7', '/var/lang/lib/python3.7/lib-dynload', '/var/lang/lib/python3.7/site-packages', '/opt/python/lib/python3.7/site-packages', '/opt/python']

use pyenv-ubuntu.sh to get python installed

then do
```
$ pyenv virtualenv 3.7.4 aws-dev
$ pyenv activate aws-dev

# install python packages into python/ folder
$ mkdir python
$ pip install -t ./python <packages>	# like pip install -t /python flask requests

# compress the files into a zip
$ zip -r aws-python.zip ./python
```
Upload zip to Lambda layer

Lambda unzips into /opt, hence the /python folder when zipping
