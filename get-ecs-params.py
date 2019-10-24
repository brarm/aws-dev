#!/usr/bin/env python

import boto3
import json
import sys
import jmespath

cf = boto3.client('cloudformation')

def _parse_template(template):
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data

template_summary = cf.get_template_summary(TemplateBody=_parse_template('test.yaml'))
template_parameters = template_summary['Parameters']

input_parameters = []
for t_p in template_parameters:
    input_parameter = {}
    p_key = "ParameterKey"
    p_value = "ParameterValue"
    input_parameter[p_key] = t_p[p_key]
    if t_p['ParameterType'].startswith('List'):
        input_parameter[p_value] = []
    else:
        input_parameter[p_value] = ""
    input_parameters.append(input_parameter)

print(input_parameters)

ec2 = boto3.client('ec2')
default_vpcs = ec2.describe_vpcs(Filters=[{'Name':'isDefault','Values':['true']}])

default_vpc = jmespath.search('Vpcs[].VpcId', default_vpcs)
print(default_vpc)

default_subnets = ec2.describe_subnets(Filters=[{'Name':'vpc-id','Values':[default_vpc[0]]}])
default_subnet = jmespath.search('Subnets[].SubnetId', default_subnets)
print(default_subnet)

default_sgs = ec2.describe_security_groups(Filters=[{'Name':'vpc-id','Values':[default_vpc[0]]},{'Name':'group-name','Values':['default']}])
default_sg = jmespath.search('SecurityGroups[].GroupId',default_sgs)
print(default_sg)

for i_p in input_parameters:
    if i_p['ParameterKey'] == "DefaultSubnets":
        i_p['ParameterValue'].extend(default_subnet[0:2])
    elif i_p['ParameterKey'] == 'DefaultVPC':
        i_p['ParameterValue'].extend(default_vpc)
    elif i_p['ParameterKey'] == 'DefaultSecurityGroup':
        i_p['ParameterValue'].extend(default_sg)

print(input_parameters)

with open('test-parameters.json','w') as params_outfile:
    params_outfile.write(json.dumps(input_parameters, indent=4))
