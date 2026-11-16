import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from site_components import WHATSAPP_CONTEXT, WHATSAPP_MESSAGES, whatsapp_message, whatsapp_topic_key


class WhatsAppLink(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('class') == 'site-whatsapp':
            self.href = attrs['href']


class WhatsAppContextTests(unittest.TestCase):
    def test_location_addresses_the_current_guest(self):
        self.assertEqual(whatsapp_message('pt', '/pt/localizacao/'),
                         'Olá, estou hospedado(a) no apartamento de temporada em Copacabana e tenho dúvidas sobre a localização.')

    def test_topic_and_language_follow_the_page(self):
        self.assertIn('the Wi-Fi connection', whatsapp_message('en', '/en/wifi/'))
        self.assertIn('la cerradura electrónica', whatsapp_message('es', '/es/comodidades/fechadura/'))
        self.assertEqual(whatsapp_message('en', '/en/amenities/'),
                         whatsapp_message('en', '/en/comodidades/'))

    def test_rendered_links_cover_every_route_without_falling_back_to_booking(self):
        for lang in ['pt', 'en', 'es']:
            for page in (ROOT / lang).rglob('index.html'):
                route = str(page.relative_to(ROOT))
                topic = whatsapp_topic_key(route)
                parser = WhatsAppLink()
                parser.feed(page.read_text())
                url = urlparse(parser.href)
                message = parse_qs(url.query)['text'][0]
                with self.subTest(page=route):
                    self.assertEqual(url.path, '/5521981020150')
                    if topic is None:
                        self.assertEqual(message, WHATSAPP_MESSAGES[lang])
                    else:
                        self.assertIn(topic, WHATSAPP_CONTEXT['topics'])
                        self.assertIn(WHATSAPP_CONTEXT['topics'][topic][lang], message)
                        self.assertNotEqual(message, WHATSAPP_MESSAGES[lang])


if __name__ == '__main__':
    unittest.main()
