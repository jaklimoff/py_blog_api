from __future__ import unicode_literals

from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from django.db import models

from blogposts import settings


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Post(models.Model):
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('content'), blank=True)
    author = models.ForeignKey(AUTH_USER_MODEL, related_name='added_posts')
    created = models.DateTimeField(_("Created"), default=timezone.now, editable=False)


    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __unicode__(self):
        return u'%s' % self.title