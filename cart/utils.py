

def get_cart_key(request, session_token=None):
    if request.user.is_authenticated:
        return f'cart:user:{request.user.id}'
    else:
        token = session_token or  request.headers.get('X-Session-Token')
        return f'cart:guest:{token}'