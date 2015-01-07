from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField

class Clipping(models.Model):

    """Clipping maps a placeholder to a name that is unique for a given site.

    """

    identifier = models.CharField(max_length=255, db_index=True)
    site = models.ForeignKey(Site, null=True)
    content = PlaceholderField('clipping')

    def save(self, *args, **kwargs):
        super(Clipping, self).save(*args, **kwargs)
        if self.identifier:
            identifier_parts = self.identifier.split('::')
            identifier_name = '/'.join(identifier_parts)

            counter = 0
            while len(identifier_name) > 38:
                counter -= 1
                identifier_name = '/'.join(identifier_parts[counter:])

            identifier_name = u'Clipping :: %s' % identifier_name.title()

            self.content.slot = identifier_name
            self.content.save()


    class Meta:
        unique_together = (("identifier", "site"),)

    identifier.verbose_name = _("identifier")
    site.verbose_name = _("site")
    content.verbose_name = _("content")

    identifier.help_text = _("The name used to find and display this clipping")
    site.help_text = _("The web site where this clipping will be displayed")

    def __unicode__(self):
        return self.identifier

