# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Christopher Lenz
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import random
import sys
from couchdb import client

class TempDatabaseMixin(object):

    temp_dbs = None
    _db = None

    def setUp(self):
        self.server = client.Server(full_commit=False)

    def tearDown(self):
        if self.temp_dbs:
            for name in self.temp_dbs:
                self.server.delete(name)

    def temp_db(self):
        if self.temp_dbs is None:
            self.temp_dbs = {}
        # Find an unused database name
        while True:
            name = 'couchdb-python/%d' % random.randint(0, sys.maxint)
            if name not in self.temp_dbs:
                break
        db = self.server.create(name)
        self.temp_dbs[name] = db
        return name, db

    def del_db(self, name):
        del self.temp_dbs[name]
        self.server.delete(name)

    @property
    def db(self):
        if self._db is None:
            name, self._db = self.temp_db()
        return self._db
