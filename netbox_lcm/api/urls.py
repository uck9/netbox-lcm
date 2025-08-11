from netbox.api.routers import NetBoxRouter
from netbox_lcm.api.views import *

router = NetBoxRouter()
router.register('devices', DeviceLifecycleViewSet)
router.register('external-assessment-types', ExternalAssessmentTypeViewSet)
router.register('external-assessments', ExternalAssessmentViewSet)
router.register('hardwarelifecycle', HardwareLifecycleViewSet)
router.register('hardwarelifecycleplan', HardwareLifecyclePlanViewSet)
router.register('license', LicenseViewSet)
router.register('licenseassignment', LicenseAssignmentViewSet)
router.register('sku', SupportSKUViewSet)
router.register('supportcontract', SupportContractViewSet)
router.register('supportcontractassignment', SupportContractAssignmentViewSet)
router.register('vendor', VendorViewSet)
urlpatterns = router.urls
