from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    'SupportCoverageStatusChoices',
)

class SupportCoverageStatusChoices(ChoiceSet):
    key = 'SupportCoverage.status'
    
    NO_LONGER_SUPPORTED = 'past_eox_date'
    UNSUPPORTED_VENDOR = 'unsupported_vendor'
    INTERNAL_SUPPORT = 'internal_support'
    UNDER_REVIEW = 'under_review'
    VENDOR_CONTRACT_ATTACHED = 'vendor_contract_attached'
    VENDOR_CONTRACT_EXPIRED = 'vendor_contract_expired'
    VENDOR_CONTRACT_REVIEW = 'vendor_contract_review'
    SUPPORT_REQUIRED = 'vendor_contract_required'

    CHOICES = [
        (VENDOR_CONTRACT_ATTACHED, _('Supported - Vendor Contract Attached'), 'green'),
        (VENDOR_CONTRACT_REVIEW, _('Supported - Vendor Contract Details require review'), 'yellow'),
        (VENDOR_CONTRACT_EXPIRED, _('Unsupported - Vendor Contract Expired'), 'yellow'),
        (INTERNAL_SUPPORT, _('Supported - Internal Support Only'), 'green'),
        (SUPPORT_REQUIRED, _('Unsupported - Vendor Contract Required'), 'red'),
        (NO_LONGER_SUPPORTED ,_('Unsupported - Past Vendor End of EoX (EoS/LDoA) Date'), 'orange'),
        (UNSUPPORTED_VENDOR, _('Unsupported - Unsupported Vendor or Product'),' gray'),
        (UNDER_REVIEW, _('Unsupported - Requires Review'), 'yellow'),
    ]

    @classmethod
    def get_label(cls, value):
        for choice in cls.CHOICES:
            if choice[0] == value:
                return str(choice[1])
        return None