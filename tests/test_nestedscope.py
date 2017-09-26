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
        with nestedcontext.nestedcontext(abc="def"):
            self.assertEqual(nestedcontext.lookup('abc'), "def")

        with self.assertRaises(KeyError):
            nestedcontext.lookup('abc')

    def test_context_names(self):
        with nestedcontext.nestedcontext(abc="def"):
            self.assertEqual(nestedcontext.lookup('abc'), "def")
            with nestedcontext.nestedcontext(abc="ghi", stackname="otherstack"):
                self.assertEqual(nestedcontext.lookup('abc'), "def")
                self.assertEqual(nestedcontext.lookup('abc', stackname="otherstack"), "ghi")

        with self.assertRaises(KeyError):
            nestedcontext.lookup('abc')
        with self.assertRaises(KeyError):
            nestedcontext.lookup('abc', stackname="otherstack")

    def test_nestedcontext(self):
        with nestedcontext.nestedcontext(abc="def"):
            self.assertEqual(nestedcontext.lookup('abc'), "def")
            with nestedcontext.nestedcontext(abc="ghi"):
                self.assertEqual(nestedcontext.lookup('abc'), "ghi")

        with self.assertRaises(KeyError):
            nestedcontext.lookup('abc')

    def test_nestedcontext_detect_conflicts(self):
        with nestedcontext.nestedcontext(abc="def"):
            self.assertEqual(nestedcontext.lookup('abc'), "def")
            with self.assertRaises(ValueError):
                with nestedcontext.nestedcontext(abc="ghi", conflicts_are_errors=True):
                    self.fail("Why am I here?")
            self.assertEqual(nestedcontext.lookup('abc'), "def")

        with self.assertRaises(KeyError):
            nestedcontext.lookup('abc')


if __name__ == '__main__':
    unittest.main()
