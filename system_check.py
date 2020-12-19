#!/usr/bin/env python3
import shutil
import psutil
import socket
import email.message
import smtplib

#CPU utilization > 80%
cpu_threshold = 80.0
#Free disk space < 20%
free_disk_threshold = 20
#Available memory < 500MB
mem_threshold = 500000000
#Resolve hostname Check
test_host = "localhost"
test_ip = "127.0.0.1"
#Configure email address
sender = "automated@email.com"
receiver = "dev@email.com"

errors_found = []
def cpu_check():
    cpu_usage = psutil.cpu_percent(1)
    if cpu_usage >= cpu_threshold:
        errors_found.append("Error - CPU usage is over 80%")

def mem_check():
    mem = psutil.virtual_memory()
    if mem.available <= mem_threshold:
        errors_found.append("Error - Available memory is less than 500MB")

def disk_check():
    total, used, free = shutil.disk_usage("/")
    free_disk_percent = free / total * 100
    if free_disk_percent <= free_disk_threshold:
        errors_found.append("Error - Available disk space is less than 20%")

def network_check():
    ipaddress = socket.gethostbyname(test_host)
    if ipaddress is not test_ip:
        errors_found.append("Error - {} cannot be resolved to {}".format(test_host, test_ip))

def generate_email_body(sender, recipient, subject, body):
    '''create email message format'''
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    return message

def send_email(message):
    """Sends the message to the configured SMTP server."""
    mail_server = smtplib.SMTP('localhost')
    mail_server.send_message(message)
    mail_server.quit()

if __name__ == "__main__":
    cpu_check()
    mem_check()
    disk_check()
    network_check()
    for error in errors_found:
        from_ip = socket.gethostbyname(socket.gethostname())
        from_hostname = socket.gethostname()
        subject = "[{}] {}".format(from_hostname, error)
        body = "[{}:{}] | {}".format(from_hostname, from_ip, error)
        message = generate_email_body(sender, receiver, subject, body)
        emails.send_email(message)

