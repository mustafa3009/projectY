# Voting App Deployment Automation - Solution 1

## Pre-requisites:
1. Install the latest version of the aws-cli
2. Install python (ver 2.7.x)
3. Install pip (ver 9.x)
4. Install the requests package by running "pip install requests"
5. Run "aws configure" to setup the access and secret keys
6. Login to the AWS console and generate a key pair or use an existing key pair (for use in step 1 of Run section ). 


## Installation
1. Extract the zip file to a suitable location on a Mac OS or a linux environment (e.g /home/some-user/thoughtworks). 
This will be the HOME folder 
2. Use the shell and change directory to the home folder (e.g cd /home/some-user/thoughtworks)

## Run
1. Execute the following script using the shell in the HOME folder
	code/ec2/run.sh <cf stack name> <path to cf template> <keypairname from pre-requisites step 6>
    e.g.	code/ec2/run.sh voting-app conf/ec2/cf-voting-app-ec2.template candidate1

	a. The above script will check for existing cloudformation stacks by the same and delete them first.
	b. It will then build out the entire infrastructure required for the voting app i.e. VPC, Subnets, EC2 instances,
		Security groups, load balancers and other required resources . 
		PLEASE NOTE THAT THIS STEP CAN TAKE UPTO 15 MINUTES.
	c. It will then execute a smoke test followed by functional tests though python scripts. 

2. All the infrastructure can be removed using the AWS Console -> Cloudformation -> voting-app -> Delete stack option


## HOME Folder layout
code - Contains the shell script automating the deploy and test steps. 
		This can be very easily integrated with existing CI/CD tools

conf - Stores the configuration files like cloudformation templates. These templates can be imported into a cloudformation designer to visualize it as a schematic.

doc - Contains the documentation i.e. Solution approach, README and Issue log.

tests - Contains the python test scripts used for smoke and functional tests

## Solution Approach
Kindly refer to the doc/SolutionApproach.pptx for the design approach taken for solution 1. I have also tried to explain how the solution would be implemented in a real world situation.  

