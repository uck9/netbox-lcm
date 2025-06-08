from utilities.choices import ChoiceSet

class SoftwareReleaseStatusChoices(ChoiceSet):
    key = 'SoftwareRelease.status'
    
    TARGET = 'target'
    ACCEPTED = 'accepted'
    RETIRED_SEV_01 = 'retired_sev_01'
    RETIRED_SEV_02 = 'retired_sev_02'
    EXEMPTED = 'exempted'

    CHOICES = [
        (TARGET, 'Target Active Version'),
        (ACCEPTED, 'Accepted Active Version'),
        (RETIRED_SEV_01, 'Upgrade Required - Retired Sev. 1'),
        (RETIRED_SEV_02, 'Upgrade Required - Retired Sev. 2'),
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