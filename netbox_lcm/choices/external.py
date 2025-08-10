from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet


__all__ = (
    'ExternalAssessmentStatusChoices',
)


class ExternalAssessmentStatusChoices(ChoiceSet):
    key = 'ExternalAssessment.status'

    PASSING = 'pass'
    FAILING = 'fail'
    EXEMPT  = 'exempt'
    UNKNOWN = 'unknown'

    CHOICES = [
        (PASSING, _('Pass'), 'green'),
        (FAILING, _('Fail'), 'red'),
        (EXEMPT, _('Exempt'), 'yellow'),
        (UNKNOWN, _('Unknown'), 'grey'),
    ]

    @classmethod
    def get_label(cls, value):
        for choice in cls.CHOICES:
            if choice[0] == value:
                return str(choice[1])
        return None