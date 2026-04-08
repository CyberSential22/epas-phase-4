def get_client_ip(request):
    """
    Retrieves the client's real IP address, considering proxy headers
    provided by Vercel/Render, with fallback to standard remote_addr.
    """
    # Check X-Forwarded-For (standard for proxies like Vercel/Render)
    # The header is often comma-separated: client, proxy1, proxy2...
    if 'X-Forwarded-For' in request.headers:
        # Take the first IP if multiple are listed
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()

    # Check X-Real-IP (used by some proxies)
    if 'X-Real-IP' in request.headers:
        return request.headers.get('X-Real-IP')

    # Fallback to direct client connection IP
    return request.remote_addr
