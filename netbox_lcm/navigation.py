from netbox.plugins import PluginMenuItem, PluginMenu

lifecycle = PluginMenuItem(
    link='plugins:netbox_lcm:hardwarelifecycle_list',
    link_text='Hardware Lifecycle',
    permissions=['netbox_lcm.view_hardwarelifecycle'],
)

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
    link_text='Contracts',
    permissions=['netbox_lcm.view_supportcontrnact'],
)
contract_assignments = PluginMenuItem(
    link='plugins:netbox_lcm:supportcontractassignment_list',
    link_text='Contract Assignments',
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
        ('Lifecycle', (lifecycle, )),
        ('Support Contracts', (vendors, skus, contracts, contract_assignments)),
        ('Licensing', (licenses, license_assignments)),
    ),
    icon_class='mdi mdi-server'
)
