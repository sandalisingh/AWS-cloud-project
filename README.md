# AWS Cloud ML Web Application

A cloud-based Machine Learning web application deployed on **AWS EC2**, integrated with multiple AWS services.

## Architecture

User → EC2 (Flask App with Jinja) →  
• Fetch ML Model from S3  
• Store Metrics in RDS (PostgreSQL)  
• Trigger AWS Lambda (if required)

---

## Tech Stack

- Python 3.x
- Flask
- Jinja2
- PostgreSQL
- AWS 

---

# Prerequisites

- AWS Account
- EC2 Instance (Amazon Linux)
- RDS PostgreSQL Instance
- S3 Bucket (with ML model stored)
- IAM Role attached to EC2 with:
  - S3 Read Access
- Python 3 installed

---

# Deployment Steps

## 1. Connect to EC2

```bash
ssh -i <CERTIFICATE.pem> ec2-user@<PUBLIC-IP>
````

---

## 2. Copy Project to EC2

```bash
rsync -avz \
  --exclude-from=<RSYNCIGNORE-FILE> \
  -e "ssh -i <CERTIFICATE.pem>" \
  <PROJECT-FOLDER> \
  ec2-user@<PUBLIC-IP>:~
```

---

## 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```
MODEL_URL=model.pkl
CLASS_URL=class_indices.pkl

RDS_HOST=your-rds-endpoint
RDS_DB=your-database
RDS_USER=your-username
RDS_PASSWORD=your-password
RDS_PORT=5432
```

---

## 5. Run Flask (Jinja) Application

```bash
python3 app.py
```

Access the application at:

```
http://<EC2-PUBLIC-IP>:5000
```

⚠ Make sure your EC2 Security Group allows inbound traffic on port 5000 (or 80 if configured).

---

# Connecting to RDS (PostgreSQL)

From EC2:

```bash
psql -h <DATABASE-ENDPOINT> \
     -U <USERNAME> \
     -d <DATABASE> \
     -p <PORT>
```

---