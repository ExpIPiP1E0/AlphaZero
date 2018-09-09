#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class dotdict(dict):
    def __getattr__(self,name):
        return self[name]

