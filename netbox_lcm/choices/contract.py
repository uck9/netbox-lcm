from utilities.choices import ChoiceSet
from django.utils.translation import gettext as _

class SupportCoverageStatusChoices(ChoiceSet):
    key = 'SupportCoverageStatus.reason'

    NO_LONGER_SUPPORTED = 'eox'
    NOT_REQUIRED = 'not_required'
    UNSUPPORTED_VENDOR = 'unsupported_vendor'
    INTERNAL_SUPPORT = 'internal_support'
    UNDER_REVIEW = 'under_review'
    VENDOR_SUPPORTED = 'vendor_supported'
    SUPPORT_REQUIRED = 'required'

    CHOICES = [
        (VENDOR_SUPPORTED, 'Vendor Supported'),
        (SUPPORT_REQUIRED, 'Support Required – Contract Needed'),
        (NO_LONGER_SUPPORTED ,'Past End of EoX (EoS/LDoA)'),
        (NOT_REQUIRED, 'Support Not Required'),
        (UNSUPPORTED_VENDOR,'Unsupported Vendor or Product'),
        (INTERNAL_SUPPORT, 'Internal Support Only'),
        (UNDER_REVIEW, 'Unknown – Under Review'),
    ]