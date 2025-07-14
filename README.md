# 📧 SmartMail – Serverless Email Delivery Platform

**MailSutra** is a fully serverless, secure, and scalable bulk email delivery system built with **AWS Lambda**, **Amazon SES**, and **S3**. Designed to handle thousands of recipients efficiently, it supports dynamic personalization, error handling, retry logic, and optional scheduling via EventBridge. Ideal for use cases like healthcare reminders, corporate campaigns, and educational updates.

Developed as part of a **Cloud Computing academic project**, it follows cloud-native design patterns with production-readiness in mind.

---

## 🚀 Features

- 📨 **Bulk Email Delivery** – Send personalized emails to thousands of users in one operation.
- 🪣 **S3 Integration** – Reads recipient data from Amazon S3 (CSV format).
- 🔐 **Secure SMTP with TLS** – Email delivery via SES SMTP with TLS encryption.
- 🔁 **Retry Logic** – Exponential backoff on failures (up to 3 retries).
- 📉 **Rate Limiting** – Token-bucket style limiter to prevent SES quota breaches.
- 🧵 **Threaded Execution** – Uses `ThreadPoolExecutor` for parallel sending.
- 🪵 **Logging & Monitoring** – Logs outcomes for each batch and supports CloudWatch.
- 🕓 **EventBridge Ready** – Supports scheduled delivery via cron jobs or fixed rates.
- ⚙️ **IAM Policy Controlled** – Follows least-privilege access principles.

---

## 🧰 Tech Stack

| Component        | Usage                           |
|------------------|----------------------------------|
| AWS Lambda       | Serverless compute for dispatch |
| Amazon SES       | Email sending service           |
| Amazon S3        | Recipient data storage          |
| EventBridge      | Optional scheduling trigger     |
| Python 3.x       | Core language                   |
| smtplib + TLS    | SMTP-based email transmission   |
| threading        | Concurrency (parallel batches)  |

---

## 📂 Project Structure

```
smart-mail/
├── smartmail.py         # Main logic file
├── IAMpolicy.json       # IAM permissions for Lambda
├── README.md            # Project documentation
```

---

## 🛠️ Setup Instructions

### Prerequisites

- ✅ AWS Account (S3, Lambda, SES configured)
- ✅ SMTP credentials (e.g., from Amazon SES)
- ✅ AWS CLI installed and configured
- ✅ Python 3.x environment

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/smartmail.git
cd smartmail
```

### 2. Configure AWS S3

- Go to the AWS Console and create a bucket (e.g., `awsemailbucket123`)
- Upload a CSV named `emails_data.csv` with the format:

```csv
Name,Email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

### 3. Update Configuration in `smartmail.py`

```python
SMTP_USER = '<your-smtp-username>'
SMTP_PASSWORD = '<your-smtp-password>'
S3_BUCKET_NAME = 'awsemailbucket123'
S3_OBJECT_KEY = 'emails_data.csv'
```

### 4. Deploy the Lambda Function

```bash
zip function.zip smartmail.py

aws lambda create-function \
  --function-name MailSutra \
  --runtime python3.x \
  --role <role-arn> \
  --handler smartmail.lambda_handler \
  --timeout 30 \
  --zip-file fileb://function.zip
```

> Replace `<role-arn>` with your IAM Role ARN.

---

## 📤 Triggering the Function

### 1. Manually via AWS Console

- Open Lambda → MailSutra → Test → Use payload:
```json
{
  "send_emails": true
}
```

### 2. AWS CLI

```bash
aws lambda invoke \
  --function-name MailSutra \
  --payload '{"send_emails": true}' \
  output.json
```

### 3. Scheduled via EventBridge

- Go to EventBridge → Create Rule → Schedule → rate(1 day)
- Add MailSutra Lambda as the target

---

## 📨 Example Email Output

**Subject:** Daily Reminder  
**Body:**
```
Hello, this is your daily reminder for the day! Here is some random info: 1234

Thank you for staying on track with your goals.
```

---

## 🧪 Troubleshooting

1. ✅ **S3 Bucket Access** – Check bucket name/object key and permissions  
2. ✅ **SMTP Auth** – Verify SES credentials and TLS port (typically 587)  
3. ✅ **CloudWatch Logs** – Inspect execution logs for issues  
4. ✅ **Test Email** – Try sending to your own email  
5. ✅ **SES Rate Limits** – Check if you're throttled by SES

---

## 🔐 IAM Policy Sample (`IAMpolicy.json`)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ses:SendEmail",
        "ses:SendRawEmail",
        "s3:GetObject"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push: `git push origin feature-name`
5. Open a pull request

---

## 📜 License

Licensed under the MIT License – see `LICENSE` file for details.

---

## 🙏 Acknowledgments

Thanks to the AWS and open-source Python communities for tools, docs, and support that made this project possible.
