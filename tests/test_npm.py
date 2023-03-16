#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) The python-semanticversion project
# This code is distributed under the two-clause BSD License.

"""Test NPM-style specifications."""

import sys
import unittest

from semantic_version import base


class NpmSpecTests(unittest.TestCase):
    if sys.version_info[0] <= 2:
        import contextlib

        @contextlib.contextmanager
        def subTest(self, **kwargs):
            yield

    examples = {
        # range: [matchings], [failings]
        '>=1.2.7': (
            ['1.2.7', '1.2.8', '1.3.9'],
            ['1.2.6', '1.1.0'],
        ),
        '>=1.2.7 <1.3.0': (
            ['1.2.7', '1.2.8', '1.2.99'],
            ['1.2.6', '1.3.0', '1.1.0'],
        ),
        '1.2.7 || >=1.2.9 <2.0.0': (
            ['1.2.7', '1.2.9', '1.4.6'],
            ['1.2.8', '2.0.0'],
        ),
        '>1.2.3-alpha.3': (
            ['1.2.3-alpha.7', '3.4.5'],
            ['1.2.3-alpha.3', '3.4.5-alpha.9'],
        ),
        '>=1.2.3-alpha.3': (
            ['1.2.3-alpha.3', '1.2.3-alpha.7', '3.4.5'],
            ['1.2.3-alpha.2', '3.4.5-alpha.9'],
        ),
        '>1.2.3-alpha <1.2.3-beta': (
            ['1.2.3-alpha.0', '1.2.3-alpha.1'],
            ['1.2.3', '1.2.3-beta.0', '1.2.3-bravo'],
        ),
        '1.2.3 - 2.3.4': (
            ['1.2.3', '1.2.99', '2.2.0', '2.3.4', '2.3.4+b42'],
            ['1.2.0', '1.2.3-alpha.1', '2.3.5'],
        ),
        '~1.2.3-beta.2': (
            ['1.2.3-beta.2', '1.2.3-beta.4', '1.2.4'],
            ['1.2.4-beta.2', '1.3.0'],
        ),
        '<2020-09-14': (
            ['2020-09-13', '2020-08-14', '2019-09-14'],
            ['2020-09-14', '2022-09-14'],
        ),
        '<1.2.3.4': (  # minor issue here, 1.2.3.5 is bigger, but considered a prerelease
            ['1.2.3.0', '1.2.3.4', '1.2.3.4-beta', '1.2.3.5'],
            ['1.2.4.0'],
        ),
        '<1.2.3a4': (
            ['1.2.2', '1.2.3a3', '1.2.3a4'],
            ['1.2.3', '1.3.4'],
        ),
    }

    def test_spec(self):
        for spec, lists in self.examples.items():
            matching, failing = lists
            for version in matching:
                with self.subTest(spec=spec, version=version):
                    self.assertIn(base.Version(version), base.NpmSpec(spec))
            for version in failing:
                with self.subTest(spec=spec, version=version):
                    self.assertNotIn(base.Version(version), base.NpmSpec(spec))

    expansions = {
        # Basic
        '>1.2.3': '>1.2.3',
        '<1.2.3': '<1.2.3',
        '<=1.2.3': '<=1.2.3',
        '>=19.04.0': '>=19.4.0',
        '>01.02.03': '>1.2.3',
        '>1.0003.3': '>1.3.3',


        # Hyphen ranges
        '1.2.3 - 2.3.4': '>=1.2.3 <=2.3.4',
        '1.2 - 2.3.4': '>=1.2.0 <=2.3.4',
        '1.2.3 - 2.3': '>=1.2.3 <2.4.0',
        '1.2.3 - 2': '>=1.2.3 <3',
        '1.2.3    - 2': '>=1.2.3 <3',

        # X-Ranges
        '*': '>=0.0.0',
        '>=*': '>=0.0.0',
        '1.x': '>=1.0.0 <2.0.0',
        '1.2.x': '>=1.2.0 <1.3.0',
        '': '*',
        'x': '*',
        '1': '1.x.x',
        '1.x.x': '>=1.0.0 <2.0.0',
        '1.2': '1.2.x',

        # Partial GT LT Ranges
        '>=1': '>=1.0.0',
        '>1': '>=2.0.0',
        '>1.2': '>=1.3.0',
        '<1': '<1.0.0',

        # Tilde ranges
        '~1.2.3': '>=1.2.3 <1.3.0',
        '~1.2': '>=1.2.0 <1.3.0',
        '~1': '>=1.0.0 <2.0.0',
        '~0.2.3': '>=0.2.3 <0.3.0',
        '~0.2': '>=0.2.0 <0.3.0',
        '~0': '>=0.0.0 <1.0.0',
        '~1.2.3-beta.2': '>=1.2.3-beta.2 <1.3.0',
        '~ 1.2.3': '>=1.2.3 <1.3.0',
        '~    1.2.3': '>=1.2.3 <1.3.0',
        '~>1.2.3': '>=1.2.3 <1.3.0',
        '~> 1.2.3': '>=1.2.3 <1.3.0',

        # Caret ranges
        '^1.2.3': '>=1.2.3 <2.0.0',
        '^0.2.3': '>=0.2.3 <0.3.0',
        '^0.0.3': '>=0.0.3 <0.0.4',
        '^1.2.3-beta.2': '>=1.2.3-beta.2 <2.0.0',
        '^0.0.3-beta': '>=0.0.3-beta <0.0.4',
        '^1.2.x': '>=1.2.0 <2.0.0',
        '^0.0.x': '>=0.0.0 <0.1.0',
        '^0.0': '>=0.0.0 <0.1.0',
        '^1.x': '>=1.0.0 <2.0.0',
        '^0.x': '>=0.0.0 <1.0.0',
        '^0': '>=0.0.0 <1.0.0',
        '^ 1.2.3': '>=1.2.3 <2.0.0',
        '^   1.2.3': '>=1.2.3 <2.0.0',

        # Weird whitespace ranges
        '>= 1.2.3': '>=1.2.3',
        '>=\t1.2.3': '>=1.2.3',
        '>=   1.2.3': '>=1.2.3',
        '>=1.2.3      <2.0.0': '>=1.2.3 <2.0.0',
        '   >=1.2.4 <2.0.0    ': '>=1.2.4 <2.0.0',
        '>= 1.2.3 <  2.0.0': '>=1.2.3 <2.0.0',
        '>=1.2.3 < 2.0.0': '>=1.2.3 <2.0.0',
        '>= 1.2.3 < 2.0.0': '>=1.2.3 <2.0.0',
        '>=  1.2.3 <    2.0.0': '>=1.2.3 <2.0.0',
        '   >=1.2.3 <2.0.0    ': '>=1.2.3 <2.0.0',
        '1.2.7 ||    >=1.2.9 <2.0.0': '1.2.7 || >=1.2.9 <2.0.0',
        '1.2.7 ||    >= 1.2.9 < 2.0.0': '1.2.7 || >=1.2.9 <2.0.0',

        # With v prefix
        '^v1.2.3': '^1.2.3',
        'v1.2.3 || ^v3.4.5': '1.2.3 || ^3.4.5',
        '>=v1.2.3 || <=v3.4.5': '>=1.2.3 || <=3.4.5',

        # With dashes instead of points
        '1-2-3': '1.2.3',
        '<2020-09-14': '<2020.9.14',
        '>2020-09-14-beta3': '>2020.9.14-beta3',

        # Overlong strings
        '<2.0.8.1': '<2.0.8.1',

        # Direct attached prereleases
        '<1.2.3a2': '<1.2.3-a2',

    }

    def test_expand(self):
        for source, expanded in self.expansions.items():
            with self.subTest(source=source):
                self.assertEqual(
                    base.NpmSpec(source).clause,
                    base.NpmSpec(expanded).clause,
                )

    equivalent_npmspecs = {
        '||': '*',
        # '>1.2.3 || *': '*',
        # '>=1.2.1 <=2.3.4': '>1.2.0 <2.3.5',
    }

    def test_equivalent(self):
        # like expand, but we also simplify both sides
        # NOTE: some specs can be equivalent but don't
        # currently simplify to the same clauses
        for left, right in self.equivalent_npmspecs.items():
            with self.subTest(l=left, r=right):
                self.assertEqual(
                    base.NpmSpec(left).clause.simplify(),
                    base.NpmSpec(right).clause.simplify(),
                )

    invalid_npmspecs = [
        '==0.1.2',
        '>>0.1.2',
        '> = 0.1.2',
        '<=>0.1.2',
        # '~1.2.3beta',
        '~=1.2.3',
        '!0.1.2',
        '!=0.1.2',
        '>1.00004.3',
        '<1a.2.3',
        '<1.2a.3',
    ]

    def test_invalid(self):
        for invalid in self.invalid_npmspecs:
            with self.subTest(spec=invalid):
                with self.assertRaises(ValueError, msg="NpmSpec(%r) should be invalid" % invalid):
                    base.NpmSpec(invalid)
