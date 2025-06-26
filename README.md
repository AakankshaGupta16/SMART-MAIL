
# 📧 SMART MAIL – Serverless Email Delivery Platform

A fully serverless, fault-tolerant email delivery system built using **AWS Lambda**, **Amazon SES**, **S3**, and **Python**. Designed to send dynamic, personalized emails at scale, this platform features concurrent processing, retry logic, rate limiting, and event-driven automation.

Developed as part of a **Cloud Computing academic project**, it demonstrates scalable backend design using cloud-native tools with production-ready patterns.

---

## 🚀 Key Features

- 📨 **Bulk Email Delivery**: Sends large volumes of emails via **Amazon SES** with SMTP and TLS.
- 🔁 **Retry Logic**: Implements exponential backoff for email failures with up to 3 retries.
- 🔄 **Rate Limiting**: Prevents abuse of SES quotas using a token-bucket style limiter.
- 🧵 **Threaded Batch Processing**: Uses Python's `ThreadPoolExecutor` for parallel email dispatch.
- 🪣 **S3 Integration**: Reads recipient lists from an S3 bucket, enabling scalable data handling.
- 🔐 **IAM-Secured**: Uses a tightly scoped IAM policy to access SES and S3 services.
- 📊 **Metrics Logging**: Tracks batch success for analysis and monitoring.

---

## 🛠️ Tech Stack

- **AWS Lambda** – Serverless compute platform for email dispatch
- **Amazon SES** – Email sending service
- **Amazon S3** – Storage for recipient lists
- **EventBridge** *(optional)* – Can be extended for real-time event triggers
- **Python** – Core programming language
- **SMTP (via smtplib)** – Used for sending mail through SES
- **Threading** – For concurrent execution

---

## 📂 Project Structure
smart-mail/
┣ 📜 smartmail.py ← all logic combined in one file
┣ 📜 IAMpolicy.json ← standalone IAM policy in valid JSON
┣ 📜 README.md ← this file


---
Academic Context
This project was developed and submitted as part of the Cloud Computing course
## 🧠 How It Works

### 🔹 `smartmail.py`

- `send_bulk_email()` – Sends one email with retry logic
- `process_recipient_data()` – Reads recipients from S3 and batches them
- `process_batch()` – Sends batch concurrently with `ThreadPoolExecutor`
- `RateLimiter` – Ensures emails are sent within SES quota limits

---

## 🔐 IAM Policy

You’ll find the policy defined in both:
- `IAMpolicy.json` (valid JSON for AWS Console / Terraform)
- `iam_policy = {...}` inside `smartmail.py` (for reference)

The policy grants:
```json
"Action": ["ses:SendEmail", "ses:SendRawEmail", "s3:GetObject"]



Author
Aakanksha Gupta
ECE Undergraduate
