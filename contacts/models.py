# contacts/models.py

from django.db import models
from django.db.models import permalink

from contacts.fields import CountryField
from contacts.managers import *
from contacts.settings import CONTACT_MARKUP

class ContactBase(models.Model):
    """
    
    Abstract contact model. Includes fields shared
    between all contact types.
        
    """
    objects = ContactManager()

    TYPE_PERSON = 1
    TYPE_COMMERCIAL = 2
    TYPE_EDUCATIONAL = 3
    TYPE_NONPROFIT = 4
    TYPE_GOVERNMENTAL = 5
    TYPE_CHOICES = (
        (TYPE_PERSON, 'Person'),
        (TYPE_COMMERCIAL, 'Commercial Business'),
        (TYPE_EDUCATIONAL, 'Educational Institution'),
        (TYPE_NONPROFIT, 'Non-Profit Organization'),
        (TYPE_GOVERNMENTAL, 'Governmental Organization'),
    )

    # core fields
    contact_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField('state/province', max_length=128, blank=True)
    code = models.CharField(max_length=32, blank=True, help_text="Zip or Postal Code")
    country = CountryField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=64, blank=True)
    mobile = models.CharField(max_length=64, blank=True)
    fax = models.CharField(max_length=64, blank=True)
    website = models.URLField(blank=True, verify_exists=True)

    # metadata
    slug = models.SlugField(unique=True,
                            help_text="Unique web title automatically generated from name.")

    #autogenerated fields
    first_name = models.CharField(max_length=255, blank=True, editable=False)
    middle_name = models.CharField(max_length=255, blank=True, editable=False)
    last_name = models.CharField(max_length=255, blank=True, editable=False)

    # Fields to store generated HTML.
    description_html = models.TextField(editable=False, blank=True)
        
    class Meta:
        abstract = True
        ordering = ('contact_type', 'name',)

    @permalink
    def get_absolute_url(self):
        return ('contacts_contact_detail', [str(self.slug)])

    def __unicode__(self):
        return u'%s' % self.name

    def render_markup(self):
        """Turns any markup into HTML"""
        original = self.description_html

        if CONTACT_MARKUP == 'markdown':
            self.description_html = markup.markdown(self.description)
        elif CONTACT_MARKUP == 'restructured_text':
            self.description_html = markup.restructuredtext(self.description)
        elif CONTACT_MARKUP == 'textile':
            self.description_html = markup.textile(self.description)
        elif CONTACT_MARKUP == 'wysiwyg':
            self.description_html = self.description
        elif CONTACT_MARKUP == 'html':
            self.description_html = self.description
        else:
            self.description_html = strip_tags(self.description)

    def save(self, force_insert=False, force_update=False):
        self.render_markup()
        if self.contact_type == self.TYPE_PERSON:
            names = self.name.split()
            self.first_name = names[0]
            self.last_name = names[-1]
            if len(names) == 3:
                self.middle_name = names[1]
        super(Affiliate, self).save(force_insert, force_update)