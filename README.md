This script monitors a specific file, and uploads the file to a specific s3 bucket

Setup:

Before this script is executed, the following varaibles need to be set in the environment of the OS it is executed in

AWS_REGION
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

Here's a sample command to start the script

python main.py ido20221027200632903600000001 myfile.txt

where ido20221027200632903600000001 is the s3 bucket, and myfile.txt as the file to monitor.