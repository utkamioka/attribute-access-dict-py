from unittest import TestCase

from map import Map


class TestMap(TestCase):
    def test_getattr(self):
        m = Map(a=10, b=20, z=Map(x=100, y=200))
        self.assertEqual(m.a, 10)
        self.assertEqual(m.b, 20)
        self.assertEqual(m.z, dict(x=100, y=200))
        self.assertEqual(m.z.x, 100)
        self.assertEqual(m.z.y, 200)

        with self.assertRaises(KeyError):
            _ = m.c

        with self.assertRaises(KeyError):
            _ = m.z.xx

    def test_setattr(self):
        m = Map()

        with self.assertRaises(KeyError):
            _ = m.a

        m.a = 'A'
        m.b = 'B'

        self.assertEqual(m.a, 'A')
        self.assertEqual(m.b, 'B')

        with self.assertRaises(KeyError):
            m.z.x = 'X'

    def test_delattr(self):
        m = Map(a=10, b=20, z=Map(x=100, y=200))
        self.assertEqual(m.a, 10)
        self.assertEqual(m.b, 20)
        self.assertEqual(m.z.x, 100)
        self.assertEqual(m.z.y, 200)

        del m.a

        with self.assertRaises(KeyError):
            _ = m.a

        del m.z.x

        with self.assertRaises(KeyError):
            _ = m.z.x

    def test_via_json_loads(self):
        import json

        book = json.loads('''
        {
            "title": "吾輩は猫である",
            "publish": {
                "date": 1905 
            },
            "author": {
                "name": "夏目漱石",
                "birth": 1867
            }
        }
        ''', object_hook=Map)
        self.assertEqual(book.title, '吾輩は猫である')
        self.assertEqual(book.author.name, '夏目漱石')
        self.assertEqual(book.author.birth, 1867)

        from operator import attrgetter
        ext = attrgetter('title', 'author.name', 'publish.date')
        self.assertEqual(ext(book), ('吾輩は猫である', '夏目漱石', 1905))

    def test_via_toml_loads(self):
        import toml

        book = toml.loads('''
        title = "吾輩は猫である"
        [publish]
        date = 1905
        [author]
        name = "夏目漱石"
        birth = 1867
        ''', _dict=Map)

        self.assertEqual(book.title, '吾輩は猫である')
        self.assertEqual(book.author.name, '夏目漱石')
        self.assertEqual(book.author.birth, 1867)

        from operator import attrgetter
        ext = attrgetter('title', 'author.name', 'publish.date')
        self.assertEqual(ext(book), ('吾輩は猫である', '夏目漱石', 1905))

        from operator import itemgetter
        ext = itemgetter('title', 'author.name', 'publish.date')
        with self.assertRaisesRegex(KeyError, r"'author.name'"):
            ext(book)
