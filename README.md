# 🚀 AWS Cloud ML Web Application

A cloud-based Machine Learning web application deployed on **AWS EC2**, integrated with multiple AWS services.

## 🧱 Architecture

User → EC2 (Flask App with Jinja) →  
• Fetch ML Model from S3  
• Store Metrics in RDS (PostgreSQL)  
• Trigger AWS Lambda (if required)

---

## 🛠 Tech Stack

- Python 3.x
- Flask
- Jinja2
- boto3
- PostgreSQL
- AWS EC2
- AWS S3
- AWS RDS
- AWS Lambda

---

# 📋 Prerequisites

- AWS Account
- EC2 Instance (Amazon Linux / Ubuntu)
- RDS PostgreSQL Instance
- S3 Bucket (with ML model stored)
- IAM Role attached to EC2 with:
  - S3 Read Access
  - Lambda Invoke Permission
- Python 3 installed

---

# 🚀 Deployment Steps

## 1️⃣ Connect to EC2

```bash
ssh -i <CERTIFICATE.pem> ec2-user@<PUBLIC-IP>
````

---

## 2️⃣ Copy Project to EC2

```bash
rsync -avz \
  --exclude-from=<RSYNCIGNORE-FILE> \
  -e "ssh -i <CERTIFICATE.pem>" \
  <PROJECT-FOLDER> \
  ec2-user@<PUBLIC-IP>:~
```

---

## 3️⃣ Install Dependencies

```bash
pip3 install -r requirements.txt
```

### (Recommended) Use Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```
S3_BUCKET_NAME=your-bucket-name
MODEL_FILE_KEY=model.pkl

RDS_HOST=your-rds-endpoint
RDS_DB=your-database
RDS_USER=your-username
RDS_PASSWORD=your-password
RDS_PORT=5432

AWS_REGION=ap-south-1
LAMBDA_FUNCTION_NAME=your-lambda-name
```

---

## 5️⃣ Run Flask (Jinja) Application

```bash
python3 app.py
```

For production-style execution:

```bash
flask run --host=0.0.0.0 --port=5000
```

Access the application at:

```
http://<EC2-PUBLIC-IP>:5000
```

⚠ Make sure your EC2 Security Group allows inbound traffic on port 5000 (or 80 if configured).

---

# 🗄 Connecting to RDS (PostgreSQL)

From EC2:

```bash
psql -h <DATABASE-ENDPOINT> \
     -U <USERNAME> \
     -d <DATABASE> \
     -p <PORT>
```

---

# 📁 Project Structure

```
.
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
├── utils/
│   └── model_loader.py
├── lambda/
│   └── lambda_function.py
└── README.md
```