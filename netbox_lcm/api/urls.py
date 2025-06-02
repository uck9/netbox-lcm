from netbox.api.routers import NetBoxRouter
from .views import *

router = NetBoxRouter()
router.register('hardwarelifecycle', HardwareLifecycleViewSet)
router.register('hardwarelifecycleplan', HardwareLifecyclePlanViewSet)
router.register('device-type-families', DeviceTypeFamilyViewSet)
router.register('softwareproduct', SoftwareProductViewSet)
router.register('softwarerelease', SoftwareReleaseViewSet)
router.register('softwarereleaseassignment', SoftwareReleaseAssignmentViewSet)
router.register('license', LicenseViewSet)
router.register('licenseassignment', LicenseAssignmentViewSet)
router.register('sku', SupportSKUViewSet)
router.register('supportcontract', SupportContractViewSet)
router.register('supportcontractassignment', SupportContractAssignmentViewSet)
router.register('vendor', VendorViewSet)
urlpatterns = router.urls
