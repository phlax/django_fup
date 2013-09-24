from django.forms.models import BaseInlineFormSet


class AtLeastOneImageFormSet(BaseInlineFormSet):

    def __init__(self, *la, **kwa):
        if 'request' in kwa:
            kwa.pop('request')

        super(AtLeastOneImageFormSet, self).__init__(*la, **kwa)
        if self.forms:
            self.forms[0].empty_permitted = False
