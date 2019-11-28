# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.



import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.gen
import os
import subprocess
import commands


from tornado.options import define, options
define('port', default=7777, help='run on the given port', type=int)


class Handler(tornado.web.RequestHandler):
        def option(self):
                self.set_header('Access-Control-Allow-Origin: *')
                self.set_header('Access-Control-Allow-Methods: GET')
                self.write("ok")

        def get(self):
                git_rev = self.get_argument("git_rev", default = None)
                vendor = self.get_argument("vendor", default = None)
                self.set_header('Access-Control-Allow-Origin', "*")
                self.set_header('Access-Control-Allow-Methods', "GET")
                if not(git_rev and vendor):
                        self.write("")
                else:
                        try:
                                repo = {
                                        "V8": "/home/user/work/repos/v8/base/v8",
                                        "JerryScript": "/home/user/work/repos/jerryscript",
                                        "Chromium": "/home/user/work/repos/chrome/arm/chromium/src",
                                        "JavaScriptCore": "/home/user/work/repos/jsc/base/webkit",
                                }
                                cmd = "cd %s && git log -1 %s" % (repo[vendor], git_rev)
                                print cmd
                                try:
                                   status, o = commands.getstatusoutput(cmd)
                                except Exception as e:
                                   print e
                                o = o.decode("utf-8")
                                self.write(o)
                        except Exception,e:
                                self.write(str(e))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
             (r'/',Handler),
            ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            # template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            # static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
