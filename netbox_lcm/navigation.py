from netbox.plugins import PluginMenuItem, PluginMenu

device_lifecycle = PluginMenuItem(
    link='plugins:netbox_lcm:devicelifecycle_list',
    link_text='Device Lifecycle Information',
    permissions=['netbox_lcm.view_devicelifecycle'],
)

lifecycle = PluginMenuItem(
    link='plugins:netbox_lcm:hardwarelifecycle_list',
    link_text='Hardware Lifecycle Notices',
    permissions=['netbox_lcm.view_hardwarelifecycle'],
)

lifecycle_plans = PluginMenuItem(
    link='plugins:netbox_lcm:hardwarelifecycleplan_list',
    link_text='Hardware Lifecycle Plans',
    permissions=['netbox_lcm.view_hardwarelifecycleplan'],
)

external_assessments = PluginMenuItem(
    link="plugins:netbox_lcm:externalassessment_list",
    link_text="External Assessments",
    permissions=["netbox_lcm.view_externalassessment"],
),

vendors = PluginMenuItem(
    link='plugins:netbox_lcm:vendor_list',
    link_text='Vendors',
    permissions=['netbox_lcm.view_vendor'],
)
skus = PluginMenuItem(
    link='plugins:netbox_lcm:supportsku_list',
    link_text='Support SKUs',
    permissions=['netbox_lcm.view_supportsku'],
)
contracts = PluginMenuItem(
    link='plugins:netbox_lcm:supportcontract_list',
    link_text='Support Contracts',
    permissions=['netbox_lcm.view_supportcontract'],
)
contract_assignments = PluginMenuItem(
    link='plugins:netbox_lcm:supportcontractassignment_list',
    link_text='Support Assignments',
    permissions=['netbox_lcm.view_supportcontractassignment'],
)
licenses = PluginMenuItem(
    link='plugins:netbox_lcm:license_list',
    link_text='Licenses',
    permissions=['netbox_lcm.view_license'],
)
license_assignments = PluginMenuItem(
    link='plugins:netbox_lcm:licenseassignment_list',
    link_text='License Assignments',
    permissions=['netbox_lcm.view_licenseassignment'],
)


menu = PluginMenu(
    label='Lifecycle Management',
    groups=(
        ('Device Info', (device_lifecycle, external_assessments)),
        ('Hardware Lifecycle', (lifecycle, lifecycle_plans)),
        ('Vendor Support', (vendors, skus, contracts, contract_assignments)),
        ('Licensing', (licenses, license_assignments)),
    ),
    icon_class='mdi mdi-server'
)
