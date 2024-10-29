from .models import ActivityLog

class TrackingActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Catat aktivitas berdasarkan URL
            activity_type = "akses_buku"  # Ubah ini sesuai dengan halaman yang diakses
            if request.path in ['/books/', '/borrow/', '/returns/']:  # Daftar halaman yang dilacak
                ActivityLog.objects.create(user=request.user.profile, activity_type=activity_type)

        return response