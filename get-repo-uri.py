#!/usr/bin/env python

import json
import sys

if __name__ == '__main__':
    long_json = ''
    for line in sys.stdin:
        long_json += line

    repos = json.loads(long_json)
    # {u'repositories': [{u'repositoryArn': u'arn:aws:ecr:us-west-1:799480191532:repository/wb-app/docker-images', u'repositoryName': u'wb-app/docker-images', u'registryId': u'799480191532', u'createdAt': 1570808115.0, u'repositoryUri': u'799480191532.dkr.ecr.us-west-1.amazonaws.com/wb-app/docker-images'}]}
    for repo in repos['repositories']:
        if repo['repositoryName'] == 'wb-app/docker-images':
            sys.stdout.write(repo['repositoryUri'])
