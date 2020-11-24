from email.mime.text import MIMEText
import smtplib
import configuration as cfg


def send_email(subject, body, notifier_config):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = ', '.join(notifier_config.receivers)
    msg['From'] = notifier_config.sender

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(notifier_config.sender, notifier_config.password)
    s.sendmail(notifier_config.sender, notifier_config.receivers, msg.as_string())
    s.close()


if __name__ == "__main__":
    config = cfg.get_configuration()
    send_email("test", "this is a test", config.notifier)
