'''Tests for kuma/wiki/views/edit.py'''
import pytest

from kuma.core.models import IPBan
from kuma.core.tests import assert_no_cache_header
from kuma.core.urlresolvers import reverse


def test_edit_get(editor_client, root_doc):
    url = reverse('wiki.edit', args=[root_doc.slug])
    response = editor_client.get(url)
    assert response.status_code == 200
    assert response['X-Robots-Tag'] == 'noindex'
    assert_no_cache_header(response)


@pytest.mark.parametrize('method', ('GET', 'POST'))
def test_edit_banned_ip_not_allowed(method, editor_client, root_doc,
                                    cleared_cacheback_cache):
    ip = '127.0.0.1'
    IPBan.objects.create(ip=ip)
    url = reverse('wiki.edit', args=[root_doc.slug])
    caller = getattr(editor_client, method.lower())
    response = caller(url, REMOTE_ADDR=ip)
    assert response.status_code == 403
    assert_no_cache_header(response)
    assert 'Your IP address has been banned.' in response.content
