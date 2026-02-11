# AWS CLOUD PROJECT
* Runs on EC2 instance 
* Uses ML model stored on S3
* Uses Jinja for dynamic frontend
* Connected with RDS to store metrics
* Uses Lambda function

## TO INSTALL LIBRARIES ON EC2
pip3 install -r requirements.txt

## TO RUN JINJA FLASK APP
python3 app.py

## TO COPY TO EC2 INSTANCE
rsync -avz \
  --exclude-from=<RSYNCIGNORE-FILE> \
  -e "ssh -i <CERTIFICATE>" \
  <PROJECT-FOLDER> \
  ec2-user@<PUBLIC-IP>:~

## TO CONNECT TO EC2 INSTANCE
ssh -i <CERTIFICATE> ec2-user@<PUBLIC-IP>

## TO CONNECT TO RDS
psql -h <DATABASE-ENDPOINT> \
     -U <USERNAME> \
     -d <DATABASE> \
     -p <PORT>
