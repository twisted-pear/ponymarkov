#!/usr/bin/env python2

class ProviderI:
    def get_lines(self):
        raise NotImplementedError("Please implement this yourself.")

class AnyProvider(ProviderI):
    def __init__(self, providers):
	self.__providers = providers;

    def get_lines(self):
        for prov in self.__providers:
            lines = prov.get_lines()
            if (lines):
                return lines

        return list()

class AllProviders(ProviderI):
    def __init__(self, providers):
	self.__providers = providers;

    def get_lines(self):
        lines = list()
        for prov in self.__providers:
            lines.extend(prov.get_lines())

        return lines
