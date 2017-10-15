#!/bin/bash
set -e

stackname=$1
cftemplate=$2
keypairname=$3


if [ -z "$stackname" ] || [ -z "$cftemplate" ] || [ -z "$keypairname" ]
then
	echo "Not all the required arguments are provided." 
	echo "Usage: ./run.sh <stack name> <cf template path> <key pair name>"
	echo "e.g. ./run.sh voting-app /Users/mk/thoughtworks/conf/ec2/cf-voting-app-ec2.template MusTraining"
	exit 1
fi


echo "Checking for existing $stackname stack........"
sn=$(aws cloudformation describe-stacks --query="Stacks[].StackName" --output text || exit 0)

#echo "Stack Name is $sn" 

if [ ! -z "$sn" ] && [ "$sn" == "$stackname" ]
then
	echo "Found $sn"
	echo "Deleting stack $stackname"
	aws cloudformation delete-stack --stack-name $stackname
	
	echo "Waiting for stack create deletion. This may take several minutes ...."
	aws cloudformation wait stack-delete-complete --stack-name $stackname
else
	echo "No existing stack by the name of $stackname found." 
fi
# if [ status == "CREATE_COMPLETE" ] || [ status == "ROLLBACK_COMPLETE" ]
# then
# 	echo "Deleting stack"
# 	aws cloudformation delete-stack --stack-name $stackname
# 	
# 	echo "Waiting for stack create deletion....this may take several minutes"
# 	aws cloudformation stack-delete-complete --stack-name stackname
# fi


echo "Creating Stack $stackname"
### Take the template body as a CL argument passing a relative path from the code/ec2 folder
aws cloudformation create-stack --stack-name $stackname \
--template-body file://$cftemplate \
--parameters ParameterKey=KeyName,ParameterValue=$keypairname \
  ParameterKey=InstanceType,ParameterValue=t2.nano 
#  > cfresponse.json

#si=$(jq '.StackId' cfresponse.json) 
#echo "StackID is $si"

aws cloudformation describe-stacks --stack-name $stackname --output text

echo "Waiting for stack create completion. This may take several minutes ......."
aws cloudformation wait stack-create-complete --stack-name $stackname

status=$(aws cloudformation describe-stacks --stack-name $stackname --query="Stacks[].StackStatus" --output text)

echo "Status of stack creation is $status"
if [ "$status" != "CREATE_COMPLETE" ]
then
	echo "Stack creation failed for $stackname" 
	exit 1 	
fi

#Waiting for extra time to ensure the ALB is operational
echo "Waiting for the system to warm up......."
sleep 60s

echo "Running tests......"
appURL=$(aws cloudformation describe-stacks --stack-name $stackname --query="Stacks[].Outputs[].OutputValue" --output text)
echo "Application URL for testing is $appURL"

echo "Running smoke tests......"
python tests/ec2/test_smoke.py --baseURL $appURL

echo "Running acceptance tests......"
python tests/ec2/test_func.py --baseURL $appURL
