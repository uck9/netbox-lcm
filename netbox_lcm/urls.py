from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import views
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan, SupportContract, License, \
    LicenseAssignment, SupportContractAssignment, SupportSKU, Vendor

urlpatterns = [
    path('hardware/', views.HardwareLifecycleListView.as_view(), name='hardwarelifecycle_list'),
    path('hardware/add', views.HardwareLifecycleEditView.as_view(), name='hardwarelifecycle_add'),
    path('hardware/edit', views.HardwareLifecycleBulkEditView.as_view(), name='hardwarelifecycle_bulk_edit'),
    path('hardware/delete', views.HardwareLifecycleBulkDeleteView.as_view(), name='hardwarelifecycle_bulk_delete'),
    path('hardware/<int:pk>', views.HardwareLifecycleView.as_view(), name='hardwarelifecycle'),
    path('hardware/<int:pk>/edit', views.HardwareLifecycleEditView.as_view(), name='hardwarelifecycle_edit'),
    path('hardware/<int:pk>/delete', views.HardwareLifecycleDeleteView.as_view(), name='hardwarelifecycle_delete'),
    path('hardware/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='hardwarelifecycle_changelog', \
        kwargs={'model': HardwareLifecycle}),

    path('hardware-plan/', views.HardwareLifecyclePlanListView.as_view(), name='hardwarelifecycleplan_list'),
    path('hardware-plan/add', views.HardwareLifecyclePlanEditView.as_view(), name='hardwarelifecycleplan_add'),
    path('hardware-plan/edit', views.HardwareLifecyclePlanBulkEditView.as_view(), name='hardwarelifecycleplan_bulk_edit'),
    path('hardware-plan/delete', views.HardwareLifecyclePlanBulkDeleteView.as_view(), name='hardwarelifecycleplan_bulk_delete'),
    path('hardware-plan/<int:pk>', views.HardwareLifecyclePlanView.as_view(), name='hardwarelifecycleplan'),
    path('hardware-plan/<int:pk>/edit', views.HardwareLifecyclePlanEditView.as_view(), name='hardwarelifecycleplan_edit'),
    path('hardware-plan/<int:pk>/delete', views.HardwareLifecyclePlanDeleteView.as_view(), name='hardwarelifecycleplan_delete'),
    path('hardware-plan/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='hardwarelifecycleplan_changelog', \
         kwargs={'model': HardwareLifecyclePlan}),

    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/add', views.VendorEditView.as_view(), name='vendor_add'),
    path('vendors/edit', views.VendorBulkEditView.as_view(), name='vendor_bulk_edit'),
    path('vendors/delete', views.VendorBulkDeleteView.as_view(), name='vendor_bulk_delete'),
    path('vendors/<int:pk>', views.VendorView.as_view(), name='vendor'),
    path('vendors/<int:pk>/edit', views.VendorEditView.as_view(), name='vendor_edit'),
    path('vendors/<int:pk>/delete', views.VendorDeleteView.as_view(), name='vendor_delete'),
    path('vendors/<int:pk>/changelog', ObjectChangeLogView.as_view(), \
        name='vendor_changelog', kwargs={'model': Vendor}),

    path('contracts/', views.SupportContractListView.as_view(), name='supportcontract_list'),
    path('contracts/add', views.SupportContractEditView.as_view(), name='supportcontract_add'),
    path('contracts/edit', views.SupportContractBulkEditView.as_view(), name='supportcontract_bulk_edit'),
    path('contracts/delete', views.SupportContractBulkDeleteView.as_view(), name='supportcontract_bulk_delete'),
    path('contracts/<int:pk>', views.SupportContractView.as_view(), name='supportcontract'),
    path('contracts/<int:pk>/devices', views.SupportContractAssignmentsView.as_view(), name='supportcontract_assignments'),
    path('contracts/<int:pk>/edit', views.SupportContractEditView.as_view(), name='supportcontract_edit'),
    path('contracts/<int:pk>/delete', views.SupportContractDeleteView.as_view(), name='supportcontract_delete'),
    path('contracts/<int:pk>/changelog', ObjectChangeLogView.as_view(), \
        name='supportcontract_changelog', kwargs={'model': SupportContract}),

    path('contract-assignment/', views.SupportContractAssignmentListView.as_view(), \
        name='supportcontractassignment_list'),
    path('contract-assignment/add', views.SupportContractAssignmentEditView.as_view(), \
        name='supportcontractassignment_add'),
    path('contract-assignment/edit/', views.SupportContractAssignmentBulkEditView.as_view(), \
        name='supportcontractassignment_bulk_edit'),
    path('contract-assignment/delete/', views.SupportContractAssignmentBulkDeleteView.as_view(), \
        name='supportcontractassignment_bulk_delete'),
    path('contract-assignment/<int:pk>', views.SupportContractAssignmentView.as_view(), \
        name='supportcontractassignment'),
    path('contract-assignment/<int:pk>/edit', views.SupportContractAssignmentEditView.as_view(), \
        name='supportcontractassignment_edit'),
    path('contract-assignment/<int:pk>/delete', views.SupportContractAssignmentDeleteView.as_view(), \
        name='supportcontractassignment_delete'),
    path('contract-assignment/<int:pk>/changelog', ObjectChangeLogView.as_view(), \
        name='supportcontractassignment_changelog', kwargs={'model': SupportContractAssignment}),

    path('license/', views.LicenseListView.as_view(), name='license_list'),
    path('license/add', views.LicenseEditView.as_view(), name='license_add'),
    path('license/edit', views.LicenseBulkEditView.as_view(), name='license_bulk_edit'),
    path('license/delete', views.LicenseBulkDeleteView.as_view(), name='license_bulk_delete'),
    path('license/<int:pk>', views.LicenseView.as_view(), name='license'),
    path('license/<int:pk>/assignments', views.LicenseAssignmentsView.as_view(), name='license_assignments'),
    path('license/<int:pk>/edit', views.LicenseEditView.as_view(), name='license_edit'),
    path('license/<int:pk>/delete', views.LicenseDeleteView.as_view(), name='license_delete'),
    path('license/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='license_changelog', \
         kwargs={'model': License}),

    path('sku/', views.SupportSKUListView.as_view(), name='supportsku_list'),
    path('sku/add', views.SupportSKUEditView.as_view(), name='supportsku_add'),
    path('sku/edit', views.SupportSKUBulkEditView.as_view(), name='supportsku_bulk_edit'),
    path('sku/delete', views.SupportSKUBulkDeleteView.as_view(), name='supportsku_bulk_delete'),
    path('sku/<int:pk>', views.SupportSKUView.as_view(), name='supportsku'),
    path('sku/<int:pk>/edit', views.SupportSKUEditView.as_view(), name='supportsku_edit'),
    path('sku/<int:pk>/delete', views.SupportSKUDeleteView.as_view(), name='supportsku_delete'),
    path('sku/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='supportsku_changelog', \
         kwargs={'model': SupportSKU}),

    path('license-assignment/', views.LicenseAssignmentListView.as_view(), name='licenseassignment_list'),
    path('license-assignment/add', views.LicenseAssignmentEditView.as_view(), name='licenseassignment_add'),
    path('license-assignment/edit', views.LicenseAssignmentBulkEditView.as_view(), name='licenseassignment_bulk_edit'),
    path('license-assignment/delete/', views.LicenseAssignmentBulkDeleteView.as_view(), name='licenseassignment_bulk_delete'),
    path('license-assignment/<int:pk>', views.LicenseAssignmentView.as_view(), name='licenseassignment'),
    path('license-assignment/<int:pk>/edit', views.LicenseAssignmentEditView.as_view(), name='licenseassignment_edit'),
    path('license-assignment/<int:pk>/delete', views.LicenseAssignmentDeleteView.as_view(), name='licenseassignment_delete'),
    path('license-assignment/<int:pk>/changelog', ObjectChangeLogView.as_view(), \
        name='licenseassignment_changelog', kwargs={'model': LicenseAssignment}),

    path('devices/', views.DeviceLifecycleListView.as_view(), name='devicelifecycle_list'),
]
