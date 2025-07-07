from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    'BackupSystemChoices',
    'BackupStatusChoices',
)

class BackupSystemChoices(ChoiceSet):
    key = 'Backup.system'

    SYSTEM_ORCHESTRATED = 'system_orchestrated'
    CATALYST_CENTER = 'catalyst_center'
    SOLARWINDS_NCM = 'solarwinds_ncm'
    MANUAL = 'manual'
    NONE = 'none'

    CHOICES = [
        (SYSTEM_ORCHESTRATED, _('System Orchestrated'), 'green'),
        (CATALYST_CENTER, _('Cisco Catalyst Center'), 'green'),
        (SOLARWINDS_NCM, _('Solarwinds NCM'), 'green'),
        (MANUAL, _('Manually Backed Up'), 'orange'),
        (NONE, _('Not Backed Up'), 'red'),
    ]

    @classmethod
    def get_label(cls, value):
        for choice in cls.CHOICES:
            if choice[0] == value:
                return str(choice[1])
        return None

class BackupStatusChoices(ChoiceSet):
    key = 'Backup.status'

    SUCCESS = 'success'
    FAILURE = 'failure'
    SKIPPED = 'skipped'
    UNKNOWN = 'unknown'

    CHOICES = [
        (SUCCESS , _('Success'), 'green'),
        (FAILURE, _('Failure'), 'green'),
        (SKIPPED, _('Skipped'), 'green'),
        (UNKNOWN, _('Unknown Status'), 'orange'),
    ]

    @classmethod
    def get_label(cls, value):
        for choice in cls.CHOICES:
            if choice[0] == value:
                return str(choice[1])
        return None