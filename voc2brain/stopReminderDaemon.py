#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,signal
from lockfile.pidlockfile import PIDLockFile

pidlock = PIDLockFile('/tmp/foo.pid')
pid = pidlock.read_pid()
os.kill(pid,signal.SIGTERM)
