"""Utility methods."""
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import logging
import os
import smtplib
from jinja2 import Template
import requests

# Load logging configuration
log = logging.getLogger(__name__)


def get_parameter(section: str, parameter_name: str = None):
    """Get parameters from flat file config.cfg."""
    configuration = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    configuration.read(path + '/scripts.cfg')
    if parameter_name:
        parameters = configuration[section][parameter_name]
    else:
        parameters = {}
        for key in configuration[section]:
            parameters[key] = configuration[section][key]

    return parameters


def execute_graphql_request(payload: object):
    """Execute queries and mutations on the GraphQL API."""
    url = get_parameter('graphql', 'url')
    headers = {'Content-Type': 'application/graphql'}
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    return data


def send_mail(session_id: int, distribution_list: list, template: str = None, attachment: any = None, **kwargs):
    """Send e-mail to the distribution list."""
    # Verify e-mail configuration
    config = get_parameter('mail')
    for key, value in config.items():
        if value in ['change_me', '', None]:
            error_message = f'Cannot send e-mail notification due to invalid configuration for mail parameter {key}.'
            log.error(error_message)
            raise Exception(error_message)

    # Construct e-mail header
    email = MIMEMultipart()
    email['From'] = config['sender']
    email['To'] = ', '.join(distribution_list)

    # Construct e-mail body and update body template
    if template == 'indicator':
        indicator_name = kwargs['indicator_name']
        email['Subject'] = f'Data quality alert: {indicator_name}'
        html = open(os.path.dirname(__file__) + f'/email/{template}.html', 'r')
        body = html.read()
        body = Template(body)
        body = body.render(**kwargs)

    elif template == 'error':
        indicator_name = kwargs['indicator_name']
        email['Subject'] = f'Data quality error: {indicator_name}'
        html = open(os.path.dirname(__file__) + f'/email/{template}.html', 'r')
        body = html.read()
        body = Template(body)
        kwargs['session_id'] = session_id
        body = body.render(**kwargs)

    else:
        email['Subject'] = 'Data quality notification'
        html = open(os.path.dirname(__file__) + '/email/default.html', 'r')
        body = html.read()
        body = Template(body)
        body = body.render(**kwargs)

    # Attache body to e-mail
    body = MIMEText(body, 'html')
    email.attach(body)

    # Add attachment to e-mail
    if attachment:
        attachment_path = os.path.join(os.path.dirname(__file__), attachment)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment_path, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        email.attach(part)

    # Connect to smtp server
    connection = smtplib.SMTP(config['host'], config['port'])

    # If smtp server is Gmail activate encryption and authenticate user
    if config['host'] == 'smtp.gmail.com':
        connection.ehlo()
        connection.starttls()
        connection.login(config['sender'], config['password'])

    # Send email
    connection.sendmail(email['From'], email['To'], email.as_string())
    connection.quit()

    return True


def send_error(indicator_id: int, indicator_name: str, session_id: int, distribution_list: list, error_message: str):
    """Build the error e-mail to be sent for the session."""
    # Prepare e-mail body
    body = {}
    body['indicator_id'] = indicator_id
    body['indicator_name'] = indicator_name
    body['error_message'] = error_message

    # Send e-mail
    log.info('Send error e-mail.')
    send_mail(session_id, distribution_list, 'error', None, **body)

    return True
