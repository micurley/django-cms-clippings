
from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdmin
from clippings.models import Clipping
from django.contrib.admin.views.main import ChangeList

class ClippingAdmin(PlaceholderAdmin):
    list_display = ('clipping_path', 'identifier')
    search_fields = ('identifier',)

    def clipping_path(self, obj):
        if obj.identifier:
            identifier_parts = obj.identifier.split('::')
            identifier = '/'.join(identifier_parts)

        return identifier.title()
    clipping_path.short_description = 'Clipping Path'

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.

        Force get_ordering to return None (if no ordering specified)
        to prevent  from applying ordering.
        """
        class SortedChangeList(ChangeList):
            def get_query_set(self, *args, **kwargs):
                qs = super(SortedChangeList, self).get_query_set(*args, **kwargs)
                return qs.order_by('identifier')

        if request.GET.get('o'):
            return ChangeList

        return SortedChangeList

admin.site.register(Clipping, ClippingAdmin)
