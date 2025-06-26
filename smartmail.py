# === Listing 1. Lambda Email Sending Function ===
def send_bulk_email(subject, body, recipient_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'mailsutra@knmcadibav.com'
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SMTP_USER, SMTP_PASSWORD)
                    server.sendmail(msg['From'], recipient_email, msg.as_string())
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise e
                time.sleep(2 ** retry_count)

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")

# === Listing 2. Recipient Data Processing ===
def process_recipient_data(batch_size=100):
    try:
        recipients = get_recipients_from_s3()
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]
            process_batch(batch)
            log_metrics('BatchProcessed', len(batch), 'Count')
    except Exception as e:
        logger.error(f"Data processing failed: {str(e)}")
        raise e

# === Listing 3. Batch Email Processing with Thread Pool ===
def process_batch(recipients):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_email, recipient) for recipient in recipients]
        wait(futures, timeout=30)

# === Listing 4. Rate Limiter Implementation ===
class RateLimiter:
    def __init__(self, max_rate):
        self.max_rate = max_rate
        self.tokens = max_rate
        self.last_update = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            time_passed = now - self.last_update
            self.tokens = min(
                self.max_rate,
                self.tokens + time_passed * self.max_rate
            )
            if self.tokens >= 1:
                self.tokens -= 1
                self.last_update = now
                return True
            return False

# === Listing 5. IAM Policy for SES and S3 Access ===
iam_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::${bucket_name}/*"
            ]
        }
    ]
}
