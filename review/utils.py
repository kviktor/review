def get_ip_address_from_request(request):
    return request.META.get("REMOTE_ADDR", "")
