import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.utils.translation import gettext as _
from django.utils.html import format_html, format_html_join

from netbox.tables import NetBoxTable, columns

from dcim.models import Device, DeviceType, Manufacturer
from tenancy.models import Tenant

__all__ = (
    'DeviceLifecycleTable',
)

class DeviceLifecycleTable(NetBoxTable):
    actions = None
    name = tables.Column(
        linkify=True,
        verbose_name=_('Name')
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_('Status'),
    )
    serial = tables.Column(
        verbose_name=_("Serial Number")
    )
    manufacturer = tables.Column(
        accessor='device_type.manufacturer',
        linkify=True,
        verbose_name=_('Manufacturer')
    )
    device_type = tables.Column(
        accessor='device_type',
        linkify=True,
        verbose_name='Device Type'
    )
    tenant_group = tables.Column(
        accessor='tenant.group', 
        verbose_name='Tenant Group'
    )
    tenant = tables.Column(
        linkify=True
    )
    site = tables.Column(
        accessor='site',
        linkify=True,
        verbose_name='Site'
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
    {% with valid_contracts=record.prefetched_contracts|dictsort:"contract.contract_id" %}
        {% if valid_contracts %}
            {% for c in valid_contracts %}
                {% if c.contract.contract_id %}
                    <a href="{{ c.get_absolute_url }}">{{ c.contract.contract_id }}</a>{% if not forloop.last %}<br>{% endif %}
                {% endif %}
            {% endfor %}
        {% else %}
            — 
        {% endif %}
    {% endwith %}
    """,
    verbose_name='Support Contract ID'
    )

    support_contract_sku = tables.Column(
        verbose_name='Support SKU',
        accessor='prefetched_contracts',  # still required for export
        orderable=False
    )

    def render_support_contract_sku(self, value):
        skus = [c.sku.sku for c in value if getattr(c.sku, 'sku', None)]
        if not skus:
            return "—"
        return format_html_join('<br>', '{}', ((sku,) for sku in skus))

    support_contract_end = TemplateColumn(
    template_code="""
    {% load lcm_filters %}
    {% if record.prefetched_contracts %}
        {% for c in record.prefetched_contracts %}
            {% if c.end %}
                <span {{ c.end|date_badge_class }}>{{ c.end }}</span>{% if not forloop.last %}<br>{% endif %}
            {% endif %}
        {% endfor %}
    {% else %}—{% endif %}
    """,
    verbose_name='Support Contract End'
    )

    
    class Meta(NetBoxTable.Meta):
        model = Device
        
        fields = (
            'name', 'site', 'status', 'serial', 'manufacturer', 'device_type', 
            'tenant_group', 'tenant', 'hw_end_of_security', 'hw_end_of_support',
            'support_contract_id', 'support_contract_sku', 'support_contract_end'
        )
        default_columns = (
            'name', 'site', 'status', 'manufacturer', 'device_type',
            'hw_end_of_security', 
            'support_contract_id', 'support_contract_sku', 'support_contract_end'
        )
        attrs = {"class": "table table-hover table-striped"}
