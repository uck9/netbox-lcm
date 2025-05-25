import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.utils.translation import gettext as _
from django.utils.html import format_html, format_html_join

from netbox.tables import columns, NetBoxTable

from dcim.models import Device

__all__ = (
    'DeviceLifecycleTable',
)

class DeviceLifecycleTable(NetBoxTable):
    actions = None
    device = tables.Column(
        linkify=True,
        verbose_name=_('Name')
    )

    site = tables.Column(
        accessor='site',
        linkify=True,
        verbose_name='Site'
    )

    status = tables.Column(
        verbose_name=_('Status')
    )
    
    device_type = tables.Column(
        accessor='device_type',
        linkify=True,
        verbose_name='Device Type'
    )

    hw_end_of_security = TemplateColumn(
        template_code="""
        {% load lcm_filters %}
        <span {{ record.hw_end_of_security|date_badge_class }}>{{ record.hw_end_of_security }}</span>
        """,
        verbose_name="HW - EoVSS"
    )

    hw_end_of_support = TemplateColumn(
        template_code="""
        {% load lcm_filters %}
        <span {{ record.hw_end_of_support|date_badge_class }}>{{ record.hw_end_of_support }}</span>
        """,
        verbose_name="HW - EoS"
    )
    
    support_contract_id = TemplateColumn(
        template_code="""
        {% if record.prefetched_contracts %}
            {% for c in record.prefetched_contracts %}
                {{ c.contract.contract_id }}
            {% endfor %}
        {% else %}—{% endif %}
        """,
        verbose_name='Support Contract ID'
    )

    support_contract_sku = TemplateColumn(
        template_code="""
        {% if record.prefetched_contracts %}
            {% for c in record.prefetched_contracts %}
                {{ c.sku.sku }}
            {% endfor %}
        {% else %}—{% endif %}
        """,
        verbose_name='Support SKU'
    )

    support_contract_end = TemplateColumn(
        template_code="""
        {% load lcm_filters %}
        {% if record.prefetched_contracts %}
            {% for c in record.prefetched_contracts %}
                <span {{ c.end|default:c.contract.end|date_badge_class }}>{{ c.end|default:c.contract.end }}</span>
            {% endfor %}
        {% else %}—{% endif %}
        """,
        verbose_name='Support Contract End'
    )
    
    class Meta(NetBoxTable.Meta):
        model = Device
        
        fields = (
            'name', 'site', 'status', 'device_type',
            'hw_end_of_security', 'hw_end_of_support',
            'support_contract_id', 'support_contract_sku', 'support_contract_end' )
        default_columns = (
            'name', 'site', 'status', 'device_type',
            'hw_end_of_security', 
            'support_contract_id', 'support_contract_sku', 'support_contract_end'
        )
        attrs = {"class": "table table-hover table-striped"}
