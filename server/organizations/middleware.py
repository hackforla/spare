class OrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.org = None

        user = request.user

        if user and user.is_authenticated() and not user.is_superuser:
            request.org = user.org

        return self.get_response(request)
