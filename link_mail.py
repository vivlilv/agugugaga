import imaplib
import email
from lxml import html
import re
from bs4 import BeautifulSoup


def get_latest_message(imap_host, imap_user, imap_pass):
    """Retrieves the latest message from the inbox and extracts attributes.

    Args:
        imap_host: The hostname of the IMAP server.
        imap_user: The email address.
        imap_pass: The email password.

    Returns:
        A dictionary containing sender, subject, date, and content (HTML or plain text).
    """

    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(imap_user, imap_pass)
    mail.select("inbox")

    status, data = mail.search(None, '(FROM "notify@email.galxe.com")')
    if status != 'OK':
        print('Error searching for emails')
        return None

    msg_ids = data[0].split()
    latest_msg_id = msg_ids[-1]

    status, data = mail.fetch(latest_msg_id, '(RFC822)')
    if status != 'OK':
        print('Error fetching email')
        return None

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    message_info = {
        'sender': msg['From'],
        'subject': msg['Subject'],
        'date': msg['Date']
    }

    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            message_info['content'] = part.get_payload(decode=True).decode('utf-8')
            
    return message_info['content']


def extract_code_with_regex(html_content):
    """Extracts the code between the given markers in the HTML content.

    Args:
        html_content: The HTML content as a string.

    Returns:
        The extracted code, or None if not found.
    """

    # Regex pattern to match text between 'mso-line-height-rule:exactly;">' and '</p></td>'
    pattern = r'mso-line-height-rule:exactly;">(.*?)</p></td>'
    
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# usage:





def main(mail,mail_pass):
    imap_host = 'outlook.office365.com'
    imap_user = mail
    # 'deborah_piercenrsi@outlook.com'
    imap_pass = mail_pass
    # 'w6nHnhrjALL7GEk'
    message_data = get_latest_message(imap_host, imap_user, imap_pass)
    if message_data:
        print('message found')
        h1_text = extract_code_with_regex(message_data)
        if h1_text:
            print(h1_text)
            return h1_text
        else:
            print("H1 element not found")
    else:
      print('Error retrieving message')