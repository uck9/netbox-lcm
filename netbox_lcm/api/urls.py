from netbox.api.routers import NetBoxRouter
from .views import *

router = NetBoxRouter()
router.register('devicelifecycle', DeviceLifecycleViewSet)
router.register('hardwarelifecycle', HardwareLifecycleViewSet)
router.register('hardwarelifecycleplan', HardwareLifecyclePlanViewSet)
router.register('device-type-families', DeviceTypeFamilyViewSet)
router.register('software-product', SoftwareProductViewSet)
router.register('software-release', SoftwareReleaseViewSet)
router.register('software-release-compatibility', SoftwareReleaseCompatibilityViewSet)
router.register('software-release-compatibility-status', SoftwareReleaseCompatibilityStatusViewSet)
router.register('software-release-assignment', SoftwareReleaseAssignmentViewSet)
router.register('license', LicenseViewSet)
router.register('licenseassignment', LicenseAssignmentViewSet)
router.register('sku', SupportSKUViewSet)
router.register('supportcontract', SupportContractViewSet)
router.register('supportcontractassignment', SupportContractAssignmentViewSet)
router.register('vendor', VendorViewSet)
urlpatterns = router.urls
