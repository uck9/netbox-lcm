from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    'SupportCoverageStatusChoices',
)

class SupportCoverageStatusChoices(ChoiceSet):
    key = 'SupportCoverage.status'
    
    NO_LONGER_SUPPORTED = 'past_eox_date'
    NOT_REQUIRED = 'not_required'
    UNSUPPORTED_VENDOR = 'unsupported_vendor'
    INTERNAL_SUPPORT = 'internal_support'
    UNDER_REVIEW = 'under_review'
    VENDOR_CONTRACT_ATTACHED = 'vendor_contract_attached'
    SUPPORT_REQUIRED = 'vendor_contract_required'

    CHOICES = [
        (VENDOR_CONTRACT_ATTACHED, _('Supported - Vendor Contract Attached'), 'green'),
        (INTERNAL_SUPPORT, _('Supported - Internal Support Only'), 'green'),
        (SUPPORT_REQUIRED, _('Unsupported - Vendor Contract Required'), 'red'),
        (NO_LONGER_SUPPORTED ,_('Unsupported - Past Vendor End of EoX (EoS/LDoA) Date'), 'orange'),
        (NOT_REQUIRED, _('Support Not Required'), 'gray'),
        (UNSUPPORTED_VENDOR, _('Unsupported Vendor or Product'),' gray'),
        (UNDER_REVIEW, _('Unknown – Under Review'), 'yellow'),
    ]

    @classmethod
    def get_label(cls, value):
        for choice in cls.CHOICES:
            if choice[0] == value:
                return str(choice[1])
        return None