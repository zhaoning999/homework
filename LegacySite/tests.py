from django.test import TestCase
# Create your tests here.

from . import extras
import json
import io
from .views import SALT_LEN

class MyTest(TestCase):
    fixtures = ['default.json']

    def test_bug_1_xss(self):
        response = self.client.get('/buy.html?director=<script type="text/javascript">alert("XSS"); </script>')
        self.assertContains(response=response, text='&lt;script type=&quot;text/javascript&quot;&gt;alert('
                                                    '&quot;XSS&quot;); &lt;/script&gt;')

    def test_bug_2_purchase(self):
        self.client.login(username='uname', password='uname')
        response = self.client.post('/gift.html', {'username': 'ushanka', 'amount': 13})
        self.assertContains(response, text="Don't gift a card on other's behalf")

    def test_bug_3_sql_injection_password(self):
        self.client.login(username='uname', password='uname')
        response1 = self.client.post('/buy.html', {'amount': 14})
        giftcard = io.BytesIO(response1.content)
        card_data = json.loads(giftcard.read())
        card_data['records'][0]['signature'] = card_data['records'][0]['signature'] + '\' or 1=1; select * from ' \
                                                                             'LegacySite_user -- '
        giftcard = io.BytesIO(json.dumps(card_data).encode('utf-8'))
        response2 = self.client.post('/use.html', data={'card_data': giftcard, 'card_supplied': True})
        self.assertNotContains(response=response2, text='admin', html=True)

    def test_bug_4_random_seed(self):
        self.assertFalse(extras.generate_salt(SALT_LEN) == extras.generate_salt(SALT_LEN))
