from utilities.choices import ChoiceSet

class SoftwareReleaseStatusChoices(ChoiceSet):
    key = 'SoftwareRelease.status'
    
    TARGET = 'target'
    ACCEPTED = 'accepted'
    RETIRED_UPGRADE_PRI_01 = 'retired_upgrade_pri_01'
    RETIRED_UPGRADE_PRI_02 = 'retired_upgrade_pri_02'
    RETIRED_UPGRADE_PRI_03 = 'retired_upgrade_pri_03'
    EXEMPTED = 'exempted'

    CHOICES = [
        (TARGET, 'Target Active Version'),
        (ACCEPTED, 'Accepted Active Version'),
        (RETIRED_UPGRADE_PRI_01, 'Upgrade Required - High Priority'),
        (RETIRED_UPGRADE_PRI_02, 'Upgrade Required - Medium Priority'),
        (RETIRED_UPGRADE_PRI_03, 'Upgrade Required - Low Priority'),
        (EXEMPTED, 'Exempted'),
    ]

    default = ACCEPTED


class CVESeverityChoices(ChoiceSet):
    """Choices for the types of CVE severities."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"

    CHOICES = (
        (CRITICAL, CRITICAL),
        (HIGH, HIGH),
        (MEDIUM, MEDIUM),
        (LOW, LOW),
        (NONE, NONE),
    )