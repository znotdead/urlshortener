from django.views import View
from django.shortcuts import get_object_or_404, redirect

from shorturl.models import ShortURL


class ShortURLView(View):
    '''
    Redirect to original URL by code.
    Example: visiting the shortened URL http://localhost/A7dw
        would redirect the browser to the real URL. 
    '''

    def get(self, request, code,  *args, **kwargs):
        shorturl = get_object_or_404(ShortURL, code=code)
        return redirect(shorturl.long_url, permanent=False)
