import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import pandas as pd
from dotenv import load_dotenv

df = pd.read_csv('dev.csv')  # change this to data.csv to send real emails
df.dropna(subset=['Email'], inplace=True) # remove any rows with no email address
load_dotenv()  # read the API key from .env
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email('test@example.com') # this email needs to be verified in sendgrid
from_name = 'Name'

def build_email(index, row):
    email_address = row['Email']
    recipient_name = ' '.join(row['First Name'], row['Last Name'])
    subject = f'Test'
    content = Content('text/html',
                      f"""<p style="font-family: Arial, sans-serif; font-size: 14px;">Hi {recipient_name},</p>
                      <p style="font-family: Arial, sans-serif; font-size: 14px;">My name's {from_name}.</p>
                      <p style="font-family: Arial, sans-serif; font-size: 14px;">Looking forward to hearing from you,</p>
                      <p style="font-family: Arial, sans-serif; font-size: 14px;">___</p>
                      <p style="font-family: Arial, sans-serif; font-size: 14px;"></p>""")
    to_email = To(email_address)
    mail = Mail(from_email, to_email, subject, content)

    return mail

for index, row in df.iterrows():
    mail = build_email(index, row)
    mail_json = mail.get() # Get a JSON-ready representation of the Mail object

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
