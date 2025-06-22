from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

class SupportCoverageStatusChoices(ChoiceSet):
    key = 'SupportCoverage.status'
    
    NO_LONGER_SUPPORTED = 'eox'
    NOT_REQUIRED = 'not_required'
    UNSUPPORTED_VENDOR = 'unsupported_vendor'
    INTERNAL_SUPPORT = 'internal_support'
    UNDER_REVIEW = 'under_review'
    VENDOR_SUPPORTED = 'vendor_supported'
    SUPPORT_REQUIRED = 'required'

    CHOICES = [
        (VENDOR_SUPPORTED, _('Supported - Active Vendor Contract'), 'green'),
        (INTERNAL_SUPPORT, _('Supported - Internal Support Only'), 'green'),
        (SUPPORT_REQUIRED, _('Unsupported - Contract Required'), 'red'),
        (NO_LONGER_SUPPORTED ,_('Unsupported - Past End of EoX (EoS/LDoA)'), 'orange'),
        (NOT_REQUIRED, _('Support Not Required'), 'gray'),
        (UNSUPPORTED_VENDOR, _('Unsupported Vendor or Product'),' gray'),
        (UNDER_REVIEW, _('Unknown – Under Review'), 'yellow'),
    ]
