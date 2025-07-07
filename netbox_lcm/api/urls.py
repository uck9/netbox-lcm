from netbox.api.routers import NetBoxRouter
from .views import *

router = NetBoxRouter()

router.register('devicebackuppolicy', DeviceBackupPolicyViewSet)
router.register('devicebackupresult', DeviceBackupResultViewSet)
router.register('devices', DeviceLifecycleViewSet)
router.register('hardwarelifecycle', HardwareLifecycleViewSet)
router.register('hardwarelifecycleplan', HardwareLifecyclePlanViewSet)
router.register('license', LicenseViewSet)
router.register('licenseassignment', LicenseAssignmentViewSet)
router.register('sku', SupportSKUViewSet)
router.register('supportcontract', SupportContractViewSet)
router.register('supportcontractassignment', SupportContractAssignmentViewSet)
router.register('vendor', VendorViewSet)
urlpatterns = router.urls
