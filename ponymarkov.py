#!/usr/bin/env python2

from __future__ import print_function
import sys

from generators.line_generator import LineGenerator
from providers.mlpwikia_provider import MLPWikiaProvider

if __name__ == "__main__":
    character = sys.argv[1]

    provider = MLPWikiaProvider([character])
    generator = LineGenerator(provider)

    content = generator.generate()

    for c in content:
        if c.endswith('\n'):
            print(c, end='')
        else:
            print(c, end=' ')
    print()
