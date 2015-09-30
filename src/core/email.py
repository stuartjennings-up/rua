from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings

from core import models
from core import log

from pprint import pprint

def filepath(book, attachment):
	return '%s/%s/%s' % (settings.BOOK_DIR, book.id, attachment.uuid_filename)

def send_email(subject, context, from_email, to, html_template, book=None, attachment=None):

	htmly = Template(html_template)
	con = Context(context)
	html_content = htmly.render(con)

	msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")

	if attachment:
		msg.attach_file(filepath(book, attachment))

	msg.send()

	if book:
		log.add_email_log_entry(book, subject, from_email, to, html_content)
