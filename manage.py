#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-09 12:57:35
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-20 19:46:24
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from app import create_app
from flask_script import Manager


config_name = os.getenv("FLASK_CONFIG", 'default')

app = create_app(config_name)

manager = Manager(app)


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover(tests)
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

