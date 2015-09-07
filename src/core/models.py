from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User

import uuid
import os

from autoslug import AutoSlugField

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

SALUTATION_CHOICES = (
	('Miss', 'Miss'),
	('Ms', 'Ms'),
	('Mrs', 'Mrs'),
	('Mr', 'Mr'),
	('Dr', 'Dr'),
	('Prof.', 'Prof.'),
)

COUNTRY_CHOICES = [('', 'Countries...'), (u'AF', u'Afghanistan'), (u'AX', u'\xc5land Islands'), (u'AL', u'Albania'), (u'DZ', u'Algeria'), (u'AS', u'American Samoa'), (u'AD', u'Andorra'), (u'AO', u'Angola'), (u'AI', u'Anguilla'), (u'AQ', u'Antarctica'), (u'AG', u'Antigua and Barbuda'), (u'AR', u'Argentina'), (u'AM', u'Armenia'), (u'AW', u'Aruba'), (u'AU', u'Australia'), (u'AT', u'Austria'), (u'AZ', u'Azerbaijan'), (u'BS', u'Bahamas'), (u'BH', u'Bahrain'), (u'BD', u'Bangladesh'), (u'BB', u'Barbados'), (u'BY', u'Belarus'), (u'BE', u'Belgium'), (u'BZ', u'Belize'), (u'BJ', u'Benin'), (u'BM', u'Bermuda'), (u'BT', u'Bhutan'), (u'BO', u'Bolivia, Plurinational State of'), (u'BQ', u'Bonaire, Sint Eustatius and Saba'), (u'BA', u'Bosnia and Herzegovina'), (u'BW', u'Botswana'), (u'BV', u'Bouvet Island'), (u'BR', u'Brazil'), (u'IO', u'British Indian Ocean Territory'), (u'BN', u'Brunei Darussalam'), (u'BG', u'Bulgaria'), (u'BF', u'Burkina Faso'), (u'BI', u'Burundi'), (u'KH', u'Cambodia'), (u'CM', u'Cameroon'), (u'CA', u'Canada'), (u'CV', u'Cape Verde'), (u'KY', u'Cayman Islands'), (u'CF', u'Central African Republic'), (u'TD', u'Chad'), (u'CL', u'Chile'), (u'CN', u'China'), (u'CX', u'Christmas Island'), (u'CC', u'Cocos (Keeling) Islands'), (u'CO', u'Colombia'), (u'KM', u'Comoros'), (u'CG', u'Congo'), (u'CD', u'Congo, The Democratic Republic of the'), (u'CK', u'Cook Islands'), (u'CR', u'Costa Rica'), (u'CI', u"C\xf4te d'Ivoire"), (u'HR', u'Croatia'), (u'CU', u'Cuba'), (u'CW', u'Cura\xe7ao'), (u'CY', u'Cyprus'), (u'CZ', u'Czech Republic'), (u'DK', u'Denmark'), (u'DJ', u'Djibouti'), (u'DM', u'Dominica'), (u'DO', u'Dominican Republic'), (u'EC', u'Ecuador'), (u'EG', u'Egypt'), (u'SV', u'El Salvador'), (u'GQ', u'Equatorial Guinea'), (u'ER', u'Eritrea'), (u'EE', u'Estonia'), (u'ET', u'Ethiopia'), (u'FK', u'Falkland Islands (Malvinas)'), (u'FO', u'Faroe Islands'), (u'FJ', u'Fiji'), (u'FI', u'Finland'), (u'FR', u'France'), (u'GF', u'French Guiana'), (u'PF', u'French Polynesia'), (u'TF', u'French Southern Territories'), (u'GA', u'Gabon'), (u'GM', u'Gambia'), (u'GE', u'Georgia'), (u'DE', u'Germany'), (u'GH', u'Ghana'), (u'GI', u'Gibraltar'), (u'GR', u'Greece'), (u'GL', u'Greenland'), (u'GD', u'Grenada'), (u'GP', u'Guadeloupe'), (u'GU', u'Guam'), (u'GT', u'Guatemala'), (u'GG', u'Guernsey'), (u'GN', u'Guinea'), (u'GW', u'Guinea-Bissau'), (u'GY', u'Guyana'), (u'HT', u'Haiti'), (u'HM', u'Heard Island and McDonald Islands'), (u'VA', u'Holy See (Vatican City State)'), (u'HN', u'Honduras'), (u'HK', u'Hong Kong'), (u'HU', u'Hungary'), (u'IS', u'Iceland'), (u'IN', u'India'), (u'ID', u'Indonesia'), (u'IR', u'Iran, Islamic Republic of'), (u'IQ', u'Iraq'), (u'IE', u'Ireland'), (u'IM', u'Isle of Man'), (u'IL', u'Israel'), (u'IT', u'Italy'), (u'JM', u'Jamaica'), (u'JP', u'Japan'), (u'JE', u'Jersey'), (u'JO', u'Jordan'), (u'KZ', u'Kazakhstan'), (u'KE', u'Kenya'), (u'KI', u'Kiribati'), (u'KP', u"Korea, Democratic People's Republic of"), (u'KR', u'Korea, Republic of'), (u'KW', u'Kuwait'), (u'KG', u'Kyrgyzstan'), (u'LA', u"Lao People's Democratic Republic"), (u'LV', u'Latvia'), (u'LB', u'Lebanon'), (u'LS', u'Lesotho'), (u'LR', u'Liberia'), (u'LY', u'Libya'), (u'LI', u'Liechtenstein'), (u'LT', u'Lithuania'), (u'LU', u'Luxembourg'), (u'MO', u'Macao'), (u'MK', u'Macedonia, Republic of'), (u'MG', u'Madagascar'), (u'MW', u'Malawi'), (u'MY', u'Malaysia'), (u'MV', u'Maldives'), (u'ML', u'Mali'), (u'MT', u'Malta'), (u'MH', u'Marshall Islands'), (u'MQ', u'Martinique'), (u'MR', u'Mauritania'), (u'MU', u'Mauritius'), (u'YT', u'Mayotte'), (u'MX', u'Mexico'), (u'FM', u'Micronesia, Federated States of'), (u'MD', u'Moldova, Republic of'), (u'MC', u'Monaco'), (u'MN', u'Mongolia'), (u'ME', u'Montenegro'), (u'MS', u'Montserrat'), (u'MA', u'Morocco'), (u'MZ', u'Mozambique'), (u'MM', u'Myanmar'), (u'NA', u'Namibia'), (u'NR', u'Nauru'), (u'NP', u'Nepal'), (u'NL', u'Netherlands'), (u'NC', u'New Caledonia'), (u'NZ', u'New Zealand'), (u'NI', u'Nicaragua'), (u'NE', u'Niger'), (u'NG', u'Nigeria'), (u'NU', u'Niue'), (u'NF', u'Norfolk Island'), (u'MP', u'Northern Mariana Islands'), (u'NO', u'Norway'), (u'OM', u'Oman'), (u'PK', u'Pakistan'), (u'PW', u'Palau'), (u'PS', u'Palestine, State of'), (u'PA', u'Panama'), (u'PG', u'Papua New Guinea'), (u'PY', u'Paraguay'), (u'PE', u'Peru'), (u'PH', u'Philippines'), (u'PN', u'Pitcairn'), (u'PL', u'Poland'), (u'PT', u'Portugal'), (u'PR', u'Puerto Rico'), (u'QA', u'Qatar'), (u'RE', u'R\xe9union'), (u'RO', u'Romania'), (u'RU', u'Russian Federation'), (u'RW', u'Rwanda'), (u'BL', u'Saint Barth\xe9lemy'), (u'SH', u'Saint Helena, Ascension and Tristan da Cunha'), (u'KN', u'Saint Kitts and Nevis'), (u'LC', u'Saint Lucia'), (u'MF', u'Saint Martin (French part)'), (u'PM', u'Saint Pierre and Miquelon'), (u'VC', u'Saint Vincent and the Grenadines'), (u'WS', u'Samoa'), (u'SM', u'San Marino'), (u'ST', u'Sao Tome and Principe'), (u'SA', u'Saudi Arabia'), (u'SN', u'Senegal'), (u'RS', u'Serbia'), (u'SC', u'Seychelles'), (u'SL', u'Sierra Leone'), (u'SG', u'Singapore'), (u'SX', u'Sint Maarten (Dutch part)'), (u'SK', u'Slovakia'), (u'SI', u'Slovenia'), (u'SB', u'Solomon Islands'), (u'SO', u'Somalia'), (u'ZA', u'South Africa'), (u'GS', u'South Georgia and the South Sandwich Islands'), (u'ES', u'Spain'), (u'LK', u'Sri Lanka'), (u'SD', u'Sudan'), (u'SR', u'Suriname'), (u'SS', u'South Sudan'), (u'SJ', u'Svalbard and Jan Mayen'), (u'SZ', u'Swaziland'), (u'SE', u'Sweden'), (u'CH', u'Switzerland'), (u'SY', u'Syrian Arab Republic'), (u'TW', u'Taiwan, Province of China'), (u'TJ', u'Tajikistan'), (u'TZ', u'Tanzania, United Republic of'), (u'TH', u'Thailand'), (u'TL', u'Timor-Leste'), (u'TG', u'Togo'), (u'TK', u'Tokelau'), (u'TO', u'Tonga'), (u'TT', u'Trinidad and Tobago'), (u'TN', u'Tunisia'), (u'TR', u'Turkey'), (u'TM', u'Turkmenistan'), (u'TC', u'Turks and Caicos Islands'), (u'TV', u'Tuvalu'), (u'UG', u'Uganda'), (u'UA', u'Ukraine'), (u'AE', u'United Arab Emirates'), (u'GB', u'United Kingdom'), (u'US', u'United States'), (u'UM', u'United States Minor Outlying Islands'), (u'UY', u'Uruguay'), (u'UZ', u'Uzbekistan'), (u'VU', u'Vanuatu'), (u'VE', u'Venezuela, Bolivarian Republic of'), (u'VN', u'Viet Nam'), (u'VG', u'Virgin Islands, British'), (u'VI', u'Virgin Islands, U.S.'), (u'WF', u'Wallis and Futuna'), (u'EH', u'Western Sahara'), (u'YE', u'Yemen'), (u'ZM', u'Zambia'), (u'ZW', u'Zimbabwe')]

def profile_images_upload_path(instance, filename):
    try:
        filename = str(uuid.uuid4()) + '.' + str(filename.split('.')[1])
    except IndexError:
        filename = str(uuid.uuid4())

    path = "profile_images/"
    return os.path.join(path, filename)

def cover_images_upload_path(instance, filename):
    try:
        filename = str(uuid.uuid4()) + '.' + str(filename.split('.')[1])
    except IndexError:
        filename = str(uuid.uuid4())

    path = "cover_images/"
    return os.path.join(path, filename)

def task_choices():
	choices = (
		('submission', 'Submission'),
		('review', 'Review'),
		('editing', 'Editing'),
		('production', 'Production'),
		('personal', 'Personal'),
	)
	return choices

def book_type_choices():
	return (
		('monograph', 'Monograph'),
		('edited_volume', 'Edited Volume'),
	)

def review_type_choices():
	return (
		('closed', 'Closed'),
		('open-with', 'Open with Reviewer Info'),
		('open-without', 'Open without Reviewer Info'),
	)

class Language(models.Model):
	code = models.CharField(max_length=200)
	display = models.CharField(max_length=300)

	def __unicode__(self):
		return u'%s' % (self.display)

	def __repr__(self):
		return u'%s' % (self.display)

class Profile(models.Model):
	user = models.OneToOneField(User)
	activation_code = models.CharField(max_length=100, null=True, blank=True)
	salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=True, blank=True)
	middle_name = models.CharField(max_length=300, null=True, blank=True)
	biography = models.TextField(null=True, blank=True)
	orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")
	institution = models.CharField(max_length=1000)
	department = models.CharField(max_length=300, null=True, blank=True)
	country = models.CharField(max_length=300, choices=COUNTRY_CHOICES)
	twitter = models.CharField(max_length=300, null=True, blank=True, verbose_name="Twitter Handle")
	facebook = models.CharField(max_length=300, null=True, blank=True, verbose_name="Facebook Handle")
	linkedin = models.CharField(max_length=300, null=True, blank=True, verbose_name="Linkedin Profile")
	impactstory = models.CharField(max_length=300, null=True, blank=True, verbose_name="ImpactStory ID")
	github = models.CharField(max_length=300, null=True, blank=True, verbose_name="Github Username")
	profile_image = models.ImageField(upload_to=profile_images_upload_path, null=True, blank=True, storage=fs)
	email_sent = models.DateTimeField(blank=True, null=True)
	date_confirmed = models.DateTimeField(blank=True, null=True)
	confirmation_code = models.CharField(max_length=200, blank=True, null=True)
	roles = models.ManyToManyField('Role')

	def full_name(self):
		if self.middle_name:
			return "%s %s %s" % (self.user.first_name, self.middle_name, self.user.last_name)
		else:
			return "%s %s" % (self.user.first_name, self.user.last_name)

class Author(models.Model):
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100)
	salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=True, blank=True)
	institution = models.CharField(max_length=1000)
	department = models.CharField(max_length=300, null=True, blank=True)
	country = models.CharField(max_length=300, choices=COUNTRY_CHOICES)
	author_email = models.CharField(max_length=100)
	biography = models.TextField(max_length=3000, null=True, blank=True)
	orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")
	twitter = models.CharField(max_length=300, null=True, blank=True, verbose_name="Twitter Handle")
	linkedin = models.CharField(max_length=300, null=True, blank=True, verbose_name="Linkedin Profile")
	facebook = models.CharField(max_length=300, null=True, blank=True, verbose_name="Facebook Profile")
	sequence = models.IntegerField(default=1, null=True, blank=True)

	class Meta:
		ordering = ('sequence',)

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

	def __repr__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

	def full_name(self):
		if self.middle_name:
			return "%s %s %s" % (self.user.first_name, self.middle_name, self.user.last_name)
		else:
			return "%s %s" % (self.user.first_name, self.user.last_name)

class Book(models.Model):
	prefix = models.CharField(max_length=100, null=True, blank=True)
	title = models.CharField(max_length=1000, null=True, blank=True)
	subtitle = models.CharField(max_length=1000, null=True, blank=True)
	series = models.ForeignKey('Series', null=True, blank=True, help_text="If you are submitting this work to an existing Series please selected it.")
	author = models.ManyToManyField('Author', null=True, blank=True)
	editor = models.ManyToManyField('Editor', null=True, blank=True)
	description = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Abstract")
	keywords = models.ManyToManyField('Keyword', null=True, blank=True)
	subject = models.ManyToManyField('Subject', null=True, blank=True)
	license = models.ForeignKey('License', null=True, blank=True, help_text="The license you recommend for this work.")
	cover = models.ImageField(upload_to=cover_images_upload_path, null=True, blank=True)
	pages = models.CharField(max_length=10, null=True, blank=True)
	slug = models.CharField(max_length=1000, null=True, blank=True)
	cover_letter = models.TextField(null=True, blank=True, help_text="A covering letter for the Editors.")
	reviewer_suggestions = models.TextField(null=True, blank=True)
	competing_interests = models.TextField(null=True, blank=True, help_text="If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'")
	book_type = models.CharField(max_length=50, null=True, blank=True, choices=book_type_choices(), help_text="A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.")
	review_type = models.CharField(max_length=50, choices=review_type_choices(), default='closed')
	languages = models.ManyToManyField('Language', null=True, blank=True)

	# Book Owner
	owner = models.ForeignKey(User, null=True, blank=True)

	# Dates
	submission_date = models.DateField(auto_now_add=True, null=True, blank=True)
	publication_date = models.DateField(null=True, blank=True)

	# Stage
	stage = models.ForeignKey('Stage', null=True, blank=True)
	submission_stage = models.IntegerField(null=True, blank=True)

	# Review
	review_assignments = models.ManyToManyField('ReviewAssignment', related_name='review', null=True, blank=True)
	review_form = models.ForeignKey('review.Form', null=True, blank=True)

	# Files
	files = models.ManyToManyField('File', null=True, blank=True)
	internal_review_files = models.ManyToManyField('File', null=True, blank=True, related_name='internal_review_files')
	external_review_files = models.ManyToManyField('File', null=True, blank=True, related_name='external_review_files')
	misc_files = models.ManyToManyField('File', null=True, blank=True, related_name='misc_files')

	# Contract
	contract = models.ForeignKey('Contract', null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.title

	def __repr__(self):
		return u'%s' % self.title

	def get_latest_review_round(self):
		try:
			return self.reviewround_set.all().order_by('-round_number')[0].round_number
		except IndexError:
			return 0

	def authors_or_editors(self):
		authors_or_editors = []
		if self.book_type == 'monograph':
			for author in self.author.all():
				if author.middle_name:
					authors_or_editors.append("%s %s %s" % (author.first_name, author.middle_name, author.last_name))
				else:
					authors_or_editors.append("%s %s" % (author.first_name, author.last_name))
		elif self.book_type == 'edited_volume':
			for editor in self.editor.all():
				if editor.middle_name:
					authors_or_editors.append("%s %s %s" % (editor.first_name, editor.middle_name, editor.last_name))
				else:
					authors_or_editors.append("%s %s" % (editor.first_name, editor.last_name))

		return authors_or_editors

	def formats(self):
		return self.format_set.all()

def identifier_choices():
	return (
		('doi', 'DOI'),
		('isbn-10', 'ISBN 10'),
		('isbn-13', 'ISBN 13'),
		('urn', 'URN'),
	)

class Identifier(models.Model):
	book = models.ForeignKey(Book)
	identifier = models.CharField(max_length=20, choices=identifier_choices())
	value = models.CharField(max_length=300)
	displayed = models.BooleanField(default=True)

class PrintSales(models.Model):
	book = models.ForeignKey(Book)
	url = models.URLField()
	name = models.CharField(max_length=200)

class Contract(models.Model):
	title = models.CharField(max_length=1000)
	notes = models.TextField(blank=True, null=True)
	editor_file = models.ForeignKey('File', related_name='editor_file', blank=True, null=True)
	author_file = models.ForeignKey('File', related_name='author_file', blank=True, null=True)
	editor_signed_off = models.DateField(blank=True, null=True)
	author_signed_off = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.title

	def __repr__(self):
		return u'%s' % self.title

def review_type_choices():
	return (
		('internal', 'Internal'),
		('external', 'External'),
	)

def review_recommendation():
	return (
		('accept', 'Accept'),
		('reject', 'Reject'),
		('revisions', 'Revisions Required')
	)

class ReviewRound(models.Model):

	book = models.ForeignKey(Book)
	round_number = models.IntegerField()

	class Meta:
		unique_together = ('book', 'round_number')

	def __unicode__(self):
		return u'%s - %s round_number: %s' % (self.pk, self.book.title, self.round_number)

	def __repr__(self):
		return u'%s - %s round number: %s' %  (self.pk, self.book.title, self.round_number)

class ReviewAssignment(models.Model):
	book = models.ForeignKey(Book) #TODO: Remove this as it is already linked to the book through the review round
	review_round = models.ForeignKey(ReviewRound, blank=True, null=True)
	review_type = models.CharField(max_length=15, choices=review_type_choices())
	user = models.ForeignKey(User)
	assigned = models.DateField(auto_now=True)
	accepted = models.DateField(blank=True, null=True)
	declined = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)
	files = models.ManyToManyField('File', blank=True, null=True)
	body = models.TextField(blank=True, null=True)
	access_key = models.CharField(max_length=200)
	results = models.ForeignKey('review.FormResult', null=True, blank=True)
	recommendation = models.CharField(max_length=10, choices=review_recommendation(), null=True, blank=True)
	competing_interests = models.TextField(blank=True, null=True, help_text="If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'")

	# Used to ensure that an email is not sent more than once.
	unaccepted_reminder = models.BooleanField(default=False)
	accepted_reminder = models.BooleanField(default=False)
	overdue_reminder = models.BooleanField(default=False)

	class Meta:
		unique_together = ('book', 'user', 'review_type', 'review_round')

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.book.title, self.user.username)

	def __repr__(self):
		return u'%s - %s %s' %  (self.pk, self.book.title, self.user.username)

class CopyeditAssignment(models.Model):
	book = models.ForeignKey(Book)
	copyeditor = models.ForeignKey(User, related_name='copyeditor')
	requestor = models.ForeignKey(User, related_name='copyedit_requestor')
	requested = models.DateField(auto_now_add=True)
	accepted = models.DateField(blank=True, null=True)
	declined = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)
	editor_review = models.DateField(blank=True, null=True)
	author_invited = models.DateField(blank=True, null=True)
	author_completed = models.DateField(blank=True, null=True)
	note = models.TextField(blank=True, null=True)
	note_to_author = models.TextField(blank=True, null=True)
	note_from_author = models.TextField(blank=True, null=True)

	files = models.ManyToManyField('File', blank=True, null=True, related_name='cp_assigned_files')
	copyedit_files = models.ManyToManyField('File', blank=True, null=True, related_name='copyedit_files')
	author_files = models.ManyToManyField('File', blank=True, null=True, related_name='author_copyedit_files')

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.book.title, self.copyeditor.username)

	def __repr__(self):
		return u'%s - %s %s' %  (self.pk, self.book.title, self.copyeditor.username)

class IndexAssignment(models.Model):
	book = models.ForeignKey(Book)
	indexer = models.ForeignKey(User, related_name='indexer')
	requestor = models.ForeignKey(User, related_name='index_requestor')
	requested = models.DateField(auto_now_add=True)
	accepted = models.DateField(blank=True, null=True)
	declined = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)
	note_from_indexer = models.TextField(blank=True, null=True)

	files = models.ManyToManyField('File', blank=True, null=True)
	index_files = models.ManyToManyField('File', blank=True, null=True, related_name='index_files')
	

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.book.title, self.indexer.username)

	def __repr__(self):
		return u'%s - %s %s' %  (self.pk, self.book.title, self.indexer.username)

class TypesetAssignment(models.Model):
	book = models.ForeignKey(Book)
	typesetter = models.ForeignKey(User, related_name='typesetter')
	requestor = models.ForeignKey(User, related_name='typeset_requestor')
	requested = models.DateField(auto_now_add=True)
	accepted = models.DateField(blank=True, null=True)
	declined = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)
	editor_review = models.DateField(blank=True, null=True)
	author_invited = models.DateField(blank=True, null=True)
	author_completed = models.DateField(blank=True, null=True)
	editor_second_review = models.DateField(blank=True, null=True)
	typesetter_invited = models.DateField(blank=True, null=True)
	typsetter_completed = models.DateField(blank=True, null=True)

	note = models.TextField(blank=True, null=True)
	note_to_author = models.TextField(blank=True, null=True)
	note_from_author = models.TextField(blank=True, null=True)
	note_to_typesetter = models.TextField(blank=True, null=True)
	note_from_typesetter = models.TextField(blank=True, null=True)

	files = models.ManyToManyField('File', blank=True, null=True)
	typeset_files = models.ManyToManyField('File', blank=True, null=True, related_name='typeset_files')
	author_files = models.ManyToManyField('File', blank=True, null=True, related_name='author_typeset_files')
	typesetter_files = models.ManyToManyField('File', blank=True, null=True, related_name='typsetter_files')

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.book.title, self.typesetter.username)

	def __repr__(self):
		return u'%s - %s %s' %  (self.pk, self.book.title, self.typesetter.username)

class License(models.Model):
	name = models.CharField(max_length=1000)
	short_name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	version = models.CharField(max_length=10)
	url = models.URLField(null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.short_name

	def __repr__(self):
		return u'%s' % self.short_name

class Series(models.Model):
	name = models.CharField(max_length=100)
	editor = models.ForeignKey(User, null=True, blank=True)
	issn = models.CharField(max_length=15)
	description = models.TextField(null=True, blank=True)
	url = models.URLField(null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Editor(models.Model):
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100)
	salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=True, blank=True)
	institution = models.CharField(max_length=1000)
	department = models.CharField(max_length=300, null=True, blank=True)
	country = models.CharField(max_length=300, choices=COUNTRY_CHOICES)
	author_email = models.CharField(max_length=100)
	biography = models.TextField(max_length=3000, null=True, blank=True)
	orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")
	twitter = models.CharField(max_length=300, null=True, blank=True, verbose_name="Twitter Handle")
	linkedin = models.CharField(max_length=300, null=True, blank=True, verbose_name="Linkedin Profile")
	facebook = models.CharField(max_length=300, null=True, blank=True, verbose_name="Facebook Profile")
	sequence = models.IntegerField(default=1, null=True, blank=True)

	class Meta:
		ordering = ('sequence',)

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

	def __repr__(self):
		return u'%s - %s %s' % (self.pk, self.first_name, self.last_name)

	def full_name(self):
		if self.middle_name:
			return "%s %s %s" % (self.user.first_name, self.middle_name, self.user.last_name)
		else:
			return "%s %s" % (self.user.first_name, self.user.last_name)

class File(models.Model):
	mime_type = models.CharField(max_length=50)
	original_filename = models.CharField(max_length=1000)
	uuid_filename = models.CharField(max_length=100)
	label = models.CharField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	date_uploaded = models.DateTimeField(auto_now=True)
	stage_uploaded = models.IntegerField()
	kind = models.CharField(max_length=100)
	sequence = models.IntegerField(default=1)
	owner = models.ForeignKey(User)

	def __unicode__(self):
		return u'%s' % self.original_filename

	def __repr__(self):
		return u'%s' % self.original_filename

	class Meta:
		ordering = ('sequence', '-kind')

class FileVersion(models.Model):
	file = models.ForeignKey(File)
	original_filename = models.CharField(max_length=1000)
	uuid_filename = models.CharField(max_length=100)
	date_uploaded = models.DateTimeField()
	owner = models.ForeignKey(User)

	class Meta:
		ordering = ('-date_uploaded',)

class Subject(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Keyword(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

stage_choices = (
	('proposal', 'Proposal'),
	('submission', 'New Submission'),
	('review', 'Review'),
	('editing', 'Editing'),
	('production', 'Production'),
	('published', 'Published'),
	('declined', 'Declined'),
)

class Stage(models.Model):
	current_stage = models.CharField(max_length="20", choices=stage_choices, null=True, blank=True)
	proposal = models.DateTimeField(null=True, blank=True)
	submission = models.DateTimeField(null=True, blank=True)
	review = models.DateTimeField(null=True, blank=True)
	internal_review = models.DateTimeField(null=True, blank=True)
	external_review = models.DateTimeField(null=True, blank=True)
	editing = models.DateTimeField(null=True, blank=True)
	production = models.DateTimeField(null=True, blank=True)
	publication = models.DateTimeField(null=True, blank=True)
	declined = models.DateTimeField(null=True, blank=True)

	# Optional stages
	copyediting = models.DateTimeField(null=True, blank=True)
	indexing = models.DateTimeField(null=True, blank=True)
	typesetting = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return u'%s' % self.current_stage

	def __repr__(self):
		return u'%s' % self.current_stage

class Task(models.Model):
	book = models.ForeignKey(Book, null=True, blank=True)
	creator = models.ForeignKey(User, related_name='creator')
	assignee = models.ForeignKey(User, related_name='assignee')
	text = models.CharField(max_length=200)
	workflow = models.CharField(max_length=50, choices=task_choices())
	assigned = models.DateField(auto_now_add=True, null=True, blank=True)
	due = models.DateField(null=True, blank=True)
	completed = models.DateField(null=True, blank=True)

class Role(models.Model):
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

log_choices = (
	('submission', 'Submission'),
	('workflow', 'Workflow'),
	('file', 'File'),
	('copyedit', 'Copyedit'),
	('review', 'Review'),
	('index', 'Index'),
	('typeset', 'Typeset'),
)

class Log(models.Model):
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	kind = models.CharField(max_length=100, choices=log_choices)
	short_name = models.CharField(max_length=100)
	message = models.TextField()
	date_logged = models.DateTimeField(auto_now_add=True, null=True, blank=True)

setting_types = (
	('rich_text', 'Rich Text'),
	('text', 'Text'),
	('char', 'Characters'),
	('number', 'Number'),
	('boolean', 'Boolean'),
	('file', 'File'),
)

class SettingGroup(models.Model):
	name = models.CharField(max_length=100)
	enabled = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Setting(models.Model):
	name = models.CharField(max_length=100, unique=True)
	group = models.ForeignKey(SettingGroup)
	types = models.CharField(max_length=20, choices=setting_types)
	value = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ('group', 'name')

	def __unicode__(self):
		return u'%s' % self.name

	def __repr__(self):
		return u'%s' % self.name

class Format(models.Model):
	book = models.ForeignKey(Book)
	file = models.ForeignKey(File)
	name = models.CharField(max_length=200)
	identifier = models.CharField(max_length=200, unique=True)
	sequence = models.IntegerField(default=9999)

	class Meta:
		ordering = ('sequence', 'name')

	def __unicode__(self):
		return u'%s - %s' % (self.book, self.identifier)

	def __repr__(self):
		return u'%s - %s' % (self.book, self.identifier)

class Chapter(models.Model):
	book = models.ForeignKey(Book)
	file = models.ForeignKey(File)
	name = models.CharField(max_length=200)
	identifier = models.CharField(max_length=200, unique=True)
	sequence = models.IntegerField(default=9999)

	class Meta:
		ordering = ('sequence', 'name')

	def __unicode__(self):
		return u'%s - %s' % (self.book, self.identifier)

	def __repr__(self):
		return u'%s - %s' % (self.book, self.indentifier)

class ProposalForm(models.Model):
	name = models.CharField(max_length=100)
	ref = models.CharField(max_length=20, help_text='for proposals: press_code-proposal eg. sup-proposal')
	intro_text = models.TextField(max_length=1000, help_text='Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.')
	completion_text = models.TextField(max_length=1000, help_text='Accepts HTML. Para elements should be wrapped in paragraph tags or they will not have fonts.')
	fields = models.ManyToManyField('ProposalFormElement', through='ProposalFormElementsRelationship')

	def __unicode__(self):
		return u'%s' % self.name
	def __repr__(self):
		return u'%s' % self.name


class ProposalFormElement(models.Model):
	field_choices = (
		('text', 'Text Field'),
		('textarea', 'Text Area'),
		('check', 'Check Box'),
		('select', 'Select'),
		('email', 'Email'),
		('upload', 'Upload'),
		('date', 'Date'),
	)

	name = models.CharField(max_length=1000)
	choices = models.CharField(max_length=500, null=True, blank=True, help_text='Seperate choices with the bar | character.')
	field_type = models.CharField(max_length=100, choices=field_choices)
	required = models.BooleanField()

	def __unicode__(self):
		return '%s' % (self.name)

	def __repr__(self):
		return '<FormElement %s>' % (self.name)

class ProposalFormElementsRelationship(models.Model):
	bs_class_choices = (
		('col-md-4','third'),
		('col-md-6', 'half'),
		('col-md-12', 'full'),
	)

	form = models.ForeignKey(ProposalForm)
	element = models.ForeignKey(ProposalFormElement)
	order = models.IntegerField()
	width = models.CharField(max_length=20, choices = bs_class_choices, help_text='Vertical Space taken by the element when rendering the form')
	help_text = models.TextField(max_length=1000, null=True, blank=True)

	def __unicode__(self):
		return '%s: %s' % (self.form.name, self.element.name)

	def __repr__(self):
		return '<FormElementsRelation %s: %s' % (self.form.name, self.element.name)

	class Meta:
		ordering = ('order',)

