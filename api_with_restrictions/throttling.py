from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class AnonThrottle(AnonRateThrottle):
    rate = '10/minute'

class UserThrottle(UserRateThrottle):
    rate = '20/minute'