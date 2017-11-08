#!/usr/bin/env python
# coding: utf-8

"""
Functional Test of the API
"""

import os, sys, unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))  # noqa
sys.path.insert(0, pkg_root)  # noqa

import nestedcontext


class TestNestedScope(unittest.TestCase):
    def test_simplecontext(self):
        with nestedcontext.bind(abc="def"):
            self.assertEqual(nestedcontext.inject('abc'), "def")

        with self.assertRaises(KeyError):
            nestedcontext.inject('abc')

    def test_context_names(self):
        with nestedcontext.bind(abc="def"):
            self.assertEqual(nestedcontext.inject('abc'), "def")
            with nestedcontext.bind(abc="ghi", stackname="otherstack"):
                self.assertEqual(nestedcontext.inject('abc'), "def")
                self.assertEqual(nestedcontext.inject('abc', stackname="otherstack"), "ghi")

        with self.assertRaises(KeyError):
            nestedcontext.inject('abc')
        with self.assertRaises(KeyError):
            nestedcontext.inject('abc', stackname="otherstack")

        self.assertEqual("def", nestedcontext.inject('abc', stackname="otherstack", default="def"))

    def test_nestedcontext(self):
        with nestedcontext.bind(abc="def"):
            self.assertEqual(nestedcontext.inject('abc'), "def")
            with nestedcontext.bind(abc="ghi"):
                self.assertEqual(nestedcontext.inject('abc'), "ghi")

        with self.assertRaises(KeyError):
            nestedcontext.inject('abc')

    def test_nestedcontext_detect_conflicts(self):
        with nestedcontext.bind(abc="def"):
            self.assertEqual(nestedcontext.inject('abc'), "def")
            with self.assertRaises(ValueError):
                with nestedcontext.bind(abc="ghi", conflicts_are_errors=True):
                    self.fail("Why am I here?")
            self.assertEqual(nestedcontext.inject('abc'), "def")

        with self.assertRaises(KeyError):
            nestedcontext.inject('abc')


if __name__ == '__main__':
    unittest.main()
