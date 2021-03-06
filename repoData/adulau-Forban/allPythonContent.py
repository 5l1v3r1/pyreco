__FILENAME__ = forban_announce
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2012 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time
import os
import logging
import logging.handlers
import ConfigParser

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))

try:
    forbanpath = config.get('global','path')
except ConfigParser.Error:
    forbanpath = os.path.join(guesspath())

try:
    announceinterval = config.getint('global','announceinterval')
except ConfigParser.Error:
    announceinterval = 10

try:
    indexrebuild = config.getint('global','indexrebuild')
except ConfigParser.Error:
    indexrebuild = 1

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.Error:
    forbanshareroot = os.path.join(forbanpath,"var","share/")

try:
    forbanlogginglevel = config.get('global','logging')
except ConfigParser.Error:
    forbanlogginglevel = "INFO"

try:
    forbanloggingsize = config.get('global','loggingmaxsize')
except ConfigParser.Error:
    forbanloggingsize = 100000


announceinterval = float(announceinterval)
forbanpathlib=os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)

import announce
import index
import tools

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=forbanpathlog+"/forban_announce.log"
flogger = logging.getLogger('forban_announce')

if forbanlogginglevel == "INFO":
    flogger.setLevel(logging.INFO)
else:
    flogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(forbanpathlogfile, backupCount=5, maxBytes = forbanloggingsize)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
flogger.addHandler(handler)

if __name__ == "__main__":

    try:
        forbanname = config.get('global','name')
    except ConfigParser.Error:
        forbanname = tools.guesshostname()

    try:
        ipv6_disabled =  config.get('global' , 'disabled_ipv6')
	flogger.debug ( "Read ipv6_disabled")
    except  ConfigParser.Error:
        ipv6_disabled = 0

    msg = announce.message(name=forbanname, dynpath=os.path.join(forbanpath,"var"))

    if  ipv6_disabled == "1":
        flogger.info("forban_announce without ipv6")
        msg.disableIpv6()

    try:
        destination =  config.get('global' , 'destination')
        flogger.debug( "Read custom destinations: >"+ destination + "< ")
        msg.setDestination( eval ( destination ) )
    except  ConfigParser.Error:
        msg.setDestination()

    forbanindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
    flogger.info("forban_announce starting...")

    announce.flogger = flogger

forbansharebundle = os.path.join(forbanshareroot,"forban")

# bundle directory includes static pages but also index from the
# Forban itself.

if not os.path.exists(forbansharebundle):
    os.mkdir(forbansharebundle)

intervalcounter = 1
while 1:
    # rebuild forban index (at startup always rebuild)
    if intervalcounter <= 1:
        forbanindex.build()
        intervalcounter = indexrebuild
        flogger.debug("Index rebuilt")
    msg.gen()
    msg.auth(value=forbanindex.gethmac())
    flogger.debug(msg.get())
    msg.send()
    intervalcounter = intervalcounter - 1
    time.sleep(announceinterval)

########NEW FILE########
__FILENAME__ = forban_discover
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import ConfigParser

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))

try:
    disable_ipv6 =  config.get('global','disabled_ipv6')
except ConfigParser.NoOptionError:
    disable_ipv6 = 0
except ConfigParser.NoSectionError:
    disable_ipv6 = 0

try:
    forbanpath = config.get('global','path')
except ConfigParser.NoSectionError:
    print "Forban config file is missing or incorrect"
    print "You should go into ../cfg/ and cp forban.cfg-sample forban.cfg"
    print "In any case, Forban should be able to work even without the config file"
    forbanpath = os.path.join(guesspath())
except ConfigParser.NoOptionError:
    forbanpath = os.path.join(guesspath())

forbanpathlib = os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)

import discover


if __name__ == "__main__":

    while 1:
        HOST, PORT = ("", 12555)
        server = discover.UDPServer((HOST, PORT), discover.MyUDPHandler)
	if disable_ipv6 == "1":
              server.setIPv6 ( 0 )
	else:
              server.setIPv6 ( 1 )
        server.serve_forever()


########NEW FILE########
__FILENAME__ = forban_opportunistic
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import os.path
import sys
import string
import time
import ConfigParser
import re
import logging
import logging.handlers

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))


try:
    forbanpath = config.get('global','path')
except ConfigParser.Error:
    forbanpath = os.path.join(guesspath())

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.Error:
    forbanshareroot = os.path.join(forbanpath,"var","share/")
except ConfigParser.NoOptionError:
    forbanpath = os.path.join(guesspath())
    forbanshareroot = os.path.join(forbanpath,"var","share/")

forbanpathlib = os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)
import index
import loot
import fetch
import base64e

try:
    forbanmode = config.get('global','mode')
except ConfigParser.Error:
    forbanmode = "opportunistic"

if not forbanmode == "opportunistic":
    print "not configured in opportunistic mode"
    exit(1)


try:
    announceinterval = config.get('global','announceinterval')
except ConfigParser.Error:
    announceinterval = 10

announceinterval = float(announceinterval)

try:
    forbanlogginglevel = config.get('global','logging')
except ConfigParser.Error:
    forbanlogginglevel = "INFO"

try:
    forbanloggingsize = config.get('global','loggingmaxsize')
except ConfigParser.Error:
    forbanloggingsize = 100000

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=os.path.join(forbanpathlog,"forban_opportunistic.log")

flogger = logging.getLogger('forban_opportunistic')

if forbanlogginglevel == "INFO":
    flogger.setLevel(logging.INFO)
else:
    flogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(forbanpathlogfile, backupCount=5, maxBytes = forbanloggingsize)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
flogger.addHandler(handler)

try:
    ofilter = config.get('opportunistic','filter')
except ConfigParser.Error:
    ofilter = ""

try:
    efilter = config.get('opportunistic','efilter')
except ConfigParser.Error:
    efilter = None

refilter = re.compile(ofilter, re.I)
if efilter is not None:
    exfilter = re.compile(efilter, re.I)
else:
    exfilter = re.compile("", re.I)

try:
    maxsize = config.get('opportunistic','maxsize')
except ConfigParser.Error:
    maxsize = 0

discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
allindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
allindex.build()

flogger.info("forban_opportunistic starting...")
flogger.info("applied including regexp filter: %s" % ofilter)
flogger.info("applied excluding regexp filter: %s" % efilter)
while(1):

    for uuid in discoveredloot.listall():

        # check if my loot is not exceeding the maxsize
        mysize = allindex.totalfilesize(discoveredloot.whoami())
        if float(maxsize) != 0:
            if mysize is False:
                continue
            if float(mysize[:-2])>float(maxsize):
                flogger.info("maxsize exceeded (current:%s - max:%sGB)" % (mysize, maxsize))
                continue
        # fetch the index of all discovered and recently announced loots
        # allowing to compare local loot to announced loot
        if discoveredloot.exist(uuid) and discoveredloot.lastannounced(uuid):
            allindex.cache(uuid)

        if not discoveredloot.lastannounced(uuid):
            flogger.info("%s (%s) not seen recently, skipped" % (discoveredloot.getname(uuid),(uuid)))
            continue

        missingfiles = allindex.howfar(uuid)

        if (discoveredloot.whoami() == uuid):
            flogger.debug("we are not opportunistic on ourself %s (%s)" % (discoveredloot.getname(uuid),uuid))
        elif not missingfiles:
            flogger.info("missing no files with %s (%s)" % (discoveredloot.getname(uuid),uuid))
        else:
            for missedfile in missingfiles:
                if re.search(refilter, missedfile) and not (re.search(exfilter, missedfile) and efilter is not None):
                    sourcev4 = discoveredloot.getipv4(uuid)
                    url =  """http://%s:12555/s/?g=%s&f=b64e""" % (sourcev4, base64e.encode(missedfile))
                    localfile = forbanshareroot + "/" + missedfile
                    localsize = allindex.getfilesize(filename=missedfile)
                    remotesize = allindex.getfilesize(filename=missedfile,uuid=uuid)
                    if localsize < remotesize:
                        flogger.info("local file smaller - from %s fetching %s to be saved in %s" % (uuid,url,localfile))
                        fetch.urlget(url,localfile)
                    elif localsize is False:
                        flogger.info("local file not existing - from %s fetching %s to be saved in %s" % (uuid,url,localfile))
                        fetch.urlget(url,localfile)
                    elif remotesize is False:
                        flogger.info("remote file index issue for %s on loot %s" % (missedfile, uuid))
                    else:
                        flogger.info("local file larger or corrupt %s - don't fetch it" % (localfile))
                    allindex.build()

    time.sleep(announceinterval*(announceinterval/(announceinterval-2)))


########NEW FILE########
__FILENAME__ = forban_opportunistic_fs
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2011 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import os.path
import sys
import string
import time
import ConfigParser
import re
import logging
import logging.handlers

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))


try:
    forbanpath = config.get('global','path')
except ConfigParser.Error:
    forbanpath = os.path.join(guesspath())

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.Error:
    forbanshareroot = os.path.join(forbanpath,"var","share/")
except ConfigParser.NoOptionError:
    forbanpath = os.path.join(guesspath())
    forbanshareroot = os.path.join(forbanpath,"var","share/")

forbanpathlib = os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)
import index
import loot
import fetch
import base64e

try:
    forbanmode = config.get('global','mode')
except ConfigParser.Error:
    forbanmode = "opportunistic"


try:
    forbanlogginglevel = config.get('global','logging')
except ConfigParser.Error:
    forbanlogginglevel = "INFO"

try:
    forbanloggingsize = config.get('global','loggingmaxsize')
except ConfigParser.Error:
    forbanloggingsize = 100000

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=os.path.join(forbanpathlog,"forban_opportunistic_fs.log")

flogger = logging.getLogger('forban_opportunistic_fs')

if forbanlogginglevel == "INFO":
    flogger.setLevel(logging.INFO)
else:
    flogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(forbanpathlogfile, backupCount=5, maxBytes = forbanloggingsize)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
flogger.addHandler(handler)

try:
    forbanopportunisticfsdir = config.get('opportunistic_fs','directory')
except ConfigParser.Error:
    flogger.info("not started / no configuration present")
    exit(1)

if forbanopportunisticfsdir == "":
    flogger.info("not started - directory not set")
    exit(1)

flogger.info("starting using input/output directory %s",forbanopportunisticfsdir)
flogger.info("using mode %s",forbanmode)

########NEW FILE########
__FILENAME__ = forban_share
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import os.path
import sys
import string
import ConfigParser
import socket
import re

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))

try:
    forbanpath = config.get('global','path')
except ConfigParser.Error:
    forbanpath = os.path.join(guesspath())

forbandiscoveredloots = os.path.join(forbanpath,"var","loot")

try:
    forbanmode = config.get('global','mode')
except ConfigParser.Error:
    forbanmode = "opportunistic"

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.Error:
    forbanshareroot = os.path.join(forbanpath,"var","share/")


try:
    disable_ipv6 = config.get('global' , 'ipv6_disabled')
except ConfigParser.Error:
    disable_ipv6 = "0"

forbanpathlib = os.path.join (forbanpath,"lib")
sys.path.append(forbanpathlib)

import index
import loot
import base64e
import tools

try:
    forbanname = config.get('global','name')
except ConfigParser.Error:
    forbanname = tools.guesshostname()

try:
    import cherrypy
    from cherrypy.lib.static import serve_file
except ImportError:
    libexternal = os.path.join(forbanpath,"lib","ext")
    sys.path.append(libexternal)
    import cherrypy
    from cherrypy.lib.static import serve_file

import mimetypes

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=os.path.join(forbanpathlog,"forban_share_access.log")
forbanpathlogfilee=os.path.join(forbanpathlog,"forban_share_error.log")

if socket.has_ipv6 and disable_ipv6 == "0" :
    try:
        socktest = socket.socket(socket.AF_INET6)
        bindhost = "::"
        socktest.close()
    except:
        bindhost = "0.0.0.0"
else:
    bindhost = "0.0.0.0"

cherrypy.config.update({ 'log.screen': False, 'server.socket_port': 12555 , 'server.socket_host': bindhost, 'tools.static.root':forbanshareroot, 'log.access_file':forbanpathlogfile, 'log.error_file':forbanpathlogfilee, 'request.show_tracebacks': False})

forbanpathcherry = { '/css/style.css': {'tools.staticfile.on': True,
'tools.staticfile.filename':os.path.join(forbanshareroot,'forban/css/x.css')},
               '/img/forban-small.png': {'tools.staticfile.on': True,
               'tools.staticfile.filename':os.path.join(forbanshareroot,'forban/img/forban-small.png')}
             }

htmlheader = """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
lang="en"> <head> <link rel="stylesheet" type="text/css" href="/css/style.css"
/> </head>"""

htmlfooter =  """<div id="w3c"><p><small>Forban is free software released under
the <a href="http://www.gnu.org/licenses/agpl.html">AGPL</a>. For more information about Forban and source code : <a
href="http://www.foo.be/forban/">foo.be/forban/</a>.</small></p></div></div><!--
end wrapper --></div></body></html>"""

htmlnav = """ <body><div id="nav"><a href="/"><img src="/img/forban-small.png" alt="forban
logo : a small island where a stream of bits is going to and coming from"
/></a><br /><ul><li><span class="home">Description : <i>%s</i><br/>Mode : <i>%s</i></span></li>
</ul></div><div id="wrapper">
""" % (forbanname, forbanmode)

def mime_type(filename):
    if re.search('/forban/index',filename):
        return 'text/plain'
    else:
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def forban_geturl(uuid=None, filename=None, protocol="v4"):

    if uuid is None or filename is None:
        return False

    discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))

    if not discoveredloot.exist(uuid):
        return False

    if protocol == "v4":
        ip = discoveredloot.getipv4(uuid)
    else:
        ip = discoveredloot.getipv6(uuid)

    if protocol == "v4":
        url = "http://%s:12555/s/?g=%s&f=b64e" % (ip,base64e.encode(filename))
    else:
        url = "http://[%s]:12555/s/?g=%s&f=b64e" % (ip,base64e.encode(filename))

    return url

class Root:
    def index(self, directory=forbanshareroot):
        html = htmlheader
        html += htmlnav
        html += """<br/> <br/> <br/> <div class="right inner">"""
        html += """ <h2>Search the loot...</h2> """
        html += """ <form method=get action="q/"><input type="text" name="v" value=""> <input
        type="submit" value="search"></form> """
        html += """</div> <div class="left inner">"""
        html += """ <h2>Discovered link-local Forban available with their loot in the last 3 minutes</h2> """
        html += "<table>"
        html += "<th><td>Access</td><td>Name</td><td>Last seen</td><td>Size</td><td>How many files are missing from yourself?</td><td></td></th>"
        discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        mysourcev4 = discoveredloot.getipv4(discoveredloot.whoami())
        allindex =  index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        for name in discoveredloot.listall():
            if (discoveredloot.exist(name) and discoveredloot.lastannounced(name)):
                allindex.cache(name)
            if discoveredloot.lastannounced(name):
                html += "<tr>"
                rname = discoveredloot.getname(name)
                sourcev4 = discoveredloot.getipv4(name)
                if sourcev4 is not None:
                    html += """<td><a href="http://%s:12555/">v4</a></td> """ % sourcev4
                else:
                    html += """<td></td>"""
                sourcev6 = discoveredloot.getipv6(name)
            
                if sourcev6 is not None:
                    html += """<td><a href="http://[%s]:12555/">v6</a></td> """ % sourcev6
                else:
                    html += """<td></td>"""

                html += "<td>"+rname+"</td>"

                lastseen = discoveredloot.lastannounced(name)

                if lastseen is not None:
                    html += """<td>%s secs ago</td>""" % lastseen
                else:
                    html += "<td>never seen</td>"
                missingfiles = allindex.howfar(name)

                totalsize = allindex.totalfilesize(name)
                html +="<td>%s</td>" % str(totalsize)

                if type(missingfiles) is bool:
                    html += "<td><b>Missing index</b> from this loot"
                elif missingfiles is not None:
                    html += "<td>Missing %s files from this loot" % len(missingfiles)
                else:
                    html += "<td>Missing no files from this loot"

                if name != discoveredloot.whoami():
                    html += """ <a href="http://%s:12555/v/%s">[missing?]</a> """ % (mysourcev4,name)
                    html += """ <a href="http://%s:12555/l/%s">[browse]</a> """ % (mysourcev4,name)
                if name == discoveredloot.whoami():
                    html += """ <a href="/l/%s">[browse]</a> """ % (name)
                    html += "<td><i>yourself</i></td>"
                else:
                    html += "<td></td>"
                html += "</tr>"

        html += "</table></div>"
        html += htmlfooter
        return html
    
    def q(self, v=None, r=None):
        querystring = v
        mindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        searchresult = []
        for name in discoveredloot.listall():
            if (discoveredloot.exist(name) and discoveredloot.lastannounced(name)):
               fileavailable = mindex.search( uuid=name, query=querystring)
               for filefound in fileavailable:
                   searchresult.append((filefound,name))
        searchresult.sort()
        html = htmlheader
        html += "<title>search results of %s</title>" % (querystring)
        if r is not None:
            html += """<meta http-equiv="refresh" content="%s">""" % (r)
        html += "</head>"
        html += htmlnav
        html += """<br/> <br/> <div class="left inner">"""
        previousfile = None
        html += "<table><tr><th>Filename</th><th>Available on</th></tr>"
        for foundfiles in searchresult:

            if foundfiles[0] == previousfile:
                html += """<a href="%s">%s</a> """ % (forban_geturl(uuid=foundfiles[1],filename=filename),discoveredloot.getname(foundfiles[1]))
            elif previousfile == None:
                filename = foundfiles[0].rsplit(",",1)[0]
                html += """<td>%s</td> <td><a href="%s">%s</a> """ % (foundfiles[0].rsplit(",",1)[0],forban_geturl(uuid=foundfiles[1],filename=filename),discoveredloot.getname(foundfiles[1]))
            else:
                filename = foundfiles[0].rsplit(",",1)[0]
                html += """</td></tr><td>%s</td> <td><a href="%s">%s</a> """ % (foundfiles[0].rsplit(",",1)[0],forban_geturl(uuid=foundfiles[1],filename=filename),discoveredloot.getname(foundfiles[1]))

            previousfile=foundfiles[0]
        html += "</td></tr></table></div>"
        return html

    def v(self, uuid):
        mindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        dloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        missingfiles = mindex.howfar(uuid)
        html = htmlheader
        html += """<br/> <br/> <br/> <div class="left inner"> <h2>Missing files on your loot from %s </h2>""" % dloot.getname(uuid)
        html += htmlnav
        html += "<table>"

        if missingfiles is None:

                html += "You are not missing any files with %s " % dloot.getname(uuid)
        else:

            for filemissed in missingfiles:
                html += "<tr>"
                sourcev4 = dloot.getipv4(uuid)
                sourcev6 = dloot.getipv6(uuid)
                html += """<td>%s</td><td><a
                href="http://%s:12555/s/?g=%s&f=b64e">v4</a></td> """ % (filemissed,sourcev4,base64e.encode(filemissed))
                if sourcev6 is not None:
                    html += """<td><a href="http://[%s]:12555/s/?g=%s&f=b64e">v6</a></td>""" % (sourcev6, base64e.encode(filemissed))
                html += "</tr>"

        html += "</table>"
        html += htmlfooter
        return html

    def l(self, uuid):
        mindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        dloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        html = htmlheader

        html += """<br/> <br/> <br /> <div class="left inner"> <h2>Files available in loot %s </h2>""" % dloot.getname(uuid)
        html += htmlnav
        html += "<table>"
        html += "<tr><td>Filename</td><td>Fetch</td></tr>"
        tempindex = mindex.search("^((?!forban).)*$", uuid)
        tempindex.sort(key=string.lower)
        for fileinindex in tempindex:
            filei = fileinindex.rsplit(",",1)[0]
            if re.search('/\.',filei):
                continue
            if re.search('^\+\.',filei):
                continue
            html += "<tr>"
            sourcev4 = dloot.getipv4(uuid)
            sourcev6 = dloot.getipv6(uuid)
            size = tools.convertbytes(mindex.getfilesize(filename=filei,uuid=uuid))
            html += """<td>%s (%s)</td><td><a href="/s/?g=%s&f=b64e">get</a></td> """ % (filei,size,base64e.encode(filei))
            html += "</tr>"

        html += "</table>"
        html += htmlfooter
        return html

    index.exposed = True
    q.exposed = True
    v.exposed = True
    l.exposed = True

class Download:
    def index(self, g=None, f=None):
        if f is not None:
            g = base64e.decode(g)
        gs = string.replace(g, "..", "")
        gs = forbanshareroot + gs
        mimetypeguessed = mime_type(gs)
        return serve_file(gs, content_type=mimetypeguessed,disposition=True, name=os.path.basename(gs))

    index.exposed = True


if __name__ == '__main__':
    
    root = Root()
    favicon_path = os.path.join(forbanshareroot, "forban", "img", "forban-favicon.png")
    root.favicon_ico = cherrypy.tools.staticfile.handler(filename=favicon_path)
    root.s = Download()
    cherrypy.quickstart(root, config=forbanpathcherry)


########NEW FILE########
__FILENAME__ = announce
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2012 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socket
import string
import time
import datetime
try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1
import hmac
import re
import sys


flogger = None

# forban internal junk
sys.path.append('.')
import fid

debug = 0

class message:

    def __init__(self,name="notset", uuid=None, port="12555", timestamp=None,
    auth=None, destination=["ff02::1","255.255.255.255", ], dynpath="../var"):
            self.name       = name
            self.uuid       = uuid
            self.port       = port
            self.count      = 0
            self.destination = destination
            self.dynpath    = dynpath
            self.ipv6_disabled = 0

    def disableIpv6(self):
            self.ipv6_disabled = 1
            self.destination   = ["255.255.255.255", ]

    def setDestination(self, destination=["ff02::1","255.255.255.255", ] ):
             self.destination = destination

    def gen (self):
            self.payload    = "forban;name;" + self.name + ";"
            myid = fid.manage(dynpath=self.dynpath)
            self.payload    = self.payload + "uuid;" + myid.get()

    def auth(self,value=None):

        if value is None or value is False:
            self.payload = self.payload
        else:
            self.payload = self.payload + ";hmac;" + value

    def get (self):
            return self.payload

    def __debugMessage (self, msg ):
        if  flogger is not None:
            flogger.debug ( msg )
        elif debug == 1:
            print msg

    def __errorMessage (self, msg):
        if flogger is not None:
            flogger.error ( msg )
        elif debug == 1:
            print msg


    def send(self):
        for destination in self.destination:
            if socket.has_ipv6 and re.search(":", destination) and not  self.ipv6_disabled == 1:
               
		self.__debugMessage(  "working in ipv6 part on destination " + destination )

                # Even if Python is compiled with IPv6, it doesn't mean that the os
                # is supporting IPv6. (like the Nokia N900)
                try:
                    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                    # Required on some version of MacOS X while sending IPv6 UDP
                    # datagram
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
                except:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

            else:
                self.__debugMessage (  "open ipv4 socket on destination " + destination )
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            try:
                sock.sendto(self.payload, (destination, int(self.port)))
            except socket.error, msg:
                self.__errorMessage ( "Error sending to "+ destination + " : " + msg.strerror  )
                continue
        sock.close()



def managetest():
    msg = message()
    msg.gen()
    msg.auth()
    print msg.get()
    msg.send()
    msg.auth("forbankey")
    print msg.get()

if __name__ == "__main__":
    managetest()


########NEW FILE########
__FILENAME__ = base64e
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64

def encode( istring ):
    b64s = base64.urlsafe_b64encode(istring)
    b64s = b64s.replace("=","!")
    return b64s

def decode( istring ):
    istring = istring.replace("!","=")
    b64s = base64.urlsafe_b64decode(istring.encode("utf-8"))
    return b64s

if __name__ == "__main__":
    encodedone = encode("some string with")
    print encodedone
    decodedone = decode(encodedone)
    print decodedone

########NEW FILE########
__FILENAME__ = discover
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import SocketServer
import socket
import sys
import os
# forban internal junk
sys.path.append('.')
import loot

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

forbanpath = os.path.join(guesspath())

class MyUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        if data[:6] == "forban":
            myloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
            myloot.add(data, self.client_address[0])
        else:
            print "debug : not a forban message"

class UDPServer(SocketServer.UDPServer):
    
    def setIPv6 (self, ipv6 = 1 ):
        if  ipv6 == 0 :
            self.disable_ipv6 = 1
        else:
            self.disable_ipv6 = 0

    def useIPv6 (self ):
        return True

        if self.disable_ipv6 == 1 :
            return False
        else:
            return True


    if socket.has_ipv6 :
        try:
            socktest = socket.socket(socket.AF_INET6)
            socktest.close()
            address_family = socket.AF_INET6
        except:
            address_family = socket.AF_INET

    def server_bind(self):

        if self.useIPv6():

             self.v6success = True
             try:
                 socktest = socket.socket(socket.AF_INET6)
                 socktest.close()
             except:
                 self.v6success = False

             if socket.has_ipv6 and self.v6success:
                 address_family = socket.AF_INET6

             #allowing to work in dual-stack when IPv6 is used
             if socket.has_ipv6 and self.v6success:
                 self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
          
        self.socket.bind(self.server_address)

if __name__ == "__main__":

   HOST, PORT = ("::",12555)
   server = UDPServer((HOST, PORT), MyUDPHandler)
   server.serve_forever()


########NEW FILE########
__FILENAME__ = auth
import cherrypy
from cherrypy.lib import httpauth


def check_auth(users, encrypt=None, realm=None):
    """If an authorization header contains credentials, return True, else False."""
    request = cherrypy.serving.request
    if 'authorization' in request.headers:
        # make sure the provided credentials are correctly set
        ah = httpauth.parseAuthorization(request.headers['authorization'])
        if ah is None:
            raise cherrypy.HTTPError(400, 'Bad Request')
        
        if not encrypt:
            encrypt = httpauth.DIGEST_AUTH_ENCODERS[httpauth.MD5]
        
        if hasattr(users, '__call__'):
            try:
                # backward compatibility
                users = users() # expect it to return a dictionary
                
                if not isinstance(users, dict):
                    raise ValueError("Authentication users must be a dictionary")
                
                # fetch the user password
                password = users.get(ah["username"], None)
            except TypeError:
                # returns a password (encrypted or clear text)
                password = users(ah["username"])
        else:
            if not isinstance(users, dict):
                raise ValueError("Authentication users must be a dictionary")
            
            # fetch the user password
            password = users.get(ah["username"], None)
        
        # validate the authorization by re-computing it here
        # and compare it with what the user-agent provided
        if httpauth.checkResponse(ah, password, method=request.method,
                                  encrypt=encrypt, realm=realm):
            request.login = ah["username"]
            return True
        
        request.login = False
    return False

def basic_auth(realm, users, encrypt=None, debug=False):
    """If auth fails, raise 401 with a basic authentication header.
    
    realm
        A string containing the authentication realm.
        
    users
        A dict of the form: {username: password} or a callable returning a dict.
        
    encrypt
        callable used to encrypt the password returned from the user-agent.
        if None it defaults to a md5 encryption.
        
    """
    if check_auth(users, encrypt):
        if debug:
            cherrypy.log('Auth successful', 'TOOLS.BASIC_AUTH')
        return
    
    # inform the user-agent this path is protected
    cherrypy.serving.response.headers['www-authenticate'] = httpauth.basicAuth(realm)
    
    raise cherrypy.HTTPError(401, "You are not authorized to access that resource")

def digest_auth(realm, users, debug=False):
    """If auth fails, raise 401 with a digest authentication header.
    
    realm
        A string containing the authentication realm.
    users
        A dict of the form: {username: password} or a callable returning a dict.
    """
    if check_auth(users, realm=realm):
        if debug:
            cherrypy.log('Auth successful', 'TOOLS.DIGEST_AUTH')
        return
    
    # inform the user-agent this path is protected
    cherrypy.serving.response.headers['www-authenticate'] = httpauth.digestAuth(realm)
    
    raise cherrypy.HTTPError(401, "You are not authorized to access that resource")

########NEW FILE########
__FILENAME__ = auth_basic
# This file is part of CherryPy <http://www.cherrypy.org/>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab:fileencoding=utf-8

__doc__ = """This module provides a CherryPy 3.x tool which implements
the server-side of HTTP Basic Access Authentication, as described in :rfc:`2617`.

Example usage, using the built-in checkpassword_dict function which uses a dict
as the credentials store::

    userpassdict = {'bird' : 'bebop', 'ornette' : 'wayout'}
    checkpassword = cherrypy.lib.auth_basic.checkpassword_dict(userpassdict)
    basic_auth = {'tools.auth_basic.on': True,
                  'tools.auth_basic.realm': 'earth',
                  'tools.auth_basic.checkpassword': checkpassword,
    }
    app_config = { '/' : basic_auth }

"""

__author__ = 'visteya'
__date__ = 'April 2009'

import binascii
from cherrypy._cpcompat import base64_decode
import cherrypy


def checkpassword_dict(user_password_dict):
    """Returns a checkpassword function which checks credentials
    against a dictionary of the form: {username : password}.

    If you want a simple dictionary-based authentication scheme, use
    checkpassword_dict(my_credentials_dict) as the value for the
    checkpassword argument to basic_auth().
    """
    def checkpassword(realm, user, password):
        p = user_password_dict.get(user)
        return p and p == password or False

    return checkpassword


def basic_auth(realm, checkpassword, debug=False):
    """A CherryPy tool which hooks at before_handler to perform
    HTTP Basic Access Authentication, as specified in :rfc:`2617`.

    If the request has an 'authorization' header with a 'Basic' scheme, this
    tool attempts to authenticate the credentials supplied in that header.  If
    the request has no 'authorization' header, or if it does but the scheme is
    not 'Basic', or if authentication fails, the tool sends a 401 response with
    a 'WWW-Authenticate' Basic header.

    realm
        A string containing the authentication realm.

    checkpassword
        A callable which checks the authentication credentials.
        Its signature is checkpassword(realm, username, password). where
        username and password are the values obtained from the request's
        'authorization' header.  If authentication succeeds, checkpassword
        returns True, else it returns False.
    
    """
    
    if '"' in realm:
        raise ValueError('Realm cannot contain the " (quote) character.')
    request = cherrypy.serving.request
    
    auth_header = request.headers.get('authorization')
    if auth_header is not None:
        try:
            scheme, params = auth_header.split(' ', 1)
            if scheme.lower() == 'basic':
                username, password = base64_decode(params).split(':', 1)
                if checkpassword(realm, username, password):
                    if debug:
                        cherrypy.log('Auth succeeded', 'TOOLS.AUTH_BASIC')
                    request.login = username
                    return # successful authentication
        except (ValueError, binascii.Error): # split() error, base64.decodestring() error
            raise cherrypy.HTTPError(400, 'Bad Request')
    
    # Respond with 401 status and a WWW-Authenticate header
    cherrypy.serving.response.headers['www-authenticate'] = 'Basic realm="%s"' % realm
    raise cherrypy.HTTPError(401, "You are not authorized to access that resource")


########NEW FILE########
__FILENAME__ = auth_digest
# This file is part of CherryPy <http://www.cherrypy.org/>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab:fileencoding=utf-8

__doc__ = """An implementation of the server-side of HTTP Digest Access
Authentication, which is described in :rfc:`2617`.

Example usage, using the built-in get_ha1_dict_plain function which uses a dict
of plaintext passwords as the credentials store::

    userpassdict = {'alice' : '4x5istwelve'}
    get_ha1 = cherrypy.lib.auth_digest.get_ha1_dict_plain(userpassdict)
    digest_auth = {'tools.auth_digest.on': True,
                   'tools.auth_digest.realm': 'wonderland',
                   'tools.auth_digest.get_ha1': get_ha1,
                   'tools.auth_digest.key': 'a565c27146791cfb',
    }
    app_config = { '/' : digest_auth }
"""

__author__ = 'visteya'
__date__ = 'April 2009'


import time
from cherrypy._cpcompat import parse_http_list, parse_keqv_list

import cherrypy
from cherrypy._cpcompat import md5, ntob
md5_hex = lambda s: md5(ntob(s)).hexdigest()

qop_auth = 'auth'
qop_auth_int = 'auth-int'
valid_qops = (qop_auth, qop_auth_int)

valid_algorithms = ('MD5', 'MD5-sess')


def TRACE(msg):
    cherrypy.log(msg, context='TOOLS.AUTH_DIGEST')

# Three helper functions for users of the tool, providing three variants
# of get_ha1() functions for three different kinds of credential stores.
def get_ha1_dict_plain(user_password_dict):
    """Returns a get_ha1 function which obtains a plaintext password from a
    dictionary of the form: {username : password}.

    If you want a simple dictionary-based authentication scheme, with plaintext
    passwords, use get_ha1_dict_plain(my_userpass_dict) as the value for the
    get_ha1 argument to digest_auth().
    """
    def get_ha1(realm, username):
        password = user_password_dict.get(username)
        if password:
            return md5_hex('%s:%s:%s' % (username, realm, password))
        return None

    return get_ha1

def get_ha1_dict(user_ha1_dict):
    """Returns a get_ha1 function which obtains a HA1 password hash from a
    dictionary of the form: {username : HA1}.

    If you want a dictionary-based authentication scheme, but with
    pre-computed HA1 hashes instead of plain-text passwords, use
    get_ha1_dict(my_userha1_dict) as the value for the get_ha1
    argument to digest_auth().
    """
    def get_ha1(realm, username):
        return user_ha1_dict.get(user)

    return get_ha1

def get_ha1_file_htdigest(filename):
    """Returns a get_ha1 function which obtains a HA1 password hash from a
    flat file with lines of the same format as that produced by the Apache
    htdigest utility. For example, for realm 'wonderland', username 'alice',
    and password '4x5istwelve', the htdigest line would be::

        alice:wonderland:3238cdfe91a8b2ed8e39646921a02d4c

    If you want to use an Apache htdigest file as the credentials store,
    then use get_ha1_file_htdigest(my_htdigest_file) as the value for the
    get_ha1 argument to digest_auth().  It is recommended that the filename
    argument be an absolute path, to avoid problems.
    """
    def get_ha1(realm, username):
        result = None
        f = open(filename, 'r')
        for line in f:
            u, r, ha1 = line.rstrip().split(':')
            if u == username and r == realm:
                result = ha1
                break
        f.close()
        return result

    return get_ha1


def synthesize_nonce(s, key, timestamp=None):
    """Synthesize a nonce value which resists spoofing and can be checked for staleness.
    Returns a string suitable as the value for 'nonce' in the www-authenticate header.

    s
        A string related to the resource, such as the hostname of the server.

    key
        A secret string known only to the server.
    
    timestamp
        An integer seconds-since-the-epoch timestamp
    
    """
    if timestamp is None:
        timestamp = int(time.time())
    h = md5_hex('%s:%s:%s' % (timestamp, s, key))
    nonce = '%s:%s' % (timestamp, h)
    return nonce


def H(s):
    """The hash function H"""
    return md5_hex(s)


class HttpDigestAuthorization (object):
    """Class to parse a Digest Authorization header and perform re-calculation
    of the digest.
    """

    def errmsg(self, s):
        return 'Digest Authorization header: %s' % s

    def __init__(self, auth_header, http_method, debug=False):
        self.http_method = http_method
        self.debug = debug
        scheme, params  = auth_header.split(" ", 1)
        self.scheme = scheme.lower()
        if self.scheme != 'digest':
            raise ValueError('Authorization scheme is not "Digest"')

        self.auth_header = auth_header

        # make a dict of the params
        items = parse_http_list(params)
        paramsd = parse_keqv_list(items)

        self.realm = paramsd.get('realm')
        self.username = paramsd.get('username')
        self.nonce = paramsd.get('nonce')
        self.uri = paramsd.get('uri')
        self.method = paramsd.get('method')
        self.response = paramsd.get('response') # the response digest
        self.algorithm = paramsd.get('algorithm', 'MD5')
        self.cnonce = paramsd.get('cnonce')
        self.opaque = paramsd.get('opaque')
        self.qop = paramsd.get('qop') # qop
        self.nc = paramsd.get('nc') # nonce count

        # perform some correctness checks
        if self.algorithm not in valid_algorithms:
            raise ValueError(self.errmsg("Unsupported value for algorithm: '%s'" % self.algorithm))

        has_reqd = self.username and \
                   self.realm and \
                   self.nonce and \
                   self.uri and \
                   self.response
        if not has_reqd:
            raise ValueError(self.errmsg("Not all required parameters are present."))

        if self.qop:
            if self.qop not in valid_qops:
                raise ValueError(self.errmsg("Unsupported value for qop: '%s'" % self.qop))
            if not (self.cnonce and self.nc):
                raise ValueError(self.errmsg("If qop is sent then cnonce and nc MUST be present"))
        else:
            if self.cnonce or self.nc:
                raise ValueError(self.errmsg("If qop is not sent, neither cnonce nor nc can be present"))


    def __str__(self):
        return 'authorization : %s' % self.auth_header

    def validate_nonce(self, s, key):
        """Validate the nonce.
        Returns True if nonce was generated by synthesize_nonce() and the timestamp
        is not spoofed, else returns False.

        s
            A string related to the resource, such as the hostname of the server.
            
        key
            A secret string known only to the server.
        
        Both s and key must be the same values which were used to synthesize the nonce
        we are trying to validate.
        """
        try:
            timestamp, hashpart = self.nonce.split(':', 1)
            s_timestamp, s_hashpart = synthesize_nonce(s, key, timestamp).split(':', 1)
            is_valid = s_hashpart == hashpart
            if self.debug:
                TRACE('validate_nonce: %s' % is_valid)
            return is_valid
        except ValueError: # split() error
            pass
        return False


    def is_nonce_stale(self, max_age_seconds=600):
        """Returns True if a validated nonce is stale. The nonce contains a
        timestamp in plaintext and also a secure hash of the timestamp. You should
        first validate the nonce to ensure the plaintext timestamp is not spoofed.
        """
        try:
            timestamp, hashpart = self.nonce.split(':', 1)
            if int(timestamp) + max_age_seconds > int(time.time()):
                return False
        except ValueError: # int() error
            pass
        if self.debug:
            TRACE("nonce is stale")
        return True


    def HA2(self, entity_body=''):
        """Returns the H(A2) string. See :rfc:`2617` section 3.2.2.3."""
        # RFC 2617 3.2.2.3
        # If the "qop" directive's value is "auth" or is unspecified, then A2 is:
        #    A2 = method ":" digest-uri-value
        #
        # If the "qop" value is "auth-int", then A2 is:
        #    A2 = method ":" digest-uri-value ":" H(entity-body)
        if self.qop is None or self.qop == "auth":
            a2 = '%s:%s' % (self.http_method, self.uri)
        elif self.qop == "auth-int":
            a2 = "%s:%s:%s" % (self.http_method, self.uri, H(entity_body))
        else:
            # in theory, this should never happen, since I validate qop in __init__()
            raise ValueError(self.errmsg("Unrecognized value for qop!"))
        return H(a2)


    def request_digest(self, ha1, entity_body=''):
        """Calculates the Request-Digest. See :rfc:`2617` section 3.2.2.1.

        ha1
            The HA1 string obtained from the credentials store.

        entity_body
            If 'qop' is set to 'auth-int', then A2 includes a hash
            of the "entity body".  The entity body is the part of the
            message which follows the HTTP headers. See :rfc:`2617` section
            4.3.  This refers to the entity the user agent sent in the request which
            has the Authorization header. Typically GET requests don't have an entity,
            and POST requests do.
        
        """
        ha2 = self.HA2(entity_body)
        # Request-Digest -- RFC 2617 3.2.2.1
        if self.qop:
            req = "%s:%s:%s:%s:%s" % (self.nonce, self.nc, self.cnonce, self.qop, ha2)
        else:
            req = "%s:%s" % (self.nonce, ha2)

        # RFC 2617 3.2.2.2
        #
        # If the "algorithm" directive's value is "MD5" or is unspecified, then A1 is:
        # A1 = unq(username-value) ":" unq(realm-value) ":" passwd
        #
        # If the "algorithm" directive's value is "MD5-sess", then A1 is
        # calculated only once - on the first request by the client following
        # receipt of a WWW-Authenticate challenge from the server.
        # A1 = H( unq(username-value) ":" unq(realm-value) ":" passwd )
        #         ":" unq(nonce-value) ":" unq(cnonce-value)
        if self.algorithm == 'MD5-sess':
            ha1 = H('%s:%s:%s' % (ha1, self.nonce, self.cnonce))

        digest = H('%s:%s' % (ha1, req))
        return digest



def www_authenticate(realm, key, algorithm='MD5', nonce=None, qop=qop_auth, stale=False):
    """Constructs a WWW-Authenticate header for Digest authentication."""
    if qop not in valid_qops:
        raise ValueError("Unsupported value for qop: '%s'" % qop)
    if algorithm not in valid_algorithms:
        raise ValueError("Unsupported value for algorithm: '%s'" % algorithm)

    if nonce is None:
        nonce = synthesize_nonce(realm, key)
    s = 'Digest realm="%s", nonce="%s", algorithm="%s", qop="%s"' % (
                realm, nonce, algorithm, qop)
    if stale:
        s += ', stale="true"'
    return s


def digest_auth(realm, get_ha1, key, debug=False):
    """A CherryPy tool which hooks at before_handler to perform
    HTTP Digest Access Authentication, as specified in :rfc:`2617`.
    
    If the request has an 'authorization' header with a 'Digest' scheme, this
    tool authenticates the credentials supplied in that header.  If
    the request has no 'authorization' header, or if it does but the scheme is
    not "Digest", or if authentication fails, the tool sends a 401 response with
    a 'WWW-Authenticate' Digest header.
    
    realm
        A string containing the authentication realm.
    
    get_ha1
        A callable which looks up a username in a credentials store
        and returns the HA1 string, which is defined in the RFC to be
        MD5(username : realm : password).  The function's signature is:
        ``get_ha1(realm, username)``
        where username is obtained from the request's 'authorization' header.
        If username is not found in the credentials store, get_ha1() returns
        None.
    
    key
        A secret string known only to the server, used in the synthesis of nonces.
    
    """
    request = cherrypy.serving.request
    
    auth_header = request.headers.get('authorization')
    nonce_is_stale = False
    if auth_header is not None:
        try:
            auth = HttpDigestAuthorization(auth_header, request.method, debug=debug)
        except ValueError:
            raise cherrypy.HTTPError(400, "The Authorization header could not be parsed.")
        
        if debug:
            TRACE(str(auth))
        
        if auth.validate_nonce(realm, key):
            ha1 = get_ha1(realm, auth.username)
            if ha1 is not None:
                # note that for request.body to be available we need to hook in at
                # before_handler, not on_start_resource like 3.1.x digest_auth does.
                digest = auth.request_digest(ha1, entity_body=request.body)
                if digest == auth.response: # authenticated
                    if debug:
                        TRACE("digest matches auth.response")
                    # Now check if nonce is stale.
                    # The choice of ten minutes' lifetime for nonce is somewhat arbitrary
                    nonce_is_stale = auth.is_nonce_stale(max_age_seconds=600)
                    if not nonce_is_stale:
                        request.login = auth.username
                        if debug:
                            TRACE("authentication of %s successful" % auth.username)
                        return
    
    # Respond with 401 status and a WWW-Authenticate header
    header = www_authenticate(realm, key, stale=nonce_is_stale)
    if debug:
        TRACE(header)
    cherrypy.serving.response.headers['WWW-Authenticate'] = header
    raise cherrypy.HTTPError(401, "You are not authorized to access that resource")


########NEW FILE########
__FILENAME__ = caching
"""
CherryPy implements a simple caching system as a pluggable Tool. This tool tries
to be an (in-process) HTTP/1.1-compliant cache. It's not quite there yet, but
it's probably good enough for most sites.

In general, GET responses are cached (along with selecting headers) and, if
another request arrives for the same resource, the caching Tool will return 304
Not Modified if possible, or serve the cached response otherwise. It also sets
request.cached to True if serving a cached representation, and sets
request.cacheable to False (so it doesn't get cached again).

If POST, PUT, or DELETE requests are made for a cached resource, they invalidate
(delete) any cached response.

Usage
=====

Configuration file example::

    [/]
    tools.caching.on = True
    tools.caching.delay = 3600

You may use a class other than the default
:class:`MemoryCache<cherrypy.lib.caching.MemoryCache>` by supplying the config
entry ``cache_class``; supply the full dotted name of the replacement class
as the config value. It must implement the basic methods ``get``, ``put``,
``delete``, and ``clear``.

You may set any attribute, including overriding methods, on the cache
instance by providing them in config. The above sets the
:attr:`delay<cherrypy.lib.caching.MemoryCache.delay>` attribute, for example.
"""

import datetime
import sys
import threading
import time

import cherrypy
from cherrypy.lib import cptools, httputil
from cherrypy._cpcompat import copyitems, ntob, set_daemon, sorted


class Cache(object):
    """Base class for Cache implementations."""
    
    def get(self):
        """Return the current variant if in the cache, else None."""
        raise NotImplemented
    
    def put(self, obj, size):
        """Store the current variant in the cache."""
        raise NotImplemented
    
    def delete(self):
        """Remove ALL cached variants of the current resource."""
        raise NotImplemented
    
    def clear(self):
        """Reset the cache to its initial, empty state."""
        raise NotImplemented



# ------------------------------- Memory Cache ------------------------------- #


class AntiStampedeCache(dict):
    """A storage system for cached items which reduces stampede collisions."""
    
    def wait(self, key, timeout=5, debug=False):
        """Return the cached value for the given key, or None.
        
        If timeout is not None, and the value is already
        being calculated by another thread, wait until the given timeout has
        elapsed. If the value is available before the timeout expires, it is
        returned. If not, None is returned, and a sentinel placed in the cache
        to signal other threads to wait.
        
        If timeout is None, no waiting is performed nor sentinels used.
        """
        value = self.get(key)
        if isinstance(value, threading._Event):
            if timeout is None:
                # Ignore the other thread and recalc it ourselves.
                if debug:
                    cherrypy.log('No timeout', 'TOOLS.CACHING')
                return None
            
            # Wait until it's done or times out.
            if debug:
                cherrypy.log('Waiting up to %s seconds' % timeout, 'TOOLS.CACHING')
            value.wait(timeout)
            if value.result is not None:
                # The other thread finished its calculation. Use it.
                if debug:
                    cherrypy.log('Result!', 'TOOLS.CACHING')
                return value.result
            # Timed out. Stick an Event in the slot so other threads wait
            # on this one to finish calculating the value.
            if debug:
                cherrypy.log('Timed out', 'TOOLS.CACHING')
            e = threading.Event()
            e.result = None
            dict.__setitem__(self, key, e)
            
            return None
        elif value is None:
            # Stick an Event in the slot so other threads wait
            # on this one to finish calculating the value.
            if debug:
                cherrypy.log('Timed out', 'TOOLS.CACHING')
            e = threading.Event()
            e.result = None
            dict.__setitem__(self, key, e)
        return value
    
    def __setitem__(self, key, value):
        """Set the cached value for the given key."""
        existing = self.get(key)
        dict.__setitem__(self, key, value)
        if isinstance(existing, threading._Event):
            # Set Event.result so other threads waiting on it have
            # immediate access without needing to poll the cache again.
            existing.result = value
            existing.set()


class MemoryCache(Cache):
    """An in-memory cache for varying response content.
    
    Each key in self.store is a URI, and each value is an AntiStampedeCache.
    The response for any given URI may vary based on the values of
    "selecting request headers"; that is, those named in the Vary
    response header. We assume the list of header names to be constant
    for each URI throughout the lifetime of the application, and store
    that list in ``self.store[uri].selecting_headers``.
    
    The items contained in ``self.store[uri]`` have keys which are tuples of
    request header values (in the same order as the names in its
    selecting_headers), and values which are the actual responses.
    """
    
    maxobjects = 1000
    """The maximum number of cached objects; defaults to 1000."""
    
    maxobj_size = 100000
    """The maximum size of each cached object in bytes; defaults to 100 KB."""
    
    maxsize = 10000000
    """The maximum size of the entire cache in bytes; defaults to 10 MB."""
    
    delay = 600
    """Seconds until the cached content expires; defaults to 600 (10 minutes)."""
    
    antistampede_timeout = 5
    """Seconds to wait for other threads to release a cache lock."""
    
    expire_freq = 0.1
    """Seconds to sleep between cache expiration sweeps."""
    
    debug = False
    
    def __init__(self):
        self.clear()
        
        # Run self.expire_cache in a separate daemon thread.
        t = threading.Thread(target=self.expire_cache, name='expire_cache')
        self.expiration_thread = t
        set_daemon(t, True)
        t.start()
    
    def clear(self):
        """Reset the cache to its initial, empty state."""
        self.store = {}
        self.expirations = {}
        self.tot_puts = 0
        self.tot_gets = 0
        self.tot_hist = 0
        self.tot_expires = 0
        self.tot_non_modified = 0
        self.cursize = 0
    
    def expire_cache(self):
        """Continuously examine cached objects, expiring stale ones.
        
        This function is designed to be run in its own daemon thread,
        referenced at ``self.expiration_thread``.
        """
        # It's possible that "time" will be set to None
        # arbitrarily, so we check "while time" to avoid exceptions.
        # See tickets #99 and #180 for more information.
        while time:
            now = time.time()
            # Must make a copy of expirations so it doesn't change size
            # during iteration
            for expiration_time, objects in copyitems(self.expirations):
                if expiration_time <= now:
                    for obj_size, uri, sel_header_values in objects:
                        try:
                            del self.store[uri][tuple(sel_header_values)]
                            self.tot_expires += 1
                            self.cursize -= obj_size
                        except KeyError:
                            # the key may have been deleted elsewhere
                            pass
                    del self.expirations[expiration_time]
            time.sleep(self.expire_freq)
    
    def get(self):
        """Return the current variant if in the cache, else None."""
        request = cherrypy.serving.request
        self.tot_gets += 1
        
        uri = cherrypy.url(qs=request.query_string)
        uricache = self.store.get(uri)
        if uricache is None:
            return None
        
        header_values = [request.headers.get(h, '')
                         for h in uricache.selecting_headers]
        variant = uricache.wait(key=tuple(sorted(header_values)),
                                timeout=self.antistampede_timeout,
                                debug=self.debug)
        if variant is not None:
            self.tot_hist += 1
        return variant
    
    def put(self, variant, size):
        """Store the current variant in the cache."""
        request = cherrypy.serving.request
        response = cherrypy.serving.response
        
        uri = cherrypy.url(qs=request.query_string)
        uricache = self.store.get(uri)
        if uricache is None:
            uricache = AntiStampedeCache()
            uricache.selecting_headers = [
                e.value for e in response.headers.elements('Vary')]
            self.store[uri] = uricache
        
        if len(self.store) < self.maxobjects:
            total_size = self.cursize + size
            
            # checks if there's space for the object
            if (size < self.maxobj_size and total_size < self.maxsize):
                # add to the expirations list
                expiration_time = response.time + self.delay
                bucket = self.expirations.setdefault(expiration_time, [])
                bucket.append((size, uri, uricache.selecting_headers))
                
                # add to the cache
                header_values = [request.headers.get(h, '')
                                 for h in uricache.selecting_headers]
                uricache[tuple(sorted(header_values))] = variant
                self.tot_puts += 1
                self.cursize = total_size
    
    def delete(self):
        """Remove ALL cached variants of the current resource."""
        uri = cherrypy.url(qs=cherrypy.serving.request.query_string)
        self.store.pop(uri, None)


def get(invalid_methods=("POST", "PUT", "DELETE"), debug=False, **kwargs):
    """Try to obtain cached output. If fresh enough, raise HTTPError(304).
    
    If POST, PUT, or DELETE:
        * invalidates (deletes) any cached response for this resource
        * sets request.cached = False
        * sets request.cacheable = False
    
    else if a cached copy exists:
        * sets request.cached = True
        * sets request.cacheable = False
        * sets response.headers to the cached values
        * checks the cached Last-Modified response header against the
          current If-(Un)Modified-Since request headers; raises 304
          if necessary.
        * sets response.status and response.body to the cached values
        * returns True
    
    otherwise:
        * sets request.cached = False
        * sets request.cacheable = True
        * returns False
    """
    request = cherrypy.serving.request
    response = cherrypy.serving.response
    
    if not hasattr(cherrypy, "_cache"):
        # Make a process-wide Cache object.
        cherrypy._cache = kwargs.pop("cache_class", MemoryCache)()
        
        # Take all remaining kwargs and set them on the Cache object.
        for k, v in kwargs.items():
            setattr(cherrypy._cache, k, v)
        cherrypy._cache.debug = debug
    
    # POST, PUT, DELETE should invalidate (delete) the cached copy.
    # See http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.10.
    if request.method in invalid_methods:
        if debug:
            cherrypy.log('request.method %r in invalid_methods %r' %
                         (request.method, invalid_methods), 'TOOLS.CACHING')
        cherrypy._cache.delete()
        request.cached = False
        request.cacheable = False
        return False
    
    if 'no-cache' in [e.value for e in request.headers.elements('Pragma')]:
        request.cached = False
        request.cacheable = True
        return False
    
    cache_data = cherrypy._cache.get()
    request.cached = bool(cache_data)
    request.cacheable = not request.cached
    if request.cached:
        # Serve the cached copy.
        max_age = cherrypy._cache.delay
        for v in [e.value for e in request.headers.elements('Cache-Control')]:
            atoms = v.split('=', 1)
            directive = atoms.pop(0)
            if directive == 'max-age':
                if len(atoms) != 1 or not atoms[0].isdigit():
                    raise cherrypy.HTTPError(400, "Invalid Cache-Control header")
                max_age = int(atoms[0])
                break
            elif directive == 'no-cache':
                if debug:
                    cherrypy.log('Ignoring cache due to Cache-Control: no-cache',
                                 'TOOLS.CACHING')
                request.cached = False
                request.cacheable = True
                return False
        
        if debug:
            cherrypy.log('Reading response from cache', 'TOOLS.CACHING')
        s, h, b, create_time = cache_data
        age = int(response.time - create_time)
        if (age > max_age):
            if debug:
                cherrypy.log('Ignoring cache due to age > %d' % max_age,
                             'TOOLS.CACHING')
            request.cached = False
            request.cacheable = True
            return False
        
        # Copy the response headers. See http://www.cherrypy.org/ticket/721.
        response.headers = rh = httputil.HeaderMap()
        for k in h:
            dict.__setitem__(rh, k, dict.__getitem__(h, k))
        
        # Add the required Age header
        response.headers["Age"] = str(age)
        
        try:
            # Note that validate_since depends on a Last-Modified header;
            # this was put into the cached copy, and should have been
            # resurrected just above (response.headers = cache_data[1]).
            cptools.validate_since()
        except cherrypy.HTTPRedirect:
            x = sys.exc_info()[1]
            if x.status == 304:
                cherrypy._cache.tot_non_modified += 1
            raise
        
        # serve it & get out from the request
        response.status = s
        response.body = b
    else:
        if debug:
            cherrypy.log('request is not cached', 'TOOLS.CACHING')
    return request.cached


def tee_output():
    """Tee response output to cache storage. Internal."""
    # Used by CachingTool by attaching to request.hooks
    
    request = cherrypy.serving.request
    if 'no-store' in request.headers.values('Cache-Control'):
        return
    
    def tee(body):
        """Tee response.body into a list."""
        if ('no-cache' in response.headers.values('Pragma') or
            'no-store' in response.headers.values('Cache-Control')):
            for chunk in body:
                yield chunk
            return
        
        output = []
        for chunk in body:
            output.append(chunk)
            yield chunk
        
        # save the cache data
        body = ntob('').join(output)
        cherrypy._cache.put((response.status, response.headers or {},
                             body, response.time), len(body))
    
    response = cherrypy.serving.response
    response.body = tee(response.body)


def expires(secs=0, force=False, debug=False):
    """Tool for influencing cache mechanisms using the 'Expires' header.

    secs
        Must be either an int or a datetime.timedelta, and indicates the
        number of seconds between response.time and when the response should
        expire. The 'Expires' header will be set to response.time + secs.
        If secs is zero, the 'Expires' header is set one year in the past, and
        the following "cache prevention" headers are also set:
        
            * Pragma: no-cache
            * Cache-Control': no-cache, must-revalidate

    force
        If False, the following headers are checked:
        
            * Etag
            * Last-Modified
            * Age
            * Expires
        
        If any are already present, none of the above response headers are set.
    
    """
    
    response = cherrypy.serving.response
    headers = response.headers
    
    cacheable = False
    if not force:
        # some header names that indicate that the response can be cached
        for indicator in ('Etag', 'Last-Modified', 'Age', 'Expires'):
            if indicator in headers:
                cacheable = True
                break
    
    if not cacheable and not force:
        if debug:
            cherrypy.log('request is not cacheable', 'TOOLS.EXPIRES')
    else:
        if debug:
            cherrypy.log('request is cacheable', 'TOOLS.EXPIRES')
        if isinstance(secs, datetime.timedelta):
            secs = (86400 * secs.days) + secs.seconds
        
        if secs == 0:
            if force or ("Pragma" not in headers):
                headers["Pragma"] = "no-cache"
            if cherrypy.serving.request.protocol >= (1, 1):
                if force or "Cache-Control" not in headers:
                    headers["Cache-Control"] = "no-cache, must-revalidate"
            # Set an explicit Expires date in the past.
            expiry = httputil.HTTPDate(1169942400.0)
        else:
            expiry = httputil.HTTPDate(response.time + secs)
        if force or "Expires" not in headers:
            headers["Expires"] = expiry

########NEW FILE########
__FILENAME__ = covercp
"""Code-coverage tools for CherryPy.

To use this module, or the coverage tools in the test suite,
you need to download 'coverage.py', either Gareth Rees' `original 
implementation <http://www.garethrees.org/2001/12/04/python-coverage/>`_
or Ned Batchelder's `enhanced version:
<http://www.nedbatchelder.com/code/modules/coverage.html>`_

To turn on coverage tracing, use the following code::

    cherrypy.engine.subscribe('start', covercp.start)

DO NOT subscribe anything on the 'start_thread' channel, as previously
recommended. Calling start once in the main thread should be sufficient
to start coverage on all threads. Calling start again in each thread
effectively clears any coverage data gathered up to that point.

Run your code, then use the ``covercp.serve()`` function to browse the
results in a web browser. If you run this module from the command line,
it will call ``serve()`` for you.
"""

import re
import sys
import cgi
from cherrypy._cpcompat import quote_plus
import os, os.path
localFile = os.path.join(os.path.dirname(__file__), "coverage.cache")

the_coverage = None
try:
    from coverage import coverage
    the_coverage = coverage(data_file=localFile)
    def start():
        the_coverage.start()
except ImportError:
    # Setting the_coverage to None will raise errors
    # that need to be trapped downstream.
    the_coverage = None
    
    import warnings
    warnings.warn("No code coverage will be performed; coverage.py could not be imported.")
    
    def start():
        pass
start.priority = 20

TEMPLATE_MENU = """<html>
<head>
    <title>CherryPy Coverage Menu</title>
    <style>
        body {font: 9pt Arial, serif;}
        #tree {
            font-size: 8pt;
            font-family: Andale Mono, monospace;
            white-space: pre;
            }
        #tree a:active, a:focus {
            background-color: black;
            padding: 1px;
            color: white;
            border: 0px solid #9999FF;
            -moz-outline-style: none;
            }
        .fail { color: red;}
        .pass { color: #888;}
        #pct { text-align: right;}
        h3 {
            font-size: small;
            font-weight: bold;
            font-style: italic;
            margin-top: 5px; 
            }
        input { border: 1px solid #ccc; padding: 2px; }
        .directory {
            color: #933;
            font-style: italic;
            font-weight: bold;
            font-size: 10pt;
            }
        .file {
            color: #400;
            }
        a { text-decoration: none; }
        #crumbs {
            color: white;
            font-size: 8pt;
            font-family: Andale Mono, monospace;
            width: 100%;
            background-color: black;
            }
        #crumbs a {
            color: #f88;
            }
        #options {
            line-height: 2.3em;
            border: 1px solid black;
            background-color: #eee;
            padding: 4px;
            }
        #exclude {
            width: 100%;
            margin-bottom: 3px;
            border: 1px solid #999;
            }
        #submit {
            background-color: black;
            color: white;
            border: 0;
            margin-bottom: -9px;
            }
    </style>
</head>
<body>
<h2>CherryPy Coverage</h2>"""

TEMPLATE_FORM = """
<div id="options">
<form action='menu' method=GET>
    <input type='hidden' name='base' value='%(base)s' />
    Show percentages <input type='checkbox' %(showpct)s name='showpct' value='checked' /><br />
    Hide files over <input type='text' id='pct' name='pct' value='%(pct)s' size='3' />%%<br />
    Exclude files matching<br />
    <input type='text' id='exclude' name='exclude' value='%(exclude)s' size='20' />
    <br />

    <input type='submit' value='Change view' id="submit"/>
</form>
</div>""" 

TEMPLATE_FRAMESET = """<html>
<head><title>CherryPy coverage data</title></head>
<frameset cols='250, 1*'>
    <frame src='menu?base=%s' />
    <frame name='main' src='' />
</frameset>
</html>
"""

TEMPLATE_COVERAGE = """<html>
<head>
    <title>Coverage for %(name)s</title>
    <style>
        h2 { margin-bottom: .25em; }
        p { margin: .25em; }
        .covered { color: #000; background-color: #fff; }
        .notcovered { color: #fee; background-color: #500; }
        .excluded { color: #00f; background-color: #fff; }
         table .covered, table .notcovered, table .excluded
             { font-family: Andale Mono, monospace;
               font-size: 10pt; white-space: pre; }

         .lineno { background-color: #eee;}
         .notcovered .lineno { background-color: #000;}
         table { border-collapse: collapse;
    </style>
</head>
<body>
<h2>%(name)s</h2>
<p>%(fullpath)s</p>
<p>Coverage: %(pc)s%%</p>"""

TEMPLATE_LOC_COVERED = """<tr class="covered">
    <td class="lineno">%s&nbsp;</td>
    <td>%s</td>
</tr>\n"""
TEMPLATE_LOC_NOT_COVERED = """<tr class="notcovered">
    <td class="lineno">%s&nbsp;</td>
    <td>%s</td>
</tr>\n"""
TEMPLATE_LOC_EXCLUDED = """<tr class="excluded">
    <td class="lineno">%s&nbsp;</td>
    <td>%s</td>
</tr>\n"""

TEMPLATE_ITEM = "%s%s<a class='file' href='report?name=%s' target='main'>%s</a>\n"

def _percent(statements, missing):
    s = len(statements)
    e = s - len(missing)
    if s > 0:
        return int(round(100.0 * e / s))
    return 0

def _show_branch(root, base, path, pct=0, showpct=False, exclude="",
                 coverage=the_coverage):
    
    # Show the directory name and any of our children
    dirs = [k for k, v in root.items() if v]
    dirs.sort()
    for name in dirs:
        newpath = os.path.join(path, name)
        
        if newpath.lower().startswith(base):
            relpath = newpath[len(base):]
            yield "| " * relpath.count(os.sep)
            yield "<a class='directory' href='menu?base=%s&exclude=%s'>%s</a>\n" % \
                   (newpath, quote_plus(exclude), name)
        
        for chunk in _show_branch(root[name], base, newpath, pct, showpct, exclude, coverage=coverage):
            yield chunk
    
    # Now list the files
    if path.lower().startswith(base):
        relpath = path[len(base):]
        files = [k for k, v in root.items() if not v]
        files.sort()
        for name in files:
            newpath = os.path.join(path, name)
            
            pc_str = ""
            if showpct:
                try:
                    _, statements, _, missing, _ = coverage.analysis2(newpath)
                except:
                    # Yes, we really want to pass on all errors.
                    pass
                else:
                    pc = _percent(statements, missing)
                    pc_str = ("%3d%% " % pc).replace(' ','&nbsp;')
                    if pc < float(pct) or pc == -1:
                        pc_str = "<span class='fail'>%s</span>" % pc_str
                    else:
                        pc_str = "<span class='pass'>%s</span>" % pc_str
            
            yield TEMPLATE_ITEM % ("| " * (relpath.count(os.sep) + 1),
                                   pc_str, newpath, name)

def _skip_file(path, exclude):
    if exclude:
        return bool(re.search(exclude, path))

def _graft(path, tree):
    d = tree
    
    p = path
    atoms = []
    while True:
        p, tail = os.path.split(p)
        if not tail:
            break
        atoms.append(tail)
    atoms.append(p)
    if p != "/":
        atoms.append("/")
    
    atoms.reverse()
    for node in atoms:
        if node:
            d = d.setdefault(node, {})

def get_tree(base, exclude, coverage=the_coverage):
    """Return covered module names as a nested dict."""
    tree = {}
    runs = coverage.data.executed_files()
    for path in runs:
        if not _skip_file(path, exclude) and not os.path.isdir(path):
            _graft(path, tree)
    return tree

class CoverStats(object):
    
    def __init__(self, coverage, root=None):
        self.coverage = coverage
        if root is None:
            # Guess initial depth. Files outside this path will not be
            # reachable from the web interface.
            import cherrypy
            root = os.path.dirname(cherrypy.__file__)
        self.root = root
    
    def index(self):
        return TEMPLATE_FRAMESET % self.root.lower()
    index.exposed = True
    
    def menu(self, base="/", pct="50", showpct="",
             exclude=r'python\d\.\d|test|tut\d|tutorial'):
        
        # The coverage module uses all-lower-case names.
        base = base.lower().rstrip(os.sep)
        
        yield TEMPLATE_MENU
        yield TEMPLATE_FORM % locals()
        
        # Start by showing links for parent paths
        yield "<div id='crumbs'>"
        path = ""
        atoms = base.split(os.sep)
        atoms.pop()
        for atom in atoms:
            path += atom + os.sep
            yield ("<a href='menu?base=%s&exclude=%s'>%s</a> %s"
                   % (path, quote_plus(exclude), atom, os.sep))
        yield "</div>"
        
        yield "<div id='tree'>"
        
        # Then display the tree
        tree = get_tree(base, exclude, self.coverage)
        if not tree:
            yield "<p>No modules covered.</p>"
        else:
            for chunk in _show_branch(tree, base, "/", pct,
                                      showpct=='checked', exclude, coverage=self.coverage):
                yield chunk
        
        yield "</div>"
        yield "</body></html>"
    menu.exposed = True
    
    def annotated_file(self, filename, statements, excluded, missing):
        source = open(filename, 'r')
        buffer = []
        for lineno, line in enumerate(source.readlines()):
            lineno += 1
            line = line.strip("\n\r")
            empty_the_buffer = True
            if lineno in excluded:
                template = TEMPLATE_LOC_EXCLUDED
            elif lineno in missing:
                template = TEMPLATE_LOC_NOT_COVERED
            elif lineno in statements:
                template = TEMPLATE_LOC_COVERED
            else:
                empty_the_buffer = False
                buffer.append((lineno, line))
            if empty_the_buffer:
                for lno, pastline in buffer:
                    yield template % (lno, cgi.escape(pastline))
                buffer = []
                yield template % (lineno, cgi.escape(line))
    
    def report(self, name):
        filename, statements, excluded, missing, _ = self.coverage.analysis2(name)
        pc = _percent(statements, missing)
        yield TEMPLATE_COVERAGE % dict(name=os.path.basename(name),
                                       fullpath=name,
                                       pc=pc)
        yield '<table>\n'
        for line in self.annotated_file(filename, statements, excluded,
                                        missing):
            yield line
        yield '</table>'
        yield '</body>'
        yield '</html>'
    report.exposed = True


def serve(path=localFile, port=8080, root=None):
    if coverage is None:
        raise ImportError("The coverage module could not be imported.")
    from coverage import coverage
    cov = coverage(data_file = path)
    cov.load()
    
    import cherrypy
    cherrypy.config.update({'server.socket_port': int(port),
                            'server.thread_pool': 10,
                            'environment': "production",
                            })
    cherrypy.quickstart(CoverStats(cov, root))

if __name__ == "__main__":
    serve(*tuple(sys.argv[1:]))


########NEW FILE########
__FILENAME__ = cpstats
"""CPStats, a package for collecting and reporting on program statistics.

Overview
========

Statistics about program operation are an invaluable monitoring and debugging
tool. Unfortunately, the gathering and reporting of these critical values is
usually ad-hoc. This package aims to add a centralized place for gathering
statistical performance data, a structure for recording that data which
provides for extrapolation of that data into more useful information,
and a method of serving that data to both human investigators and
monitoring software. Let's examine each of those in more detail.

Data Gathering
--------------

Just as Python's `logging` module provides a common importable for gathering
and sending messages, performance statistics would benefit from a similar
common mechanism, and one that does *not* require each package which wishes
to collect stats to import a third-party module. Therefore, we choose to
re-use the `logging` module by adding a `statistics` object to it.

That `logging.statistics` object is a nested dict. It is not a custom class,
because that would 1) require libraries and applications to import a third-
party module in order to participate, 2) inhibit innovation in extrapolation
approaches and in reporting tools, and 3) be slow. There are, however, some
specifications regarding the structure of the dict.

    {
   +----"SQLAlchemy": {
   |        "Inserts": 4389745,
   |        "Inserts per Second":
   |            lambda s: s["Inserts"] / (time() - s["Start"]),
   |  C +---"Table Statistics": {
   |  o |        "widgets": {-----------+
 N |  l |            "Rows": 1.3M,      | Record
 a |  l |            "Inserts": 400,    |
 m |  e |        },---------------------+
 e |  c |        "froobles": {
 s |  t |            "Rows": 7845,
 p |  i |            "Inserts": 0,
 a |  o |        },
 c |  n +---},
 e |        "Slow Queries":
   |            [{"Query": "SELECT * FROM widgets;",
   |              "Processing Time": 47.840923343,
   |              },
   |             ],
   +----},
    }

The `logging.statistics` dict has four levels. The topmost level is nothing
more than a set of names to introduce modularity, usually along the lines of
package names. If the SQLAlchemy project wanted to participate, for example,
it might populate the item `logging.statistics['SQLAlchemy']`, whose value
would be a second-layer dict we call a "namespace". Namespaces help multiple
packages to avoid collisions over key names, and make reports easier to read,
to boot. The maintainers of SQLAlchemy should feel free to use more than one
namespace if needed (such as 'SQLAlchemy ORM'). Note that there are no case
or other syntax constraints on the namespace names; they should be chosen
to be maximally readable by humans (neither too short nor too long).

Each namespace, then, is a dict of named statistical values, such as
'Requests/sec' or 'Uptime'. You should choose names which will look
good on a report: spaces and capitalization are just fine.

In addition to scalars, values in a namespace MAY be a (third-layer)
dict, or a list, called a "collection". For example, the CherryPy StatsTool
keeps track of what each request is doing (or has most recently done)
in a 'Requests' collection, where each key is a thread ID; each
value in the subdict MUST be a fourth dict (whew!) of statistical data about
each thread. We call each subdict in the collection a "record". Similarly,
the StatsTool also keeps a list of slow queries, where each record contains
data about each slow query, in order.

Values in a namespace or record may also be functions, which brings us to:

Extrapolation
-------------

The collection of statistical data needs to be fast, as close to unnoticeable
as possible to the host program. That requires us to minimize I/O, for example,
but in Python it also means we need to minimize function calls. So when you
are designing your namespace and record values, try to insert the most basic
scalar values you already have on hand.

When it comes time to report on the gathered data, however, we usually have
much more freedom in what we can calculate. Therefore, whenever reporting
tools (like the provided StatsPage CherryPy class) fetch the contents of
`logging.statistics` for reporting, they first call `extrapolate_statistics`
(passing the whole `statistics` dict as the only argument). This makes a
deep copy of the statistics dict so that the reporting tool can both iterate
over it and even change it without harming the original. But it also expands
any functions in the dict by calling them. For example, you might have a
'Current Time' entry in the namespace with the value "lambda scope: time.time()".
The "scope" parameter is the current namespace dict (or record, if we're
currently expanding one of those instead), allowing you access to existing
static entries. If you're truly evil, you can even modify more than one entry
at a time.

However, don't try to calculate an entry and then use its value in further
extrapolations; the order in which the functions are called is not guaranteed.
This can lead to a certain amount of duplicated work (or a redesign of your
schema), but that's better than complicating the spec.

After the whole thing has been extrapolated, it's time for:

Reporting
---------

The StatsPage class grabs the `logging.statistics` dict, extrapolates it all,
and then transforms it to HTML for easy viewing. Each namespace gets its own
header and attribute table, plus an extra table for each collection. This is
NOT part of the statistics specification; other tools can format how they like.

You can control which columns are output and how they are formatted by updating
StatsPage.formatting, which is a dict that mirrors the keys and nesting of
`logging.statistics`. The difference is that, instead of data values, it has
formatting values. Use None for a given key to indicate to the StatsPage that a
given column should not be output. Use a string with formatting (such as '%.3f')
to interpolate the value(s), or use a callable (such as lambda v: v.isoformat())
for more advanced formatting. Any entry which is not mentioned in the formatting
dict is output unchanged.

Monitoring
----------

Although the HTML output takes pains to assign unique id's to each <td> with
statistical data, you're probably better off fetching /cpstats/data, which
outputs the whole (extrapolated) `logging.statistics` dict in JSON format.
That is probably easier to parse, and doesn't have any formatting controls,
so you get the "original" data in a consistently-serialized format.
Note: there's no treatment yet for datetime objects. Try time.time() instead
for now if you can. Nagios will probably thank you.

Turning Collection Off
----------------------

It is recommended each namespace have an "Enabled" item which, if False,
stops collection (but not reporting) of statistical data. Applications
SHOULD provide controls to pause and resume collection by setting these
entries to False or True, if present.


Usage
=====

To collect statistics on CherryPy applications:

    from cherrypy.lib import cpstats
    appconfig['/']['tools.cpstats.on'] = True

To collect statistics on your own code:

    import logging
    # Initialize the repository
    if not hasattr(logging, 'statistics'): logging.statistics = {}
    # Initialize my namespace
    mystats = logging.statistics.setdefault('My Stuff', {})
    # Initialize my namespace's scalars and collections
    mystats.update({
        'Enabled': True,
        'Start Time': time.time(),
        'Important Events': 0,
        'Events/Second': lambda s: (
            (s['Important Events'] / (time.time() - s['Start Time']))),
        })
    ...
    for event in events:
        ...
        # Collect stats
        if mystats.get('Enabled', False):
            mystats['Important Events'] += 1

To report statistics:

    root.cpstats = cpstats.StatsPage()

To format statistics reports:

    See 'Reporting', above.

"""

# -------------------------------- Statistics -------------------------------- #

import logging
if not hasattr(logging, 'statistics'): logging.statistics = {}

def extrapolate_statistics(scope):
    """Return an extrapolated copy of the given scope."""
    c = {}
    for k, v in list(scope.items()):
        if isinstance(v, dict):
            v = extrapolate_statistics(v)
        elif isinstance(v, (list, tuple)):
            v = [extrapolate_statistics(record) for record in v]
        elif hasattr(v, '__call__'):
            v = v(scope)
        c[k] = v
    return c


# --------------------- CherryPy Applications Statistics --------------------- #

import threading
import time

import cherrypy

appstats = logging.statistics.setdefault('CherryPy Applications', {})
appstats.update({
    'Enabled': True,
    'Bytes Read/Request': lambda s: (s['Total Requests'] and
        (s['Total Bytes Read'] / float(s['Total Requests'])) or 0.0),
    'Bytes Read/Second': lambda s: s['Total Bytes Read'] / s['Uptime'](s),
    'Bytes Written/Request': lambda s: (s['Total Requests'] and
        (s['Total Bytes Written'] / float(s['Total Requests'])) or 0.0),
    'Bytes Written/Second': lambda s: s['Total Bytes Written'] / s['Uptime'](s),
    'Current Time': lambda s: time.time(),
    'Current Requests': 0,
    'Requests/Second': lambda s: float(s['Total Requests']) / s['Uptime'](s),
    'Server Version': cherrypy.__version__,
    'Start Time': time.time(),
    'Total Bytes Read': 0,
    'Total Bytes Written': 0,
    'Total Requests': 0,
    'Total Time': 0,
    'Uptime': lambda s: time.time() - s['Start Time'],
    'Requests': {},
    })

proc_time = lambda s: time.time() - s['Start Time']


class ByteCountWrapper(object):
    """Wraps a file-like object, counting the number of bytes read."""
    
    def __init__(self, rfile):
        self.rfile = rfile
        self.bytes_read = 0
    
    def read(self, size=-1):
        data = self.rfile.read(size)
        self.bytes_read += len(data)
        return data
    
    def readline(self, size=-1):
        data = self.rfile.readline(size)
        self.bytes_read += len(data)
        return data
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline()
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline()
        return lines
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        return self
    
    def next(self):
        data = self.rfile.next()
        self.bytes_read += len(data)
        return data


average_uriset_time = lambda s: s['Count'] and (s['Sum'] / s['Count']) or 0


class StatsTool(cherrypy.Tool):
    """Record various information about the current request."""
    
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_end_request', self.record_stop)
    
    def _setup(self):
        """Hook this tool into cherrypy.request.
        
        The standard CherryPy request object will automatically call this
        method when the tool is "turned on" in config.
        """
        if appstats.get('Enabled', False):
            cherrypy.Tool._setup(self)
            self.record_start()
    
    def record_start(self):
        """Record the beginning of a request."""
        request = cherrypy.serving.request
        if not hasattr(request.rfile, 'bytes_read'):
            request.rfile = ByteCountWrapper(request.rfile)
            request.body.fp = request.rfile
        
        r = request.remote
        
        appstats['Current Requests'] += 1
        appstats['Total Requests'] += 1
        appstats['Requests'][threading._get_ident()] = {
            'Bytes Read': None,
            'Bytes Written': None,
            # Use a lambda so the ip gets updated by tools.proxy later
            'Client': lambda s: '%s:%s' % (r.ip, r.port),
            'End Time': None,
            'Processing Time': proc_time,
            'Request-Line': request.request_line,
            'Response Status': None,
            'Start Time': time.time(),
            }

    def record_stop(self, uriset=None, slow_queries=1.0, slow_queries_count=100,
                    debug=False, **kwargs):
        """Record the end of a request."""
        resp = cherrypy.serving.response
        w = appstats['Requests'][threading._get_ident()]
        
        r = cherrypy.request.rfile.bytes_read
        w['Bytes Read'] = r
        appstats['Total Bytes Read'] += r
        
        if resp.stream:
            w['Bytes Written'] = 'chunked'
        else:
            cl = int(resp.headers.get('Content-Length', 0))
            w['Bytes Written'] = cl
            appstats['Total Bytes Written'] += cl
        
        w['Response Status'] = getattr(resp, 'output_status', None) or resp.status
        
        w['End Time'] = time.time()
        p = w['End Time'] - w['Start Time']
        w['Processing Time'] = p
        appstats['Total Time'] += p
        
        appstats['Current Requests'] -= 1
        
        if debug:
            cherrypy.log('Stats recorded: %s' % repr(w), 'TOOLS.CPSTATS')
        
        if uriset:
            rs = appstats.setdefault('URI Set Tracking', {})
            r = rs.setdefault(uriset, {
                'Min': None, 'Max': None, 'Count': 0, 'Sum': 0,
                'Avg': average_uriset_time})
            if r['Min'] is None or p < r['Min']:
                r['Min'] = p
            if r['Max'] is None or p > r['Max']:
                r['Max'] = p
            r['Count'] += 1
            r['Sum'] += p
        
        if slow_queries and p > slow_queries:
            sq = appstats.setdefault('Slow Queries', [])
            sq.append(w.copy())
            if len(sq) > slow_queries_count:
                sq.pop(0)


import cherrypy
cherrypy.tools.cpstats = StatsTool()


# ---------------------- CherryPy Statistics Reporting ---------------------- #

import os
thisdir = os.path.abspath(os.path.dirname(__file__))

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        json = None


missing = object()

locale_date = lambda v: time.strftime('%c', time.gmtime(v))
iso_format = lambda v: time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(v))

def pause_resume(ns):
    def _pause_resume(enabled):
        pause_disabled = ''
        resume_disabled = ''
        if enabled:
            resume_disabled = 'disabled="disabled" '
        else:
            pause_disabled = 'disabled="disabled" '
        return """
            <form action="pause" method="POST" style="display:inline">
            <input type="hidden" name="namespace" value="%s" />
            <input type="submit" value="Pause" %s/>
            </form>
            <form action="resume" method="POST" style="display:inline">
            <input type="hidden" name="namespace" value="%s" />
            <input type="submit" value="Resume" %s/>
            </form>
            """ % (ns, pause_disabled, ns, resume_disabled)
    return _pause_resume


class StatsPage(object):
    
    formatting = {
        'CherryPy Applications': {
            'Enabled': pause_resume('CherryPy Applications'),
            'Bytes Read/Request': '%.3f',
            'Bytes Read/Second': '%.3f',
            'Bytes Written/Request': '%.3f',
            'Bytes Written/Second': '%.3f',
            'Current Time': iso_format,
            'Requests/Second': '%.3f',
            'Start Time': iso_format,
            'Total Time': '%.3f',
            'Uptime': '%.3f',
            'Slow Queries': {
                'End Time': None,
                'Processing Time': '%.3f',
                'Start Time': iso_format,
                },
            'URI Set Tracking': {
                'Avg': '%.3f',
                'Max': '%.3f',
                'Min': '%.3f',
                'Sum': '%.3f',
                },
            'Requests': {
                'Bytes Read': '%s',
                'Bytes Written': '%s',
                'End Time': None,
                'Processing Time': '%.3f',
                'Start Time': None,
                },
        },
        'CherryPy WSGIServer': {
            'Enabled': pause_resume('CherryPy WSGIServer'),
            'Connections/second': '%.3f',
            'Start time': iso_format,
        },
    }
    
    
    def index(self):
        # Transform the raw data into pretty output for HTML
        yield """
<html>
<head>
    <title>Statistics</title>
<style>

th, td {
    padding: 0.25em 0.5em;
    border: 1px solid #666699;
}

table {
    border-collapse: collapse;
}

table.stats1 {
    width: 100%;
}

table.stats1 th {
    font-weight: bold;
    text-align: right;
    background-color: #CCD5DD;
}

table.stats2, h2 {
    margin-left: 50px;
}

table.stats2 th {
    font-weight: bold;
    text-align: center;
    background-color: #CCD5DD;
}

</style>
</head>
<body>
"""
        for title, scalars, collections in self.get_namespaces():
            yield """
<h1>%s</h1>

<table class='stats1'>
    <tbody>
""" % title
            for i, (key, value) in enumerate(scalars):
                colnum = i % 3
                if colnum == 0: yield """
        <tr>"""
                yield """
            <th>%(key)s</th><td id='%(title)s-%(key)s'>%(value)s</td>""" % vars()
                if colnum == 2: yield """
        </tr>"""
            
            if colnum == 0: yield """
            <th></th><td></td>
            <th></th><td></td>
        </tr>"""
            elif colnum == 1: yield """
            <th></th><td></td>
        </tr>"""
            yield """
    </tbody>
</table>"""

            for subtitle, headers, subrows in collections:
                yield """
<h2>%s</h2>
<table class='stats2'>
    <thead>
        <tr>""" % subtitle
                for key in headers:
                    yield """
            <th>%s</th>""" % key
                yield """
        </tr>
    </thead>
    <tbody>"""
                for subrow in subrows:
                    yield """
        <tr>"""
                    for value in subrow:
                        yield """
            <td>%s</td>""" % value
                    yield """
        </tr>"""
                yield """
    </tbody>
</table>"""
        yield """
</body>
</html>
"""
    index.exposed = True
    
    def get_namespaces(self):
        """Yield (title, scalars, collections) for each namespace."""
        s = extrapolate_statistics(logging.statistics)
        for title, ns in sorted(s.items()):
            scalars = []
            collections = []
            ns_fmt = self.formatting.get(title, {})
            for k, v in sorted(ns.items()):
                fmt = ns_fmt.get(k, {})
                if isinstance(v, dict):
                    headers, subrows = self.get_dict_collection(v, fmt)
                    collections.append((k, ['ID'] + headers, subrows))
                elif isinstance(v, (list, tuple)):
                    headers, subrows = self.get_list_collection(v, fmt)
                    collections.append((k, headers, subrows))
                else:
                    format = ns_fmt.get(k, missing)
                    if format is None:
                        # Don't output this column.
                        continue
                    if hasattr(format, '__call__'):
                        v = format(v)
                    elif format is not missing:
                        v = format % v
                    scalars.append((k, v))
            yield title, scalars, collections
    
    def get_dict_collection(self, v, formatting):
        """Return ([headers], [rows]) for the given collection."""
        # E.g., the 'Requests' dict.
        headers = []
        for record in v.itervalues():
            for k3 in record:
                format = formatting.get(k3, missing)
                if format is None:
                    # Don't output this column.
                    continue
                if k3 not in headers:
                    headers.append(k3)
        headers.sort()
        
        subrows = []
        for k2, record in sorted(v.items()):
            subrow = [k2]
            for k3 in headers:
                v3 = record.get(k3, '')
                format = formatting.get(k3, missing)
                if format is None:
                    # Don't output this column.
                    continue
                if hasattr(format, '__call__'):
                    v3 = format(v3)
                elif format is not missing:
                    v3 = format % v3
                subrow.append(v3)
            subrows.append(subrow)
        
        return headers, subrows
    
    def get_list_collection(self, v, formatting):
        """Return ([headers], [subrows]) for the given collection."""
        # E.g., the 'Slow Queries' list.
        headers = []
        for record in v:
            for k3 in record:
                format = formatting.get(k3, missing)
                if format is None:
                    # Don't output this column.
                    continue
                if k3 not in headers:
                    headers.append(k3)
        headers.sort()
        
        subrows = []
        for record in v:
            subrow = []
            for k3 in headers:
                v3 = record.get(k3, '')
                format = formatting.get(k3, missing)
                if format is None:
                    # Don't output this column.
                    continue
                if hasattr(format, '__call__'):
                    v3 = format(v3)
                elif format is not missing:
                    v3 = format % v3
                subrow.append(v3)
            subrows.append(subrow)
        
        return headers, subrows
    
    if json is not None:
        def data(self):
            s = extrapolate_statistics(logging.statistics)
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return json.dumps(s, sort_keys=True, indent=4)
        data.exposed = True
    
    def pause(self, namespace):
        logging.statistics.get(namespace, {})['Enabled'] = False
        raise cherrypy.HTTPRedirect('./')
    pause.exposed = True
    pause.cp_config = {'tools.allow.on': True,
                       'tools.allow.methods': ['POST']}
    
    def resume(self, namespace):
        logging.statistics.get(namespace, {})['Enabled'] = True
        raise cherrypy.HTTPRedirect('./')
    resume.exposed = True
    resume.cp_config = {'tools.allow.on': True,
                        'tools.allow.methods': ['POST']}


########NEW FILE########
__FILENAME__ = cptools
"""Functions for builtin CherryPy tools."""

import logging
import re

import cherrypy
from cherrypy._cpcompat import basestring, ntob, md5, set
from cherrypy.lib import httputil as _httputil


#                     Conditional HTTP request support                     #

def validate_etags(autotags=False, debug=False):
    """Validate the current ETag against If-Match, If-None-Match headers.
    
    If autotags is True, an ETag response-header value will be provided
    from an MD5 hash of the response body (unless some other code has
    already provided an ETag header). If False (the default), the ETag
    will not be automatic.
    
    WARNING: the autotags feature is not designed for URL's which allow
    methods other than GET. For example, if a POST to the same URL returns
    no content, the automatic ETag will be incorrect, breaking a fundamental
    use for entity tags in a possibly destructive fashion. Likewise, if you
    raise 304 Not Modified, the response body will be empty, the ETag hash
    will be incorrect, and your application will break.
    See :rfc:`2616` Section 14.24.
    """
    response = cherrypy.serving.response
    
    # Guard against being run twice.
    if hasattr(response, "ETag"):
        return
    
    status, reason, msg = _httputil.valid_status(response.status)
    
    etag = response.headers.get('ETag')
    
    # Automatic ETag generation. See warning in docstring.
    if etag:
        if debug:
            cherrypy.log('ETag already set: %s' % etag, 'TOOLS.ETAGS')
    elif not autotags:
        if debug:
            cherrypy.log('Autotags off', 'TOOLS.ETAGS')
    elif status != 200:
        if debug:
            cherrypy.log('Status not 200', 'TOOLS.ETAGS')
    else:
        etag = response.collapse_body()
        etag = '"%s"' % md5(etag).hexdigest()
        if debug:
            cherrypy.log('Setting ETag: %s' % etag, 'TOOLS.ETAGS')
        response.headers['ETag'] = etag
    
    response.ETag = etag
    
    # "If the request would, without the If-Match header field, result in
    # anything other than a 2xx or 412 status, then the If-Match header
    # MUST be ignored."
    if debug:
        cherrypy.log('Status: %s' % status, 'TOOLS.ETAGS')
    if status >= 200 and status <= 299:
        request = cherrypy.serving.request
        
        conditions = request.headers.elements('If-Match') or []
        conditions = [str(x) for x in conditions]
        if debug:
            cherrypy.log('If-Match conditions: %s' % repr(conditions),
                         'TOOLS.ETAGS')
        if conditions and not (conditions == ["*"] or etag in conditions):
            raise cherrypy.HTTPError(412, "If-Match failed: ETag %r did "
                                     "not match %r" % (etag, conditions))
        
        conditions = request.headers.elements('If-None-Match') or []
        conditions = [str(x) for x in conditions]
        if debug:
            cherrypy.log('If-None-Match conditions: %s' % repr(conditions),
                         'TOOLS.ETAGS')
        if conditions == ["*"] or etag in conditions:
            if debug:
                cherrypy.log('request.method: %s' % request.method, 'TOOLS.ETAGS')
            if request.method in ("GET", "HEAD"):
                raise cherrypy.HTTPRedirect([], 304)
            else:
                raise cherrypy.HTTPError(412, "If-None-Match failed: ETag %r "
                                         "matched %r" % (etag, conditions))

def validate_since():
    """Validate the current Last-Modified against If-Modified-Since headers.
    
    If no code has set the Last-Modified response header, then no validation
    will be performed.
    """
    response = cherrypy.serving.response
    lastmod = response.headers.get('Last-Modified')
    if lastmod:
        status, reason, msg = _httputil.valid_status(response.status)
        
        request = cherrypy.serving.request
        
        since = request.headers.get('If-Unmodified-Since')
        if since and since != lastmod:
            if (status >= 200 and status <= 299) or status == 412:
                raise cherrypy.HTTPError(412)
        
        since = request.headers.get('If-Modified-Since')
        if since and since == lastmod:
            if (status >= 200 and status <= 299) or status == 304:
                if request.method in ("GET", "HEAD"):
                    raise cherrypy.HTTPRedirect([], 304)
                else:
                    raise cherrypy.HTTPError(412)


#                                Tool code                                #

def allow(methods=None, debug=False):
    """Raise 405 if request.method not in methods (default ['GET', 'HEAD']).
    
    The given methods are case-insensitive, and may be in any order.
    If only one method is allowed, you may supply a single string;
    if more than one, supply a list of strings.
    
    Regardless of whether the current method is allowed or not, this
    also emits an 'Allow' response header, containing the given methods.
    """
    if not isinstance(methods, (tuple, list)):
        methods = [methods]
    methods = [m.upper() for m in methods if m]
    if not methods:
        methods = ['GET', 'HEAD']
    elif 'GET' in methods and 'HEAD' not in methods:
        methods.append('HEAD')
    
    cherrypy.response.headers['Allow'] = ', '.join(methods)
    if cherrypy.request.method not in methods:
        if debug:
            cherrypy.log('request.method %r not in methods %r' %
                         (cherrypy.request.method, methods), 'TOOLS.ALLOW')
        raise cherrypy.HTTPError(405)
    else:
        if debug:
            cherrypy.log('request.method %r in methods %r' %
                         (cherrypy.request.method, methods), 'TOOLS.ALLOW')


def proxy(base=None, local='X-Forwarded-Host', remote='X-Forwarded-For',
          scheme='X-Forwarded-Proto', debug=False):
    """Change the base URL (scheme://host[:port][/path]).
    
    For running a CP server behind Apache, lighttpd, or other HTTP server.
    
    For Apache and lighttpd, you should leave the 'local' argument at the
    default value of 'X-Forwarded-Host'. For Squid, you probably want to set
    tools.proxy.local = 'Origin'.
    
    If you want the new request.base to include path info (not just the host),
    you must explicitly set base to the full base path, and ALSO set 'local'
    to '', so that the X-Forwarded-Host request header (which never includes
    path info) does not override it. Regardless, the value for 'base' MUST
    NOT end in a slash.
    
    cherrypy.request.remote.ip (the IP address of the client) will be
    rewritten if the header specified by the 'remote' arg is valid.
    By default, 'remote' is set to 'X-Forwarded-For'. If you do not
    want to rewrite remote.ip, set the 'remote' arg to an empty string.
    """
    
    request = cherrypy.serving.request
    
    if scheme:
        s = request.headers.get(scheme, None)
        if debug:
            cherrypy.log('Testing scheme %r:%r' % (scheme, s), 'TOOLS.PROXY')
        if s == 'on' and 'ssl' in scheme.lower():
            # This handles e.g. webfaction's 'X-Forwarded-Ssl: on' header
            scheme = 'https'
        else:
            # This is for lighttpd/pound/Mongrel's 'X-Forwarded-Proto: https'
            scheme = s
    if not scheme:
        scheme = request.base[:request.base.find("://")]
    
    if local:
        lbase = request.headers.get(local, None)
        if debug:
            cherrypy.log('Testing local %r:%r' % (local, lbase), 'TOOLS.PROXY')
        if lbase is not None:
            base = lbase.split(',')[0]
    if not base:
        port = request.local.port
        if port == 80:
            base = '127.0.0.1'
        else:
            base = '127.0.0.1:%s' % port
    
    if base.find("://") == -1:
        # add http:// or https:// if needed
        base = scheme + "://" + base
    
    request.base = base
    
    if remote:
        xff = request.headers.get(remote)
        if debug:
            cherrypy.log('Testing remote %r:%r' % (remote, xff), 'TOOLS.PROXY')
        if xff:
            if remote == 'X-Forwarded-For':
                # See http://bob.pythonmac.org/archives/2005/09/23/apache-x-forwarded-for-caveat/
                xff = xff.split(',')[-1].strip()
            request.remote.ip = xff


def ignore_headers(headers=('Range',), debug=False):
    """Delete request headers whose field names are included in 'headers'.
    
    This is a useful tool for working behind certain HTTP servers;
    for example, Apache duplicates the work that CP does for 'Range'
    headers, and will doubly-truncate the response.
    """
    request = cherrypy.serving.request
    for name in headers:
        if name in request.headers:
            if debug:
                cherrypy.log('Ignoring request header %r' % name,
                             'TOOLS.IGNORE_HEADERS')
            del request.headers[name]


def response_headers(headers=None, debug=False):
    """Set headers on the response."""
    if debug:
        cherrypy.log('Setting response headers: %s' % repr(headers),
                     'TOOLS.RESPONSE_HEADERS')
    for name, value in (headers or []):
        cherrypy.serving.response.headers[name] = value
response_headers.failsafe = True


def referer(pattern, accept=True, accept_missing=False, error=403,
            message='Forbidden Referer header.', debug=False):
    """Raise HTTPError if Referer header does/does not match the given pattern.
    
    pattern
        A regular expression pattern to test against the Referer.
        
    accept
        If True, the Referer must match the pattern; if False,
        the Referer must NOT match the pattern.

    accept_missing
        If True, permit requests with no Referer header.

    error
        The HTTP error code to return to the client on failure.
        
    message
        A string to include in the response body on failure.
    
    """
    try:
        ref = cherrypy.serving.request.headers['Referer']
        match = bool(re.match(pattern, ref))
        if debug:
            cherrypy.log('Referer %r matches %r' % (ref, pattern),
                         'TOOLS.REFERER')
        if accept == match:
            return
    except KeyError:
        if debug:
            cherrypy.log('No Referer header', 'TOOLS.REFERER')
        if accept_missing:
            return
    
    raise cherrypy.HTTPError(error, message)


class SessionAuth(object):
    """Assert that the user is logged in."""
    
    session_key = "username"
    debug = False
    
    def check_username_and_password(self, username, password):
        pass
    
    def anonymous(self):
        """Provide a temporary user name for anonymous users."""
        pass
    
    def on_login(self, username):
        pass
    
    def on_logout(self, username):
        pass
    
    def on_check(self, username):
        pass
    
    def login_screen(self, from_page='..', username='', error_msg='', **kwargs):
        return ntob("""<html><body>
Message: %(error_msg)s
<form method="post" action="do_login">
    Login: <input type="text" name="username" value="%(username)s" size="10" /><br />
    Password: <input type="password" name="password" size="10" /><br />
    <input type="hidden" name="from_page" value="%(from_page)s" /><br />
    <input type="submit" />
</form>
</body></html>""" % {'from_page': from_page, 'username': username,
                     'error_msg': error_msg}, "utf-8")
    
    def do_login(self, username, password, from_page='..', **kwargs):
        """Login. May raise redirect, or return True if request handled."""
        response = cherrypy.serving.response
        error_msg = self.check_username_and_password(username, password)
        if error_msg:
            body = self.login_screen(from_page, username, error_msg)
            response.body = body
            if "Content-Length" in response.headers:
                # Delete Content-Length header so finalize() recalcs it.
                del response.headers["Content-Length"]
            return True
        else:
            cherrypy.serving.request.login = username
            cherrypy.session[self.session_key] = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")
    
    def do_logout(self, from_page='..', **kwargs):
        """Logout. May raise redirect, or return True if request handled."""
        sess = cherrypy.session
        username = sess.get(self.session_key)
        sess[self.session_key] = None
        if username:
            cherrypy.serving.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page)
    
    def do_check(self):
        """Assert username. May raise redirect, or return True if request handled."""
        sess = cherrypy.session
        request = cherrypy.serving.request
        response = cherrypy.serving.response
        
        username = sess.get(self.session_key)
        if not username:
            sess[self.session_key] = username = self.anonymous()
            if self.debug:
                cherrypy.log('No session[username], trying anonymous', 'TOOLS.SESSAUTH')
        if not username:
            url = cherrypy.url(qs=request.query_string)
            if self.debug:
                cherrypy.log('No username, routing to login_screen with '
                             'from_page %r' % url, 'TOOLS.SESSAUTH')
            response.body = self.login_screen(url)
            if "Content-Length" in response.headers:
                # Delete Content-Length header so finalize() recalcs it.
                del response.headers["Content-Length"]
            return True
        if self.debug:
            cherrypy.log('Setting request.login to %r' % username, 'TOOLS.SESSAUTH')
        request.login = username
        self.on_check(username)
    
    def run(self):
        request = cherrypy.serving.request
        response = cherrypy.serving.response
        
        path = request.path_info
        if path.endswith('login_screen'):
            if self.debug:
                cherrypy.log('routing %r to login_screen' % path, 'TOOLS.SESSAUTH')
            return self.login_screen(**request.params)
        elif path.endswith('do_login'):
            if request.method != 'POST':
                response.headers['Allow'] = "POST"
                if self.debug:
                    cherrypy.log('do_login requires POST', 'TOOLS.SESSAUTH')
                raise cherrypy.HTTPError(405)
            if self.debug:
                cherrypy.log('routing %r to do_login' % path, 'TOOLS.SESSAUTH')
            return self.do_login(**request.params)
        elif path.endswith('do_logout'):
            if request.method != 'POST':
                response.headers['Allow'] = "POST"
                raise cherrypy.HTTPError(405)
            if self.debug:
                cherrypy.log('routing %r to do_logout' % path, 'TOOLS.SESSAUTH')
            return self.do_logout(**request.params)
        else:
            if self.debug:
                cherrypy.log('No special path, running do_check', 'TOOLS.SESSAUTH')
            return self.do_check()


def session_auth(**kwargs):
    sa = SessionAuth()
    for k, v in kwargs.items():
        setattr(sa, k, v)
    return sa.run()
session_auth.__doc__ = """Session authentication hook.

Any attribute of the SessionAuth class may be overridden via a keyword arg
to this function:

""" + "\n".join(["%s: %s" % (k, type(getattr(SessionAuth, k)).__name__)
                 for k in dir(SessionAuth) if not k.startswith("__")])


def log_traceback(severity=logging.ERROR, debug=False):
    """Write the last error's traceback to the cherrypy error log."""
    cherrypy.log("", "HTTP", severity=severity, traceback=True)

def log_request_headers(debug=False):
    """Write request headers to the cherrypy error log."""
    h = ["  %s: %s" % (k, v) for k, v in cherrypy.serving.request.header_list]
    cherrypy.log('\nRequest Headers:\n' + '\n'.join(h), "HTTP")

def log_hooks(debug=False):
    """Write request.hooks to the cherrypy error log."""
    request = cherrypy.serving.request
    
    msg = []
    # Sort by the standard points if possible.
    from cherrypy import _cprequest
    points = _cprequest.hookpoints
    for k in request.hooks.keys():
        if k not in points:
            points.append(k)
    
    for k in points:
        msg.append("    %s:" % k)
        v = request.hooks.get(k, [])
        v.sort()
        for h in v:
            msg.append("        %r" % h)
    cherrypy.log('\nRequest Hooks for ' + cherrypy.url() +
                 ':\n' + '\n'.join(msg), "HTTP")

def redirect(url='', internal=True, debug=False):
    """Raise InternalRedirect or HTTPRedirect to the given url."""
    if debug:
        cherrypy.log('Redirecting %sto: %s' %
                     ({True: 'internal ', False: ''}[internal], url),
                     'TOOLS.REDIRECT')
    if internal:
        raise cherrypy.InternalRedirect(url)
    else:
        raise cherrypy.HTTPRedirect(url)

def trailing_slash(missing=True, extra=False, status=None, debug=False):
    """Redirect if path_info has (missing|extra) trailing slash."""
    request = cherrypy.serving.request
    pi = request.path_info
    
    if debug:
        cherrypy.log('is_index: %r, missing: %r, extra: %r, path_info: %r' %
                     (request.is_index, missing, extra, pi),
                     'TOOLS.TRAILING_SLASH')
    if request.is_index is True:
        if missing:
            if not pi.endswith('/'):
                new_url = cherrypy.url(pi + '/', request.query_string)
                raise cherrypy.HTTPRedirect(new_url, status=status or 301)
    elif request.is_index is False:
        if extra:
            # If pi == '/', don't redirect to ''!
            if pi.endswith('/') and pi != '/':
                new_url = cherrypy.url(pi[:-1], request.query_string)
                raise cherrypy.HTTPRedirect(new_url, status=status or 301)

def flatten(debug=False):
    """Wrap response.body in a generator that recursively iterates over body.
    
    This allows cherrypy.response.body to consist of 'nested generators';
    that is, a set of generators that yield generators.
    """
    import types
    def flattener(input):
        numchunks = 0
        for x in input:
            if not isinstance(x, types.GeneratorType):
                numchunks += 1
                yield x
            else:
                for y in flattener(x):
                    numchunks += 1
                    yield y
        if debug:
            cherrypy.log('Flattened %d chunks' % numchunks, 'TOOLS.FLATTEN')
    response = cherrypy.serving.response
    response.body = flattener(response.body)


def accept(media=None, debug=False):
    """Return the client's preferred media-type (from the given Content-Types).
    
    If 'media' is None (the default), no test will be performed.
    
    If 'media' is provided, it should be the Content-Type value (as a string)
    or values (as a list or tuple of strings) which the current resource
    can emit. The client's acceptable media ranges (as declared in the
    Accept request header) will be matched in order to these Content-Type
    values; the first such string is returned. That is, the return value
    will always be one of the strings provided in the 'media' arg (or None
    if 'media' is None).
    
    If no match is found, then HTTPError 406 (Not Acceptable) is raised.
    Note that most web browsers send */* as a (low-quality) acceptable
    media range, which should match any Content-Type. In addition, "...if
    no Accept header field is present, then it is assumed that the client
    accepts all media types."
    
    Matching types are checked in order of client preference first,
    and then in the order of the given 'media' values.
    
    Note that this function does not honor accept-params (other than "q").
    """
    if not media:
        return
    if isinstance(media, basestring):
        media = [media]
    request = cherrypy.serving.request
    
    # Parse the Accept request header, and try to match one
    # of the requested media-ranges (in order of preference).
    ranges = request.headers.elements('Accept')
    if not ranges:
        # Any media type is acceptable.
        if debug:
            cherrypy.log('No Accept header elements', 'TOOLS.ACCEPT')
        return media[0]
    else:
        # Note that 'ranges' is sorted in order of preference
        for element in ranges:
            if element.qvalue > 0:
                if element.value == "*/*":
                    # Matches any type or subtype
                    if debug:
                        cherrypy.log('Match due to */*', 'TOOLS.ACCEPT')
                    return media[0]
                elif element.value.endswith("/*"):
                    # Matches any subtype
                    mtype = element.value[:-1]  # Keep the slash
                    for m in media:
                        if m.startswith(mtype):
                            if debug:
                                cherrypy.log('Match due to %s' % element.value,
                                             'TOOLS.ACCEPT')
                            return m
                else:
                    # Matches exact value
                    if element.value in media:
                        if debug:
                            cherrypy.log('Match due to %s' % element.value,
                                         'TOOLS.ACCEPT')
                        return element.value
    
    # No suitable media-range found.
    ah = request.headers.get('Accept')
    if ah is None:
        msg = "Your client did not send an Accept header."
    else:
        msg = "Your client sent this Accept header: %s." % ah
    msg += (" But this resource only emits these media types: %s." %
            ", ".join(media))
    raise cherrypy.HTTPError(406, msg)


class MonitoredHeaderMap(_httputil.HeaderMap):
    
    def __init__(self):
        self.accessed_headers = set()
    
    def __getitem__(self, key):
        self.accessed_headers.add(key)
        return _httputil.HeaderMap.__getitem__(self, key)
    
    def __contains__(self, key):
        self.accessed_headers.add(key)
        return _httputil.HeaderMap.__contains__(self, key)
    
    def get(self, key, default=None):
        self.accessed_headers.add(key)
        return _httputil.HeaderMap.get(self, key, default=default)
    
    if hasattr({}, 'has_key'):
        # Python 2
        def has_key(self, key):
            self.accessed_headers.add(key)
            return _httputil.HeaderMap.has_key(self, key)


def autovary(ignore=None, debug=False):
    """Auto-populate the Vary response header based on request.header access."""
    request = cherrypy.serving.request
    
    req_h = request.headers
    request.headers = MonitoredHeaderMap()
    request.headers.update(req_h)
    if ignore is None:
        ignore = set(['Content-Disposition', 'Content-Length', 'Content-Type'])
    
    def set_response_header():
        resp_h = cherrypy.serving.response.headers
        v = set([e.value for e in resp_h.elements('Vary')])
        if debug:
            cherrypy.log('Accessed headers: %s' % request.headers.accessed_headers,
                         'TOOLS.AUTOVARY')
        v = v.union(request.headers.accessed_headers)
        v = v.difference(ignore)
        v = list(v)
        v.sort()
        resp_h['Vary'] = ', '.join(v)
    request.hooks.attach('before_finalize', set_response_header, 95)


########NEW FILE########
__FILENAME__ = encoding
import struct
import time

import cherrypy
from cherrypy._cpcompat import basestring, BytesIO, ntob, set, unicodestr
from cherrypy.lib import file_generator
from cherrypy.lib import set_vary_header


def decode(encoding=None, default_encoding='utf-8'):
    """Replace or extend the list of charsets used to decode a request entity.
    
    Either argument may be a single string or a list of strings.
    
    encoding
        If not None, restricts the set of charsets attempted while decoding
        a request entity to the given set (even if a different charset is given in
        the Content-Type request header).
    
    default_encoding
        Only in effect if the 'encoding' argument is not given.
        If given, the set of charsets attempted while decoding a request entity is
        *extended* with the given value(s).
    
    """
    body = cherrypy.request.body
    if encoding is not None:
        if not isinstance(encoding, list):
            encoding = [encoding]
        body.attempt_charsets = encoding
    elif default_encoding:
        if not isinstance(default_encoding, list):
            default_encoding = [default_encoding]
        body.attempt_charsets = body.attempt_charsets + default_encoding


class ResponseEncoder:
    
    default_encoding = 'utf-8'
    failmsg = "Response body could not be encoded with %r."
    encoding = None
    errors = 'strict'
    text_only = True
    add_charset = True
    debug = False
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        self.attempted_charsets = set()
        request = cherrypy.serving.request
        if request.handler is not None:
            # Replace request.handler with self
            if self.debug:
                cherrypy.log('Replacing request.handler', 'TOOLS.ENCODE')
            self.oldhandler = request.handler
            request.handler = self
    
    def encode_stream(self, encoding):
        """Encode a streaming response body.
        
        Use a generator wrapper, and just pray it works as the stream is
        being written out.
        """
        if encoding in self.attempted_charsets:
            return False
        self.attempted_charsets.add(encoding)
        
        def encoder(body):
            for chunk in body:
                if isinstance(chunk, unicodestr):
                    chunk = chunk.encode(encoding, self.errors)
                yield chunk
        self.body = encoder(self.body)
        return True
    
    def encode_string(self, encoding):
        """Encode a buffered response body."""
        if encoding in self.attempted_charsets:
            return False
        self.attempted_charsets.add(encoding)
        
        try:
            body = []
            for chunk in self.body:
                if isinstance(chunk, unicodestr):
                    chunk = chunk.encode(encoding, self.errors)
                body.append(chunk)
            self.body = body
        except (LookupError, UnicodeError):
            return False
        else:
            return True
    
    def find_acceptable_charset(self):
        request = cherrypy.serving.request
        response = cherrypy.serving.response
        
        if self.debug:
            cherrypy.log('response.stream %r' % response.stream, 'TOOLS.ENCODE')
        if response.stream:
            encoder = self.encode_stream
        else:
            encoder = self.encode_string
            if "Content-Length" in response.headers:
                # Delete Content-Length header so finalize() recalcs it.
                # Encoded strings may be of different lengths from their
                # unicode equivalents, and even from each other. For example:
                # >>> t = u"\u7007\u3040"
                # >>> len(t)
                # 2
                # >>> len(t.encode("UTF-8"))
                # 6
                # >>> len(t.encode("utf7"))
                # 8
                del response.headers["Content-Length"]
        
        # Parse the Accept-Charset request header, and try to provide one
        # of the requested charsets (in order of user preference).
        encs = request.headers.elements('Accept-Charset')
        charsets = [enc.value.lower() for enc in encs]
        if self.debug:
            cherrypy.log('charsets %s' % repr(charsets), 'TOOLS.ENCODE')
        
        if self.encoding is not None:
            # If specified, force this encoding to be used, or fail.
            encoding = self.encoding.lower()
            if self.debug:
                cherrypy.log('Specified encoding %r' % encoding, 'TOOLS.ENCODE')
            if (not charsets) or "*" in charsets or encoding in charsets:
                if self.debug:
                    cherrypy.log('Attempting encoding %r' % encoding, 'TOOLS.ENCODE')
                if encoder(encoding):
                    return encoding
        else:
            if not encs:
                if self.debug:
                    cherrypy.log('Attempting default encoding %r' %
                                 self.default_encoding, 'TOOLS.ENCODE')
                # Any character-set is acceptable.
                if encoder(self.default_encoding):
                    return self.default_encoding
                else:
                    raise cherrypy.HTTPError(500, self.failmsg % self.default_encoding)
            else:
                for element in encs:
                    if element.qvalue > 0:
                        if element.value == "*":
                            # Matches any charset. Try our default.
                            if self.debug:
                                cherrypy.log('Attempting default encoding due '
                                             'to %r' % element, 'TOOLS.ENCODE')
                            if encoder(self.default_encoding):
                                return self.default_encoding
                        else:
                            encoding = element.value
                            if self.debug:
                                cherrypy.log('Attempting encoding %s (qvalue >'
                                             '0)' % element, 'TOOLS.ENCODE')
                            if encoder(encoding):
                                return encoding
                
                if "*" not in charsets:
                    # If no "*" is present in an Accept-Charset field, then all
                    # character sets not explicitly mentioned get a quality
                    # value of 0, except for ISO-8859-1, which gets a quality
                    # value of 1 if not explicitly mentioned.
                    iso = 'iso-8859-1'
                    if iso not in charsets:
                        if self.debug:
                            cherrypy.log('Attempting ISO-8859-1 encoding',
                                         'TOOLS.ENCODE')
                        if encoder(iso):
                            return iso
        
        # No suitable encoding found.
        ac = request.headers.get('Accept-Charset')
        if ac is None:
            msg = "Your client did not send an Accept-Charset header."
        else:
            msg = "Your client sent this Accept-Charset header: %s." % ac
        msg += " We tried these charsets: %s." % ", ".join(self.attempted_charsets)
        raise cherrypy.HTTPError(406, msg)
    
    def __call__(self, *args, **kwargs):
        response = cherrypy.serving.response
        self.body = self.oldhandler(*args, **kwargs)
        
        if isinstance(self.body, basestring):
            # strings get wrapped in a list because iterating over a single
            # item list is much faster than iterating over every character
            # in a long string.
            if self.body:
                self.body = [self.body]
            else:
                # [''] doesn't evaluate to False, so replace it with [].
                self.body = []
        elif hasattr(self.body, 'read'):
            self.body = file_generator(self.body)
        elif self.body is None:
            self.body = []
        
        ct = response.headers.elements("Content-Type")
        if self.debug:
            cherrypy.log('Content-Type: %r' % [str(h) for h in ct], 'TOOLS.ENCODE')
        if ct:
            ct = ct[0]
            if self.text_only:
                if ct.value.lower().startswith("text/"):
                    if self.debug:
                        cherrypy.log('Content-Type %s starts with "text/"' % ct,
                                     'TOOLS.ENCODE')
                    do_find = True
                else:
                    if self.debug:
                        cherrypy.log('Not finding because Content-Type %s does '
                                     'not start with "text/"' % ct,
                                     'TOOLS.ENCODE')
                    do_find = False
            else:
                if self.debug:
                    cherrypy.log('Finding because not text_only', 'TOOLS.ENCODE')
                do_find = True
            
            if do_find:
                # Set "charset=..." param on response Content-Type header
                ct.params['charset'] = self.find_acceptable_charset()
                if self.add_charset:
                    if self.debug:
                        cherrypy.log('Setting Content-Type %s' % ct,
                                     'TOOLS.ENCODE')
                    response.headers["Content-Type"] = str(ct)
        
        return self.body

# GZIP

def compress(body, compress_level):
    """Compress 'body' at the given compress_level."""
    import zlib
    
    # See http://www.gzip.org/zlib/rfc-gzip.html
    yield ntob('\x1f\x8b')       # ID1 and ID2: gzip marker
    yield ntob('\x08')           # CM: compression method
    yield ntob('\x00')           # FLG: none set
    # MTIME: 4 bytes
    yield struct.pack("<L", int(time.time()) & int('FFFFFFFF', 16))
    yield ntob('\x02')           # XFL: max compression, slowest algo
    yield ntob('\xff')           # OS: unknown
    
    crc = zlib.crc32(ntob(""))
    size = 0
    zobj = zlib.compressobj(compress_level,
                            zlib.DEFLATED, -zlib.MAX_WBITS,
                            zlib.DEF_MEM_LEVEL, 0)
    for line in body:
        size += len(line)
        crc = zlib.crc32(line, crc)
        yield zobj.compress(line)
    yield zobj.flush()
    
    # CRC32: 4 bytes
    yield struct.pack("<L", crc & int('FFFFFFFF', 16))
    # ISIZE: 4 bytes
    yield struct.pack("<L", size & int('FFFFFFFF', 16))

def decompress(body):
    import gzip
    
    zbuf = BytesIO()
    zbuf.write(body)
    zbuf.seek(0)
    zfile = gzip.GzipFile(mode='rb', fileobj=zbuf)
    data = zfile.read()
    zfile.close()
    return data


def gzip(compress_level=5, mime_types=['text/html', 'text/plain'], debug=False):
    """Try to gzip the response body if Content-Type in mime_types.
    
    cherrypy.response.headers['Content-Type'] must be set to one of the
    values in the mime_types arg before calling this function.

    The provided list of mime-types must be of one of the following form:
        * type/subtype
        * type/*
        * type/*+subtype
    
    No compression is performed if any of the following hold:
        * The client sends no Accept-Encoding request header
        * No 'gzip' or 'x-gzip' is present in the Accept-Encoding header
        * No 'gzip' or 'x-gzip' with a qvalue > 0 is present
        * The 'identity' value is given with a qvalue > 0.
    
    """
    request = cherrypy.serving.request
    response = cherrypy.serving.response
    
    set_vary_header(response, "Accept-Encoding")
    
    if not response.body:
        # Response body is empty (might be a 304 for instance)
        if debug:
            cherrypy.log('No response body', context='TOOLS.GZIP')
        return
    
    # If returning cached content (which should already have been gzipped),
    # don't re-zip.
    if getattr(request, "cached", False):
        if debug:
            cherrypy.log('Not gzipping cached response', context='TOOLS.GZIP')
        return
    
    acceptable = request.headers.elements('Accept-Encoding')
    if not acceptable:
        # If no Accept-Encoding field is present in a request,
        # the server MAY assume that the client will accept any
        # content coding. In this case, if "identity" is one of
        # the available content-codings, then the server SHOULD use
        # the "identity" content-coding, unless it has additional
        # information that a different content-coding is meaningful
        # to the client.
        if debug:
            cherrypy.log('No Accept-Encoding', context='TOOLS.GZIP')
        return
    
    ct = response.headers.get('Content-Type', '').split(';')[0]
    for coding in acceptable:
        if coding.value == 'identity' and coding.qvalue != 0:
            if debug:
                cherrypy.log('Non-zero identity qvalue: %s' % coding,
                             context='TOOLS.GZIP')
            return
        if coding.value in ('gzip', 'x-gzip'):
            if coding.qvalue == 0:
                if debug:
                    cherrypy.log('Zero gzip qvalue: %s' % coding,
                                 context='TOOLS.GZIP')
                return
            
            if ct not in mime_types:
                # If the list of provided mime-types contains tokens
                # such as 'text/*' or 'application/*+xml',
                # we go through them and find the most appropriate one
                # based on the given content-type.
                # The pattern matching is only caring about the most
                # common cases, as stated above, and doesn't support
                # for extra parameters.
                found = False
                if '/' in ct:
                    ct_media_type, ct_sub_type = ct.split('/')
                    for mime_type in mime_types:
                        if '/' in mime_type:
                            media_type, sub_type = mime_type.split('/')
                            if ct_media_type == media_type:
                                if sub_type == '*':
                                    found = True
                                    break
                                elif '+' in sub_type and '+' in ct_sub_type:
                                    ct_left, ct_right = ct_sub_type.split('+')
                                    left, right = sub_type.split('+')
                                    if left == '*' and ct_right == right:
                                        found = True
                                        break

                if not found:
                    if debug:
                        cherrypy.log('Content-Type %s not in mime_types %r' %
                                     (ct, mime_types), context='TOOLS.GZIP')
                    return
            
            if debug:
                cherrypy.log('Gzipping', context='TOOLS.GZIP')
            # Return a generator that compresses the page
            response.headers['Content-Encoding'] = 'gzip'
            response.body = compress(response.body, compress_level)
            if "Content-Length" in response.headers:
                # Delete Content-Length header so finalize() recalcs it.
                del response.headers["Content-Length"]
            
            return
    
    if debug:
        cherrypy.log('No acceptable encoding found.', context='GZIP')
    cherrypy.HTTPError(406, "identity, gzip").set_response()


########NEW FILE########
__FILENAME__ = gctools
import gc
import inspect
import os
import sys
import time
 
try:
    import objgraph
except ImportError:
    objgraph = None

import cherrypy
from cherrypy import _cprequest, _cpwsgi
from cherrypy.process.plugins import SimplePlugin


class ReferrerTree(object):
    """An object which gathers all referrers of an object to a given depth."""

    peek_length = 40

    def __init__(self, ignore=None, maxdepth=2, maxparents=10):
        self.ignore = ignore or []
        self.ignore.append(inspect.currentframe().f_back)
        self.maxdepth = maxdepth
        self.maxparents = maxparents

    def ascend(self, obj, depth=1):
        """Return a nested list containing referrers of the given object."""
        depth += 1
        parents = []

        # Gather all referrers in one step to minimize
        # cascading references due to repr() logic.
        refs = gc.get_referrers(obj)
        self.ignore.append(refs)
        if len(refs) > self.maxparents:
            return [("[%s referrers]" % len(refs), [])]

        try:
            ascendcode = self.ascend.__code__
        except AttributeError:
            ascendcode = self.ascend.im_func.func_code
        for parent in refs:
            if inspect.isframe(parent) and parent.f_code is ascendcode:
                continue
            if parent in self.ignore:
                continue
            if depth <= self.maxdepth:
                parents.append((parent, self.ascend(parent, depth)))
            else:
                parents.append((parent, []))

        return parents

    def peek(self, s):
        """Return s, restricted to a sane length."""
        if len(s) > (self.peek_length + 3):
            half = self.peek_length // 2
            return s[:half] + '...' + s[-half:]
        else:
            return s

    def _format(self, obj, descend=True):
        """Return a string representation of a single object."""
        if inspect.isframe(obj):
            filename, lineno, func, context, index = inspect.getframeinfo(obj)
            return "<frame of function '%s'>" % func

        if not descend:
            return self.peek(repr(obj))

        if isinstance(obj, dict):
            return "{" + ", ".join(["%s: %s" % (self._format(k, descend=False),
                                                self._format(v, descend=False))
                                    for k, v in obj.items()]) + "}"
        elif isinstance(obj, list):
            return "[" + ", ".join([self._format(item, descend=False)
                                    for item in obj]) + "]"
        elif isinstance(obj, tuple):
            return "(" + ", ".join([self._format(item, descend=False)
                                    for item in obj]) + ")"

        r = self.peek(repr(obj))
        if isinstance(obj, (str, int, float)):
            return r
        return "%s: %s" % (type(obj), r)

    def format(self, tree):
        """Return a list of string reprs from a nested list of referrers."""
        output = []
        def ascend(branch, depth=1):
            for parent, grandparents in branch:
                output.append(("    " * depth) + self._format(parent))
                if grandparents:
                    ascend(grandparents, depth + 1)
        ascend(tree)
        return output


def get_instances(cls):
    return [x for x in gc.get_objects() if isinstance(x, cls)]


class RequestCounter(SimplePlugin):
    
    def start(self):
        self.count = 0
    
    def before_request(self):
        self.count += 1
    
    def after_request(self):
        self.count -=1
request_counter = RequestCounter(cherrypy.engine)
request_counter.subscribe()


def get_context(obj):
    if isinstance(obj, _cprequest.Request):
        return "path=%s;stage=%s" % (obj.path_info, obj.stage)
    elif isinstance(obj, _cprequest.Response):
        return "status=%s" % obj.status
    elif isinstance(obj, _cpwsgi.AppResponse):
        return "PATH_INFO=%s" % obj.environ.get('PATH_INFO', '')
    elif hasattr(obj, "tb_lineno"):
        return "tb_lineno=%s" % obj.tb_lineno
    return ""


class GCRoot(object):
    """A CherryPy page handler for testing reference leaks."""

    classes = [(_cprequest.Request, 2, 2,
                "Should be 1 in this request thread and 1 in the main thread."),
               (_cprequest.Response, 2, 2,
                "Should be 1 in this request thread and 1 in the main thread."),
               (_cpwsgi.AppResponse, 1, 1,
                "Should be 1 in this request thread only."),
               ]

    def index(self):
        return "Hello, world!"
    index.exposed = True

    def stats(self):
        output = ["Statistics:"]
        
        for trial in range(10):
            if request_counter.count > 0:
                break
            time.sleep(0.5)
        else:
            output.append("\nNot all requests closed properly.")
        
        # gc_collect isn't perfectly synchronous, because it may
        # break reference cycles that then take time to fully
        # finalize. Call it thrice and hope for the best.
        gc.collect()
        gc.collect()
        unreachable = gc.collect()
        if unreachable:
            if objgraph is not None:
                final = objgraph.by_type('Nondestructible')
                if final:
                    objgraph.show_backrefs(final, filename='finalizers.png')

            trash = {}
            for x in gc.garbage:
                trash[type(x)] = trash.get(type(x), 0) + 1
            if trash:
                output.insert(0, "\n%s unreachable objects:" % unreachable)
                trash = [(v, k) for k, v in trash.items()]
                trash.sort()
                for pair in trash:
                    output.append("    " + repr(pair))

        # Check declared classes to verify uncollected instances.
        # These don't have to be part of a cycle; they can be
        # any objects that have unanticipated referrers that keep
        # them from being collected.
        allobjs = {}
        for cls, minobj, maxobj, msg in self.classes:
            allobjs[cls] = get_instances(cls)

        for cls, minobj, maxobj, msg in self.classes:
            objs = allobjs[cls]
            lenobj = len(objs)
            if lenobj < minobj or lenobj > maxobj:
                if minobj == maxobj:
                    output.append(
                        "\nExpected %s %r references, got %s." %
                        (minobj, cls, lenobj))
                else:
                    output.append(
                        "\nExpected %s to %s %r references, got %s." %
                        (minobj, maxobj, cls, lenobj))

                for obj in objs:
                    if objgraph is not None:
                        ig = [id(objs), id(inspect.currentframe())]
                        fname = "graph_%s_%s.png" % (cls.__name__, id(obj))
                        objgraph.show_backrefs(
                            obj, extra_ignore=ig, max_depth=4, too_many=20,
                            filename=fname, extra_info=get_context)
                    output.append("\nReferrers for %s (refcount=%s):" %
                                  (repr(obj), sys.getrefcount(obj)))
                    t = ReferrerTree(ignore=[objs], maxdepth=3)
                    tree = t.ascend(obj)
                    output.extend(t.format(tree))
        
        return "\n".join(output)
    stats.exposed = True


########NEW FILE########
__FILENAME__ = http
import warnings
warnings.warn('cherrypy.lib.http has been deprecated and will be removed '
              'in CherryPy 3.3 use cherrypy.lib.httputil instead.',
              DeprecationWarning)

from cherrypy.lib.httputil import *


########NEW FILE########
__FILENAME__ = httpauth
"""
This module defines functions to implement HTTP Digest Authentication (:rfc:`2617`).
This has full compliance with 'Digest' and 'Basic' authentication methods. In
'Digest' it supports both MD5 and MD5-sess algorithms.

Usage:
    First use 'doAuth' to request the client authentication for a
    certain resource. You should send an httplib.UNAUTHORIZED response to the
    client so he knows he has to authenticate itself.
    
    Then use 'parseAuthorization' to retrieve the 'auth_map' used in
    'checkResponse'.

    To use 'checkResponse' you must have already verified the password associated
    with the 'username' key in 'auth_map' dict. Then you use the 'checkResponse'
    function to verify if the password matches the one sent by the client.

SUPPORTED_ALGORITHM - list of supported 'Digest' algorithms
SUPPORTED_QOP - list of supported 'Digest' 'qop'.
"""
__version__ = 1, 0, 1
__author__ = "Tiago Cogumbreiro <cogumbreiro@users.sf.net>"
__credits__ = """
    Peter van Kampen for its recipe which implement most of Digest authentication:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/302378
"""

__license__ = """
Copyright (c) 2005, Tiago Cogumbreiro <cogumbreiro@users.sf.net>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * Neither the name of Sylvain Hellegouarch nor the names of his contributors 
      may be used to endorse or promote products derived from this software 
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__all__ = ("digestAuth", "basicAuth", "doAuth", "checkResponse",
           "parseAuthorization", "SUPPORTED_ALGORITHM", "md5SessionKey",
           "calculateNonce", "SUPPORTED_QOP")

################################################################################
import time
from cherrypy._cpcompat import base64_decode, ntob, md5
from cherrypy._cpcompat import parse_http_list, parse_keqv_list

MD5 = "MD5"
MD5_SESS = "MD5-sess"
AUTH = "auth"
AUTH_INT = "auth-int"

SUPPORTED_ALGORITHM = (MD5, MD5_SESS)
SUPPORTED_QOP = (AUTH, AUTH_INT)

################################################################################
# doAuth
#
DIGEST_AUTH_ENCODERS = {
    MD5: lambda val: md5(ntob(val)).hexdigest(),
    MD5_SESS: lambda val: md5(ntob(val)).hexdigest(),
#    SHA: lambda val: sha.new(ntob(val)).hexdigest (),
}

def calculateNonce (realm, algorithm = MD5):
    """This is an auxaliary function that calculates 'nonce' value. It is used
    to handle sessions."""

    global SUPPORTED_ALGORITHM, DIGEST_AUTH_ENCODERS
    assert algorithm in SUPPORTED_ALGORITHM

    try:
        encoder = DIGEST_AUTH_ENCODERS[algorithm]
    except KeyError:
        raise NotImplementedError ("The chosen algorithm (%s) does not have "\
                                   "an implementation yet" % algorithm)

    return encoder ("%d:%s" % (time.time(), realm))

def digestAuth (realm, algorithm = MD5, nonce = None, qop = AUTH):
    """Challenges the client for a Digest authentication."""
    global SUPPORTED_ALGORITHM, DIGEST_AUTH_ENCODERS, SUPPORTED_QOP
    assert algorithm in SUPPORTED_ALGORITHM
    assert qop in SUPPORTED_QOP

    if nonce is None:
        nonce = calculateNonce (realm, algorithm)

    return 'Digest realm="%s", nonce="%s", algorithm="%s", qop="%s"' % (
        realm, nonce, algorithm, qop
    )

def basicAuth (realm):
    """Challengenes the client for a Basic authentication."""
    assert '"' not in realm, "Realms cannot contain the \" (quote) character."

    return 'Basic realm="%s"' % realm

def doAuth (realm):
    """'doAuth' function returns the challenge string b giving priority over
    Digest and fallback to Basic authentication when the browser doesn't
    support the first one.
    
    This should be set in the HTTP header under the key 'WWW-Authenticate'."""

    return digestAuth (realm) + " " + basicAuth (realm)


################################################################################
# Parse authorization parameters
#
def _parseDigestAuthorization (auth_params):
    # Convert the auth params to a dict
    items = parse_http_list(auth_params)
    params = parse_keqv_list(items)

    # Now validate the params

    # Check for required parameters
    required = ["username", "realm", "nonce", "uri", "response"]
    for k in required:
        if k not in params:
            return None

    # If qop is sent then cnonce and nc MUST be present
    if "qop" in params and not ("cnonce" in params \
                                      and "nc" in params):
        return None

    # If qop is not sent, neither cnonce nor nc can be present
    if ("cnonce" in params or "nc" in params) and \
       "qop" not in params:
        return None

    return params


def _parseBasicAuthorization (auth_params):
    username, password = base64_decode(auth_params).split(":", 1)
    return {"username": username, "password": password}

AUTH_SCHEMES = {
    "basic": _parseBasicAuthorization,
    "digest": _parseDigestAuthorization,
}

def parseAuthorization (credentials):
    """parseAuthorization will convert the value of the 'Authorization' key in
    the HTTP header to a map itself. If the parsing fails 'None' is returned.
    """

    global AUTH_SCHEMES

    auth_scheme, auth_params  = credentials.split(" ", 1)
    auth_scheme = auth_scheme.lower ()

    parser = AUTH_SCHEMES[auth_scheme]
    params = parser (auth_params)

    if params is None:
        return

    assert "auth_scheme" not in params
    params["auth_scheme"] = auth_scheme
    return params


################################################################################
# Check provided response for a valid password
#
def md5SessionKey (params, password):
    """
    If the "algorithm" directive's value is "MD5-sess", then A1 
    [the session key] is calculated only once - on the first request by the
    client following receipt of a WWW-Authenticate challenge from the server.

    This creates a 'session key' for the authentication of subsequent
    requests and responses which is different for each "authentication
    session", thus limiting the amount of material hashed with any one
    key.

    Because the server need only use the hash of the user
    credentials in order to create the A1 value, this construction could
    be used in conjunction with a third party authentication service so
    that the web server would not need the actual password value.  The
    specification of such a protocol is beyond the scope of this
    specification.
"""

    keys = ("username", "realm", "nonce", "cnonce")
    params_copy = {}
    for key in keys:
        params_copy[key] = params[key]

    params_copy["algorithm"] = MD5_SESS
    return _A1 (params_copy, password)

def _A1(params, password):
    algorithm = params.get ("algorithm", MD5)
    H = DIGEST_AUTH_ENCODERS[algorithm]

    if algorithm == MD5:
        # If the "algorithm" directive's value is "MD5" or is
        # unspecified, then A1 is:
        # A1 = unq(username-value) ":" unq(realm-value) ":" passwd
        return "%s:%s:%s" % (params["username"], params["realm"], password)

    elif algorithm == MD5_SESS:

        # This is A1 if qop is set
        # A1 = H( unq(username-value) ":" unq(realm-value) ":" passwd )
        #         ":" unq(nonce-value) ":" unq(cnonce-value)
        h_a1 = H ("%s:%s:%s" % (params["username"], params["realm"], password))
        return "%s:%s:%s" % (h_a1, params["nonce"], params["cnonce"])


def _A2(params, method, kwargs):
    # If the "qop" directive's value is "auth" or is unspecified, then A2 is:
    # A2 = Method ":" digest-uri-value

    qop = params.get ("qop", "auth")
    if qop == "auth":
        return method + ":" + params["uri"]
    elif qop == "auth-int":
        # If the "qop" value is "auth-int", then A2 is:
        # A2 = Method ":" digest-uri-value ":" H(entity-body)
        entity_body = kwargs.get ("entity_body", "")
        H = kwargs["H"]

        return "%s:%s:%s" % (
            method,
            params["uri"],
            H(entity_body)
        )

    else:
        raise NotImplementedError ("The 'qop' method is unknown: %s" % qop)

def _computeDigestResponse(auth_map, password, method = "GET", A1 = None,**kwargs):
    """
    Generates a response respecting the algorithm defined in RFC 2617
    """
    params = auth_map

    algorithm = params.get ("algorithm", MD5)

    H = DIGEST_AUTH_ENCODERS[algorithm]
    KD = lambda secret, data: H(secret + ":" + data)

    qop = params.get ("qop", None)

    H_A2 = H(_A2(params, method, kwargs))

    if algorithm == MD5_SESS and A1 is not None:
        H_A1 = H(A1)
    else:
        H_A1 = H(_A1(params, password))

    if qop in ("auth", "auth-int"):
        # If the "qop" value is "auth" or "auth-int":
        # request-digest  = <"> < KD ( H(A1),     unq(nonce-value)
        #                              ":" nc-value
        #                              ":" unq(cnonce-value)
        #                              ":" unq(qop-value)
        #                              ":" H(A2)
        #                      ) <">
        request = "%s:%s:%s:%s:%s" % (
            params["nonce"],
            params["nc"],
            params["cnonce"],
            params["qop"],
            H_A2,
        )
    elif qop is None:
        # If the "qop" directive is not present (this construction is
        # for compatibility with RFC 2069):
        # request-digest  =
        #         <"> < KD ( H(A1), unq(nonce-value) ":" H(A2) ) > <">
        request = "%s:%s" % (params["nonce"], H_A2)

    return KD(H_A1, request)

def _checkDigestResponse(auth_map, password, method = "GET", A1 = None, **kwargs):
    """This function is used to verify the response given by the client when
    he tries to authenticate.
    Optional arguments:
     entity_body - when 'qop' is set to 'auth-int' you MUST provide the
                   raw data you are going to send to the client (usually the
                   HTML page.
     request_uri - the uri from the request line compared with the 'uri'
                   directive of the authorization map. They must represent
                   the same resource (unused at this time).
    """

    if auth_map['realm'] != kwargs.get('realm', None):
        return False

    response =  _computeDigestResponse(auth_map, password, method, A1,**kwargs)

    return response == auth_map["response"]

def _checkBasicResponse (auth_map, password, method='GET', encrypt=None, **kwargs):
    # Note that the Basic response doesn't provide the realm value so we cannot
    # test it
    try:
        return encrypt(auth_map["password"], auth_map["username"]) == password
    except TypeError:
        return encrypt(auth_map["password"]) == password

AUTH_RESPONSES = {
    "basic": _checkBasicResponse,
    "digest": _checkDigestResponse,
}

def checkResponse (auth_map, password, method = "GET", encrypt=None, **kwargs):
    """'checkResponse' compares the auth_map with the password and optionally
    other arguments that each implementation might need.
    
    If the response is of type 'Basic' then the function has the following
    signature::
    
        checkBasicResponse (auth_map, password) -> bool
    
    If the response is of type 'Digest' then the function has the following
    signature::
    
        checkDigestResponse (auth_map, password, method = 'GET', A1 = None) -> bool
    
    The 'A1' argument is only used in MD5_SESS algorithm based responses.
    Check md5SessionKey() for more info.
    """
    checker = AUTH_RESPONSES[auth_map["auth_scheme"]]
    return checker (auth_map, password, method=method, encrypt=encrypt, **kwargs)
 




########NEW FILE########
__FILENAME__ = httputil
"""HTTP library functions.

This module contains functions for building an HTTP application
framework: any one, not just one whose name starts with "Ch". ;) If you
reference any modules from some popular framework inside *this* module,
FuManChu will personally hang you up by your thumbs and submit you
to a public caning.
"""

from binascii import b2a_base64
from cherrypy._cpcompat import BaseHTTPRequestHandler, HTTPDate, ntob, ntou, reversed, sorted
from cherrypy._cpcompat import basestring, bytestr, iteritems, nativestr, unicodestr, unquote_qs
response_codes = BaseHTTPRequestHandler.responses.copy()

# From http://www.cherrypy.org/ticket/361
response_codes[500] = ('Internal Server Error',
                      'The server encountered an unexpected condition '
                      'which prevented it from fulfilling the request.')
response_codes[503] = ('Service Unavailable',
                      'The server is currently unable to handle the '
                      'request due to a temporary overloading or '
                      'maintenance of the server.')

import re
import urllib



def urljoin(*atoms):
    """Return the given path \*atoms, joined into a single URL.
    
    This will correctly join a SCRIPT_NAME and PATH_INFO into the
    original URL, even if either atom is blank.
    """
    url = "/".join([x for x in atoms if x])
    while "//" in url:
        url = url.replace("//", "/")
    # Special-case the final url of "", and return "/" instead.
    return url or "/"

def urljoin_bytes(*atoms):
    """Return the given path *atoms, joined into a single URL.
    
    This will correctly join a SCRIPT_NAME and PATH_INFO into the
    original URL, even if either atom is blank.
    """
    url = ntob("/").join([x for x in atoms if x])
    while ntob("//") in url:
        url = url.replace(ntob("//"), ntob("/"))
    # Special-case the final url of "", and return "/" instead.
    return url or ntob("/")

def protocol_from_http(protocol_str):
    """Return a protocol tuple from the given 'HTTP/x.y' string."""
    return int(protocol_str[5]), int(protocol_str[7])

def get_ranges(headervalue, content_length):
    """Return a list of (start, stop) indices from a Range header, or None.
    
    Each (start, stop) tuple will be composed of two ints, which are suitable
    for use in a slicing operation. That is, the header "Range: bytes=3-6",
    if applied against a Python string, is requesting resource[3:7]. This
    function will return the list [(3, 7)].
    
    If this function returns an empty list, you should return HTTP 416.
    """
    
    if not headervalue:
        return None
    
    result = []
    bytesunit, byteranges = headervalue.split("=", 1)
    for brange in byteranges.split(","):
        start, stop = [x.strip() for x in brange.split("-", 1)]
        if start:
            if not stop:
                stop = content_length - 1
            start, stop = int(start), int(stop)
            if start >= content_length:
                # From rfc 2616 sec 14.16:
                # "If the server receives a request (other than one
                # including an If-Range request-header field) with an
                # unsatisfiable Range request-header field (that is,
                # all of whose byte-range-spec values have a first-byte-pos
                # value greater than the current length of the selected
                # resource), it SHOULD return a response code of 416
                # (Requested range not satisfiable)."
                continue
            if stop < start:
                # From rfc 2616 sec 14.16:
                # "If the server ignores a byte-range-spec because it
                # is syntactically invalid, the server SHOULD treat
                # the request as if the invalid Range header field
                # did not exist. (Normally, this means return a 200
                # response containing the full entity)."
                return None
            result.append((start, stop + 1))
        else:
            if not stop:
                # See rfc quote above.
                return None
            # Negative subscript (last N bytes)
            result.append((content_length - int(stop), content_length))
    
    return result


class HeaderElement(object):
    """An element (with parameters) from an HTTP header's element list."""
    
    def __init__(self, value, params=None):
        self.value = value
        if params is None:
            params = {}
        self.params = params
    
    def __cmp__(self, other):
        return cmp(self.value, other.value)
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __str__(self):
        p = [";%s=%s" % (k, v) for k, v in iteritems(self.params)]
        return "%s%s" % (self.value, "".join(p))
    
    def __bytes__(self):
        return ntob(self.__str__())

    def __unicode__(self):
        return ntou(self.__str__())
    
    def parse(elementstr):
        """Transform 'token;key=val' to ('token', {'key': 'val'})."""
        # Split the element into a value and parameters. The 'value' may
        # be of the form, "token=token", but we don't split that here.
        atoms = [x.strip() for x in elementstr.split(";") if x.strip()]
        if not atoms:
            initial_value = ''
        else:
            initial_value = atoms.pop(0).strip()
        params = {}
        for atom in atoms:
            atom = [x.strip() for x in atom.split("=", 1) if x.strip()]
            key = atom.pop(0)
            if atom:
                val = atom[0]
            else:
                val = ""
            params[key] = val
        return initial_value, params
    parse = staticmethod(parse)
    
    def from_str(cls, elementstr):
        """Construct an instance from a string of the form 'token;key=val'."""
        ival, params = cls.parse(elementstr)
        return cls(ival, params)
    from_str = classmethod(from_str)


q_separator = re.compile(r'; *q *=')

class AcceptElement(HeaderElement):
    """An element (with parameters) from an Accept* header's element list.
    
    AcceptElement objects are comparable; the more-preferred object will be
    "less than" the less-preferred object. They are also therefore sortable;
    if you sort a list of AcceptElement objects, they will be listed in
    priority order; the most preferred value will be first. Yes, it should
    have been the other way around, but it's too late to fix now.
    """
    
    def from_str(cls, elementstr):
        qvalue = None
        # The first "q" parameter (if any) separates the initial
        # media-range parameter(s) (if any) from the accept-params.
        atoms = q_separator.split(elementstr, 1)
        media_range = atoms.pop(0).strip()
        if atoms:
            # The qvalue for an Accept header can have extensions. The other
            # headers cannot, but it's easier to parse them as if they did.
            qvalue = HeaderElement.from_str(atoms[0].strip())
        
        media_type, params = cls.parse(media_range)
        if qvalue is not None:
            params["q"] = qvalue
        return cls(media_type, params)
    from_str = classmethod(from_str)
    
    def qvalue(self):
        val = self.params.get("q", "1")
        if isinstance(val, HeaderElement):
            val = val.value
        return float(val)
    qvalue = property(qvalue, doc="The qvalue, or priority, of this value.")
    
    def __cmp__(self, other):
        diff = cmp(self.qvalue, other.qvalue)
        if diff == 0:
            diff = cmp(str(self), str(other))
        return diff
    
    def __lt__(self, other):
        if self.qvalue == other.qvalue:
            return str(self) < str(other)
        else:
            return self.qvalue < other.qvalue


def header_elements(fieldname, fieldvalue):
    """Return a sorted HeaderElement list from a comma-separated header string."""
    if not fieldvalue:
        return []
    
    result = []
    for element in fieldvalue.split(","):
        if fieldname.startswith("Accept") or fieldname == 'TE':
            hv = AcceptElement.from_str(element)
        else:
            hv = HeaderElement.from_str(element)
        result.append(hv)
    
    return list(reversed(sorted(result)))

def decode_TEXT(value):
    r"""Decode :rfc:`2047` TEXT (e.g. "=?utf-8?q?f=C3=BCr?=" -> "f\xfcr")."""
    try:
        # Python 3
        from email.header import decode_header
    except ImportError:
        from email.Header import decode_header
    atoms = decode_header(value)
    decodedvalue = ""
    for atom, charset in atoms:
        if charset is not None:
            atom = atom.decode(charset)
        decodedvalue += atom
    return decodedvalue

def valid_status(status):
    """Return legal HTTP status Code, Reason-phrase and Message.
    
    The status arg must be an int, or a str that begins with an int.
    
    If status is an int, or a str and no reason-phrase is supplied,
    a default reason-phrase will be provided.
    """
    
    if not status:
        status = 200
    
    status = str(status)
    parts = status.split(" ", 1)
    if len(parts) == 1:
        # No reason supplied.
        code, = parts
        reason = None
    else:
        code, reason = parts
        reason = reason.strip()
    
    try:
        code = int(code)
    except ValueError:
        raise ValueError("Illegal response status from server "
                         "(%s is non-numeric)." % repr(code))
    
    if code < 100 or code > 599:
        raise ValueError("Illegal response status from server "
                         "(%s is out of range)." % repr(code))
    
    if code not in response_codes:
        # code is unknown but not illegal
        default_reason, message = "", ""
    else:
        default_reason, message = response_codes[code]
    
    if reason is None:
        reason = default_reason
    
    return code, reason, message


# NOTE: the parse_qs functions that follow are modified version of those
# in the python3.0 source - we need to pass through an encoding to the unquote
# method, but the default parse_qs function doesn't allow us to.  These do.

def _parse_qs(qs, keep_blank_values=0, strict_parsing=0, encoding='utf-8'):
    """Parse a query given as a string argument.
    
    Arguments:
    
    qs: URL-encoded query string to be parsed
    
    keep_blank_values: flag indicating whether blank values in
        URL encoded queries should be treated as blank strings.  A
        true value indicates that blanks should be retained as blank
        strings.  The default false value indicates that blank values
        are to be ignored and treated as if they were  not included.
    
    strict_parsing: flag indicating what to do with parsing errors. If
        false (the default), errors are silently ignored. If true,
        errors raise a ValueError exception.
    
    Returns a dict, as G-d intended.
    """
    pairs = [s2 for s1 in qs.split('&') for s2 in s1.split(';')]
    d = {}
    for name_value in pairs:
        if not name_value and not strict_parsing:
            continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError("bad query field: %r" % (name_value,))
            # Handle case of a control-name with no equal sign
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            name = unquote_qs(nv[0], encoding)
            value = unquote_qs(nv[1], encoding)
            if name in d:
                if not isinstance(d[name], list):
                    d[name] = [d[name]]
                d[name].append(value)
            else:
                d[name] = value
    return d


image_map_pattern = re.compile(r"[0-9]+,[0-9]+")

def parse_query_string(query_string, keep_blank_values=True, encoding='utf-8'):
    """Build a params dictionary from a query_string.
    
    Duplicate key/value pairs in the provided query_string will be
    returned as {'key': [val1, val2, ...]}. Single key/values will
    be returned as strings: {'key': 'value'}.
    """
    if image_map_pattern.match(query_string):
        # Server-side image map. Map the coords to 'x' and 'y'
        # (like CGI::Request does).
        pm = query_string.split(",")
        pm = {'x': int(pm[0]), 'y': int(pm[1])}
    else:
        pm = _parse_qs(query_string, keep_blank_values, encoding=encoding)
    return pm


class CaseInsensitiveDict(dict):
    """A case-insensitive dict subclass.
    
    Each key is changed on entry to str(key).title().
    """
    
    def __getitem__(self, key):
        return dict.__getitem__(self, str(key).title())
    
    def __setitem__(self, key, value):
        dict.__setitem__(self, str(key).title(), value)
    
    def __delitem__(self, key):
        dict.__delitem__(self, str(key).title())
    
    def __contains__(self, key):
        return dict.__contains__(self, str(key).title())
    
    def get(self, key, default=None):
        return dict.get(self, str(key).title(), default)
    
    if hasattr({}, 'has_key'):
        def has_key(self, key):
            return dict.has_key(self, str(key).title())
    
    def update(self, E):
        for k in E.keys():
            self[str(k).title()] = E[k]
    
    def fromkeys(cls, seq, value=None):
        newdict = cls()
        for k in seq:
            newdict[str(k).title()] = value
        return newdict
    fromkeys = classmethod(fromkeys)
    
    def setdefault(self, key, x=None):
        key = str(key).title()
        try:
            return self[key]
        except KeyError:
            self[key] = x
            return x
    
    def pop(self, key, default):
        return dict.pop(self, str(key).title(), default)


#   TEXT = <any OCTET except CTLs, but including LWS>
#
# A CRLF is allowed in the definition of TEXT only as part of a header
# field continuation. It is expected that the folding LWS will be
# replaced with a single SP before interpretation of the TEXT value."
if nativestr == bytestr:
    header_translate_table = ''.join([chr(i) for i in xrange(256)])
    header_translate_deletechars = ''.join([chr(i) for i in xrange(32)]) + chr(127)
else:
    header_translate_table = None
    header_translate_deletechars = bytes(range(32)) + bytes([127])


class HeaderMap(CaseInsensitiveDict):
    """A dict subclass for HTTP request and response headers.
    
    Each key is changed on entry to str(key).title(). This allows headers
    to be case-insensitive and avoid duplicates.
    
    Values are header values (decoded according to :rfc:`2047` if necessary).
    """
    
    protocol=(1, 1)
    encodings = ["ISO-8859-1"]
    
    # Someday, when http-bis is done, this will probably get dropped
    # since few servers, clients, or intermediaries do it. But until then,
    # we're going to obey the spec as is.
    # "Words of *TEXT MAY contain characters from character sets other than
    # ISO-8859-1 only when encoded according to the rules of RFC 2047."
    use_rfc_2047 = True
    
    def elements(self, key):
        """Return a sorted list of HeaderElements for the given header."""
        key = str(key).title()
        value = self.get(key)
        return header_elements(key, value)
    
    def values(self, key):
        """Return a sorted list of HeaderElement.value for the given header."""
        return [e.value for e in self.elements(key)]
    
    def output(self):
        """Transform self into a list of (name, value) tuples."""
        header_list = []
        for k, v in self.items():
            if isinstance(k, unicodestr):
                k = self.encode(k)
            
            if not isinstance(v, basestring):
                v = str(v)
            
            if isinstance(v, unicodestr):
                v = self.encode(v)
            
            # See header_translate_* constants above.
            # Replace only if you really know what you're doing.
            k = k.translate(header_translate_table, header_translate_deletechars)
            v = v.translate(header_translate_table, header_translate_deletechars)
            
            header_list.append((k, v))
        return header_list
    
    def encode(self, v):
        """Return the given header name or value, encoded for HTTP output."""
        for enc in self.encodings:
            try:
                return v.encode(enc)
            except UnicodeEncodeError:
                continue
        
        if self.protocol == (1, 1) and self.use_rfc_2047:
            # Encode RFC-2047 TEXT 
            # (e.g. u"\u8200" -> "=?utf-8?b?6IiA?="). 
            # We do our own here instead of using the email module
            # because we never want to fold lines--folding has
            # been deprecated by the HTTP working group.
            v = b2a_base64(v.encode('utf-8'))
            return (ntob('=?utf-8?b?') + v.strip(ntob('\n')) + ntob('?='))
        
        raise ValueError("Could not encode header part %r using "
                         "any of the encodings %r." %
                         (v, self.encodings))


class Host(object):
    """An internet address.
    
    name
        Should be the client's host name. If not available (because no DNS
        lookup is performed), the IP address should be used instead.
    
    """
    
    ip = "0.0.0.0"
    port = 80
    name = "unknown.tld"
    
    def __init__(self, ip, port, name=None):
        self.ip = ip
        self.port = port
        if name is None:
            name = ip
        self.name = name
    
    def __repr__(self):
        return "httputil.Host(%r, %r, %r)" % (self.ip, self.port, self.name)

########NEW FILE########
__FILENAME__ = jsontools
import sys
import cherrypy
from cherrypy._cpcompat import basestring, ntou, json, json_encode, json_decode

def json_processor(entity):
    """Read application/json data into request.json."""
    if not entity.headers.get(ntou("Content-Length"), ntou("")):
        raise cherrypy.HTTPError(411)
    
    body = entity.fp.read()
    try:
        cherrypy.serving.request.json = json_decode(body.decode('utf-8'))
    except ValueError:
        raise cherrypy.HTTPError(400, 'Invalid JSON document')

def json_in(content_type=[ntou('application/json'), ntou('text/javascript')],
            force=True, debug=False, processor = json_processor):
    """Add a processor to parse JSON request entities:
    The default processor places the parsed data into request.json.

    Incoming request entities which match the given content_type(s) will
    be deserialized from JSON to the Python equivalent, and the result
    stored at cherrypy.request.json. The 'content_type' argument may
    be a Content-Type string or a list of allowable Content-Type strings.
    
    If the 'force' argument is True (the default), then entities of other
    content types will not be allowed; "415 Unsupported Media Type" is
    raised instead.
    
    Supply your own processor to use a custom decoder, or to handle the parsed
    data differently.  The processor can be configured via
    tools.json_in.processor or via the decorator method.

    Note that the deserializer requires the client send a Content-Length
    request header, or it will raise "411 Length Required". If for any
    other reason the request entity cannot be deserialized from JSON,
    it will raise "400 Bad Request: Invalid JSON document".
    
    You must be using Python 2.6 or greater, or have the 'simplejson'
    package importable; otherwise, ValueError is raised during processing.
    """
    request = cherrypy.serving.request
    if isinstance(content_type, basestring):
        content_type = [content_type]
    
    if force:
        if debug:
            cherrypy.log('Removing body processors %s' %
                         repr(request.body.processors.keys()), 'TOOLS.JSON_IN')
        request.body.processors.clear()
        request.body.default_proc = cherrypy.HTTPError(
            415, 'Expected an entity of content type %s' %
            ', '.join(content_type))
    
    for ct in content_type:
        if debug:
            cherrypy.log('Adding body processor for %s' % ct, 'TOOLS.JSON_IN')
        request.body.processors[ct] = processor

def json_handler(*args, **kwargs):
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return json_encode(value)

def json_out(content_type='application/json', debug=False, handler=json_handler):
    """Wrap request.handler to serialize its output to JSON. Sets Content-Type.
    
    If the given content_type is None, the Content-Type response header
    is not set.

    Provide your own handler to use a custom encoder.  For example
    cherrypy.config['tools.json_out.handler'] = <function>, or
    @json_out(handler=function).

    You must be using Python 2.6 or greater, or have the 'simplejson'
    package importable; otherwise, ValueError is raised during processing.
    """
    request = cherrypy.serving.request
    if debug:
        cherrypy.log('Replacing %s with JSON handler' % request.handler,
                     'TOOLS.JSON_OUT')
    request._json_inner_handler = request.handler
    request.handler = handler
    if content_type is not None:
        if debug:
            cherrypy.log('Setting Content-Type to %s' % content_type, 'TOOLS.JSON_OUT')
        cherrypy.serving.response.headers['Content-Type'] = content_type


########NEW FILE########
__FILENAME__ = profiler
"""Profiler tools for CherryPy.

CherryPy users
==============

You can profile any of your pages as follows::

    from cherrypy.lib import profiler
    
    class Root:
        p = profile.Profiler("/path/to/profile/dir")
        
        def index(self):
            self.p.run(self._index)
        index.exposed = True
        
        def _index(self):
            return "Hello, world!"
    
    cherrypy.tree.mount(Root())

You can also turn on profiling for all requests
using the ``make_app`` function as WSGI middleware.

CherryPy developers
===================

This module can be used whenever you make changes to CherryPy,
to get a quick sanity-check on overall CP performance. Use the
``--profile`` flag when running the test suite. Then, use the ``serve()``
function to browse the results in a web browser. If you run this
module from the command line, it will call ``serve()`` for you.

"""


def new_func_strip_path(func_name):
    """Make profiler output more readable by adding ``__init__`` modules' parents"""
    filename, line, name = func_name
    if filename.endswith("__init__.py"):
        return os.path.basename(filename[:-12]) + filename[-12:], line, name
    return os.path.basename(filename), line, name

try:
    import profile
    import pstats
    pstats.func_strip_path = new_func_strip_path
except ImportError:
    profile = None
    pstats = None

import os, os.path
import sys
import warnings

from cherrypy._cpcompat import BytesIO

_count = 0

class Profiler(object):
    
    def __init__(self, path=None):
        if not path:
            path = os.path.join(os.path.dirname(__file__), "profile")
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)
    
    def run(self, func, *args, **params):
        """Dump profile data into self.path."""
        global _count
        c = _count = _count + 1
        path = os.path.join(self.path, "cp_%04d.prof" % c)
        prof = profile.Profile()
        result = prof.runcall(func, *args, **params)
        prof.dump_stats(path)
        return result
    
    def statfiles(self):
        """:rtype: list of available profiles.
        """
        return [f for f in os.listdir(self.path)
                if f.startswith("cp_") and f.endswith(".prof")]
    
    def stats(self, filename, sortby='cumulative'):
        """:rtype stats(index): output of print_stats() for the given profile.
        """
        sio = BytesIO()
        if sys.version_info >= (2, 5):
            s = pstats.Stats(os.path.join(self.path, filename), stream=sio)
            s.strip_dirs()
            s.sort_stats(sortby)
            s.print_stats()
        else:
            # pstats.Stats before Python 2.5 didn't take a 'stream' arg,
            # but just printed to stdout. So re-route stdout.
            s = pstats.Stats(os.path.join(self.path, filename))
            s.strip_dirs()
            s.sort_stats(sortby)
            oldout = sys.stdout
            try:
                sys.stdout = sio
                s.print_stats()
            finally:
                sys.stdout = oldout
        response = sio.getvalue()
        sio.close()
        return response
    
    def index(self):
        return """<html>
        <head><title>CherryPy profile data</title></head>
        <frameset cols='200, 1*'>
            <frame src='menu' />
            <frame name='main' src='' />
        </frameset>
        </html>
        """
    index.exposed = True
    
    def menu(self):
        yield "<h2>Profiling runs</h2>"
        yield "<p>Click on one of the runs below to see profiling data.</p>"
        runs = self.statfiles()
        runs.sort()
        for i in runs:
            yield "<a href='report?filename=%s' target='main'>%s</a><br />" % (i, i)
    menu.exposed = True
    
    def report(self, filename):
        import cherrypy
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return self.stats(filename)
    report.exposed = True


class ProfileAggregator(Profiler):
    
    def __init__(self, path=None):
        Profiler.__init__(self, path)
        global _count
        self.count = _count = _count + 1
        self.profiler = profile.Profile()
    
    def run(self, func, *args):
        path = os.path.join(self.path, "cp_%04d.prof" % self.count)
        result = self.profiler.runcall(func, *args)
        self.profiler.dump_stats(path)
        return result


class make_app:
    def __init__(self, nextapp, path=None, aggregate=False):
        """Make a WSGI middleware app which wraps 'nextapp' with profiling.
        
        nextapp
            the WSGI application to wrap, usually an instance of
            cherrypy.Application.
            
        path
            where to dump the profiling output.
            
        aggregate
            if True, profile data for all HTTP requests will go in
            a single file. If False (the default), each HTTP request will
            dump its profile data into a separate file.
        
        """
        if profile is None or pstats is None:
            msg = ("Your installation of Python does not have a profile module. "
                   "If you're on Debian, try `sudo apt-get install python-profiler`. "
                   "See http://www.cherrypy.org/wiki/ProfilingOnDebian for details.")
            warnings.warn(msg)
        
        self.nextapp = nextapp
        self.aggregate = aggregate
        if aggregate:
            self.profiler = ProfileAggregator(path)
        else:
            self.profiler = Profiler(path)
    
    def __call__(self, environ, start_response):
        def gather():
            result = []
            for line in self.nextapp(environ, start_response):
                result.append(line)
            return result
        return self.profiler.run(gather)


def serve(path=None, port=8080):
    if profile is None or pstats is None:
        msg = ("Your installation of Python does not have a profile module. "
               "If you're on Debian, try `sudo apt-get install python-profiler`. "
               "See http://www.cherrypy.org/wiki/ProfilingOnDebian for details.")
        warnings.warn(msg)
    
    import cherrypy
    cherrypy.config.update({'server.socket_port': int(port),
                            'server.thread_pool': 10,
                            'environment': "production",
                            })
    cherrypy.quickstart(Profiler(path))


if __name__ == "__main__":
    serve(*tuple(sys.argv[1:]))


########NEW FILE########
__FILENAME__ = reprconf
"""Generic configuration system using unrepr.

Configuration data may be supplied as a Python dictionary, as a filename,
or as an open file object. When you supply a filename or file, Python's
builtin ConfigParser is used (with some extensions).

Namespaces
----------

Configuration keys are separated into namespaces by the first "." in the key.

The only key that cannot exist in a namespace is the "environment" entry.
This special entry 'imports' other config entries from a template stored in
the Config.environments dict.

You can define your own namespaces to be called when new config is merged
by adding a named handler to Config.namespaces. The name can be any string,
and the handler must be either a callable or a context manager.
"""

try:
    # Python 3.0+
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

try:
    set
except NameError:
    from sets import Set as set

try:
    basestring
except NameError:
    basestring = str

try:
    # Python 3
    import builtins
except ImportError:
    # Python 2
    import __builtin__ as builtins

import operator as _operator
import sys

def as_dict(config):
    """Return a dict from 'config' whether it is a dict, file, or filename."""
    if isinstance(config, basestring):
        config = Parser().dict_from_file(config)
    elif hasattr(config, 'read'):
        config = Parser().dict_from_file(config)
    return config


class NamespaceSet(dict):
    """A dict of config namespace names and handlers.
    
    Each config entry should begin with a namespace name; the corresponding
    namespace handler will be called once for each config entry in that
    namespace, and will be passed two arguments: the config key (with the
    namespace removed) and the config value.
    
    Namespace handlers may be any Python callable; they may also be
    Python 2.5-style 'context managers', in which case their __enter__
    method should return a callable to be used as the handler.
    See cherrypy.tools (the Toolbox class) for an example.
    """
    
    def __call__(self, config):
        """Iterate through config and pass it to each namespace handler.
        
        config
            A flat dict, where keys use dots to separate
            namespaces, and values are arbitrary.
        
        The first name in each config key is used to look up the corresponding
        namespace handler. For example, a config entry of {'tools.gzip.on': v}
        will call the 'tools' namespace handler with the args: ('gzip.on', v)
        """
        # Separate the given config into namespaces
        ns_confs = {}
        for k in config:
            if "." in k:
                ns, name = k.split(".", 1)
                bucket = ns_confs.setdefault(ns, {})
                bucket[name] = config[k]
        
        # I chose __enter__ and __exit__ so someday this could be
        # rewritten using Python 2.5's 'with' statement:
        # for ns, handler in self.iteritems():
        #     with handler as callable:
        #         for k, v in ns_confs.get(ns, {}).iteritems():
        #             callable(k, v)
        for ns, handler in self.items():
            exit = getattr(handler, "__exit__", None)
            if exit:
                callable = handler.__enter__()
                no_exc = True
                try:
                    try:
                        for k, v in ns_confs.get(ns, {}).items():
                            callable(k, v)
                    except:
                        # The exceptional case is handled here
                        no_exc = False
                        if exit is None:
                            raise
                        if not exit(*sys.exc_info()):
                            raise
                        # The exception is swallowed if exit() returns true
                finally:
                    # The normal and non-local-goto cases are handled here
                    if no_exc and exit:
                        exit(None, None, None)
            else:
                for k, v in ns_confs.get(ns, {}).items():
                    handler(k, v)
    
    def __repr__(self):
        return "%s.%s(%s)" % (self.__module__, self.__class__.__name__,
                              dict.__repr__(self))
    
    def __copy__(self):
        newobj = self.__class__()
        newobj.update(self)
        return newobj
    copy = __copy__


class Config(dict):
    """A dict-like set of configuration data, with defaults and namespaces.
    
    May take a file, filename, or dict.
    """
    
    defaults = {}
    environments = {}
    namespaces = NamespaceSet()
    
    def __init__(self, file=None, **kwargs):
        self.reset()
        if file is not None:
            self.update(file)
        if kwargs:
            self.update(kwargs)
    
    def reset(self):
        """Reset self to default values."""
        self.clear()
        dict.update(self, self.defaults)
    
    def update(self, config):
        """Update self from a dict, file or filename."""
        if isinstance(config, basestring):
            # Filename
            config = Parser().dict_from_file(config)
        elif hasattr(config, 'read'):
            # Open file object
            config = Parser().dict_from_file(config)
        else:
            config = config.copy()
        self._apply(config)
    
    def _apply(self, config):
        """Update self from a dict."""
        which_env = config.get('environment')
        if which_env:
            env = self.environments[which_env]
            for k in env:
                if k not in config:
                    config[k] = env[k]
        
        dict.update(self, config)
        self.namespaces(config)
    
    def __setitem__(self, k, v):
        dict.__setitem__(self, k, v)
        self.namespaces({k: v})


class Parser(ConfigParser):
    """Sub-class of ConfigParser that keeps the case of options and that 
    raises an exception if the file cannot be read.
    """
    
    def optionxform(self, optionstr):
        return optionstr
    
    def read(self, filenames):
        if isinstance(filenames, basestring):
            filenames = [filenames]
        for filename in filenames:
            # try:
            #     fp = open(filename)
            # except IOError:
            #     continue
            fp = open(filename)
            try:
                self._read(fp, filename)
            finally:
                fp.close()
    
    def as_dict(self, raw=False, vars=None):
        """Convert an INI file to a dictionary"""
        # Load INI file into a dict
        result = {}
        for section in self.sections():
            if section not in result:
                result[section] = {}
            for option in self.options(section):
                value = self.get(section, option, raw=raw, vars=vars)
                try:
                    value = unrepr(value)
                except Exception:
                    x = sys.exc_info()[1]
                    msg = ("Config error in section: %r, option: %r, "
                           "value: %r. Config values must be valid Python." %
                           (section, option, value))
                    raise ValueError(msg, x.__class__.__name__, x.args)
                result[section][option] = value
        return result
    
    def dict_from_file(self, file):
        if hasattr(file, 'read'):
            self.readfp(file)
        else:
            self.read(file)
        return self.as_dict()


# public domain "unrepr" implementation, found on the web and then improved.


class _Builder2:
    
    def build(self, o):
        m = getattr(self, 'build_' + o.__class__.__name__, None)
        if m is None:
            raise TypeError("unrepr does not recognize %s" %
                            repr(o.__class__.__name__))
        return m(o)
    
    def astnode(self, s):
        """Return a Python2 ast Node compiled from a string."""
        try:
            import compiler
        except ImportError:
            # Fallback to eval when compiler package is not available,
            # e.g. IronPython 1.0.
            return eval(s)
        
        p = compiler.parse("__tempvalue__ = " + s)
        return p.getChildren()[1].getChildren()[0].getChildren()[1]
    
    def build_Subscript(self, o):
        expr, flags, subs = o.getChildren()
        expr = self.build(expr)
        subs = self.build(subs)
        return expr[subs]
    
    def build_CallFunc(self, o):
        children = map(self.build, o.getChildren())
        callee = children.pop(0)
        kwargs = children.pop() or {}
        starargs = children.pop() or ()
        args = tuple(children) + tuple(starargs)
        return callee(*args, **kwargs)
    
    def build_List(self, o):
        return map(self.build, o.getChildren())
    
    def build_Const(self, o):
        return o.value
    
    def build_Dict(self, o):
        d = {}
        i = iter(map(self.build, o.getChildren()))
        for el in i:
            d[el] = i.next()
        return d
    
    def build_Tuple(self, o):
        return tuple(self.build_List(o))
    
    def build_Name(self, o):
        name = o.name
        if name == 'None':
            return None
        if name == 'True':
            return True
        if name == 'False':
            return False
        
        # See if the Name is a package or module. If it is, import it.
        try:
            return modules(name)
        except ImportError:
            pass
        
        # See if the Name is in builtins.
        try:
            return getattr(builtins, name)
        except AttributeError:
            pass
        
        raise TypeError("unrepr could not resolve the name %s" % repr(name))
    
    def build_Add(self, o):
        left, right = map(self.build, o.getChildren())
        return left + right

    def build_Mul(self, o):
        left, right = map(self.build, o.getChildren())
        return left * right
    
    def build_Getattr(self, o):
        parent = self.build(o.expr)
        return getattr(parent, o.attrname)
    
    def build_NoneType(self, o):
        return None
    
    def build_UnarySub(self, o):
        return -self.build(o.getChildren()[0])
    
    def build_UnaryAdd(self, o):
        return self.build(o.getChildren()[0])


class _Builder3:
    
    def build(self, o):
        m = getattr(self, 'build_' + o.__class__.__name__, None)
        if m is None:
            raise TypeError("unrepr does not recognize %s" %
                            repr(o.__class__.__name__))
        return m(o)
    
    def astnode(self, s):
        """Return a Python3 ast Node compiled from a string."""
        try:
            import ast
        except ImportError:
            # Fallback to eval when ast package is not available,
            # e.g. IronPython 1.0.
            return eval(s)

        p = ast.parse("__tempvalue__ = " + s)
        return p.body[0].value

    def build_Subscript(self, o):
        return self.build(o.value)[self.build(o.slice)]
    
    def build_Index(self, o):
        return self.build(o.value)
    
    def build_Call(self, o):
        callee = self.build(o.func)
        
        if o.args is None:
            args = ()
        else: 
            args = tuple([self.build(a) for a in o.args]) 
        
        if o.starargs is None:
            starargs = ()
        else:
            starargs = self.build(o.starargs)
        
        if o.kwargs is None:
            kwargs = {}
        else:
            kwargs = self.build(o.kwargs)
        
        return callee(*(args + starargs), **kwargs)
    
    def build_List(self, o):
        return list(map(self.build, o.elts))
    
    def build_Str(self, o):
        return o.s
    
    def build_Num(self, o):
        return o.n
    
    def build_Dict(self, o):
        return dict([(self.build(k), self.build(v))
                     for k, v in zip(o.keys, o.values)])
    
    def build_Tuple(self, o):
        return tuple(self.build_List(o))
    
    def build_Name(self, o):
        name = o.id
        if name == 'None':
            return None
        if name == 'True':
            return True
        if name == 'False':
            return False
        
        # See if the Name is a package or module. If it is, import it.
        try:
            return modules(name)
        except ImportError:
            pass
        
        # See if the Name is in builtins.
        try:
            import builtins
            return getattr(builtins, name)
        except AttributeError:
            pass
        
        raise TypeError("unrepr could not resolve the name %s" % repr(name))
        
    def build_UnaryOp(self, o):
        op, operand = map(self.build, [o.op, o.operand])
        return op(operand)
    
    def build_BinOp(self, o):
        left, op, right = map(self.build, [o.left, o.op, o.right]) 
        return op(left, right)

    def build_Add(self, o):
        return _operator.add

    def build_Mult(self, o):
        return _operator.mul
        
    def build_USub(self, o):
        return _operator.neg

    def build_Attribute(self, o):
        parent = self.build(o.value)
        return getattr(parent, o.attr)

    def build_NoneType(self, o):
        return None


def unrepr(s):
    """Return a Python object compiled from a string."""
    if not s:
        return s
    if sys.version_info < (3, 0):
        b = _Builder2()
    else:
        b = _Builder3()
    obj = b.astnode(s)
    return b.build(obj)


def modules(modulePath):
    """Load a module and retrieve a reference to that module."""
    try:
        mod = sys.modules[modulePath]
        if mod is None:
            raise KeyError()
    except KeyError:
        # The last [''] is important.
        mod = __import__(modulePath, globals(), locals(), [''])
    return mod

def attributes(full_attribute_name):
    """Load a module and retrieve an attribute of that module."""
    
    # Parse out the path, module, and attribute
    last_dot = full_attribute_name.rfind(".")
    attr_name = full_attribute_name[last_dot + 1:]
    mod_path = full_attribute_name[:last_dot]
    
    mod = modules(mod_path)
    # Let an AttributeError propagate outward.
    try:
        attr = getattr(mod, attr_name)
    except AttributeError:
        raise AttributeError("'%s' object has no attribute '%s'"
                             % (mod_path, attr_name))
    
    # Return a reference to the attribute.
    return attr



########NEW FILE########
__FILENAME__ = sessions
"""Session implementation for CherryPy.

You need to edit your config file to use sessions. Here's an example::

    [/]
    tools.sessions.on = True
    tools.sessions.storage_type = "file"
    tools.sessions.storage_path = "/home/site/sessions"
    tools.sessions.timeout = 60

This sets the session to be stored in files in the directory /home/site/sessions,
and the session timeout to 60 minutes. If you omit ``storage_type`` the sessions
will be saved in RAM.  ``tools.sessions.on`` is the only required line for
working sessions, the rest are optional.

By default, the session ID is passed in a cookie, so the client's browser must
have cookies enabled for your site.

To set data for the current session, use
``cherrypy.session['fieldname'] = 'fieldvalue'``;
to get data use ``cherrypy.session.get('fieldname')``.

================
Locking sessions
================

By default, the ``'locking'`` mode of sessions is ``'implicit'``, which means
the session is locked early and unlocked late. If you want to control when the
session data is locked and unlocked, set ``tools.sessions.locking = 'explicit'``.
Then call ``cherrypy.session.acquire_lock()`` and ``cherrypy.session.release_lock()``.
Regardless of which mode you use, the session is guaranteed to be unlocked when
the request is complete.

=================
Expiring Sessions
=================

You can force a session to expire with :func:`cherrypy.lib.sessions.expire`.
Simply call that function at the point you want the session to expire, and it
will cause the session cookie to expire client-side.

===========================
Session Fixation Protection
===========================

If CherryPy receives, via a request cookie, a session id that it does not
recognize, it will reject that id and create a new one to return in the
response cookie. This `helps prevent session fixation attacks
<http://en.wikipedia.org/wiki/Session_fixation#Regenerate_SID_on_each_request>`_.
However, CherryPy "recognizes" a session id by looking up the saved session
data for that id. Therefore, if you never save any session data,
**you will get a new session id for every request**.

================
Sharing Sessions
================

If you run multiple instances of CherryPy (for example via mod_python behind
Apache prefork), you most likely cannot use the RAM session backend, since each
instance of CherryPy will have its own memory space. Use a different backend
instead, and verify that all instances are pointing at the same file or db
location. Alternately, you might try a load balancer which makes sessions
"sticky". Google is your friend, there.

================
Expiration Dates
================

The response cookie will possess an expiration date to inform the client at
which point to stop sending the cookie back in requests. If the server time
and client time differ, expect sessions to be unreliable. **Make sure the
system time of your server is accurate**.

CherryPy defaults to a 60-minute session timeout, which also applies to the
cookie which is sent to the client. Unfortunately, some versions of Safari
("4 public beta" on Windows XP at least) appear to have a bug in their parsing
of the GMT expiration date--they appear to interpret the date as one hour in
the past. Sixty minutes minus one hour is pretty close to zero, so you may
experience this bug as a new session id for every request, unless the requests
are less than one second apart. To fix, try increasing the session.timeout.

On the other extreme, some users report Firefox sending cookies after their
expiration date, although this was on a system with an inaccurate system time.
Maybe FF doesn't trust system time.
"""

import datetime
import os
import random
import time
import threading
import types
from warnings import warn

import cherrypy
from cherrypy._cpcompat import copyitems, pickle, random20, unicodestr
from cherrypy.lib import httputil


missing = object()

class Session(object):
    """A CherryPy dict-like Session object (one per request)."""
    
    _id = None
    
    id_observers = None
    "A list of callbacks to which to pass new id's."
    
    def _get_id(self):
        return self._id
    def _set_id(self, value):
        self._id = value
        for o in self.id_observers:
            o(value)
    id = property(_get_id, _set_id, doc="The current session ID.")
    
    timeout = 60
    "Number of minutes after which to delete session data."
    
    locked = False
    """
    If True, this session instance has exclusive read/write access
    to session data."""
    
    loaded = False
    """
    If True, data has been retrieved from storage. This should happen
    automatically on the first attempt to access session data."""
    
    clean_thread = None
    "Class-level Monitor which calls self.clean_up."
    
    clean_freq = 5
    "The poll rate for expired session cleanup in minutes."
    
    originalid = None
    "The session id passed by the client. May be missing or unsafe."
    
    missing = False
    "True if the session requested by the client did not exist."
    
    regenerated = False
    """
    True if the application called session.regenerate(). This is not set by
    internal calls to regenerate the session id."""
    
    debug=False
    
    def __init__(self, id=None, **kwargs):
        self.id_observers = []
        self._data = {}
        
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        self.originalid = id
        self.missing = False
        if id is None:
            if self.debug:
                cherrypy.log('No id given; making a new one', 'TOOLS.SESSIONS')
            self._regenerate()
        else:
            self.id = id
            if not self._exists():
                if self.debug:
                    cherrypy.log('Expired or malicious session %r; '
                                 'making a new one' % id, 'TOOLS.SESSIONS')
                # Expired or malicious session. Make a new one.
                # See http://www.cherrypy.org/ticket/709.
                self.id = None
                self.missing = True
                self._regenerate()

    def now(self):
        """Generate the session specific concept of 'now'.

        Other session providers can override this to use alternative,
        possibly timezone aware, versions of 'now'.
        """
        return datetime.datetime.now()

    def regenerate(self):
        """Replace the current session (with a new id)."""
        self.regenerated = True
        self._regenerate()
    
    def _regenerate(self):
        if self.id is not None:
            self.delete()
        
        old_session_was_locked = self.locked
        if old_session_was_locked:
            self.release_lock()
        
        self.id = None
        while self.id is None:
            self.id = self.generate_id()
            # Assert that the generated id is not already stored.
            if self._exists():
                self.id = None
        
        if old_session_was_locked:
            self.acquire_lock()
    
    def clean_up(self):
        """Clean up expired sessions."""
        pass
    
    def generate_id(self):
        """Return a new session id."""
        return random20()
    
    def save(self):
        """Save session data."""
        try:
            # If session data has never been loaded then it's never been
            #   accessed: no need to save it
            if self.loaded:
                t = datetime.timedelta(seconds = self.timeout * 60)
                expiration_time = self.now() + t
                if self.debug:
                    cherrypy.log('Saving with expiry %s' % expiration_time,
                                 'TOOLS.SESSIONS')
                self._save(expiration_time)
            
        finally:
            if self.locked:
                # Always release the lock if the user didn't release it
                self.release_lock()
    
    def load(self):
        """Copy stored session data into this session instance."""
        data = self._load()
        # data is either None or a tuple (session_data, expiration_time)
        if data is None or data[1] < self.now():
            if self.debug:
                cherrypy.log('Expired session, flushing data', 'TOOLS.SESSIONS')
            self._data = {}
        else:
            self._data = data[0]
        self.loaded = True
        
        # Stick the clean_thread in the class, not the instance.
        # The instances are created and destroyed per-request.
        cls = self.__class__
        if self.clean_freq and not cls.clean_thread:
            # clean_up is in instancemethod and not a classmethod,
            # so that tool config can be accessed inside the method.
            t = cherrypy.process.plugins.Monitor(
                cherrypy.engine, self.clean_up, self.clean_freq * 60,
                name='Session cleanup')
            t.subscribe()
            cls.clean_thread = t
            t.start()
    
    def delete(self):
        """Delete stored session data."""
        self._delete()
    
    def __getitem__(self, key):
        if not self.loaded: self.load()
        return self._data[key]
    
    def __setitem__(self, key, value):
        if not self.loaded: self.load()
        self._data[key] = value
    
    def __delitem__(self, key):
        if not self.loaded: self.load()
        del self._data[key]
    
    def pop(self, key, default=missing):
        """Remove the specified key and return the corresponding value.
        If key is not found, default is returned if given,
        otherwise KeyError is raised.
        """
        if not self.loaded: self.load()
        if default is missing:
            return self._data.pop(key)
        else:
            return self._data.pop(key, default)
    
    def __contains__(self, key):
        if not self.loaded: self.load()
        return key in self._data
    
    if hasattr({}, 'has_key'):
        def has_key(self, key):
            """D.has_key(k) -> True if D has a key k, else False."""
            if not self.loaded: self.load()
            return key in self._data
    
    def get(self, key, default=None):
        """D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None."""
        if not self.loaded: self.load()
        return self._data.get(key, default)
    
    def update(self, d):
        """D.update(E) -> None.  Update D from E: for k in E: D[k] = E[k]."""
        if not self.loaded: self.load()
        self._data.update(d)
    
    def setdefault(self, key, default=None):
        """D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D."""
        if not self.loaded: self.load()
        return self._data.setdefault(key, default)
    
    def clear(self):
        """D.clear() -> None.  Remove all items from D."""
        if not self.loaded: self.load()
        self._data.clear()
    
    def keys(self):
        """D.keys() -> list of D's keys."""
        if not self.loaded: self.load()
        return self._data.keys()
    
    def items(self):
        """D.items() -> list of D's (key, value) pairs, as 2-tuples."""
        if not self.loaded: self.load()
        return self._data.items()
    
    def values(self):
        """D.values() -> list of D's values."""
        if not self.loaded: self.load()
        return self._data.values()


class RamSession(Session):
    
    # Class-level objects. Don't rebind these!
    cache = {}
    locks = {}
    
    def clean_up(self):
        """Clean up expired sessions."""
        now = self.now()
        for id, (data, expiration_time) in copyitems(self.cache):
            if expiration_time <= now:
                try:
                    del self.cache[id]
                except KeyError:
                    pass
                try:
                    del self.locks[id]
                except KeyError:
                    pass
        
        # added to remove obsolete lock objects
        for id in list(self.locks):
            if id not in self.cache:
                self.locks.pop(id, None)
    
    def _exists(self):
        return self.id in self.cache
    
    def _load(self):
        return self.cache.get(self.id)
    
    def _save(self, expiration_time):
        self.cache[self.id] = (self._data, expiration_time)
    
    def _delete(self):
        self.cache.pop(self.id, None)
    
    def acquire_lock(self):
        """Acquire an exclusive lock on the currently-loaded session data."""
        self.locked = True
        self.locks.setdefault(self.id, threading.RLock()).acquire()
    
    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        self.locks[self.id].release()
        self.locked = False
    
    def __len__(self):
        """Return the number of active sessions."""
        return len(self.cache)


class FileSession(Session):
    """Implementation of the File backend for sessions
    
    storage_path
        The folder where session data will be saved. Each session
        will be saved as pickle.dump(data, expiration_time) in its own file;
        the filename will be self.SESSION_PREFIX + self.id.
    
    """
    
    SESSION_PREFIX = 'session-'
    LOCK_SUFFIX = '.lock'
    pickle_protocol = pickle.HIGHEST_PROTOCOL
    
    def __init__(self, id=None, **kwargs):
        # The 'storage_path' arg is required for file-based sessions.
        kwargs['storage_path'] = os.path.abspath(kwargs['storage_path'])
        Session.__init__(self, id=id, **kwargs)
    
    def setup(cls, **kwargs):
        """Set up the storage system for file-based sessions.
        
        This should only be called once per process; this will be done
        automatically when using sessions.init (as the built-in Tool does).
        """
        # The 'storage_path' arg is required for file-based sessions.
        kwargs['storage_path'] = os.path.abspath(kwargs['storage_path'])
        
        for k, v in kwargs.items():
            setattr(cls, k, v)
        
        # Warn if any lock files exist at startup.
        lockfiles = [fname for fname in os.listdir(cls.storage_path)
                     if (fname.startswith(cls.SESSION_PREFIX)
                         and fname.endswith(cls.LOCK_SUFFIX))]
        if lockfiles:
            plural = ('', 's')[len(lockfiles) > 1]
            warn("%s session lockfile%s found at startup. If you are "
                 "only running one process, then you may need to "
                 "manually delete the lockfiles found at %r."
                 % (len(lockfiles), plural, cls.storage_path))
    setup = classmethod(setup)
    
    def _get_file_path(self):
        f = os.path.join(self.storage_path, self.SESSION_PREFIX + self.id)
        if not os.path.abspath(f).startswith(self.storage_path):
            raise cherrypy.HTTPError(400, "Invalid session id in cookie.")
        return f
    
    def _exists(self):
        path = self._get_file_path()
        return os.path.exists(path)
    
    def _load(self, path=None):
        if path is None:
            path = self._get_file_path()
        try:
            f = open(path, "rb")
            try:
                return pickle.load(f)
            finally:
                f.close()
        except (IOError, EOFError):
            return None
    
    def _save(self, expiration_time):
        f = open(self._get_file_path(), "wb")
        try:
            pickle.dump((self._data, expiration_time), f, self.pickle_protocol)
        finally:
            f.close()
    
    def _delete(self):
        try:
            os.unlink(self._get_file_path())
        except OSError:
            pass
    
    def acquire_lock(self, path=None):
        """Acquire an exclusive lock on the currently-loaded session data."""
        if path is None:
            path = self._get_file_path()
        path += self.LOCK_SUFFIX
        while True:
            try:
                lockfd = os.open(path, os.O_CREAT|os.O_WRONLY|os.O_EXCL)
            except OSError:
                time.sleep(0.1)
            else:
                os.close(lockfd) 
                break
        self.locked = True
    
    def release_lock(self, path=None):
        """Release the lock on the currently-loaded session data."""
        if path is None:
            path = self._get_file_path()
        os.unlink(path + self.LOCK_SUFFIX)
        self.locked = False
    
    def clean_up(self):
        """Clean up expired sessions."""
        now = self.now()
        # Iterate over all session files in self.storage_path
        for fname in os.listdir(self.storage_path):
            if (fname.startswith(self.SESSION_PREFIX)
                and not fname.endswith(self.LOCK_SUFFIX)):
                # We have a session file: lock and load it and check
                #   if it's expired. If it fails, nevermind.
                path = os.path.join(self.storage_path, fname)
                self.acquire_lock(path)
                try:
                    contents = self._load(path)
                    # _load returns None on IOError
                    if contents is not None:
                        data, expiration_time = contents
                        if expiration_time < now:
                            # Session expired: deleting it
                            os.unlink(path)
                finally:
                    self.release_lock(path)
    
    def __len__(self):
        """Return the number of active sessions."""
        return len([fname for fname in os.listdir(self.storage_path)
                    if (fname.startswith(self.SESSION_PREFIX)
                        and not fname.endswith(self.LOCK_SUFFIX))])


class PostgresqlSession(Session):
    """ Implementation of the PostgreSQL backend for sessions. It assumes
        a table like this::

            create table session (
                id varchar(40),
                data text,
                expiration_time timestamp
            )
    
    You must provide your own get_db function.
    """
    
    pickle_protocol = pickle.HIGHEST_PROTOCOL
    
    def __init__(self, id=None, **kwargs):
        Session.__init__(self, id, **kwargs)
        self.cursor = self.db.cursor()
    
    def setup(cls, **kwargs):
        """Set up the storage system for Postgres-based sessions.
        
        This should only be called once per process; this will be done
        automatically when using sessions.init (as the built-in Tool does).
        """
        for k, v in kwargs.items():
            setattr(cls, k, v)
        
        self.db = self.get_db()
    setup = classmethod(setup)
    
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        self.db.commit()
    
    def _exists(self):
        # Select session data from table
        self.cursor.execute('select data, expiration_time from session '
                            'where id=%s', (self.id,))
        rows = self.cursor.fetchall()
        return bool(rows)
    
    def _load(self):
        # Select session data from table
        self.cursor.execute('select data, expiration_time from session '
                            'where id=%s', (self.id,))
        rows = self.cursor.fetchall()
        if not rows:
            return None
        
        pickled_data, expiration_time = rows[0]
        data = pickle.loads(pickled_data)
        return data, expiration_time
    
    def _save(self, expiration_time):
        pickled_data = pickle.dumps(self._data, self.pickle_protocol)
        self.cursor.execute('update session set data = %s, '
                            'expiration_time = %s where id = %s',
                            (pickled_data, expiration_time, self.id))
    
    def _delete(self):
        self.cursor.execute('delete from session where id=%s', (self.id,))
   
    def acquire_lock(self):
        """Acquire an exclusive lock on the currently-loaded session data."""
        # We use the "for update" clause to lock the row
        self.locked = True
        self.cursor.execute('select id from session where id=%s for update',
                            (self.id,))
    
    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        # We just close the cursor and that will remove the lock
        #   introduced by the "for update" clause
        self.cursor.close()
        self.locked = False
    
    def clean_up(self):
        """Clean up expired sessions."""
        self.cursor.execute('delete from session where expiration_time < %s',
                            (self.now(),))


class MemcachedSession(Session):
    
    # The most popular memcached client for Python isn't thread-safe.
    # Wrap all .get and .set operations in a single lock.
    mc_lock = threading.RLock()
    
    # This is a seperate set of locks per session id.
    locks = {}
    
    servers = ['127.0.0.1:11211']
    
    def setup(cls, **kwargs):
        """Set up the storage system for memcached-based sessions.
        
        This should only be called once per process; this will be done
        automatically when using sessions.init (as the built-in Tool does).
        """
        for k, v in kwargs.items():
            setattr(cls, k, v)
        
        import memcache
        cls.cache = memcache.Client(cls.servers)
    setup = classmethod(setup)
    
    def _get_id(self):
        return self._id
    def _set_id(self, value):
        # This encode() call is where we differ from the superclass.
        # Memcache keys MUST be byte strings, not unicode.
        if isinstance(value, unicodestr):
            value = value.encode('utf-8')

        self._id = value
        for o in self.id_observers:
            o(value)
    id = property(_get_id, _set_id, doc="The current session ID.")
    
    def _exists(self):
        self.mc_lock.acquire()
        try:
            return bool(self.cache.get(self.id))
        finally:
            self.mc_lock.release()
    
    def _load(self):
        self.mc_lock.acquire()
        try:
            return self.cache.get(self.id)
        finally:
            self.mc_lock.release()
    
    def _save(self, expiration_time):
        # Send the expiration time as "Unix time" (seconds since 1/1/1970)
        td = int(time.mktime(expiration_time.timetuple()))
        self.mc_lock.acquire()
        try:
            if not self.cache.set(self.id, (self._data, expiration_time), td):
                raise AssertionError("Session data for id %r not set." % self.id)
        finally:
            self.mc_lock.release()
    
    def _delete(self):
        self.cache.delete(self.id)
    
    def acquire_lock(self):
        """Acquire an exclusive lock on the currently-loaded session data."""
        self.locked = True
        self.locks.setdefault(self.id, threading.RLock()).acquire()
    
    def release_lock(self):
        """Release the lock on the currently-loaded session data."""
        self.locks[self.id].release()
        self.locked = False
    
    def __len__(self):
        """Return the number of active sessions."""
        raise NotImplementedError


# Hook functions (for CherryPy tools)

def save():
    """Save any changed session data."""
    
    if not hasattr(cherrypy.serving, "session"):
        return
    request = cherrypy.serving.request
    response = cherrypy.serving.response
    
    # Guard against running twice
    if hasattr(request, "_sessionsaved"):
        return
    request._sessionsaved = True
    
    if response.stream:
        # If the body is being streamed, we have to save the data
        #   *after* the response has been written out
        request.hooks.attach('on_end_request', cherrypy.session.save)
    else:
        # If the body is not being streamed, we save the data now
        # (so we can release the lock).
        if isinstance(response.body, types.GeneratorType):
            response.collapse_body()
        cherrypy.session.save()
save.failsafe = True

def close():
    """Close the session object for this request."""
    sess = getattr(cherrypy.serving, "session", None)
    if getattr(sess, "locked", False):
        # If the session is still locked we release the lock
        sess.release_lock()
close.failsafe = True
close.priority = 90


def init(storage_type='ram', path=None, path_header=None, name='session_id',
         timeout=60, domain=None, secure=False, clean_freq=5,
         persistent=True, httponly=False, debug=False, **kwargs):
    """Initialize session object (using cookies).
    
    storage_type
        One of 'ram', 'file', 'postgresql', 'memcached'. This will be
        used to look up the corresponding class in cherrypy.lib.sessions
        globals. For example, 'file' will use the FileSession class.
    
    path
        The 'path' value to stick in the response cookie metadata.
    
    path_header
        If 'path' is None (the default), then the response
        cookie 'path' will be pulled from request.headers[path_header].
    
    name
        The name of the cookie.
    
    timeout
        The expiration timeout (in minutes) for the stored session data.
        If 'persistent' is True (the default), this is also the timeout
        for the cookie.
    
    domain
        The cookie domain.
    
    secure
        If False (the default) the cookie 'secure' value will not
        be set. If True, the cookie 'secure' value will be set (to 1).
    
    clean_freq (minutes)
        The poll rate for expired session cleanup.
    
    persistent
        If True (the default), the 'timeout' argument will be used
        to expire the cookie. If False, the cookie will not have an expiry,
        and the cookie will be a "session cookie" which expires when the
        browser is closed.
    
    httponly
        If False (the default) the cookie 'httponly' value will not be set.
        If True, the cookie 'httponly' value will be set (to 1).
    
    Any additional kwargs will be bound to the new Session instance,
    and may be specific to the storage type. See the subclass of Session
    you're using for more information.
    """
    
    request = cherrypy.serving.request
    
    # Guard against running twice
    if hasattr(request, "_session_init_flag"):
        return
    request._session_init_flag = True
    
    # Check if request came with a session ID
    id = None
    if name in request.cookie:
        id = request.cookie[name].value
        if debug:
            cherrypy.log('ID obtained from request.cookie: %r' % id,
                         'TOOLS.SESSIONS')
    
    # Find the storage class and call setup (first time only).
    storage_class = storage_type.title() + 'Session'
    storage_class = globals()[storage_class]
    if not hasattr(cherrypy, "session"):
        if hasattr(storage_class, "setup"):
            storage_class.setup(**kwargs)
    
    # Create and attach a new Session instance to cherrypy.serving.
    # It will possess a reference to (and lock, and lazily load)
    # the requested session data.
    kwargs['timeout'] = timeout
    kwargs['clean_freq'] = clean_freq
    cherrypy.serving.session = sess = storage_class(id, **kwargs)
    sess.debug = debug
    def update_cookie(id):
        """Update the cookie every time the session id changes."""
        cherrypy.serving.response.cookie[name] = id
    sess.id_observers.append(update_cookie)
    
    # Create cherrypy.session which will proxy to cherrypy.serving.session
    if not hasattr(cherrypy, "session"):
        cherrypy.session = cherrypy._ThreadLocalProxy('session')
    
    if persistent:
        cookie_timeout = timeout
    else:
        # See http://support.microsoft.com/kb/223799/EN-US/
        # and http://support.mozilla.com/en-US/kb/Cookies
        cookie_timeout = None
    set_response_cookie(path=path, path_header=path_header, name=name,
                        timeout=cookie_timeout, domain=domain, secure=secure,
                        httponly=httponly)


def set_response_cookie(path=None, path_header=None, name='session_id',
                        timeout=60, domain=None, secure=False, httponly=False):
    """Set a response cookie for the client.
    
    path
        the 'path' value to stick in the response cookie metadata.

    path_header
        if 'path' is None (the default), then the response
        cookie 'path' will be pulled from request.headers[path_header].

    name
        the name of the cookie.

    timeout
        the expiration timeout for the cookie. If 0 or other boolean
        False, no 'expires' param will be set, and the cookie will be a
        "session cookie" which expires when the browser is closed.

    domain
        the cookie domain.

    secure
        if False (the default) the cookie 'secure' value will not
        be set. If True, the cookie 'secure' value will be set (to 1).

    httponly
        If False (the default) the cookie 'httponly' value will not be set.
        If True, the cookie 'httponly' value will be set (to 1).

    """
    # Set response cookie
    cookie = cherrypy.serving.response.cookie
    cookie[name] = cherrypy.serving.session.id
    cookie[name]['path'] = (path or cherrypy.serving.request.headers.get(path_header)
                            or '/')
    
    # We'd like to use the "max-age" param as indicated in
    # http://www.faqs.org/rfcs/rfc2109.html but IE doesn't
    # save it to disk and the session is lost if people close
    # the browser. So we have to use the old "expires" ... sigh ...
##    cookie[name]['max-age'] = timeout * 60
    if timeout:
        e = time.time() + (timeout * 60)
        cookie[name]['expires'] = httputil.HTTPDate(e)
    if domain is not None:
        cookie[name]['domain'] = domain
    if secure:
        cookie[name]['secure'] = 1
    if httponly:
        if not cookie[name].isReservedKey('httponly'):
            raise ValueError("The httponly cookie token is not supported.")
        cookie[name]['httponly'] = 1

def expire():
    """Expire the current session cookie."""
    name = cherrypy.serving.request.config.get('tools.sessions.name', 'session_id')
    one_year = 60 * 60 * 24 * 365
    e = time.time() - one_year
    cherrypy.serving.response.cookie[name]['expires'] = httputil.HTTPDate(e)



########NEW FILE########
__FILENAME__ = static
try:
    from io import UnsupportedOperation
except ImportError:
    UnsupportedOperation = object()
import logging
import mimetypes
mimetypes.init()
mimetypes.types_map['.dwg']='image/x-dwg'
mimetypes.types_map['.ico']='image/x-icon'
mimetypes.types_map['.bz2']='application/x-bzip2'
mimetypes.types_map['.gz']='application/x-gzip'

import os
import re
import stat
import time

import cherrypy
from cherrypy._cpcompat import ntob, unquote
from cherrypy.lib import cptools, httputil, file_generator_limited


def serve_file(path, content_type=None, disposition=None, name=None, debug=False):
    """Set status, headers, and body in order to serve the given path.
    
    The Content-Type header will be set to the content_type arg, if provided.
    If not provided, the Content-Type will be guessed by the file extension
    of the 'path' argument.
    
    If disposition is not None, the Content-Disposition header will be set
    to "<disposition>; filename=<name>". If name is None, it will be set
    to the basename of path. If disposition is None, no Content-Disposition
    header will be written.
    """
    
    response = cherrypy.serving.response
    
    # If path is relative, users should fix it by making path absolute.
    # That is, CherryPy should not guess where the application root is.
    # It certainly should *not* use cwd (since CP may be invoked from a
    # variety of paths). If using tools.staticdir, you can make your relative
    # paths become absolute by supplying a value for "tools.staticdir.root".
    if not os.path.isabs(path):
        msg = "'%s' is not an absolute path." % path
        if debug:
            cherrypy.log(msg, 'TOOLS.STATICFILE')
        raise ValueError(msg)
    
    try:
        st = os.stat(path)
    except OSError:
        if debug:
            cherrypy.log('os.stat(%r) failed' % path, 'TOOLS.STATIC')
        raise cherrypy.NotFound()
    
    # Check if path is a directory.
    if stat.S_ISDIR(st.st_mode):
        # Let the caller deal with it as they like.
        if debug:
            cherrypy.log('%r is a directory' % path, 'TOOLS.STATIC')
        raise cherrypy.NotFound()
    
    # Set the Last-Modified response header, so that
    # modified-since validation code can work.
    response.headers['Last-Modified'] = httputil.HTTPDate(st.st_mtime)
    cptools.validate_since()
    
    if content_type is None:
        # Set content-type based on filename extension
        ext = ""
        i = path.rfind('.')
        if i != -1:
            ext = path[i:].lower()
        content_type = mimetypes.types_map.get(ext, None)
    if content_type is not None:
        response.headers['Content-Type'] = content_type
    if debug:
        cherrypy.log('Content-Type: %r' % content_type, 'TOOLS.STATIC')
    
    cd = None
    if disposition is not None:
        if name is None:
            name = os.path.basename(path)
        cd = '%s; filename="%s"' % (disposition, name)
        response.headers["Content-Disposition"] = cd
    if debug:
        cherrypy.log('Content-Disposition: %r' % cd, 'TOOLS.STATIC')
    
    # Set Content-Length and use an iterable (file object)
    #   this way CP won't load the whole file in memory
    content_length = st.st_size
    fileobj = open(path, 'rb')
    return _serve_fileobj(fileobj, content_type, content_length, debug=debug)

def serve_fileobj(fileobj, content_type=None, disposition=None, name=None,
                  debug=False):
    """Set status, headers, and body in order to serve the given file object.
    
    The Content-Type header will be set to the content_type arg, if provided.
    
    If disposition is not None, the Content-Disposition header will be set
    to "<disposition>; filename=<name>". If name is None, 'filename' will
    not be set. If disposition is None, no Content-Disposition header will
    be written.

    CAUTION: If the request contains a 'Range' header, one or more seek()s will
    be performed on the file object.  This may cause undesired behavior if
    the file object is not seekable.  It could also produce undesired results
    if the caller set the read position of the file object prior to calling
    serve_fileobj(), expecting that the data would be served starting from that
    position.
    """
    
    response = cherrypy.serving.response
    
    try:
        st = os.fstat(fileobj.fileno())
    except AttributeError:
        if debug:
            cherrypy.log('os has no fstat attribute', 'TOOLS.STATIC')
        content_length = None
    except UnsupportedOperation:
        content_length = None
    else:
        # Set the Last-Modified response header, so that
        # modified-since validation code can work.
        response.headers['Last-Modified'] = httputil.HTTPDate(st.st_mtime)
        cptools.validate_since()
        content_length = st.st_size
    
    if content_type is not None:
        response.headers['Content-Type'] = content_type
    if debug:
        cherrypy.log('Content-Type: %r' % content_type, 'TOOLS.STATIC')
    
    cd = None
    if disposition is not None:
        if name is None:
            cd = disposition
        else:
            cd = '%s; filename="%s"' % (disposition, name)
        response.headers["Content-Disposition"] = cd
    if debug:
        cherrypy.log('Content-Disposition: %r' % cd, 'TOOLS.STATIC')
    
    return _serve_fileobj(fileobj, content_type, content_length, debug=debug)

def _serve_fileobj(fileobj, content_type, content_length, debug=False):
    """Internal. Set response.body to the given file object, perhaps ranged."""
    response = cherrypy.serving.response
    
    # HTTP/1.0 didn't have Range/Accept-Ranges headers, or the 206 code
    request = cherrypy.serving.request
    if request.protocol >= (1, 1):
        response.headers["Accept-Ranges"] = "bytes"
        r = httputil.get_ranges(request.headers.get('Range'), content_length)
        if r == []:
            response.headers['Content-Range'] = "bytes */%s" % content_length
            message = "Invalid Range (first-byte-pos greater than Content-Length)"
            if debug:
                cherrypy.log(message, 'TOOLS.STATIC')
            raise cherrypy.HTTPError(416, message)
        
        if r:
            if len(r) == 1:
                # Return a single-part response.
                start, stop = r[0]
                if stop > content_length:
                    stop = content_length
                r_len = stop - start
                if debug:
                    cherrypy.log('Single part; start: %r, stop: %r' % (start, stop),
                                 'TOOLS.STATIC')
                response.status = "206 Partial Content"
                response.headers['Content-Range'] = (
                    "bytes %s-%s/%s" % (start, stop - 1, content_length))
                response.headers['Content-Length'] = r_len
                fileobj.seek(start)
                response.body = file_generator_limited(fileobj, r_len)
            else:
                # Return a multipart/byteranges response.
                response.status = "206 Partial Content"
                try:
                    # Python 3
                    from email.generator import _make_boundary as choose_boundary
                except ImportError:
                    # Python 2
                    from mimetools import choose_boundary
                boundary = choose_boundary()
                ct = "multipart/byteranges; boundary=%s" % boundary
                response.headers['Content-Type'] = ct
                if "Content-Length" in response.headers:
                    # Delete Content-Length header so finalize() recalcs it.
                    del response.headers["Content-Length"]
                
                def file_ranges():
                    # Apache compatibility:
                    yield ntob("\r\n")
                    
                    for start, stop in r:
                        if debug:
                            cherrypy.log('Multipart; start: %r, stop: %r' % (start, stop),
                                         'TOOLS.STATIC')
                        yield ntob("--" + boundary, 'ascii')
                        yield ntob("\r\nContent-type: %s" % content_type, 'ascii')
                        yield ntob("\r\nContent-range: bytes %s-%s/%s\r\n\r\n"
                                   % (start, stop - 1, content_length), 'ascii')
                        fileobj.seek(start)
                        for chunk in file_generator_limited(fileobj, stop-start):
                            yield chunk
                        yield ntob("\r\n")
                    # Final boundary
                    yield ntob("--" + boundary + "--", 'ascii')
                    
                    # Apache compatibility:
                    yield ntob("\r\n")
                response.body = file_ranges()
            return response.body
        else:
            if debug:
                cherrypy.log('No byteranges requested', 'TOOLS.STATIC')
    
    # Set Content-Length and use an iterable (file object)
    #   this way CP won't load the whole file in memory
    response.headers['Content-Length'] = content_length
    response.body = fileobj
    return response.body

def serve_download(path, name=None):
    """Serve 'path' as an application/x-download attachment."""
    # This is such a common idiom I felt it deserved its own wrapper.
    return serve_file(path, "application/x-download", "attachment", name)


def _attempt(filename, content_types, debug=False):
    if debug:
        cherrypy.log('Attempting %r (content_types %r)' %
                     (filename, content_types), 'TOOLS.STATICDIR')
    try:
        # you can set the content types for a
        # complete directory per extension
        content_type = None
        if content_types:
            r, ext = os.path.splitext(filename)
            content_type = content_types.get(ext[1:], None)
        serve_file(filename, content_type=content_type, debug=debug)
        return True
    except cherrypy.NotFound:
        # If we didn't find the static file, continue handling the
        # request. We might find a dynamic handler instead.
        if debug:
            cherrypy.log('NotFound', 'TOOLS.STATICFILE')
        return False

def staticdir(section, dir, root="", match="", content_types=None, index="",
              debug=False):
    """Serve a static resource from the given (root +) dir.
    
    match
        If given, request.path_info will be searched for the given
        regular expression before attempting to serve static content.
    
    content_types
        If given, it should be a Python dictionary of
        {file-extension: content-type} pairs, where 'file-extension' is
        a string (e.g. "gif") and 'content-type' is the value to write
        out in the Content-Type response header (e.g. "image/gif").
    
    index
        If provided, it should be the (relative) name of a file to
        serve for directory requests. For example, if the dir argument is
        '/home/me', the Request-URI is 'myapp', and the index arg is
        'index.html', the file '/home/me/myapp/index.html' will be sought.
    """
    request = cherrypy.serving.request
    if request.method not in ('GET', 'HEAD'):
        if debug:
            cherrypy.log('request.method not GET or HEAD', 'TOOLS.STATICDIR')
        return False
    
    if match and not re.search(match, request.path_info):
        if debug:
            cherrypy.log('request.path_info %r does not match pattern %r' %
                         (request.path_info, match), 'TOOLS.STATICDIR')
        return False
    
    # Allow the use of '~' to refer to a user's home directory.
    dir = os.path.expanduser(dir)

    # If dir is relative, make absolute using "root".
    if not os.path.isabs(dir):
        if not root:
            msg = "Static dir requires an absolute dir (or root)."
            if debug:
                cherrypy.log(msg, 'TOOLS.STATICDIR')
            raise ValueError(msg)
        dir = os.path.join(root, dir)
    
    # Determine where we are in the object tree relative to 'section'
    # (where the static tool was defined).
    if section == 'global':
        section = "/"
    section = section.rstrip(r"\/")
    branch = request.path_info[len(section) + 1:]
    branch = unquote(branch.lstrip(r"\/"))
    
    # If branch is "", filename will end in a slash
    filename = os.path.join(dir, branch)
    if debug:
        cherrypy.log('Checking file %r to fulfill %r' %
                     (filename, request.path_info), 'TOOLS.STATICDIR')
    
    # There's a chance that the branch pulled from the URL might
    # have ".." or similar uplevel attacks in it. Check that the final
    # filename is a child of dir.
    if not os.path.normpath(filename).startswith(os.path.normpath(dir)):
        raise cherrypy.HTTPError(403) # Forbidden
    
    handled = _attempt(filename, content_types)
    if not handled:
        # Check for an index file if a folder was requested.
        if index:
            handled = _attempt(os.path.join(filename, index), content_types)
            if handled:
                request.is_index = filename[-1] in (r"\/")
    return handled

def staticfile(filename, root=None, match="", content_types=None, debug=False):
    """Serve a static resource from the given (root +) filename.
    
    match
        If given, request.path_info will be searched for the given
        regular expression before attempting to serve static content.
    
    content_types
        If given, it should be a Python dictionary of
        {file-extension: content-type} pairs, where 'file-extension' is
        a string (e.g. "gif") and 'content-type' is the value to write
        out in the Content-Type response header (e.g. "image/gif").
    
    """
    request = cherrypy.serving.request
    if request.method not in ('GET', 'HEAD'):
        if debug:
            cherrypy.log('request.method not GET or HEAD', 'TOOLS.STATICFILE')
        return False
    
    if match and not re.search(match, request.path_info):
        if debug:
            cherrypy.log('request.path_info %r does not match pattern %r' %
                         (request.path_info, match), 'TOOLS.STATICFILE')
        return False
    
    # If filename is relative, make absolute using "root".
    if not os.path.isabs(filename):
        if not root:
            msg = "Static tool requires an absolute filename (got '%s')." % filename
            if debug:
                cherrypy.log(msg, 'TOOLS.STATICFILE')
            raise ValueError(msg)
        filename = os.path.join(root, filename)
    
    return _attempt(filename, content_types, debug=debug)

########NEW FILE########
__FILENAME__ = xmlrpcutil
import sys

import cherrypy
from cherrypy._cpcompat import ntob

def get_xmlrpclib():
    try:
        import xmlrpc.client as x
    except ImportError:
        import xmlrpclib as x
    return x

def process_body():
    """Return (params, method) from request body."""
    try:
        return get_xmlrpclib().loads(cherrypy.request.body.read())
    except Exception:
        return ('ERROR PARAMS', ), 'ERRORMETHOD'


def patched_path(path):
    """Return 'path', doctored for RPC."""
    if not path.endswith('/'):
        path += '/'
    if path.startswith('/RPC2/'):
        # strip the first /rpc2
        path = path[5:]
    return path


def _set_response(body):
    # The XML-RPC spec (http://www.xmlrpc.com/spec) says:
    # "Unless there's a lower-level error, always return 200 OK."
    # Since Python's xmlrpclib interprets a non-200 response
    # as a "Protocol Error", we'll just return 200 every time.
    response = cherrypy.response
    response.status = '200 OK'
    response.body = ntob(body, 'utf-8')
    response.headers['Content-Type'] = 'text/xml'
    response.headers['Content-Length'] = len(body)


def respond(body, encoding='utf-8', allow_none=0):
    xmlrpclib = get_xmlrpclib()
    if not isinstance(body, xmlrpclib.Fault):
        body = (body,)
    _set_response(xmlrpclib.dumps(body, methodresponse=1,
                                  encoding=encoding,
                                  allow_none=allow_none))

def on_error(*args, **kwargs):
    body = str(sys.exc_info()[1])
    xmlrpclib = get_xmlrpclib()
    _set_response(xmlrpclib.dumps(xmlrpclib.Fault(1, body)))


########NEW FILE########
__FILENAME__ = plugins
"""Site services for use with a Web Site Process Bus."""

import os
import re
import signal as _signal
import sys
import time
import threading

from cherrypy._cpcompat import basestring, get_daemon, get_thread_ident, ntob, set

# _module__file__base is used by Autoreload to make
# absolute any filenames retrieved from sys.modules which are not
# already absolute paths.  This is to work around Python's quirk
# of importing the startup script and using a relative filename
# for it in sys.modules.
#
# Autoreload examines sys.modules afresh every time it runs. If an application
# changes the current directory by executing os.chdir(), then the next time
# Autoreload runs, it will not be able to find any filenames which are
# not absolute paths, because the current directory is not the same as when the
# module was first imported.  Autoreload will then wrongly conclude the file has
# "changed", and initiate the shutdown/re-exec sequence.
# See ticket #917.
# For this workaround to have a decent probability of success, this module
# needs to be imported as early as possible, before the app has much chance
# to change the working directory.
_module__file__base = os.getcwd()


class SimplePlugin(object):
    """Plugin base class which auto-subscribes methods for known channels."""
    
    bus = None
    """A :class:`Bus <cherrypy.process.wspbus.Bus>`, usually cherrypy.engine."""
    
    def __init__(self, bus):
        self.bus = bus
    
    def subscribe(self):
        """Register this object as a (multi-channel) listener on the bus."""
        for channel in self.bus.listeners:
            # Subscribe self.start, self.exit, etc. if present.
            method = getattr(self, channel, None)
            if method is not None:
                self.bus.subscribe(channel, method)
    
    def unsubscribe(self):
        """Unregister this object as a listener on the bus."""
        for channel in self.bus.listeners:
            # Unsubscribe self.start, self.exit, etc. if present.
            method = getattr(self, channel, None)
            if method is not None:
                self.bus.unsubscribe(channel, method)



class SignalHandler(object):
    """Register bus channels (and listeners) for system signals.
    
    You can modify what signals your application listens for, and what it does
    when it receives signals, by modifying :attr:`SignalHandler.handlers`,
    a dict of {signal name: callback} pairs. The default set is::
    
        handlers = {'SIGTERM': self.bus.exit,
                    'SIGHUP': self.handle_SIGHUP,
                    'SIGUSR1': self.bus.graceful,
                   }
    
    The :func:`SignalHandler.handle_SIGHUP`` method calls
    :func:`bus.restart()<cherrypy.process.wspbus.Bus.restart>`
    if the process is daemonized, but
    :func:`bus.exit()<cherrypy.process.wspbus.Bus.exit>`
    if the process is attached to a TTY. This is because Unix window
    managers tend to send SIGHUP to terminal windows when the user closes them.
    
    Feel free to add signals which are not available on every platform. The
    :class:`SignalHandler` will ignore errors raised from attempting to register
    handlers for unknown signals.
    """
    
    handlers = {}
    """A map from signal names (e.g. 'SIGTERM') to handlers (e.g. bus.exit)."""
    
    signals = {}
    """A map from signal numbers to names."""
    
    for k, v in vars(_signal).items():
        if k.startswith('SIG') and not k.startswith('SIG_'):
            signals[v] = k
    del k, v
    
    def __init__(self, bus):
        self.bus = bus
        # Set default handlers
        self.handlers = {'SIGTERM': self.bus.exit,
                         'SIGHUP': self.handle_SIGHUP,
                         'SIGUSR1': self.bus.graceful,
                         }

        if sys.platform[:4] == 'java':
            del self.handlers['SIGUSR1']
            self.handlers['SIGUSR2'] = self.bus.graceful
            self.bus.log("SIGUSR1 cannot be set on the JVM platform. "
                         "Using SIGUSR2 instead.")
            self.handlers['SIGINT'] = self._jython_SIGINT_handler

        self._previous_handlers = {}
    
    def _jython_SIGINT_handler(self, signum=None, frame=None):
        # See http://bugs.jython.org/issue1313
        self.bus.log('Keyboard Interrupt: shutting down bus')
        self.bus.exit()
        
    def subscribe(self):
        """Subscribe self.handlers to signals."""
        for sig, func in self.handlers.items():
            try:
                self.set_handler(sig, func)
            except ValueError:
                pass
    
    def unsubscribe(self):
        """Unsubscribe self.handlers from signals."""
        for signum, handler in self._previous_handlers.items():
            signame = self.signals[signum]
            
            if handler is None:
                self.bus.log("Restoring %s handler to SIG_DFL." % signame)
                handler = _signal.SIG_DFL
            else:
                self.bus.log("Restoring %s handler %r." % (signame, handler))
            
            try:
                our_handler = _signal.signal(signum, handler)
                if our_handler is None:
                    self.bus.log("Restored old %s handler %r, but our "
                                 "handler was not registered." %
                                 (signame, handler), level=30)
            except ValueError:
                self.bus.log("Unable to restore %s handler %r." %
                             (signame, handler), level=40, traceback=True)
    
    def set_handler(self, signal, listener=None):
        """Subscribe a handler for the given signal (number or name).
        
        If the optional 'listener' argument is provided, it will be
        subscribed as a listener for the given signal's channel.
        
        If the given signal name or number is not available on the current
        platform, ValueError is raised.
        """
        if isinstance(signal, basestring):
            signum = getattr(_signal, signal, None)
            if signum is None:
                raise ValueError("No such signal: %r" % signal)
            signame = signal
        else:
            try:
                signame = self.signals[signal]
            except KeyError:
                raise ValueError("No such signal: %r" % signal)
            signum = signal
        
        prev = _signal.signal(signum, self._handle_signal)
        self._previous_handlers[signum] = prev
        
        if listener is not None:
            self.bus.log("Listening for %s." % signame)
            self.bus.subscribe(signame, listener)
    
    def _handle_signal(self, signum=None, frame=None):
        """Python signal handler (self.set_handler subscribes it for you)."""
        signame = self.signals[signum]
        self.bus.log("Caught signal %s." % signame)
        self.bus.publish(signame)
    
    def handle_SIGHUP(self):
        """Restart if daemonized, else exit."""
        if os.isatty(sys.stdin.fileno()):
            # not daemonized (may be foreground or background)
            self.bus.log("SIGHUP caught but not daemonized. Exiting.")
            self.bus.exit()
        else:
            self.bus.log("SIGHUP caught while daemonized. Restarting.")
            self.bus.restart()


try:
    import pwd, grp
except ImportError:
    pwd, grp = None, None


class DropPrivileges(SimplePlugin):
    """Drop privileges. uid/gid arguments not available on Windows.
    
    Special thanks to Gavin Baker: http://antonym.org/node/100.
    """
    
    def __init__(self, bus, umask=None, uid=None, gid=None):
        SimplePlugin.__init__(self, bus)
        self.finalized = False
        self.uid = uid
        self.gid = gid
        self.umask = umask
    
    def _get_uid(self):
        return self._uid
    def _set_uid(self, val):
        if val is not None:
            if pwd is None:
                self.bus.log("pwd module not available; ignoring uid.",
                             level=30)
                val = None
            elif isinstance(val, basestring):
                val = pwd.getpwnam(val)[2]
        self._uid = val
    uid = property(_get_uid, _set_uid,
        doc="The uid under which to run. Availability: Unix.")
    
    def _get_gid(self):
        return self._gid
    def _set_gid(self, val):
        if val is not None:
            if grp is None:
                self.bus.log("grp module not available; ignoring gid.",
                             level=30)
                val = None
            elif isinstance(val, basestring):
                val = grp.getgrnam(val)[2]
        self._gid = val
    gid = property(_get_gid, _set_gid,
        doc="The gid under which to run. Availability: Unix.")
    
    def _get_umask(self):
        return self._umask
    def _set_umask(self, val):
        if val is not None:
            try:
                os.umask
            except AttributeError:
                self.bus.log("umask function not available; ignoring umask.",
                             level=30)
                val = None
        self._umask = val
    umask = property(_get_umask, _set_umask,
        doc="""The default permission mode for newly created files and directories.
        
        Usually expressed in octal format, for example, ``0644``.
        Availability: Unix, Windows.
        """)
    
    def start(self):
        # uid/gid
        def current_ids():
            """Return the current (uid, gid) if available."""
            name, group = None, None
            if pwd:
                name = pwd.getpwuid(os.getuid())[0]
            if grp:
                group = grp.getgrgid(os.getgid())[0]
            return name, group
        
        if self.finalized:
            if not (self.uid is None and self.gid is None):
                self.bus.log('Already running as uid: %r gid: %r' %
                             current_ids())
        else:
            if self.uid is None and self.gid is None:
                if pwd or grp:
                    self.bus.log('uid/gid not set', level=30)
            else:
                self.bus.log('Started as uid: %r gid: %r' % current_ids())
                if self.gid is not None:
                    os.setgid(self.gid)
                    os.setgroups([])
                if self.uid is not None:
                    os.setuid(self.uid)
                self.bus.log('Running as uid: %r gid: %r' % current_ids())
        
        # umask
        if self.finalized:
            if self.umask is not None:
                self.bus.log('umask already set to: %03o' % self.umask)
        else:
            if self.umask is None:
                self.bus.log('umask not set', level=30)
            else:
                old_umask = os.umask(self.umask)
                self.bus.log('umask old: %03o, new: %03o' %
                             (old_umask, self.umask))
        
        self.finalized = True
    # This is slightly higher than the priority for server.start
    # in order to facilitate the most common use: starting on a low
    # port (which requires root) and then dropping to another user.
    start.priority = 77


class Daemonizer(SimplePlugin):
    """Daemonize the running script.
    
    Use this with a Web Site Process Bus via::
    
        Daemonizer(bus).subscribe()
    
    When this component finishes, the process is completely decoupled from
    the parent environment. Please note that when this component is used,
    the return code from the parent process will still be 0 if a startup
    error occurs in the forked children. Errors in the initial daemonizing
    process still return proper exit codes. Therefore, if you use this
    plugin to daemonize, don't use the return code as an accurate indicator
    of whether the process fully started. In fact, that return code only
    indicates if the process succesfully finished the first fork.
    """
    
    def __init__(self, bus, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):
        SimplePlugin.__init__(self, bus)
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.finalized = False
    
    def start(self):
        if self.finalized:
            self.bus.log('Already deamonized.')
        
        # forking has issues with threads:
        # http://www.opengroup.org/onlinepubs/000095399/functions/fork.html
        # "The general problem with making fork() work in a multi-threaded
        #  world is what to do with all of the threads..."
        # So we check for active threads:
        if threading.activeCount() != 1:
            self.bus.log('There are %r active threads. '
                         'Daemonizing now may cause strange failures.' %
                         threading.enumerate(), level=30)
        
        # See http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        # (or http://www.faqs.org/faqs/unix-faq/programmer/faq/ section 1.7)
        # and http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
        
        # Finish up with the current stdout/stderr
        sys.stdout.flush()
        sys.stderr.flush()
        
        # Do first fork.
        try:
            pid = os.fork()
            if pid == 0:
                # This is the child process. Continue.
                pass
            else:
                # This is the first parent. Exit, now that we've forked.
                self.bus.log('Forking once.')
                os._exit(0)
        except OSError:
            # Python raises OSError rather than returning negative numbers.
            exc = sys.exc_info()[1]
            sys.exit("%s: fork #1 failed: (%d) %s\n"
                     % (sys.argv[0], exc.errno, exc.strerror))
        
        os.setsid()
        
        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                self.bus.log('Forking twice.')
                os._exit(0) # Exit second parent
        except OSError:
            exc = sys.exc_info()[1]
            sys.exit("%s: fork #2 failed: (%d) %s\n"
                     % (sys.argv[0], exc.errno, exc.strerror))
        
        os.chdir("/")
        os.umask(0)
        
        si = open(self.stdin, "r")
        so = open(self.stdout, "a+")
        se = open(self.stderr, "a+")

        # os.dup2(fd, fd2) will close fd2 if necessary,
        # so we don't explicitly close stdin/out/err.
        # See http://docs.python.org/lib/os-fd-ops.html
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
        self.bus.log('Daemonized to PID: %s' % os.getpid())
        self.finalized = True
    start.priority = 65


class PIDFile(SimplePlugin):
    """Maintain a PID file via a WSPBus."""
    
    def __init__(self, bus, pidfile):
        SimplePlugin.__init__(self, bus)
        self.pidfile = pidfile
        self.finalized = False
    
    def start(self):
        pid = os.getpid()
        if self.finalized:
            self.bus.log('PID %r already written to %r.' % (pid, self.pidfile))
        else:
            open(self.pidfile, "wb").write(ntob("%s" % pid, 'utf8'))
            self.bus.log('PID %r written to %r.' % (pid, self.pidfile))
            self.finalized = True
    start.priority = 70
    
    def exit(self):
        try:
            os.remove(self.pidfile)
            self.bus.log('PID file removed: %r.' % self.pidfile)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass


class PerpetualTimer(threading._Timer):
    """A responsive subclass of threading._Timer whose run() method repeats.
    
    Use this timer only when you really need a very interruptible timer;
    this checks its 'finished' condition up to 20 times a second, which can
    results in pretty high CPU usage 
    """
    
    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.isSet():
                return
            try:
                self.function(*self.args, **self.kwargs)
            except Exception:
                self.bus.log("Error in perpetual timer thread function %r." %
                             self.function, level=40, traceback=True)
                # Quit on first error to avoid massive logs.
                raise


class BackgroundTask(threading.Thread):
    """A subclass of threading.Thread whose run() method repeats.
    
    Use this class for most repeating tasks. It uses time.sleep() to wait
    for each interval, which isn't very responsive; that is, even if you call
    self.cancel(), you'll have to wait until the sleep() call finishes before
    the thread stops. To compensate, it defaults to being daemonic, which means
    it won't delay stopping the whole process.
    """
    
    def __init__(self, interval, function, args=[], kwargs={}, bus=None):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.running = False
        self.bus = bus
    
    def cancel(self):
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.interval)
            if not self.running:
                return
            try:
                self.function(*self.args, **self.kwargs)
            except Exception:
                if self.bus:
                    self.bus.log("Error in background task thread function %r."
                                 % self.function, level=40, traceback=True)
                # Quit on first error to avoid massive logs.
                raise
    
    def _set_daemon(self):
        return True


class Monitor(SimplePlugin):
    """WSPBus listener to periodically run a callback in its own thread."""
    
    callback = None
    """The function to call at intervals."""
    
    frequency = 60
    """The time in seconds between callback runs."""
    
    thread = None
    """A :class:`BackgroundTask<cherrypy.process.plugins.BackgroundTask>` thread."""
    
    def __init__(self, bus, callback, frequency=60, name=None):
        SimplePlugin.__init__(self, bus)
        self.callback = callback
        self.frequency = frequency
        self.thread = None
        self.name = name
    
    def start(self):
        """Start our callback in its own background thread."""
        if self.frequency > 0:
            threadname = self.name or self.__class__.__name__
            if self.thread is None:
                self.thread = BackgroundTask(self.frequency, self.callback,
                                             bus = self.bus)
                self.thread.setName(threadname)
                self.thread.start()
                self.bus.log("Started monitor thread %r." % threadname)
            else:
                self.bus.log("Monitor thread %r already started." % threadname)
    start.priority = 70
    
    def stop(self):
        """Stop our callback's background task thread."""
        if self.thread is None:
            self.bus.log("No thread running for %s." % self.name or self.__class__.__name__)
        else:
            if self.thread is not threading.currentThread():
                name = self.thread.getName()
                self.thread.cancel()
                if not get_daemon(self.thread):
                    self.bus.log("Joining %r" % name)
                    self.thread.join()
                self.bus.log("Stopped thread %r." % name)
            self.thread = None
    
    def graceful(self):
        """Stop the callback's background task thread and restart it."""
        self.stop()
        self.start()


class Autoreloader(Monitor):
    """Monitor which re-executes the process when files change.
    
    This :ref:`plugin<plugins>` restarts the process (via :func:`os.execv`)
    if any of the files it monitors change (or is deleted). By default, the
    autoreloader monitors all imported modules; you can add to the
    set by adding to ``autoreload.files``::
    
        cherrypy.engine.autoreload.files.add(myFile)
    
    If there are imported files you do *not* wish to monitor, you can adjust the
    ``match`` attribute, a regular expression. For example, to stop monitoring
    cherrypy itself::
    
        cherrypy.engine.autoreload.match = r'^(?!cherrypy).+'
    
    Like all :class:`Monitor<cherrypy.process.plugins.Monitor>` plugins,
    the autoreload plugin takes a ``frequency`` argument. The default is
    1 second; that is, the autoreloader will examine files once each second.
    """
    
    files = None
    """The set of files to poll for modifications."""
    
    frequency = 1
    """The interval in seconds at which to poll for modified files."""
    
    match = '.*'
    """A regular expression by which to match filenames."""
    
    def __init__(self, bus, frequency=1, match='.*'):
        self.mtimes = {}
        self.files = set()
        self.match = match
        Monitor.__init__(self, bus, self.run, frequency)
    
    def start(self):
        """Start our own background task thread for self.run."""
        if self.thread is None:
            self.mtimes = {}
        Monitor.start(self)
    start.priority = 70 
    
    def sysfiles(self):
        """Return a Set of sys.modules filenames to monitor."""
        files = set()
        for k, m in sys.modules.items():
            if re.match(self.match, k):
                if hasattr(m, '__loader__') and hasattr(m.__loader__, 'archive'):
                    f = m.__loader__.archive
                else:
                    f = getattr(m, '__file__', None)
                    if f is not None and not os.path.isabs(f):
                        # ensure absolute paths so a os.chdir() in the app doesn't break me
                        f = os.path.normpath(os.path.join(_module__file__base, f))
                files.add(f)
        return files
    
    def run(self):
        """Reload the process if registered files have been modified."""
        for filename in self.sysfiles() | self.files:
            if filename:
                if filename.endswith('.pyc'):
                    filename = filename[:-1]
                
                oldtime = self.mtimes.get(filename, 0)
                if oldtime is None:
                    # Module with no .py file. Skip it.
                    continue
                
                try:
                    mtime = os.stat(filename).st_mtime
                except OSError:
                    # Either a module with no .py file, or it's been deleted.
                    mtime = None
                
                if filename not in self.mtimes:
                    # If a module has no .py file, this will be None.
                    self.mtimes[filename] = mtime
                else:
                    if mtime is None or mtime > oldtime:
                        # The file has been deleted or modified.
                        self.bus.log("Restarting because %s changed." % filename)
                        self.thread.cancel()
                        self.bus.log("Stopped thread %r." % self.thread.getName())
                        self.bus.restart()
                        return


class ThreadManager(SimplePlugin):
    """Manager for HTTP request threads.
    
    If you have control over thread creation and destruction, publish to
    the 'acquire_thread' and 'release_thread' channels (for each thread).
    This will register/unregister the current thread and publish to
    'start_thread' and 'stop_thread' listeners in the bus as needed.
    
    If threads are created and destroyed by code you do not control
    (e.g., Apache), then, at the beginning of every HTTP request,
    publish to 'acquire_thread' only. You should not publish to
    'release_thread' in this case, since you do not know whether
    the thread will be re-used or not. The bus will call
    'stop_thread' listeners for you when it stops.
    """
    
    threads = None
    """A map of {thread ident: index number} pairs."""
    
    def __init__(self, bus):
        self.threads = {}
        SimplePlugin.__init__(self, bus)
        self.bus.listeners.setdefault('acquire_thread', set())
        self.bus.listeners.setdefault('start_thread', set())
        self.bus.listeners.setdefault('release_thread', set())
        self.bus.listeners.setdefault('stop_thread', set())

    def acquire_thread(self):
        """Run 'start_thread' listeners for the current thread.
        
        If the current thread has already been seen, any 'start_thread'
        listeners will not be run again.
        """
        thread_ident = get_thread_ident()
        if thread_ident not in self.threads:
            # We can't just use get_ident as the thread ID
            # because some platforms reuse thread ID's.
            i = len(self.threads) + 1
            self.threads[thread_ident] = i
            self.bus.publish('start_thread', i)
    
    def release_thread(self):
        """Release the current thread and run 'stop_thread' listeners."""
        thread_ident = get_thread_ident()
        i = self.threads.pop(thread_ident, None)
        if i is not None:
            self.bus.publish('stop_thread', i)
    
    def stop(self):
        """Release all threads and run all 'stop_thread' listeners."""
        for thread_ident, i in self.threads.items():
            self.bus.publish('stop_thread', i)
        self.threads.clear()
    graceful = stop


########NEW FILE########
__FILENAME__ = servers
"""
Starting in CherryPy 3.1, cherrypy.server is implemented as an
:ref:`Engine Plugin<plugins>`. It's an instance of
:class:`cherrypy._cpserver.Server`, which is a subclass of
:class:`cherrypy.process.servers.ServerAdapter`. The ``ServerAdapter`` class
is designed to control other servers, as well.

Multiple servers/ports
======================

If you need to start more than one HTTP server (to serve on multiple ports, or
protocols, etc.), you can manually register each one and then start them all
with engine.start::

    s1 = ServerAdapter(cherrypy.engine, MyWSGIServer(host='0.0.0.0', port=80))
    s2 = ServerAdapter(cherrypy.engine, another.HTTPServer(host='127.0.0.1', SSL=True))
    s1.subscribe()
    s2.subscribe()
    cherrypy.engine.start()

.. index:: SCGI

FastCGI/SCGI
============

There are also Flup\ **F**\ CGIServer and Flup\ **S**\ CGIServer classes in
:mod:`cherrypy.process.servers`. To start an fcgi server, for example,
wrap an instance of it in a ServerAdapter::

    addr = ('0.0.0.0', 4000)
    f = servers.FlupFCGIServer(application=cherrypy.tree, bindAddress=addr)
    s = servers.ServerAdapter(cherrypy.engine, httpserver=f, bind_addr=addr)
    s.subscribe()

The :doc:`cherryd</deployguide/cherryd>` startup script will do the above for
you via its `-f` flag.
Note that you need to download and install `flup <http://trac.saddi.com/flup>`_
yourself, whether you use ``cherryd`` or not.

.. _fastcgi:
.. index:: FastCGI

FastCGI
-------

A very simple setup lets your cherry run with FastCGI.
You just need the flup library,
plus a running Apache server (with ``mod_fastcgi``) or lighttpd server.

CherryPy code
^^^^^^^^^^^^^

hello.py::

    #!/usr/bin/python
    import cherrypy
    
    class HelloWorld:
        \"""Sample request handler class.\"""
        def index(self):
            return "Hello world!"
        index.exposed = True
    
    cherrypy.tree.mount(HelloWorld())
    # CherryPy autoreload must be disabled for the flup server to work
    cherrypy.config.update({'engine.autoreload_on':False})

Then run :doc:`/deployguide/cherryd` with the '-f' arg::

    cherryd -c <myconfig> -d -f -i hello.py

Apache
^^^^^^

At the top level in httpd.conf::

    FastCgiIpcDir /tmp
    FastCgiServer /path/to/cherry.fcgi -idle-timeout 120 -processes 4

And inside the relevant VirtualHost section::

    # FastCGI config
    AddHandler fastcgi-script .fcgi
    ScriptAliasMatch (.*$) /path/to/cherry.fcgi$1

Lighttpd
^^^^^^^^

For `Lighttpd <http://www.lighttpd.net/>`_ you can follow these
instructions. Within ``lighttpd.conf`` make sure ``mod_fastcgi`` is
active within ``server.modules``. Then, within your ``$HTTP["host"]``
directive, configure your fastcgi script like the following::

    $HTTP["url"] =~ "" {
      fastcgi.server = (
        "/" => (
          "script.fcgi" => (
            "bin-path" => "/path/to/your/script.fcgi",
            "socket"          => "/tmp/script.sock",
            "check-local"     => "disable",
            "disable-time"    => 1,
            "min-procs"       => 1,
            "max-procs"       => 1, # adjust as needed
          ),
        ),
      )
    } # end of $HTTP["url"] =~ "^/"

Please see `Lighttpd FastCGI Docs
<http://redmine.lighttpd.net/wiki/lighttpd/Docs:ModFastCGI>`_ for an explanation 
of the possible configuration options.
"""

import sys
import time


class ServerAdapter(object):
    """Adapter for an HTTP server.
    
    If you need to start more than one HTTP server (to serve on multiple
    ports, or protocols, etc.), you can manually register each one and then
    start them all with bus.start:
    
        s1 = ServerAdapter(bus, MyWSGIServer(host='0.0.0.0', port=80))
        s2 = ServerAdapter(bus, another.HTTPServer(host='127.0.0.1', SSL=True))
        s1.subscribe()
        s2.subscribe()
        bus.start()
    """
    
    def __init__(self, bus, httpserver=None, bind_addr=None):
        self.bus = bus
        self.httpserver = httpserver
        self.bind_addr = bind_addr
        self.interrupt = None
        self.running = False
    
    def subscribe(self):
        self.bus.subscribe('start', self.start)
        self.bus.subscribe('stop', self.stop)
    
    def unsubscribe(self):
        self.bus.unsubscribe('start', self.start)
        self.bus.unsubscribe('stop', self.stop)
    
    def start(self):
        """Start the HTTP server."""
        if self.bind_addr is None:
            on_what = "unknown interface (dynamic?)"
        elif isinstance(self.bind_addr, tuple):
            host, port = self.bind_addr
            on_what = "%s:%s" % (host, port)
        else:
            on_what = "socket file: %s" % self.bind_addr
        
        if self.running:
            self.bus.log("Already serving on %s" % on_what)
            return
        
        self.interrupt = None
        if not self.httpserver:
            raise ValueError("No HTTP server has been created.")
        
        # Start the httpserver in a new thread.
        if isinstance(self.bind_addr, tuple):
            wait_for_free_port(*self.bind_addr)
        
        import threading
        t = threading.Thread(target=self._start_http_thread)
        t.setName("HTTPServer " + t.getName())
        t.start()
        
        self.wait()
        self.running = True
        self.bus.log("Serving on %s" % on_what)
    start.priority = 75
    
    def _start_http_thread(self):
        """HTTP servers MUST be running in new threads, so that the
        main thread persists to receive KeyboardInterrupt's. If an
        exception is raised in the httpserver's thread then it's
        trapped here, and the bus (and therefore our httpserver)
        are shut down.
        """
        try:
            self.httpserver.start()
        except KeyboardInterrupt:
            self.bus.log("<Ctrl-C> hit: shutting down HTTP server")
            self.interrupt = sys.exc_info()[1]
            self.bus.exit()
        except SystemExit:
            self.bus.log("SystemExit raised: shutting down HTTP server")
            self.interrupt = sys.exc_info()[1]
            self.bus.exit()
            raise
        except:
            self.interrupt = sys.exc_info()[1]
            self.bus.log("Error in HTTP server: shutting down",
                         traceback=True, level=40)
            self.bus.exit()
            raise
    
    def wait(self):
        """Wait until the HTTP server is ready to receive requests."""
        while not getattr(self.httpserver, "ready", False):
            if self.interrupt:
                raise self.interrupt
            time.sleep(.1)
        
        # Wait for port to be occupied
        if isinstance(self.bind_addr, tuple):
            host, port = self.bind_addr
            wait_for_occupied_port(host, port)
    
    def stop(self):
        """Stop the HTTP server."""
        if self.running:
            # stop() MUST block until the server is *truly* stopped.
            self.httpserver.stop()
            # Wait for the socket to be truly freed.
            if isinstance(self.bind_addr, tuple):
                wait_for_free_port(*self.bind_addr)
            self.running = False
            self.bus.log("HTTP Server %s shut down" % self.httpserver)
        else:
            self.bus.log("HTTP Server %s already shut down" % self.httpserver)
    stop.priority = 25
    
    def restart(self):
        """Restart the HTTP server."""
        self.stop()
        self.start()


class FlupCGIServer(object):
    """Adapter for a flup.server.cgi.WSGIServer."""
   
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.ready = False
    
    def start(self):
        """Start the CGI server."""
        # We have to instantiate the server class here because its __init__
        # starts a threadpool. If we do it too early, daemonize won't work.
        from flup.server.cgi import WSGIServer
       
        self.cgiserver = WSGIServer(*self.args, **self.kwargs)
        self.ready = True
        self.cgiserver.run()
    
    def stop(self):
        """Stop the HTTP server."""
        self.ready = False


class FlupFCGIServer(object):
    """Adapter for a flup.server.fcgi.WSGIServer."""
    
    def __init__(self, *args, **kwargs):
        if kwargs.get('bindAddress', None) is None:
            import socket
            if not hasattr(socket, 'fromfd'):
                raise ValueError(
                    'Dynamic FCGI server not available on this platform. '
                    'You must use a static or external one by providing a '
                    'legal bindAddress.')
        self.args = args
        self.kwargs = kwargs
        self.ready = False
    
    def start(self):
        """Start the FCGI server."""
        # We have to instantiate the server class here because its __init__
        # starts a threadpool. If we do it too early, daemonize won't work.
        from flup.server.fcgi import WSGIServer
        self.fcgiserver = WSGIServer(*self.args, **self.kwargs)
        # TODO: report this bug upstream to flup.
        # If we don't set _oldSIGs on Windows, we get:
        #   File "C:\Python24\Lib\site-packages\flup\server\threadedserver.py",
        #   line 108, in run
        #     self._restoreSignalHandlers()
        #   File "C:\Python24\Lib\site-packages\flup\server\threadedserver.py",
        #   line 156, in _restoreSignalHandlers
        #     for signum,handler in self._oldSIGs:
        #   AttributeError: 'WSGIServer' object has no attribute '_oldSIGs'
        self.fcgiserver._installSignalHandlers = lambda: None
        self.fcgiserver._oldSIGs = []
        self.ready = True
        self.fcgiserver.run()
    
    def stop(self):
        """Stop the HTTP server."""
        # Forcibly stop the fcgi server main event loop.
        self.fcgiserver._keepGoing = False
        # Force all worker threads to die off.
        self.fcgiserver._threadPool.maxSpare = self.fcgiserver._threadPool._idleCount
        self.ready = False


class FlupSCGIServer(object):
    """Adapter for a flup.server.scgi.WSGIServer."""
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.ready = False
    
    def start(self):
        """Start the SCGI server."""
        # We have to instantiate the server class here because its __init__
        # starts a threadpool. If we do it too early, daemonize won't work.
        from flup.server.scgi import WSGIServer
        self.scgiserver = WSGIServer(*self.args, **self.kwargs)
        # TODO: report this bug upstream to flup.
        # If we don't set _oldSIGs on Windows, we get:
        #   File "C:\Python24\Lib\site-packages\flup\server\threadedserver.py",
        #   line 108, in run
        #     self._restoreSignalHandlers()
        #   File "C:\Python24\Lib\site-packages\flup\server\threadedserver.py",
        #   line 156, in _restoreSignalHandlers
        #     for signum,handler in self._oldSIGs:
        #   AttributeError: 'WSGIServer' object has no attribute '_oldSIGs'
        self.scgiserver._installSignalHandlers = lambda: None
        self.scgiserver._oldSIGs = []
        self.ready = True
        self.scgiserver.run()
    
    def stop(self):
        """Stop the HTTP server."""
        self.ready = False
        # Forcibly stop the scgi server main event loop.
        self.scgiserver._keepGoing = False
        # Force all worker threads to die off.
        self.scgiserver._threadPool.maxSpare = 0


def client_host(server_host):
    """Return the host on which a client can connect to the given listener."""
    if server_host == '0.0.0.0':
        # 0.0.0.0 is INADDR_ANY, which should answer on localhost.
        return '127.0.0.1'
    if server_host in ('::', '::0', '::0.0.0.0'):
        # :: is IN6ADDR_ANY, which should answer on localhost.
        # ::0 and ::0.0.0.0 are non-canonical but common ways to write IN6ADDR_ANY.
        return '::1'
    return server_host

def check_port(host, port, timeout=1.0):
    """Raise an error if the given port is not free on the given host."""
    if not host:
        raise ValueError("Host values of '' or None are not allowed.")
    host = client_host(host)
    port = int(port)
    
    import socket
    
    # AF_INET or AF_INET6 socket
    # Get the correct address family for our host (allows IPv6 addresses)
    try:
        info = socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM)
    except socket.gaierror:
        if ':' in host:
            info = [(socket.AF_INET6, socket.SOCK_STREAM, 0, "", (host, port, 0, 0))]
        else:
            info = [(socket.AF_INET, socket.SOCK_STREAM, 0, "", (host, port))]
    
    for res in info:
        af, socktype, proto, canonname, sa = res
        s = None
        try:
            s = socket.socket(af, socktype, proto)
            # See http://groups.google.com/group/cherrypy-users/
            #        browse_frm/thread/bbfe5eb39c904fe0
            s.settimeout(timeout)
            s.connect((host, port))
            s.close()
            raise IOError("Port %s is in use on %s; perhaps the previous "
                          "httpserver did not shut down properly." %
                          (repr(port), repr(host)))
        except socket.error:
            if s:
                s.close()


# Feel free to increase these defaults on slow systems:
free_port_timeout = 0.1
occupied_port_timeout = 1.0

def wait_for_free_port(host, port, timeout=None):
    """Wait for the specified port to become free (drop requests)."""
    if not host:
        raise ValueError("Host values of '' or None are not allowed.")
    if timeout is None:
        timeout = free_port_timeout
    
    for trial in range(50):
        try:
            # we are expecting a free port, so reduce the timeout
            check_port(host, port, timeout=timeout)
        except IOError:
            # Give the old server thread time to free the port.
            time.sleep(timeout)
        else:
            return
    
    raise IOError("Port %r not free on %r" % (port, host))

def wait_for_occupied_port(host, port, timeout=None):
    """Wait for the specified port to become active (receive requests)."""
    if not host:
        raise ValueError("Host values of '' or None are not allowed.")
    if timeout is None:
        timeout = occupied_port_timeout
    
    for trial in range(50):
        try:
            check_port(host, port, timeout=timeout)
        except IOError:
            return
        else:
            time.sleep(timeout)
    
    raise IOError("Port %r not bound on %r" % (port, host))

########NEW FILE########
__FILENAME__ = win32
"""Windows service. Requires pywin32."""

import os
import win32api
import win32con
import win32event
import win32service
import win32serviceutil

from cherrypy.process import wspbus, plugins


class ConsoleCtrlHandler(plugins.SimplePlugin):
    """A WSPBus plugin for handling Win32 console events (like Ctrl-C)."""
    
    def __init__(self, bus):
        self.is_set = False
        plugins.SimplePlugin.__init__(self, bus)
    
    def start(self):
        if self.is_set:
            self.bus.log('Handler for console events already set.', level=40)
            return
        
        result = win32api.SetConsoleCtrlHandler(self.handle, 1)
        if result == 0:
            self.bus.log('Could not SetConsoleCtrlHandler (error %r)' %
                         win32api.GetLastError(), level=40)
        else:
            self.bus.log('Set handler for console events.', level=40)
            self.is_set = True
    
    def stop(self):
        if not self.is_set:
            self.bus.log('Handler for console events already off.', level=40)
            return
        
        try:
            result = win32api.SetConsoleCtrlHandler(self.handle, 0)
        except ValueError:
            # "ValueError: The object has not been registered"
            result = 1
        
        if result == 0:
            self.bus.log('Could not remove SetConsoleCtrlHandler (error %r)' %
                         win32api.GetLastError(), level=40)
        else:
            self.bus.log('Removed handler for console events.', level=40)
            self.is_set = False
    
    def handle(self, event):
        """Handle console control events (like Ctrl-C)."""
        if event in (win32con.CTRL_C_EVENT, win32con.CTRL_LOGOFF_EVENT,
                     win32con.CTRL_BREAK_EVENT, win32con.CTRL_SHUTDOWN_EVENT,
                     win32con.CTRL_CLOSE_EVENT):
            self.bus.log('Console event %s: shutting down bus' % event)
            
            # Remove self immediately so repeated Ctrl-C doesn't re-call it.
            try:
                self.stop()
            except ValueError:
                pass
            
            self.bus.exit()
            # 'First to return True stops the calls'
            return 1
        return 0


class Win32Bus(wspbus.Bus):
    """A Web Site Process Bus implementation for Win32.
    
    Instead of time.sleep, this bus blocks using native win32event objects.
    """
    
    def __init__(self):
        self.events = {}
        wspbus.Bus.__init__(self)
    
    def _get_state_event(self, state):
        """Return a win32event for the given state (creating it if needed)."""
        try:
            return self.events[state]
        except KeyError:
            event = win32event.CreateEvent(None, 0, 0,
                                           "WSPBus %s Event (pid=%r)" %
                                           (state.name, os.getpid()))
            self.events[state] = event
            return event
    
    def _get_state(self):
        return self._state
    def _set_state(self, value):
        self._state = value
        event = self._get_state_event(value)
        win32event.PulseEvent(event)
    state = property(_get_state, _set_state)
    
    def wait(self, state, interval=0.1, channel=None):
        """Wait for the given state(s), KeyboardInterrupt or SystemExit.
        
        Since this class uses native win32event objects, the interval
        argument is ignored.
        """
        if isinstance(state, (tuple, list)):
            # Don't wait for an event that beat us to the punch ;)
            if self.state not in state:
                events = tuple([self._get_state_event(s) for s in state])
                win32event.WaitForMultipleObjects(events, 0, win32event.INFINITE)
        else:
            # Don't wait for an event that beat us to the punch ;)
            if self.state != state:
                event = self._get_state_event(state)
                win32event.WaitForSingleObject(event, win32event.INFINITE)


class _ControlCodes(dict):
    """Control codes used to "signal" a service via ControlService.
    
    User-defined control codes are in the range 128-255. We generally use
    the standard Python value for the Linux signal and add 128. Example:
    
        >>> signal.SIGUSR1
        10
        control_codes['graceful'] = 128 + 10
    """
    
    def key_for(self, obj):
        """For the given value, return its corresponding key."""
        for key, val in self.items():
            if val is obj:
                return key
        raise ValueError("The given object could not be found: %r" % obj)

control_codes = _ControlCodes({'graceful': 138})


def signal_child(service, command):
    if command == 'stop':
        win32serviceutil.StopService(service)
    elif command == 'restart':
        win32serviceutil.RestartService(service)
    else:
        win32serviceutil.ControlService(service, control_codes[command])


class PyWebService(win32serviceutil.ServiceFramework):
    """Python Web Service."""
    
    _svc_name_ = "Python Web Service"
    _svc_display_name_ = "Python Web Service"
    _svc_deps_ = None        # sequence of service names on which this depends
    _exe_name_ = "pywebsvc"
    _exe_args_ = None        # Default to no arguments
    
    # Only exists on Windows 2000 or later, ignored on windows NT
    _svc_description_ = "Python Web Service"
    
    def SvcDoRun(self):
        from cherrypy import process
        process.bus.start()
        process.bus.block()
    
    def SvcStop(self):
        from cherrypy import process
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        process.bus.exit()
    
    def SvcOther(self, control):
        process.bus.publish(control_codes.key_for(control))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PyWebService)

########NEW FILE########
__FILENAME__ = wspbus
"""An implementation of the Web Site Process Bus.

This module is completely standalone, depending only on the stdlib.

Web Site Process Bus
--------------------

A Bus object is used to contain and manage site-wide behavior:
daemonization, HTTP server start/stop, process reload, signal handling,
drop privileges, PID file management, logging for all of these,
and many more.

In addition, a Bus object provides a place for each web framework
to register code that runs in response to site-wide events (like
process start and stop), or which controls or otherwise interacts with
the site-wide components mentioned above. For example, a framework which
uses file-based templates would add known template filenames to an
autoreload component.

Ideally, a Bus object will be flexible enough to be useful in a variety
of invocation scenarios:

 1. The deployer starts a site from the command line via a
    framework-neutral deployment script; applications from multiple frameworks
    are mixed in a single site. Command-line arguments and configuration
    files are used to define site-wide components such as the HTTP server,
    WSGI component graph, autoreload behavior, signal handling, etc.
 2. The deployer starts a site via some other process, such as Apache;
    applications from multiple frameworks are mixed in a single site.
    Autoreload and signal handling (from Python at least) are disabled.
 3. The deployer starts a site via a framework-specific mechanism;
    for example, when running tests, exploring tutorials, or deploying
    single applications from a single framework. The framework controls
    which site-wide components are enabled as it sees fit.

The Bus object in this package uses topic-based publish-subscribe
messaging to accomplish all this. A few topic channels are built in
('start', 'stop', 'exit', 'graceful', 'log', and 'main'). Frameworks and
site containers are free to define their own. If a message is sent to a
channel that has not been defined or has no listeners, there is no effect.

In general, there should only ever be a single Bus object per process.
Frameworks and site containers share a single Bus object by publishing
messages and subscribing listeners.

The Bus object works as a finite state machine which models the current
state of the process. Bus methods move it from one state to another;
those methods then publish to subscribed listeners on the channel for
the new state.::

                        O
                        |
                        V
       STOPPING --> STOPPED --> EXITING -> X
          A   A         |
          |    \___     |
          |        \    |
          |         V   V
        STARTED <-- STARTING

"""

import atexit
import os
import sys
import threading
import time
import traceback as _traceback
import warnings

from cherrypy._cpcompat import set

# Here I save the value of os.getcwd(), which, if I am imported early enough,
# will be the directory from which the startup script was run.  This is needed
# by _do_execv(), to change back to the original directory before execv()ing a
# new process.  This is a defense against the application having changed the
# current working directory (which could make sys.executable "not found" if
# sys.executable is a relative-path, and/or cause other problems).
_startup_cwd = os.getcwd()

class ChannelFailures(Exception):
    """Exception raised when errors occur in a listener during Bus.publish()."""
    delimiter = '\n'
    
    def __init__(self, *args, **kwargs):
        # Don't use 'super' here; Exceptions are old-style in Py2.4
        # See http://www.cherrypy.org/ticket/959
        Exception.__init__(self, *args, **kwargs)
        self._exceptions = list()
    
    def handle_exception(self):
        """Append the current exception to self."""
        self._exceptions.append(sys.exc_info()[1])
    
    def get_instances(self):
        """Return a list of seen exception instances."""
        return self._exceptions[:]
    
    def __str__(self):
        exception_strings = map(repr, self.get_instances())
        return self.delimiter.join(exception_strings)

    __repr__ = __str__

    def __bool__(self):
        return bool(self._exceptions)
    __nonzero__ = __bool__

# Use a flag to indicate the state of the bus.
class _StateEnum(object):
    class State(object):
        name = None
        def __repr__(self):
            return "states.%s" % self.name
    
    def __setattr__(self, key, value):
        if isinstance(value, self.State):
            value.name = key
        object.__setattr__(self, key, value)
states = _StateEnum()
states.STOPPED = states.State()
states.STARTING = states.State()
states.STARTED = states.State()
states.STOPPING = states.State()
states.EXITING = states.State()


try:
    import fcntl
except ImportError:
    max_files = 0
else:
    try:
        max_files = os.sysconf('SC_OPEN_MAX')
    except AttributeError:
        max_files = 1024


class Bus(object):
    """Process state-machine and messenger for HTTP site deployment.
    
    All listeners for a given channel are guaranteed to be called even
    if others at the same channel fail. Each failure is logged, but
    execution proceeds on to the next listener. The only way to stop all
    processing from inside a listener is to raise SystemExit and stop the
    whole server.
    """
    
    states = states
    state = states.STOPPED
    execv = False
    max_cloexec_files = max_files
    
    def __init__(self):
        self.execv = False
        self.state = states.STOPPED
        self.listeners = dict(
            [(channel, set()) for channel
             in ('start', 'stop', 'exit', 'graceful', 'log', 'main')])
        self._priorities = {}
    
    def subscribe(self, channel, callback, priority=None):
        """Add the given callback at the given channel (if not present)."""
        if channel not in self.listeners:
            self.listeners[channel] = set()
        self.listeners[channel].add(callback)
        
        if priority is None:
            priority = getattr(callback, 'priority', 50)
        self._priorities[(channel, callback)] = priority
    
    def unsubscribe(self, channel, callback):
        """Discard the given callback (if present)."""
        listeners = self.listeners.get(channel)
        if listeners and callback in listeners:
            listeners.discard(callback)
            del self._priorities[(channel, callback)]
    
    def publish(self, channel, *args, **kwargs):
        """Return output of all subscribers for the given channel."""
        if channel not in self.listeners:
            return []
        
        exc = ChannelFailures()
        output = []
        
        items = [(self._priorities[(channel, listener)], listener)
                 for listener in self.listeners[channel]]
        try:
            items.sort(key=lambda item: item[0])
        except TypeError:
            # Python 2.3 had no 'key' arg, but that doesn't matter
            # since it could sort dissimilar types just fine.
            items.sort()
        for priority, listener in items:
            try:
                output.append(listener(*args, **kwargs))
            except KeyboardInterrupt:
                raise
            except SystemExit:
                e = sys.exc_info()[1]
                # If we have previous errors ensure the exit code is non-zero
                if exc and e.code == 0:
                    e.code = 1
                raise
            except:
                exc.handle_exception()
                if channel == 'log':
                    # Assume any further messages to 'log' will fail.
                    pass
                else:
                    self.log("Error in %r listener %r" % (channel, listener),
                             level=40, traceback=True)
        if exc:
            raise exc
        return output
    
    def _clean_exit(self):
        """An atexit handler which asserts the Bus is not running."""
        if self.state != states.EXITING:
            warnings.warn(
                "The main thread is exiting, but the Bus is in the %r state; "
                "shutting it down automatically now. You must either call "
                "bus.block() after start(), or call bus.exit() before the "
                "main thread exits." % self.state, RuntimeWarning)
            self.exit()
    
    def start(self):
        """Start all services."""
        atexit.register(self._clean_exit)
        
        self.state = states.STARTING
        self.log('Bus STARTING')
        try:
            self.publish('start')
            self.state = states.STARTED
            self.log('Bus STARTED')
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.log("Shutting down due to error in start listener:",
                     level=40, traceback=True)
            e_info = sys.exc_info()[1]
            try:
                self.exit()
            except:
                # Any stop/exit errors will be logged inside publish().
                pass
            # Re-raise the original error
            raise e_info
    
    def exit(self):
        """Stop all services and prepare to exit the process."""
        exitstate = self.state
        try:
            self.stop()
            
            self.state = states.EXITING
            self.log('Bus EXITING')
            self.publish('exit')
            # This isn't strictly necessary, but it's better than seeing
            # "Waiting for child threads to terminate..." and then nothing.
            self.log('Bus EXITED')
        except:
            # This method is often called asynchronously (whether thread,
            # signal handler, console handler, or atexit handler), so we
            # can't just let exceptions propagate out unhandled.
            # Assume it's been logged and just die.
            os._exit(70) # EX_SOFTWARE
        
        if exitstate == states.STARTING:
            # exit() was called before start() finished, possibly due to
            # Ctrl-C because a start listener got stuck. In this case,
            # we could get stuck in a loop where Ctrl-C never exits the
            # process, so we just call os.exit here.
            os._exit(70) # EX_SOFTWARE
    
    def restart(self):
        """Restart the process (may close connections).
        
        This method does not restart the process from the calling thread;
        instead, it stops the bus and asks the main thread to call execv.
        """
        self.execv = True
        self.exit()
    
    def graceful(self):
        """Advise all services to reload."""
        self.log('Bus graceful')
        self.publish('graceful')
    
    def block(self, interval=0.1):
        """Wait for the EXITING state, KeyboardInterrupt or SystemExit.
        
        This function is intended to be called only by the main thread.
        After waiting for the EXITING state, it also waits for all threads
        to terminate, and then calls os.execv if self.execv is True. This
        design allows another thread to call bus.restart, yet have the main
        thread perform the actual execv call (required on some platforms).
        """
        try:
            self.wait(states.EXITING, interval=interval, channel='main')
        except (KeyboardInterrupt, IOError):
            # The time.sleep call might raise
            # "IOError: [Errno 4] Interrupted function call" on KBInt.
            self.log('Keyboard Interrupt: shutting down bus')
            self.exit()
        except SystemExit:
            self.log('SystemExit raised: shutting down bus')
            self.exit()
            raise
        
        # Waiting for ALL child threads to finish is necessary on OS X.
        # See http://www.cherrypy.org/ticket/581.
        # It's also good to let them all shut down before allowing
        # the main thread to call atexit handlers.
        # See http://www.cherrypy.org/ticket/751.
        self.log("Waiting for child threads to terminate...")
        for t in threading.enumerate():
            if t != threading.currentThread() and t.isAlive():
                # Note that any dummy (external) threads are always daemonic.
                if hasattr(threading.Thread, "daemon"):
                    # Python 2.6+
                    d = t.daemon
                else:
                    d = t.isDaemon()
                if not d:
                    self.log("Waiting for thread %s." % t.getName())
                    t.join()
        
        if self.execv:
            self._do_execv()
    
    def wait(self, state, interval=0.1, channel=None):
        """Poll for the given state(s) at intervals; publish to channel."""
        if isinstance(state, (tuple, list)):
            states = state
        else:
            states = [state]
        
        def _wait():
            while self.state not in states:
                time.sleep(interval)
                self.publish(channel)
        
        # From http://psyco.sourceforge.net/psycoguide/bugs.html:
        # "The compiled machine code does not include the regular polling
        # done by Python, meaning that a KeyboardInterrupt will not be
        # detected before execution comes back to the regular Python
        # interpreter. Your program cannot be interrupted if caught
        # into an infinite Psyco-compiled loop."
        try:
            sys.modules['psyco'].cannotcompile(_wait)
        except (KeyError, AttributeError):
            pass
        
        _wait()
    
    def _do_execv(self):
        """Re-execute the current process.
        
        This must be called from the main thread, because certain platforms
        (OS X) don't allow execv to be called in a child thread very well.
        """
        args = sys.argv[:]
        self.log('Re-spawning %s' % ' '.join(args))
        
        if sys.platform[:4] == 'java':
            from _systemrestart import SystemRestart
            raise SystemRestart
        else:
            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]

            os.chdir(_startup_cwd)
            if self.max_cloexec_files:
                self._set_cloexec()
            os.execv(sys.executable, args)
    
    def _set_cloexec(self):
        """Set the CLOEXEC flag on all open files (except stdin/out/err).
        
        If self.max_cloexec_files is an integer (the default), then on
        platforms which support it, it represents the max open files setting
        for the operating system. This function will be called just before
        the process is restarted via os.execv() to prevent open files
        from persisting into the new process.
        
        Set self.max_cloexec_files to 0 to disable this behavior.
        """
        for fd in range(3, self.max_cloexec_files): # skip stdin/out/err
            try:
                flags = fcntl.fcntl(fd, fcntl.F_GETFD)
            except IOError:
                continue
            fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
    
    def stop(self):
        """Stop all services."""
        self.state = states.STOPPING
        self.log('Bus STOPPING')
        self.publish('stop')
        self.state = states.STOPPED
        self.log('Bus STOPPED')
    
    def start_with_callback(self, func, args=None, kwargs=None):
        """Start 'func' in a new thread T, then start self (and return T)."""
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        args = (func,) + args
        
        def _callback(func, *a, **kw):
            self.wait(states.STARTED)
            func(*a, **kw)
        t = threading.Thread(target=_callback, args=args, kwargs=kwargs)
        t.setName('Bus Callback ' + t.getName())
        t.start()
        
        self.start()
        
        return t
    
    def log(self, msg="", level=20, traceback=False):
        """Log the given message. Append the last traceback if requested."""
        if traceback:
            msg += "\n" + "".join(_traceback.format_exception(*sys.exc_info()))
        self.publish('log', msg, level)

bus = Bus()

########NEW FILE########
__FILENAME__ = ssl_builtin
"""A library for integrating Python's builtin ``ssl`` library with CherryPy.

The ssl module must be importable for SSL functionality.

To use this module, set ``CherryPyWSGIServer.ssl_adapter`` to an instance of
``BuiltinSSLAdapter``.
"""

try:
    import ssl
except ImportError:
    ssl = None

try:
    from _pyio import DEFAULT_BUFFER_SIZE
except ImportError:
    try:
        from io import DEFAULT_BUFFER_SIZE
    except ImportError:
        DEFAULT_BUFFER_SIZE = -1

import sys

from cherrypy import wsgiserver


class BuiltinSSLAdapter(wsgiserver.SSLAdapter):
    """A wrapper for integrating Python's builtin ssl module with CherryPy."""
    
    certificate = None
    """The filename of the server SSL certificate."""
    
    private_key = None
    """The filename of the server's private key file."""
    
    def __init__(self, certificate, private_key, certificate_chain=None):
        if ssl is None:
            raise ImportError("You must install the ssl module to use HTTPS.")
        self.certificate = certificate
        self.private_key = private_key
        self.certificate_chain = certificate_chain
    
    def bind(self, sock):
        """Wrap and return the given socket."""
        return sock
    
    def wrap(self, sock):
        """Wrap and return the given socket, plus WSGI environ entries."""
        try:
            s = ssl.wrap_socket(sock, do_handshake_on_connect=True,
                    server_side=True, certfile=self.certificate,
                    keyfile=self.private_key, ssl_version=ssl.PROTOCOL_SSLv23)
        except ssl.SSLError:
            e = sys.exc_info()[1]
            if e.errno == ssl.SSL_ERROR_EOF:
                # This is almost certainly due to the cherrypy engine
                # 'pinging' the socket to assert it's connectable;
                # the 'ping' isn't SSL.
                return None, {}
            elif e.errno == ssl.SSL_ERROR_SSL:
                if e.args[1].endswith('http request'):
                    # The client is speaking HTTP to an HTTPS server.
                    raise wsgiserver.NoSSLError
                elif e.args[1].endswith('unknown protocol'):
                    # The client is speaking some non-HTTP protocol.
                    # Drop the conn.
                    return None, {}
            raise
        return s, self.get_environ(s)
    
    # TODO: fill this out more with mod ssl env
    def get_environ(self, sock):
        """Create WSGI environ entries to be merged into each request."""
        cipher = sock.cipher()
        ssl_environ = {
            "wsgi.url_scheme": "https",
            "HTTPS": "on",
            'SSL_PROTOCOL': cipher[1],
            'SSL_CIPHER': cipher[0]
##            SSL_VERSION_INTERFACE 	string 	The mod_ssl program version
##            SSL_VERSION_LIBRARY 	string 	The OpenSSL program version
            }
        return ssl_environ
    
    if sys.version_info >= (3, 0):
        def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
            return wsgiserver.CP_makefile(sock, mode, bufsize)
    else:
        def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
            return wsgiserver.CP_fileobject(sock, mode, bufsize)


########NEW FILE########
__FILENAME__ = ssl_pyopenssl
"""A library for integrating pyOpenSSL with CherryPy.

The OpenSSL module must be importable for SSL functionality.
You can obtain it from http://pyopenssl.sourceforge.net/

To use this module, set CherryPyWSGIServer.ssl_adapter to an instance of
SSLAdapter. There are two ways to use SSL:

Method One
----------

 * ``ssl_adapter.context``: an instance of SSL.Context.

If this is not None, it is assumed to be an SSL.Context instance,
and will be passed to SSL.Connection on bind(). The developer is
responsible for forming a valid Context object. This approach is
to be preferred for more flexibility, e.g. if the cert and key are
streams instead of files, or need decryption, or SSL.SSLv3_METHOD
is desired instead of the default SSL.SSLv23_METHOD, etc. Consult
the pyOpenSSL documentation for complete options.

Method Two (shortcut)
---------------------

 * ``ssl_adapter.certificate``: the filename of the server SSL certificate.
 * ``ssl_adapter.private_key``: the filename of the server's private key file.

Both are None by default. If ssl_adapter.context is None, but .private_key
and .certificate are both given and valid, they will be read, and the
context will be automatically created from them.
"""

import socket
import threading
import time

from cherrypy import wsgiserver

try:
    from OpenSSL import SSL
    from OpenSSL import crypto
except ImportError:
    SSL = None


class SSL_fileobject(wsgiserver.CP_fileobject):
    """SSL file object attached to a socket object."""
    
    ssl_timeout = 3
    ssl_retry = .01
    
    def _safe_call(self, is_reader, call, *args, **kwargs):
        """Wrap the given call with SSL error-trapping.
        
        is_reader: if False EOF errors will be raised. If True, EOF errors
        will return "" (to emulate normal sockets).
        """
        start = time.time()
        while True:
            try:
                return call(*args, **kwargs)
            except SSL.WantReadError:
                # Sleep and try again. This is dangerous, because it means
                # the rest of the stack has no way of differentiating
                # between a "new handshake" error and "client dropped".
                # Note this isn't an endless loop: there's a timeout below.
                time.sleep(self.ssl_retry)
            except SSL.WantWriteError:
                time.sleep(self.ssl_retry)
            except SSL.SysCallError, e:
                if is_reader and e.args == (-1, 'Unexpected EOF'):
                    return ""
                
                errnum = e.args[0]
                if is_reader and errnum in wsgiserver.socket_errors_to_ignore:
                    return ""
                raise socket.error(errnum)
            except SSL.Error, e:
                if is_reader and e.args == (-1, 'Unexpected EOF'):
                    return ""
                
                thirdarg = None
                try:
                    thirdarg = e.args[0][0][2]
                except IndexError:
                    pass
                
                if thirdarg == 'http request':
                    # The client is talking HTTP to an HTTPS server.
                    raise wsgiserver.NoSSLError()
                
                raise wsgiserver.FatalSSLAlert(*e.args)
            except:
                raise
            
            if time.time() - start > self.ssl_timeout:
                raise socket.timeout("timed out")
    
    def recv(self, *args, **kwargs):
        buf = []
        r = super(SSL_fileobject, self).recv
        while True:
            data = self._safe_call(True, r, *args, **kwargs)
            buf.append(data)
            p = self._sock.pending()
            if not p:
                return "".join(buf)
    
    def sendall(self, *args, **kwargs):
        return self._safe_call(False, super(SSL_fileobject, self).sendall,
                               *args, **kwargs)

    def send(self, *args, **kwargs):
        return self._safe_call(False, super(SSL_fileobject, self).send,
                               *args, **kwargs)


class SSLConnection:
    """A thread-safe wrapper for an SSL.Connection.
    
    ``*args``: the arguments to create the wrapped ``SSL.Connection(*args)``.
    """
    
    def __init__(self, *args):
        self._ssl_conn = SSL.Connection(*args)
        self._lock = threading.RLock()
    
    for f in ('get_context', 'pending', 'send', 'write', 'recv', 'read',
              'renegotiate', 'bind', 'listen', 'connect', 'accept',
              'setblocking', 'fileno', 'close', 'get_cipher_list',
              'getpeername', 'getsockname', 'getsockopt', 'setsockopt',
              'makefile', 'get_app_data', 'set_app_data', 'state_string',
              'sock_shutdown', 'get_peer_certificate', 'want_read',
              'want_write', 'set_connect_state', 'set_accept_state',
              'connect_ex', 'sendall', 'settimeout', 'gettimeout'):
        exec("""def %s(self, *args):
        self._lock.acquire()
        try:
            return self._ssl_conn.%s(*args)
        finally:
            self._lock.release()
""" % (f, f))
    
    def shutdown(self, *args):
        self._lock.acquire()
        try:
            # pyOpenSSL.socket.shutdown takes no args
            return self._ssl_conn.shutdown()
        finally:
            self._lock.release()


class pyOpenSSLAdapter(wsgiserver.SSLAdapter):
    """A wrapper for integrating pyOpenSSL with CherryPy."""
    
    context = None
    """An instance of SSL.Context."""
    
    certificate = None
    """The filename of the server SSL certificate."""
    
    private_key = None
    """The filename of the server's private key file."""
    
    certificate_chain = None
    """Optional. The filename of CA's intermediate certificate bundle.
    
    This is needed for cheaper "chained root" SSL certificates, and should be
    left as None if not required."""
    
    def __init__(self, certificate, private_key, certificate_chain=None):
        if SSL is None:
            raise ImportError("You must install pyOpenSSL to use HTTPS.")
        
        self.context = None
        self.certificate = certificate
        self.private_key = private_key
        self.certificate_chain = certificate_chain
        self._environ = None
    
    def bind(self, sock):
        """Wrap and return the given socket."""
        if self.context is None:
            self.context = self.get_context()
        conn = SSLConnection(self.context, sock)
        self._environ = self.get_environ()
        return conn
    
    def wrap(self, sock):
        """Wrap and return the given socket, plus WSGI environ entries."""
        return sock, self._environ.copy()
    
    def get_context(self):
        """Return an SSL.Context from self attributes."""
        # See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/442473
        c = SSL.Context(SSL.SSLv23_METHOD)
        c.use_privatekey_file(self.private_key)
        if self.certificate_chain:
            c.load_verify_locations(self.certificate_chain)
        c.use_certificate_file(self.certificate)
        return c
    
    def get_environ(self):
        """Return WSGI environ entries to be merged into each request."""
        ssl_environ = {
            "HTTPS": "on",
            # pyOpenSSL doesn't provide access to any of these AFAICT
##            'SSL_PROTOCOL': 'SSLv2',
##            SSL_CIPHER 	string 	The cipher specification name
##            SSL_VERSION_INTERFACE 	string 	The mod_ssl program version
##            SSL_VERSION_LIBRARY 	string 	The OpenSSL program version
            }
        
        if self.certificate:
            # Server certificate attributes
            cert = open(self.certificate, 'rb').read()
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            ssl_environ.update({
                'SSL_SERVER_M_VERSION': cert.get_version(),
                'SSL_SERVER_M_SERIAL': cert.get_serial_number(),
##                'SSL_SERVER_V_START': Validity of server's certificate (start time),
##                'SSL_SERVER_V_END': Validity of server's certificate (end time),
                })
            
            for prefix, dn in [("I", cert.get_issuer()),
                               ("S", cert.get_subject())]:
                # X509Name objects don't seem to have a way to get the
                # complete DN string. Use str() and slice it instead,
                # because str(dn) == "<X509Name object '/C=US/ST=...'>"
                dnstr = str(dn)[18:-2]
                
                wsgikey = 'SSL_SERVER_%s_DN' % prefix
                ssl_environ[wsgikey] = dnstr
                
                # The DN should be of the form: /k1=v1/k2=v2, but we must allow
                # for any value to contain slashes itself (in a URL).
                while dnstr:
                    pos = dnstr.rfind("=")
                    dnstr, value = dnstr[:pos], dnstr[pos + 1:]
                    pos = dnstr.rfind("/")
                    dnstr, key = dnstr[:pos], dnstr[pos + 1:]
                    if key and value:
                        wsgikey = 'SSL_SERVER_%s_DN_%s' % (prefix, key)
                        ssl_environ[wsgikey] = value
        
        return ssl_environ
    
    def makefile(self, sock, mode='r', bufsize=-1):
        if SSL and isinstance(sock, SSL.ConnectionType):
            timeout = sock.gettimeout()
            f = SSL_fileobject(sock, mode, bufsize)
            f.ssl_timeout = timeout
            return f
        else:
            return wsgiserver.CP_fileobject(sock, mode, bufsize)


########NEW FILE########
__FILENAME__ = wsgiserver2
"""A high-speed, production ready, thread pooled, generic HTTP server.

Simplest example on how to use this module directly
(without using CherryPy's application machinery)::

    from cherrypy import wsgiserver
    
    def my_crazy_app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type','text/plain')]
        start_response(status, response_headers)
        return ['Hello world!']
    
    server = wsgiserver.CherryPyWSGIServer(
                ('0.0.0.0', 8070), my_crazy_app,
                server_name='www.cherrypy.example')
    server.start()
    
The CherryPy WSGI server can serve as many WSGI applications 
as you want in one instance by using a WSGIPathInfoDispatcher::
    
    d = WSGIPathInfoDispatcher({'/': my_crazy_app, '/blog': my_blog_app})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 80), d)
    
Want SSL support? Just set server.ssl_adapter to an SSLAdapter instance.

This won't call the CherryPy engine (application side) at all, only the
HTTP server, which is independent from the rest of CherryPy. Don't
let the name "CherryPyWSGIServer" throw you; the name merely reflects
its origin, not its coupling.

For those of you wanting to understand internals of this module, here's the
basic call flow. The server's listening thread runs a very tight loop,
sticking incoming connections onto a Queue::

    server = CherryPyWSGIServer(...)
    server.start()
    while True:
        tick()
        # This blocks until a request comes in:
        child = socket.accept()
        conn = HTTPConnection(child, ...)
        server.requests.put(conn)

Worker threads are kept in a pool and poll the Queue, popping off and then
handling each connection in turn. Each connection can consist of an arbitrary
number of requests and their responses, so we run a nested loop::

    while True:
        conn = server.requests.get()
        conn.communicate()
        ->  while True:
                req = HTTPRequest(...)
                req.parse_request()
                ->  # Read the Request-Line, e.g. "GET /page HTTP/1.1"
                    req.rfile.readline()
                    read_headers(req.rfile, req.inheaders)
                req.respond()
                ->  response = app(...)
                    try:
                        for chunk in response:
                            if chunk:
                                req.write(chunk)
                    finally:
                        if hasattr(response, "close"):
                            response.close()
                if req.close_connection:
                    return
"""

__all__ = ['HTTPRequest', 'HTTPConnection', 'HTTPServer',
           'SizeCheckWrapper', 'KnownLengthRFile', 'ChunkedRFile',
           'CP_fileobject',
           'MaxSizeExceeded', 'NoSSLError', 'FatalSSLAlert',
           'WorkerThread', 'ThreadPool', 'SSLAdapter',
           'CherryPyWSGIServer',
           'Gateway', 'WSGIGateway', 'WSGIGateway_10', 'WSGIGateway_u0',
           'WSGIPathInfoDispatcher', 'get_ssl_adapter_class']

import os
try:
    import queue
except:
    import Queue as queue
import re
import rfc822
import socket
import sys
if 'win' in sys.platform and not hasattr(socket, 'IPPROTO_IPV6'):
    socket.IPPROTO_IPV6 = 41
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
DEFAULT_BUFFER_SIZE = -1

_fileobject_uses_str_type = isinstance(socket._fileobject(None)._rbuf, basestring)

import threading
import time
import traceback
def format_exc(limit=None):
    """Like print_exc() but return a string. Backport for Python 2.3."""
    try:
        etype, value, tb = sys.exc_info()
        return ''.join(traceback.format_exception(etype, value, tb, limit))
    finally:
        etype = value = tb = None


from urllib import unquote
from urlparse import urlparse
import warnings

if sys.version_info >= (3, 0):
    bytestr = bytes
    unicodestr = str
    basestring = (bytes, str)
    def ntob(n, encoding='ISO-8859-1'):
        """Return the given native string as a byte string in the given encoding."""
        # In Python 3, the native string type is unicode
        return n.encode(encoding)
else:
    bytestr = str
    unicodestr = unicode
    basestring = basestring
    def ntob(n, encoding='ISO-8859-1'):
        """Return the given native string as a byte string in the given encoding."""
        # In Python 2, the native string type is bytes. Assume it's already
        # in the given encoding, which for ISO-8859-1 is almost always what
        # was intended.
        return n

LF = ntob('\n')
CRLF = ntob('\r\n')
TAB = ntob('\t')
SPACE = ntob(' ')
COLON = ntob(':')
SEMICOLON = ntob(';')
EMPTY = ntob('')
NUMBER_SIGN = ntob('#')
QUESTION_MARK = ntob('?')
ASTERISK = ntob('*')
FORWARD_SLASH = ntob('/')
quoted_slash = re.compile(ntob("(?i)%2F"))

import errno

def plat_specific_errors(*errnames):
    """Return error numbers for all errors in errnames on this platform.
    
    The 'errno' module contains different global constants depending on
    the specific platform (OS). This function will return the list of
    numeric values for a given list of potential names.
    """
    errno_names = dir(errno)
    nums = [getattr(errno, k) for k in errnames if k in errno_names]
    # de-dupe the list
    return list(dict.fromkeys(nums).keys())

socket_error_eintr = plat_specific_errors("EINTR", "WSAEINTR")

socket_errors_to_ignore = plat_specific_errors(
    "EPIPE",
    "EBADF", "WSAEBADF",
    "ENOTSOCK", "WSAENOTSOCK",
    "ETIMEDOUT", "WSAETIMEDOUT",
    "ECONNREFUSED", "WSAECONNREFUSED",
    "ECONNRESET", "WSAECONNRESET",
    "ECONNABORTED", "WSAECONNABORTED",
    "ENETRESET", "WSAENETRESET",
    "EHOSTDOWN", "EHOSTUNREACH",
    )
socket_errors_to_ignore.append("timed out")
socket_errors_to_ignore.append("The read operation timed out")

socket_errors_nonblocking = plat_specific_errors(
    'EAGAIN', 'EWOULDBLOCK', 'WSAEWOULDBLOCK')

comma_separated_headers = [ntob(h) for h in
    ['Accept', 'Accept-Charset', 'Accept-Encoding',
     'Accept-Language', 'Accept-Ranges', 'Allow', 'Cache-Control',
     'Connection', 'Content-Encoding', 'Content-Language', 'Expect',
     'If-Match', 'If-None-Match', 'Pragma', 'Proxy-Authenticate', 'TE',
     'Trailer', 'Transfer-Encoding', 'Upgrade', 'Vary', 'Via', 'Warning',
     'WWW-Authenticate']]


import logging
if not hasattr(logging, 'statistics'): logging.statistics = {}


def read_headers(rfile, hdict=None):
    """Read headers from the given stream into the given header dict.
    
    If hdict is None, a new header dict is created. Returns the populated
    header dict.
    
    Headers which are repeated are folded together using a comma if their
    specification so dictates.
    
    This function raises ValueError when the read bytes violate the HTTP spec.
    You should probably return "400 Bad Request" if this happens.
    """
    if hdict is None:
        hdict = {}
    
    while True:
        line = rfile.readline()
        if not line:
            # No more data--illegal end of headers
            raise ValueError("Illegal end of headers.")
        
        if line == CRLF:
            # Normal end of headers
            break
        if not line.endswith(CRLF):
            raise ValueError("HTTP requires CRLF terminators")
        
        if line[0] in (SPACE, TAB):
            # It's a continuation line.
            v = line.strip()
        else:
            try:
                k, v = line.split(COLON, 1)
            except ValueError:
                raise ValueError("Illegal header line.")
            # TODO: what about TE and WWW-Authenticate?
            k = k.strip().title()
            v = v.strip()
            hname = k
        
        if k in comma_separated_headers:
            existing = hdict.get(hname)
            if existing:
                v = ", ".join((existing, v))
        hdict[hname] = v
    
    return hdict


class MaxSizeExceeded(Exception):
    pass

class SizeCheckWrapper(object):
    """Wraps a file-like object, raising MaxSizeExceeded if too large."""
    
    def __init__(self, rfile, maxlen):
        self.rfile = rfile
        self.maxlen = maxlen
        self.bytes_read = 0
    
    def _check_length(self):
        if self.maxlen and self.bytes_read > self.maxlen:
            raise MaxSizeExceeded()
    
    def read(self, size=None):
        data = self.rfile.read(size)
        self.bytes_read += len(data)
        self._check_length()
        return data
    
    def readline(self, size=None):
        if size is not None:
            data = self.rfile.readline(size)
            self.bytes_read += len(data)
            self._check_length()
            return data
        
        # User didn't specify a size ...
        # We read the line in chunks to make sure it's not a 100MB line !
        res = []
        while True:
            data = self.rfile.readline(256)
            self.bytes_read += len(data)
            self._check_length()
            res.append(data)
            # See http://www.cherrypy.org/ticket/421
            if len(data) < 256 or data[-1:] == "\n":
                return EMPTY.join(res)
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline()
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline()
        return lines
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        data = next(self.rfile)
        self.bytes_read += len(data)
        self._check_length()
        return data
    
    def next(self):
        data = self.rfile.next()
        self.bytes_read += len(data)
        self._check_length()
        return data


class KnownLengthRFile(object):
    """Wraps a file-like object, returning an empty string when exhausted."""
    
    def __init__(self, rfile, content_length):
        self.rfile = rfile
        self.remaining = content_length
    
    def read(self, size=None):
        if self.remaining == 0:
            return ''
        if size is None:
            size = self.remaining
        else:
            size = min(size, self.remaining)
        
        data = self.rfile.read(size)
        self.remaining -= len(data)
        return data
    
    def readline(self, size=None):
        if self.remaining == 0:
            return ''
        if size is None:
            size = self.remaining
        else:
            size = min(size, self.remaining)
        
        data = self.rfile.readline(size)
        self.remaining -= len(data)
        return data
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline(sizehint)
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline(sizehint)
        return lines
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        data = next(self.rfile)
        self.remaining -= len(data)
        return data


class ChunkedRFile(object):
    """Wraps a file-like object, returning an empty string when exhausted.
    
    This class is intended to provide a conforming wsgi.input value for
    request entities that have been encoded with the 'chunked' transfer
    encoding.
    """
    
    def __init__(self, rfile, maxlen, bufsize=8192):
        self.rfile = rfile
        self.maxlen = maxlen
        self.bytes_read = 0
        self.buffer = EMPTY
        self.bufsize = bufsize
        self.closed = False
    
    def _fetch(self):
        if self.closed:
            return
        
        line = self.rfile.readline()
        self.bytes_read += len(line)
        
        if self.maxlen and self.bytes_read > self.maxlen:
            raise MaxSizeExceeded("Request Entity Too Large", self.maxlen)
        
        line = line.strip().split(SEMICOLON, 1)
        
        try:
            chunk_size = line.pop(0)
            chunk_size = int(chunk_size, 16)
        except ValueError:
            raise ValueError("Bad chunked transfer size: " + repr(chunk_size))
        
        if chunk_size <= 0:
            self.closed = True
            return
        
##            if line: chunk_extension = line[0]
        
        if self.maxlen and self.bytes_read + chunk_size > self.maxlen:
            raise IOError("Request Entity Too Large")
        
        chunk = self.rfile.read(chunk_size)
        self.bytes_read += len(chunk)
        self.buffer += chunk
        
        crlf = self.rfile.read(2)
        if crlf != CRLF:
            raise ValueError(
                 "Bad chunked transfer coding (expected '\\r\\n', "
                 "got " + repr(crlf) + ")")
    
    def read(self, size=None):
        data = EMPTY
        while True:
            if size and len(data) >= size:
                return data
            
            if not self.buffer:
                self._fetch()
                if not self.buffer:
                    # EOF
                    return data
            
            if size:
                remaining = size - len(data)
                data += self.buffer[:remaining]
                self.buffer = self.buffer[remaining:]
            else:
                data += self.buffer
    
    def readline(self, size=None):
        data = EMPTY
        while True:
            if size and len(data) >= size:
                return data
            
            if not self.buffer:
                self._fetch()
                if not self.buffer:
                    # EOF
                    return data
            
            newline_pos = self.buffer.find(LF)
            if size:
                if newline_pos == -1:
                    remaining = size - len(data)
                    data += self.buffer[:remaining]
                    self.buffer = self.buffer[remaining:]
                else:
                    remaining = min(size - len(data), newline_pos)
                    data += self.buffer[:remaining]
                    self.buffer = self.buffer[remaining:]
            else:
                if newline_pos == -1:
                    data += self.buffer
                else:
                    data += self.buffer[:newline_pos]
                    self.buffer = self.buffer[newline_pos:]
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline(sizehint)
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline(sizehint)
        return lines
    
    def read_trailer_lines(self):
        if not self.closed:
            raise ValueError(
                "Cannot read trailers until the request body has been read.")
        
        while True:
            line = self.rfile.readline()
            if not line:
                # No more data--illegal end of headers
                raise ValueError("Illegal end of headers.")
            
            self.bytes_read += len(line)
            if self.maxlen and self.bytes_read > self.maxlen:
                raise IOError("Request Entity Too Large")
            
            if line == CRLF:
                # Normal end of headers
                break
            if not line.endswith(CRLF):
                raise ValueError("HTTP requires CRLF terminators")
            
            yield line
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        # Shamelessly stolen from StringIO
        total = 0
        line = self.readline(sizehint)
        while line:
            yield line
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline(sizehint)


class HTTPRequest(object):
    """An HTTP Request (and response).
    
    A single HTTP connection may consist of multiple request/response pairs.
    """
    
    server = None
    """The HTTPServer object which is receiving this request."""
    
    conn = None
    """The HTTPConnection object on which this request connected."""
    
    inheaders = {}
    """A dict of request headers."""
    
    outheaders = []
    """A list of header tuples to write in the response."""
    
    ready = False
    """When True, the request has been parsed and is ready to begin generating
    the response. When False, signals the calling Connection that the response
    should not be generated and the connection should close."""
    
    close_connection = False
    """Signals the calling Connection that the request should close. This does
    not imply an error! The client and/or server may each request that the
    connection be closed."""
    
    chunked_write = False
    """If True, output will be encoded with the "chunked" transfer-coding.
    
    This value is set automatically inside send_headers."""
    
    def __init__(self, server, conn):
        self.server= server
        self.conn = conn
        
        self.ready = False
        self.started_request = False
        self.scheme = ntob("http")
        if self.server.ssl_adapter is not None:
            self.scheme = ntob("https")
        # Use the lowest-common protocol in case read_request_line errors.
        self.response_protocol = 'HTTP/1.0'
        self.inheaders = {}
        
        self.status = ""
        self.outheaders = []
        self.sent_headers = False
        self.close_connection = self.__class__.close_connection
        self.chunked_read = False
        self.chunked_write = self.__class__.chunked_write
    
    def parse_request(self):
        """Parse the next HTTP request start-line and message-headers."""
        self.rfile = SizeCheckWrapper(self.conn.rfile,
                                      self.server.max_request_header_size)
        try:
            success = self.read_request_line()
        except MaxSizeExceeded:
            self.simple_response("414 Request-URI Too Long",
                "The Request-URI sent with the request exceeds the maximum "
                "allowed bytes.")
            return
        else:
            if not success:
                return
        
        try:
            success = self.read_request_headers()
        except MaxSizeExceeded:
            self.simple_response("413 Request Entity Too Large",
                "The headers sent with the request exceed the maximum "
                "allowed bytes.")
            return
        else:
            if not success:
                return
        
        self.ready = True
    
    def read_request_line(self):
        # HTTP/1.1 connections are persistent by default. If a client
        # requests a page, then idles (leaves the connection open),
        # then rfile.readline() will raise socket.error("timed out").
        # Note that it does this based on the value given to settimeout(),
        # and doesn't need the client to request or acknowledge the close
        # (although your TCP stack might suffer for it: cf Apache's history
        # with FIN_WAIT_2).
        request_line = self.rfile.readline()
        
        # Set started_request to True so communicate() knows to send 408
        # from here on out.
        self.started_request = True
        if not request_line:
            return False
        
        if request_line == CRLF:
            # RFC 2616 sec 4.1: "...if the server is reading the protocol
            # stream at the beginning of a message and receives a CRLF
            # first, it should ignore the CRLF."
            # But only ignore one leading line! else we enable a DoS.
            request_line = self.rfile.readline()
            if not request_line:
                return False
        
        if not request_line.endswith(CRLF):
            self.simple_response("400 Bad Request", "HTTP requires CRLF terminators")
            return False
        
        try:
            method, uri, req_protocol = request_line.strip().split(SPACE, 2)
            rp = int(req_protocol[5]), int(req_protocol[7])
        except (ValueError, IndexError):
            self.simple_response("400 Bad Request", "Malformed Request-Line")
            return False
        
        self.uri = uri
        self.method = method
        
        # uri may be an abs_path (including "http://host.domain.tld");
        scheme, authority, path = self.parse_request_uri(uri)
        if NUMBER_SIGN in path:
            self.simple_response("400 Bad Request",
                                 "Illegal #fragment in Request-URI.")
            return False
        
        if scheme:
            self.scheme = scheme
        
        qs = EMPTY
        if QUESTION_MARK in path:
            path, qs = path.split(QUESTION_MARK, 1)
        
        # Unquote the path+params (e.g. "/this%20path" -> "/this path").
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.1.2
        #
        # But note that "...a URI must be separated into its components
        # before the escaped characters within those components can be
        # safely decoded." http://www.ietf.org/rfc/rfc2396.txt, sec 2.4.2
        # Therefore, "/this%2Fpath" becomes "/this%2Fpath", not "/this/path".
        try:
            atoms = [unquote(x) for x in quoted_slash.split(path)]
        except ValueError:
            ex = sys.exc_info()[1]
            self.simple_response("400 Bad Request", ex.args[0])
            return False
        path = "%2F".join(atoms)
        self.path = path
        
        # Note that, like wsgiref and most other HTTP servers,
        # we "% HEX HEX"-unquote the path but not the query string.
        self.qs = qs
        
        # Compare request and server HTTP protocol versions, in case our
        # server does not support the requested protocol. Limit our output
        # to min(req, server). We want the following output:
        #     request    server     actual written   supported response
        #     protocol   protocol  response protocol    feature set
        # a     1.0        1.0           1.0                1.0
        # b     1.0        1.1           1.1                1.0
        # c     1.1        1.0           1.0                1.0
        # d     1.1        1.1           1.1                1.1
        # Notice that, in (b), the response will be "HTTP/1.1" even though
        # the client only understands 1.0. RFC 2616 10.5.6 says we should
        # only return 505 if the _major_ version is different.
        sp = int(self.server.protocol[5]), int(self.server.protocol[7])
        
        if sp[0] != rp[0]:
            self.simple_response("505 HTTP Version Not Supported")
            return False

        self.request_protocol = req_protocol
        self.response_protocol = "HTTP/%s.%s" % min(rp, sp)

        return True

    def read_request_headers(self):
        """Read self.rfile into self.inheaders. Return success."""
        
        # then all the http headers
        try:
            read_headers(self.rfile, self.inheaders)
        except ValueError:
            ex = sys.exc_info()[1]
            self.simple_response("400 Bad Request", ex.args[0])
            return False
        
        mrbs = self.server.max_request_body_size
        if mrbs and int(self.inheaders.get("Content-Length", 0)) > mrbs:
            self.simple_response("413 Request Entity Too Large",
                "The entity sent with the request exceeds the maximum "
                "allowed bytes.")
            return False
        
        # Persistent connection support
        if self.response_protocol == "HTTP/1.1":
            # Both server and client are HTTP/1.1
            if self.inheaders.get("Connection", "") == "close":
                self.close_connection = True
        else:
            # Either the server or client (or both) are HTTP/1.0
            if self.inheaders.get("Connection", "") != "Keep-Alive":
                self.close_connection = True
        
        # Transfer-Encoding support
        te = None
        if self.response_protocol == "HTTP/1.1":
            te = self.inheaders.get("Transfer-Encoding")
            if te:
                te = [x.strip().lower() for x in te.split(",") if x.strip()]
        
        self.chunked_read = False
        
        if te:
            for enc in te:
                if enc == "chunked":
                    self.chunked_read = True
                else:
                    # Note that, even if we see "chunked", we must reject
                    # if there is an extension we don't recognize.
                    self.simple_response("501 Unimplemented")
                    self.close_connection = True
                    return False
        
        # From PEP 333:
        # "Servers and gateways that implement HTTP 1.1 must provide
        # transparent support for HTTP 1.1's "expect/continue" mechanism.
        # This may be done in any of several ways:
        #   1. Respond to requests containing an Expect: 100-continue request
        #      with an immediate "100 Continue" response, and proceed normally.
        #   2. Proceed with the request normally, but provide the application
        #      with a wsgi.input stream that will send the "100 Continue"
        #      response if/when the application first attempts to read from
        #      the input stream. The read request must then remain blocked
        #      until the client responds.
        #   3. Wait until the client decides that the server does not support
        #      expect/continue, and sends the request body on its own.
        #      (This is suboptimal, and is not recommended.)
        #
        # We used to do 3, but are now doing 1. Maybe we'll do 2 someday,
        # but it seems like it would be a big slowdown for such a rare case.
        if self.inheaders.get("Expect", "") == "100-continue":
            # Don't use simple_response here, because it emits headers
            # we don't want. See http://www.cherrypy.org/ticket/951
            msg = self.server.protocol + " 100 Continue\r\n\r\n"
            try:
                self.conn.wfile.sendall(msg)
            except socket.error:
                x = sys.exc_info()[1]
                if x.args[0] not in socket_errors_to_ignore:
                    raise
        return True
    
    def parse_request_uri(self, uri):
        """Parse a Request-URI into (scheme, authority, path).
        
        Note that Request-URI's must be one of::
            
            Request-URI    = "*" | absoluteURI | abs_path | authority
        
        Therefore, a Request-URI which starts with a double forward-slash
        cannot be a "net_path"::
        
            net_path      = "//" authority [ abs_path ]
        
        Instead, it must be interpreted as an "abs_path" with an empty first
        path segment::
        
            abs_path      = "/"  path_segments
            path_segments = segment *( "/" segment )
            segment       = *pchar *( ";" param )
            param         = *pchar
        """
        if uri == ASTERISK:
            return None, None, uri
        
        i = uri.find('://')
        if i > 0 and QUESTION_MARK not in uri[:i]:
            # An absoluteURI.
            # If there's a scheme (and it must be http or https), then:
            # http_URL = "http:" "//" host [ ":" port ] [ abs_path [ "?" query ]]
            scheme, remainder = uri[:i].lower(), uri[i + 3:]
            authority, path = remainder.split(FORWARD_SLASH, 1)
            path = FORWARD_SLASH + path
            return scheme, authority, path
        
        if uri.startswith(FORWARD_SLASH):
            # An abs_path.
            return None, None, uri
        else:
            # An authority.
            return None, uri, None
    
    def respond(self):
        """Call the gateway and write its iterable output."""
        mrbs = self.server.max_request_body_size
        if self.chunked_read:
            self.rfile = ChunkedRFile(self.conn.rfile, mrbs)
        else:
            cl = int(self.inheaders.get("Content-Length", 0))
            if mrbs and mrbs < cl:
                if not self.sent_headers:
                    self.simple_response("413 Request Entity Too Large",
                        "The entity sent with the request exceeds the maximum "
                        "allowed bytes.")
                return
            self.rfile = KnownLengthRFile(self.conn.rfile, cl)
        
        self.server.gateway(self).respond()
        
        if (self.ready and not self.sent_headers):
            self.sent_headers = True
            self.send_headers()
        if self.chunked_write:
            self.conn.wfile.sendall("0\r\n\r\n")
    
    def simple_response(self, status, msg=""):
        """Write a simple response back to the client."""
        status = str(status)
        buf = [self.server.protocol + SPACE +
               status + CRLF,
               "Content-Length: %s\r\n" % len(msg),
               "Content-Type: text/plain\r\n"]
        
        if status[:3] in ("413", "414"):
            # Request Entity Too Large / Request-URI Too Long
            self.close_connection = True
            if self.response_protocol == 'HTTP/1.1':
                # This will not be true for 414, since read_request_line
                # usually raises 414 before reading the whole line, and we
                # therefore cannot know the proper response_protocol.
                buf.append("Connection: close\r\n")
            else:
                # HTTP/1.0 had no 413/414 status nor Connection header.
                # Emit 400 instead and trust the message body is enough.
                status = "400 Bad Request"
        
        buf.append(CRLF)
        if msg:
            if isinstance(msg, unicodestr):
                msg = msg.encode("ISO-8859-1")
            buf.append(msg)
        
        try:
            self.conn.wfile.sendall("".join(buf))
        except socket.error:
            x = sys.exc_info()[1]
            if x.args[0] not in socket_errors_to_ignore:
                raise
    
    def write(self, chunk):
        """Write unbuffered data to the client."""
        if self.chunked_write and chunk:
            buf = [hex(len(chunk))[2:], CRLF, chunk, CRLF]
            self.conn.wfile.sendall(EMPTY.join(buf))
        else:
            self.conn.wfile.sendall(chunk)
    
    def send_headers(self):
        """Assert, process, and send the HTTP response message-headers.
        
        You must set self.status, and self.outheaders before calling this.
        """
        hkeys = [key.lower() for key, value in self.outheaders]
        status = int(self.status[:3])
        
        if status == 413:
            # Request Entity Too Large. Close conn to avoid garbage.
            self.close_connection = True
        elif "content-length" not in hkeys:
            # "All 1xx (informational), 204 (no content),
            # and 304 (not modified) responses MUST NOT
            # include a message-body." So no point chunking.
            if status < 200 or status in (204, 205, 304):
                pass
            else:
                if (self.response_protocol == 'HTTP/1.1'
                    and self.method != 'HEAD'):
                    # Use the chunked transfer-coding
                    self.chunked_write = True
                    self.outheaders.append(("Transfer-Encoding", "chunked"))
                else:
                    # Closing the conn is the only way to determine len.
                    self.close_connection = True
        
        if "connection" not in hkeys:
            if self.response_protocol == 'HTTP/1.1':
                # Both server and client are HTTP/1.1 or better
                if self.close_connection:
                    self.outheaders.append(("Connection", "close"))
            else:
                # Server and/or client are HTTP/1.0
                if not self.close_connection:
                    self.outheaders.append(("Connection", "Keep-Alive"))
        
        if (not self.close_connection) and (not self.chunked_read):
            # Read any remaining request body data on the socket.
            # "If an origin server receives a request that does not include an
            # Expect request-header field with the "100-continue" expectation,
            # the request includes a request body, and the server responds
            # with a final status code before reading the entire request body
            # from the transport connection, then the server SHOULD NOT close
            # the transport connection until it has read the entire request,
            # or until the client closes the connection. Otherwise, the client
            # might not reliably receive the response message. However, this
            # requirement is not be construed as preventing a server from
            # defending itself against denial-of-service attacks, or from
            # badly broken client implementations."
            remaining = getattr(self.rfile, 'remaining', 0)
            if remaining > 0:
                self.rfile.read(remaining)
        
        if "date" not in hkeys:
            self.outheaders.append(("Date", rfc822.formatdate()))
        
        if "server" not in hkeys:
            self.outheaders.append(("Server", self.server.server_name))
        
        buf = [self.server.protocol + SPACE + self.status + CRLF]
        for k, v in self.outheaders:
            buf.append(k + COLON + SPACE + v + CRLF)
        buf.append(CRLF)
        self.conn.wfile.sendall(EMPTY.join(buf))


class NoSSLError(Exception):
    """Exception raised when a client speaks HTTP to an HTTPS socket."""
    pass


class FatalSSLAlert(Exception):
    """Exception raised when the SSL implementation signals a fatal alert."""
    pass


class CP_fileobject(socket._fileobject):
    """Faux file object attached to a socket object."""

    def __init__(self, *args, **kwargs):
        self.bytes_read = 0
        self.bytes_written = 0
        socket._fileobject.__init__(self, *args, **kwargs)
    
    def sendall(self, data):
        """Sendall for non-blocking sockets."""
        while data:
            try:
                bytes_sent = self.send(data)
                data = data[bytes_sent:]
            except socket.error, e:
                if e.args[0] not in socket_errors_nonblocking:
                    raise

    def send(self, data):
        bytes_sent = self._sock.send(data)
        self.bytes_written += bytes_sent
        return bytes_sent

    def flush(self):
        if self._wbuf:
            buffer = "".join(self._wbuf)
            self._wbuf = []
            self.sendall(buffer)

    def recv(self, size):
        while True:
            try:
                data = self._sock.recv(size)
                self.bytes_read += len(data)
                return data
            except socket.error, e:
                if (e.args[0] not in socket_errors_nonblocking
                    and e.args[0] not in socket_error_eintr):
                    raise

    if not _fileobject_uses_str_type:
        def read(self, size=-1):
            # Use max, disallow tiny reads in a loop as they are very inefficient.
            # We never leave read() with any leftover data from a new recv() call
            # in our internal buffer.
            rbufsize = max(self._rbufsize, self.default_bufsize)
            # Our use of StringIO rather than lists of string objects returned by
            # recv() minimizes memory usage and fragmentation that occurs when
            # rbufsize is large compared to the typical return value of recv().
            buf = self._rbuf
            buf.seek(0, 2)  # seek end
            if size < 0:
                # Read until EOF
                self._rbuf = StringIO.StringIO()  # reset _rbuf.  we consume it via buf.
                while True:
                    data = self.recv(rbufsize)
                    if not data:
                        break
                    buf.write(data)
                return buf.getvalue()
            else:
                # Read until size bytes or EOF seen, whichever comes first
                buf_len = buf.tell()
                if buf_len >= size:
                    # Already have size bytes in our buffer?  Extract and return.
                    buf.seek(0)
                    rv = buf.read(size)
                    self._rbuf = StringIO.StringIO()
                    self._rbuf.write(buf.read())
                    return rv

                self._rbuf = StringIO.StringIO()  # reset _rbuf.  we consume it via buf.
                while True:
                    left = size - buf_len
                    # recv() will malloc the amount of memory given as its
                    # parameter even though it often returns much less data
                    # than that.  The returned data string is short lived
                    # as we copy it into a StringIO and free it.  This avoids
                    # fragmentation issues on many platforms.
                    data = self.recv(left)
                    if not data:
                        break
                    n = len(data)
                    if n == size and not buf_len:
                        # Shortcut.  Avoid buffer data copies when:
                        # - We have no data in our buffer.
                        # AND
                        # - Our call to recv returned exactly the
                        #   number of bytes we were asked to read.
                        return data
                    if n == left:
                        buf.write(data)
                        del data  # explicit free
                        break
                    assert n <= left, "recv(%d) returned %d bytes" % (left, n)
                    buf.write(data)
                    buf_len += n
                    del data  # explicit free
                    #assert buf_len == buf.tell()
                return buf.getvalue()

        def readline(self, size=-1):
            buf = self._rbuf
            buf.seek(0, 2)  # seek end
            if buf.tell() > 0:
                # check if we already have it in our buffer
                buf.seek(0)
                bline = buf.readline(size)
                if bline.endswith('\n') or len(bline) == size:
                    self._rbuf = StringIO.StringIO()
                    self._rbuf.write(buf.read())
                    return bline
                del bline
            if size < 0:
                # Read until \n or EOF, whichever comes first
                if self._rbufsize <= 1:
                    # Speed up unbuffered case
                    buf.seek(0)
                    buffers = [buf.read()]
                    self._rbuf = StringIO.StringIO()  # reset _rbuf.  we consume it via buf.
                    data = None
                    recv = self.recv
                    while data != "\n":
                        data = recv(1)
                        if not data:
                            break
                        buffers.append(data)
                    return "".join(buffers)

                buf.seek(0, 2)  # seek end
                self._rbuf = StringIO.StringIO()  # reset _rbuf.  we consume it via buf.
                while True:
                    data = self.recv(self._rbufsize)
                    if not data:
                        break
                    nl = data.find('\n')
                    if nl >= 0:
                        nl += 1
                        buf.write(data[:nl])
                        self._rbuf.write(data[nl:])
                        del data
                        break
                    buf.write(data)
                return buf.getvalue()
            else:
                # Read until size bytes or \n or EOF seen, whichever comes first
                buf.seek(0, 2)  # seek end
                buf_len = buf.tell()
                if buf_len >= size:
                    buf.seek(0)
                    rv = buf.read(size)
                    self._rbuf = StringIO.StringIO()
                    self._rbuf.write(buf.read())
                    return rv
                self._rbuf = StringIO.StringIO()  # reset _rbuf.  we consume it via buf.
                while True:
                    data = self.recv(self._rbufsize)
                    if not data:
                        break
                    left = size - buf_len
                    # did we just receive a newline?
                    nl = data.find('\n', 0, left)
                    if nl >= 0:
                        nl += 1
                        # save the excess data to _rbuf
                        self._rbuf.write(data[nl:])
                        if buf_len:
                            buf.write(data[:nl])
                            break
                        else:
                            # Shortcut.  Avoid data copy through buf when returning
                            # a substring of our first recv().
                            return data[:nl]
                    n = len(data)
                    if n == size and not buf_len:
                        # Shortcut.  Avoid data copy through buf when
                        # returning exactly all of our first recv().
                        return data
                    if n >= left:
                        buf.write(data[:left])
                        self._rbuf.write(data[left:])
                        break
                    buf.write(data)
                    buf_len += n
                    #assert buf_len == buf.tell()
                return buf.getvalue()
    else:
        def read(self, size=-1):
            if size < 0:
                # Read until EOF
                buffers = [self._rbuf]
                self._rbuf = ""
                if self._rbufsize <= 1:
                    recv_size = self.default_bufsize
                else:
                    recv_size = self._rbufsize

                while True:
                    data = self.recv(recv_size)
                    if not data:
                        break
                    buffers.append(data)
                return "".join(buffers)
            else:
                # Read until size bytes or EOF seen, whichever comes first
                data = self._rbuf
                buf_len = len(data)
                if buf_len >= size:
                    self._rbuf = data[size:]
                    return data[:size]
                buffers = []
                if data:
                    buffers.append(data)
                self._rbuf = ""
                while True:
                    left = size - buf_len
                    recv_size = max(self._rbufsize, left)
                    data = self.recv(recv_size)
                    if not data:
                        break
                    buffers.append(data)
                    n = len(data)
                    if n >= left:
                        self._rbuf = data[left:]
                        buffers[-1] = data[:left]
                        break
                    buf_len += n
                return "".join(buffers)

        def readline(self, size=-1):
            data = self._rbuf
            if size < 0:
                # Read until \n or EOF, whichever comes first
                if self._rbufsize <= 1:
                    # Speed up unbuffered case
                    assert data == ""
                    buffers = []
                    while data != "\n":
                        data = self.recv(1)
                        if not data:
                            break
                        buffers.append(data)
                    return "".join(buffers)
                nl = data.find('\n')
                if nl >= 0:
                    nl += 1
                    self._rbuf = data[nl:]
                    return data[:nl]
                buffers = []
                if data:
                    buffers.append(data)
                self._rbuf = ""
                while True:
                    data = self.recv(self._rbufsize)
                    if not data:
                        break
                    buffers.append(data)
                    nl = data.find('\n')
                    if nl >= 0:
                        nl += 1
                        self._rbuf = data[nl:]
                        buffers[-1] = data[:nl]
                        break
                return "".join(buffers)
            else:
                # Read until size bytes or \n or EOF seen, whichever comes first
                nl = data.find('\n', 0, size)
                if nl >= 0:
                    nl += 1
                    self._rbuf = data[nl:]
                    return data[:nl]
                buf_len = len(data)
                if buf_len >= size:
                    self._rbuf = data[size:]
                    return data[:size]
                buffers = []
                if data:
                    buffers.append(data)
                self._rbuf = ""
                while True:
                    data = self.recv(self._rbufsize)
                    if not data:
                        break
                    buffers.append(data)
                    left = size - buf_len
                    nl = data.find('\n', 0, left)
                    if nl >= 0:
                        nl += 1
                        self._rbuf = data[nl:]
                        buffers[-1] = data[:nl]
                        break
                    n = len(data)
                    if n >= left:
                        self._rbuf = data[left:]
                        buffers[-1] = data[:left]
                        break
                    buf_len += n
                return "".join(buffers)


class HTTPConnection(object):
    """An HTTP connection (active socket).
    
    server: the Server object which received this connection.
    socket: the raw socket object (usually TCP) for this connection.
    makefile: a fileobject class for reading from the socket.
    """
    
    remote_addr = None
    remote_port = None
    ssl_env = None
    rbufsize = DEFAULT_BUFFER_SIZE
    wbufsize = DEFAULT_BUFFER_SIZE
    RequestHandlerClass = HTTPRequest
    
    def __init__(self, server, sock, makefile=CP_fileobject):
        self.server = server
        self.socket = sock
        self.rfile = makefile(sock, "rb", self.rbufsize)
        self.wfile = makefile(sock, "wb", self.wbufsize)
        self.requests_seen = 0
    
    def communicate(self):
        """Read each request and respond appropriately."""
        request_seen = False
        try:
            while True:
                # (re)set req to None so that if something goes wrong in
                # the RequestHandlerClass constructor, the error doesn't
                # get written to the previous request.
                req = None
                req = self.RequestHandlerClass(self.server, self)
                
                # This order of operations should guarantee correct pipelining.
                req.parse_request()
                if self.server.stats['Enabled']:
                    self.requests_seen += 1
                if not req.ready:
                    # Something went wrong in the parsing (and the server has
                    # probably already made a simple_response). Return and
                    # let the conn close.
                    return
                
                request_seen = True
                req.respond()
                if req.close_connection:
                    return
        except socket.error:
            e = sys.exc_info()[1]
            errnum = e.args[0]
            # sadly SSL sockets return a different (longer) time out string
            if errnum == 'timed out' or errnum == 'The read operation timed out':
                # Don't error if we're between requests; only error
                # if 1) no request has been started at all, or 2) we're
                # in the middle of a request.
                # See http://www.cherrypy.org/ticket/853
                if (not request_seen) or (req and req.started_request):
                    # Don't bother writing the 408 if the response
                    # has already started being written.
                    if req and not req.sent_headers:
                        try:
                            req.simple_response("408 Request Timeout")
                        except FatalSSLAlert:
                            # Close the connection.
                            return
            elif errnum not in socket_errors_to_ignore:
                self.server.error_log("socket.error %s" % repr(errnum),
                                      level=logging.WARNING, traceback=True)
                if req and not req.sent_headers:
                    try:
                        req.simple_response("500 Internal Server Error")
                    except FatalSSLAlert:
                        # Close the connection.
                        return
            return
        except (KeyboardInterrupt, SystemExit):
            raise
        except FatalSSLAlert:
            # Close the connection.
            return
        except NoSSLError:
            if req and not req.sent_headers:
                # Unwrap our wfile
                self.wfile = CP_fileobject(self.socket._sock, "wb", self.wbufsize)
                req.simple_response("400 Bad Request",
                    "The client sent a plain HTTP request, but "
                    "this server only speaks HTTPS on this port.")
                self.linger = True
        except Exception:
            e = sys.exc_info()[1]
            self.server.error_log(repr(e), level=logging.ERROR, traceback=True)
            if req and not req.sent_headers:
                try:
                    req.simple_response("500 Internal Server Error")
                except FatalSSLAlert:
                    # Close the connection.
                    return
    
    linger = False
    
    def close(self):
        """Close the socket underlying this connection."""
        self.rfile.close()
        
        if not self.linger:
            # Python's socket module does NOT call close on the kernel socket
            # when you call socket.close(). We do so manually here because we
            # want this server to send a FIN TCP segment immediately. Note this
            # must be called *before* calling socket.close(), because the latter
            # drops its reference to the kernel socket.
            if hasattr(self.socket, '_sock'):
                self.socket._sock.close()
            self.socket.close()
        else:
            # On the other hand, sometimes we want to hang around for a bit
            # to make sure the client has a chance to read our entire
            # response. Skipping the close() calls here delays the FIN
            # packet until the socket object is garbage-collected later.
            # Someday, perhaps, we'll do the full lingering_close that
            # Apache does, but not today.
            pass


class TrueyZero(object):
    """An object which equals and does math like the integer '0' but evals True."""
    def __add__(self, other):
        return other
    def __radd__(self, other):
        return other
trueyzero = TrueyZero()


_SHUTDOWNREQUEST = None

class WorkerThread(threading.Thread):
    """Thread which continuously polls a Queue for Connection objects.
    
    Due to the timing issues of polling a Queue, a WorkerThread does not
    check its own 'ready' flag after it has started. To stop the thread,
    it is necessary to stick a _SHUTDOWNREQUEST object onto the Queue
    (one for each running WorkerThread).
    """
    
    conn = None
    """The current connection pulled off the Queue, or None."""
    
    server = None
    """The HTTP Server which spawned this thread, and which owns the
    Queue and is placing active connections into it."""
    
    ready = False
    """A simple flag for the calling server to know when this thread
    has begun polling the Queue."""
    
    
    def __init__(self, server):
        self.ready = False
        self.server = server
        
        self.requests_seen = 0
        self.bytes_read = 0
        self.bytes_written = 0
        self.start_time = None
        self.work_time = 0
        self.stats = {
            'Requests': lambda s: self.requests_seen + ((self.start_time is None) and trueyzero or self.conn.requests_seen),
            'Bytes Read': lambda s: self.bytes_read + ((self.start_time is None) and trueyzero or self.conn.rfile.bytes_read),
            'Bytes Written': lambda s: self.bytes_written + ((self.start_time is None) and trueyzero or self.conn.wfile.bytes_written),
            'Work Time': lambda s: self.work_time + ((self.start_time is None) and trueyzero or time.time() - self.start_time),
            'Read Throughput': lambda s: s['Bytes Read'](s) / (s['Work Time'](s) or 1e-6),
            'Write Throughput': lambda s: s['Bytes Written'](s) / (s['Work Time'](s) or 1e-6),
        }
        threading.Thread.__init__(self)
    
    def run(self):
        self.server.stats['Worker Threads'][self.getName()] = self.stats
        try:
            self.ready = True
            while True:
                conn = self.server.requests.get()
                if conn is _SHUTDOWNREQUEST:
                    return
                
                self.conn = conn
                if self.server.stats['Enabled']:
                    self.start_time = time.time()
                try:
                    conn.communicate()
                finally:
                    conn.close()
                    if self.server.stats['Enabled']:
                        self.requests_seen += self.conn.requests_seen
                        self.bytes_read += self.conn.rfile.bytes_read
                        self.bytes_written += self.conn.wfile.bytes_written
                        self.work_time += time.time() - self.start_time
                        self.start_time = None
                    self.conn = None
        except (KeyboardInterrupt, SystemExit):
            exc = sys.exc_info()[1]
            self.server.interrupt = exc


class ThreadPool(object):
    """A Request Queue for an HTTPServer which pools threads.
    
    ThreadPool objects must provide min, get(), put(obj), start()
    and stop(timeout) attributes.
    """
    
    def __init__(self, server, min=10, max=-1):
        self.server = server
        self.min = min
        self.max = max
        self._threads = []
        self._queue = queue.Queue()
        self.get = self._queue.get
    
    def start(self):
        """Start the pool of threads."""
        for i in range(self.min):
            self._threads.append(WorkerThread(self.server))
        for worker in self._threads:
            worker.setName("CP Server " + worker.getName())
            worker.start()
        for worker in self._threads:
            while not worker.ready:
                time.sleep(.1)
    
    def _get_idle(self):
        """Number of worker threads which are idle. Read-only."""
        return len([t for t in self._threads if t.conn is None])
    idle = property(_get_idle, doc=_get_idle.__doc__)
    
    def put(self, obj):
        self._queue.put(obj)
        if obj is _SHUTDOWNREQUEST:
            return
    
    def grow(self, amount):
        """Spawn new worker threads (not above self.max)."""
        for i in range(amount):
            if self.max > 0 and len(self._threads) >= self.max:
                break
            worker = WorkerThread(self.server)
            worker.setName("CP Server " + worker.getName())
            self._threads.append(worker)
            worker.start()
    
    def shrink(self, amount):
        """Kill off worker threads (not below self.min)."""
        # Grow/shrink the pool if necessary.
        # Remove any dead threads from our list
        for t in self._threads:
            if not t.isAlive():
                self._threads.remove(t)
                amount -= 1
        
        if amount > 0:
            for i in range(min(amount, len(self._threads) - self.min)):
                # Put a number of shutdown requests on the queue equal
                # to 'amount'. Once each of those is processed by a worker,
                # that worker will terminate and be culled from our list
                # in self.put.
                self._queue.put(_SHUTDOWNREQUEST)
    
    def stop(self, timeout=5):
        # Must shut down threads here so the code that calls
        # this method can know when all threads are stopped.
        for worker in self._threads:
            self._queue.put(_SHUTDOWNREQUEST)
        
        # Don't join currentThread (when stop is called inside a request).
        current = threading.currentThread()
        if timeout and timeout >= 0:
            endtime = time.time() + timeout
        while self._threads:
            worker = self._threads.pop()
            if worker is not current and worker.isAlive():
                try:
                    if timeout is None or timeout < 0:
                        worker.join()
                    else:
                        remaining_time = endtime - time.time()
                        if remaining_time > 0:
                            worker.join(remaining_time)
                        if worker.isAlive():
                            # We exhausted the timeout.
                            # Forcibly shut down the socket.
                            c = worker.conn
                            if c and not c.rfile.closed:
                                try:
                                    c.socket.shutdown(socket.SHUT_RD)
                                except TypeError:
                                    # pyOpenSSL sockets don't take an arg
                                    c.socket.shutdown()
                            worker.join()
                except (AssertionError,
                        # Ignore repeated Ctrl-C.
                        # See http://www.cherrypy.org/ticket/691.
                        KeyboardInterrupt):
                    pass
    
    def _get_qsize(self):
        return self._queue.qsize()
    qsize = property(_get_qsize)



try:
    import fcntl
except ImportError:
    try:
        from ctypes import windll, WinError
    except ImportError:
        def prevent_socket_inheritance(sock):
            """Dummy function, since neither fcntl nor ctypes are available."""
            pass
    else:
        def prevent_socket_inheritance(sock):
            """Mark the given socket fd as non-inheritable (Windows)."""
            if not windll.kernel32.SetHandleInformation(sock.fileno(), 1, 0):
                raise WinError()
else:
    def prevent_socket_inheritance(sock):
        """Mark the given socket fd as non-inheritable (POSIX)."""
        fd = sock.fileno()
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        fcntl.fcntl(fd, fcntl.F_SETFD, old_flags | fcntl.FD_CLOEXEC)


class SSLAdapter(object):
    """Base class for SSL driver library adapters.
    
    Required methods:
    
        * ``wrap(sock) -> (wrapped socket, ssl environ dict)``
        * ``makefile(sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE) -> socket file object``
    """
    
    def __init__(self, certificate, private_key, certificate_chain=None):
        self.certificate = certificate
        self.private_key = private_key
        self.certificate_chain = certificate_chain
    
    def wrap(self, sock):
        raise NotImplemented
    
    def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
        raise NotImplemented


class HTTPServer(object):
    """An HTTP server."""
    
    _bind_addr = "127.0.0.1"
    _interrupt = None
    
    gateway = None
    """A Gateway instance."""
    
    minthreads = None
    """The minimum number of worker threads to create (default 10)."""
    
    maxthreads = None
    """The maximum number of worker threads to create (default -1 = no limit)."""
    
    server_name = None
    """The name of the server; defaults to socket.gethostname()."""
    
    protocol = "HTTP/1.1"
    """The version string to write in the Status-Line of all HTTP responses.
    
    For example, "HTTP/1.1" is the default. This also limits the supported
    features used in the response."""
    
    request_queue_size = 5
    """The 'backlog' arg to socket.listen(); max queued connections (default 5)."""
    
    shutdown_timeout = 5
    """The total time, in seconds, to wait for worker threads to cleanly exit."""
    
    timeout = 10
    """The timeout in seconds for accepted connections (default 10)."""
    
    version = "CherryPy/3.2.2"
    """A version string for the HTTPServer."""
    
    software = None
    """The value to set for the SERVER_SOFTWARE entry in the WSGI environ.
    
    If None, this defaults to ``'%s Server' % self.version``."""
    
    ready = False
    """An internal flag which marks whether the socket is accepting connections."""
    
    max_request_header_size = 0
    """The maximum size, in bytes, for request headers, or 0 for no limit."""
    
    max_request_body_size = 0
    """The maximum size, in bytes, for request bodies, or 0 for no limit."""
    
    nodelay = True
    """If True (the default since 3.1), sets the TCP_NODELAY socket option."""
    
    ConnectionClass = HTTPConnection
    """The class to use for handling HTTP connections."""
    
    ssl_adapter = None
    """An instance of SSLAdapter (or a subclass).
    
    You must have the corresponding SSL driver library installed."""
    
    def __init__(self, bind_addr, gateway, minthreads=10, maxthreads=-1,
                 server_name=None):
        self.bind_addr = bind_addr
        self.gateway = gateway
        
        self.requests = ThreadPool(self, min=minthreads or 1, max=maxthreads)
        
        if not server_name:
            server_name = socket.gethostname()
        self.server_name = server_name
        self.clear_stats()
    
    def clear_stats(self):
        self._start_time = None
        self._run_time = 0
        self.stats = {
            'Enabled': False,
            'Bind Address': lambda s: repr(self.bind_addr),
            'Run time': lambda s: (not s['Enabled']) and -1 or self.runtime(),
            'Accepts': 0,
            'Accepts/sec': lambda s: s['Accepts'] / self.runtime(),
            'Queue': lambda s: getattr(self.requests, "qsize", None),
            'Threads': lambda s: len(getattr(self.requests, "_threads", [])),
            'Threads Idle': lambda s: getattr(self.requests, "idle", None),
            'Socket Errors': 0,
            'Requests': lambda s: (not s['Enabled']) and -1 or sum([w['Requests'](w) for w
                                       in s['Worker Threads'].values()], 0),
            'Bytes Read': lambda s: (not s['Enabled']) and -1 or sum([w['Bytes Read'](w) for w
                                         in s['Worker Threads'].values()], 0),
            'Bytes Written': lambda s: (not s['Enabled']) and -1 or sum([w['Bytes Written'](w) for w
                                            in s['Worker Threads'].values()], 0),
            'Work Time': lambda s: (not s['Enabled']) and -1 or sum([w['Work Time'](w) for w
                                         in s['Worker Threads'].values()], 0),
            'Read Throughput': lambda s: (not s['Enabled']) and -1 or sum(
                [w['Bytes Read'](w) / (w['Work Time'](w) or 1e-6)
                 for w in s['Worker Threads'].values()], 0),
            'Write Throughput': lambda s: (not s['Enabled']) and -1 or sum(
                [w['Bytes Written'](w) / (w['Work Time'](w) or 1e-6)
                 for w in s['Worker Threads'].values()], 0),
            'Worker Threads': {},
            }
        logging.statistics["CherryPy HTTPServer %d" % id(self)] = self.stats
    
    def runtime(self):
        if self._start_time is None:
            return self._run_time
        else:
            return self._run_time + (time.time() - self._start_time)
    
    def __str__(self):
        return "%s.%s(%r)" % (self.__module__, self.__class__.__name__,
                              self.bind_addr)
    
    def _get_bind_addr(self):
        return self._bind_addr
    def _set_bind_addr(self, value):
        if isinstance(value, tuple) and value[0] in ('', None):
            # Despite the socket module docs, using '' does not
            # allow AI_PASSIVE to work. Passing None instead
            # returns '0.0.0.0' like we want. In other words:
            #     host    AI_PASSIVE     result
            #      ''         Y         192.168.x.y
            #      ''         N         192.168.x.y
            #     None        Y         0.0.0.0
            #     None        N         127.0.0.1
            # But since you can get the same effect with an explicit
            # '0.0.0.0', we deny both the empty string and None as values.
            raise ValueError("Host values of '' or None are not allowed. "
                             "Use '0.0.0.0' (IPv4) or '::' (IPv6) instead "
                             "to listen on all active interfaces.")
        self._bind_addr = value
    bind_addr = property(_get_bind_addr, _set_bind_addr,
        doc="""The interface on which to listen for connections.
        
        For TCP sockets, a (host, port) tuple. Host values may be any IPv4
        or IPv6 address, or any valid hostname. The string 'localhost' is a
        synonym for '127.0.0.1' (or '::1', if your hosts file prefers IPv6).
        The string '0.0.0.0' is a special IPv4 entry meaning "any active
        interface" (INADDR_ANY), and '::' is the similar IN6ADDR_ANY for
        IPv6. The empty string or None are not allowed.
        
        For UNIX sockets, supply the filename as a string.""")
    
    def start(self):
        """Run the server forever."""
        # We don't have to trap KeyboardInterrupt or SystemExit here,
        # because cherrpy.server already does so, calling self.stop() for us.
        # If you're using this server with another framework, you should
        # trap those exceptions in whatever code block calls start().
        self._interrupt = None
        
        if self.software is None:
            self.software = "%s Server" % self.version
        
        # SSL backward compatibility
        if (self.ssl_adapter is None and
            getattr(self, 'ssl_certificate', None) and
            getattr(self, 'ssl_private_key', None)):
            warnings.warn(
                    "SSL attributes are deprecated in CherryPy 3.2, and will "
                    "be removed in CherryPy 3.3. Use an ssl_adapter attribute "
                    "instead.",
                    DeprecationWarning
                )
            try:
                from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
            except ImportError:
                pass
            else:
                self.ssl_adapter = pyOpenSSLAdapter(
                    self.ssl_certificate, self.ssl_private_key,
                    getattr(self, 'ssl_certificate_chain', None))
        
        # Select the appropriate socket
        if isinstance(self.bind_addr, basestring):
            # AF_UNIX socket
            
            # So we can reuse the socket...
            try: os.unlink(self.bind_addr)
            except: pass
            
            # So everyone can access the socket...
            try: os.chmod(self.bind_addr, 511) # 0777
            except: pass
            
            info = [(socket.AF_UNIX, socket.SOCK_STREAM, 0, "", self.bind_addr)]
        else:
            # AF_INET or AF_INET6 socket
            # Get the correct address family for our host (allows IPv6 addresses)
            host, port = self.bind_addr
            try:
                info = socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
            except socket.gaierror:
                if ':' in self.bind_addr[0]:
                    info = [(socket.AF_INET6, socket.SOCK_STREAM,
                             0, "", self.bind_addr + (0, 0))]
                else:
                    info = [(socket.AF_INET, socket.SOCK_STREAM,
                             0, "", self.bind_addr)]
        
        self.socket = None
        msg = "No socket could be created"
        for res in info:
            af, socktype, proto, canonname, sa = res
            try:
                self.bind(af, socktype, proto)
            except socket.error:
                if self.socket:
                    self.socket.close()
                self.socket = None
                continue
            break
        if not self.socket:
            raise socket.error(msg)
        
        # Timeout so KeyboardInterrupt can be caught on Win32
        self.socket.settimeout(1)
        self.socket.listen(self.request_queue_size)
        
        # Create worker threads
        self.requests.start()
        
        self.ready = True
        self._start_time = time.time()
        while self.ready:
            try:
                self.tick()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.error_log("Error in HTTPServer.tick", level=logging.ERROR,
                               traceback=True)
            
            if self.interrupt:
                while self.interrupt is True:
                    # Wait for self.stop() to complete. See _set_interrupt.
                    time.sleep(0.1)
                if self.interrupt:
                    raise self.interrupt

    def error_log(self, msg="", level=20, traceback=False):
        # Override this in subclasses as desired
        sys.stderr.write(msg + '\n')
        sys.stderr.flush()
        if traceback:
            tblines = format_exc()
            sys.stderr.write(tblines)
            sys.stderr.flush()

    def bind(self, family, type, proto=0):
        """Create (or recreate) the actual socket object."""
        self.socket = socket.socket(family, type, proto)
        prevent_socket_inheritance(self.socket)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.nodelay and not isinstance(self.bind_addr, str):
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        if self.ssl_adapter is not None:
            self.socket = self.ssl_adapter.bind(self.socket)
        
        # If listening on the IPV6 any address ('::' = IN6ADDR_ANY),
        # activate dual-stack. See http://www.cherrypy.org/ticket/871.
        if (hasattr(socket, 'AF_INET6') and family == socket.AF_INET6
            and self.bind_addr[0] in ('::', '::0', '::0.0.0.0')):
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except (AttributeError, socket.error):
                # Apparently, the socket option is not available in
                # this machine's TCP stack
                pass
        
        self.socket.bind(self.bind_addr)
    
    def tick(self):
        """Accept a new connection and put it on the Queue."""
        try:
            s, addr = self.socket.accept()
            if self.stats['Enabled']:
                self.stats['Accepts'] += 1
            if not self.ready:
                return
            
            prevent_socket_inheritance(s)
            if hasattr(s, 'settimeout'):
                s.settimeout(self.timeout)
            
            makefile = CP_fileobject
            ssl_env = {}
            # if ssl cert and key are set, we try to be a secure HTTP server
            if self.ssl_adapter is not None:
                try:
                    s, ssl_env = self.ssl_adapter.wrap(s)
                except NoSSLError:
                    msg = ("The client sent a plain HTTP request, but "
                           "this server only speaks HTTPS on this port.")
                    buf = ["%s 400 Bad Request\r\n" % self.protocol,
                           "Content-Length: %s\r\n" % len(msg),
                           "Content-Type: text/plain\r\n\r\n",
                           msg]
                    
                    wfile = makefile(s, "wb", DEFAULT_BUFFER_SIZE)
                    try:
                        wfile.sendall("".join(buf))
                    except socket.error:
                        x = sys.exc_info()[1]
                        if x.args[0] not in socket_errors_to_ignore:
                            raise
                    return
                if not s:
                    return
                makefile = self.ssl_adapter.makefile
                # Re-apply our timeout since we may have a new socket object
                if hasattr(s, 'settimeout'):
                    s.settimeout(self.timeout)
            
            conn = self.ConnectionClass(self, s, makefile)
            
            if not isinstance(self.bind_addr, basestring):
                # optional values
                # Until we do DNS lookups, omit REMOTE_HOST
                if addr is None: # sometimes this can happen
                    # figure out if AF_INET or AF_INET6.
                    if len(s.getsockname()) == 2:
                        # AF_INET
                        addr = ('0.0.0.0', 0)
                    else:
                        # AF_INET6
                        addr = ('::', 0)
                conn.remote_addr = addr[0]
                conn.remote_port = addr[1]
            
            conn.ssl_env = ssl_env
            
            self.requests.put(conn)
        except socket.timeout:
            # The only reason for the timeout in start() is so we can
            # notice keyboard interrupts on Win32, which don't interrupt
            # accept() by default
            return
        except socket.error:
            x = sys.exc_info()[1]
            if self.stats['Enabled']:
                self.stats['Socket Errors'] += 1
            if x.args[0] in socket_error_eintr:
                # I *think* this is right. EINTR should occur when a signal
                # is received during the accept() call; all docs say retry
                # the call, and I *think* I'm reading it right that Python
                # will then go ahead and poll for and handle the signal
                # elsewhere. See http://www.cherrypy.org/ticket/707.
                return
            if x.args[0] in socket_errors_nonblocking:
                # Just try again. See http://www.cherrypy.org/ticket/479.
                return
            if x.args[0] in socket_errors_to_ignore:
                # Our socket was closed.
                # See http://www.cherrypy.org/ticket/686.
                return
            raise
    
    def _get_interrupt(self):
        return self._interrupt
    def _set_interrupt(self, interrupt):
        self._interrupt = True
        self.stop()
        self._interrupt = interrupt
    interrupt = property(_get_interrupt, _set_interrupt,
                         doc="Set this to an Exception instance to "
                             "interrupt the server.")
    
    def stop(self):
        """Gracefully shutdown a server that is serving forever."""
        self.ready = False
        if self._start_time is not None:
            self._run_time += (time.time() - self._start_time)
        self._start_time = None
        
        sock = getattr(self, "socket", None)
        if sock:
            if not isinstance(self.bind_addr, basestring):
                # Touch our own socket to make accept() return immediately.
                try:
                    host, port = sock.getsockname()[:2]
                except socket.error:
                    x = sys.exc_info()[1]
                    if x.args[0] not in socket_errors_to_ignore:
                        # Changed to use error code and not message
                        # See http://www.cherrypy.org/ticket/860.
                        raise
                else:
                    # Note that we're explicitly NOT using AI_PASSIVE,
                    # here, because we want an actual IP to touch.
                    # localhost won't work if we've bound to a public IP,
                    # but it will if we bound to '0.0.0.0' (INADDR_ANY).
                    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                                  socket.SOCK_STREAM):
                        af, socktype, proto, canonname, sa = res
                        s = None
                        try:
                            s = socket.socket(af, socktype, proto)
                            # See http://groups.google.com/group/cherrypy-users/
                            #        browse_frm/thread/bbfe5eb39c904fe0
                            s.settimeout(1.0)
                            s.connect((host, port))
                            s.close()
                        except socket.error:
                            if s:
                                s.close()
            if hasattr(sock, "close"):
                sock.close()
            self.socket = None
        
        self.requests.stop(self.shutdown_timeout)


class Gateway(object):
    """A base class to interface HTTPServer with other systems, such as WSGI."""
    
    def __init__(self, req):
        self.req = req
    
    def respond(self):
        """Process the current request. Must be overridden in a subclass."""
        raise NotImplemented


# These may either be wsgiserver.SSLAdapter subclasses or the string names
# of such classes (in which case they will be lazily loaded).
ssl_adapters = {
    'builtin': 'cherrypy.wsgiserver.ssl_builtin.BuiltinSSLAdapter',
    'pyopenssl': 'cherrypy.wsgiserver.ssl_pyopenssl.pyOpenSSLAdapter',
    }

def get_ssl_adapter_class(name='pyopenssl'):
    """Return an SSL adapter class for the given name."""
    adapter = ssl_adapters[name.lower()]
    if isinstance(adapter, basestring):
        last_dot = adapter.rfind(".")
        attr_name = adapter[last_dot + 1:]
        mod_path = adapter[:last_dot]
        
        try:
            mod = sys.modules[mod_path]
            if mod is None:
                raise KeyError()
        except KeyError:
            # The last [''] is important.
            mod = __import__(mod_path, globals(), locals(), [''])
        
        # Let an AttributeError propagate outward.
        try:
            adapter = getattr(mod, attr_name)
        except AttributeError:
            raise AttributeError("'%s' object has no attribute '%s'"
                                 % (mod_path, attr_name))
    
    return adapter

# -------------------------------- WSGI Stuff -------------------------------- #


class CherryPyWSGIServer(HTTPServer):
    """A subclass of HTTPServer which calls a WSGI application."""
    
    wsgi_version = (1, 0)
    """The version of WSGI to produce."""
    
    def __init__(self, bind_addr, wsgi_app, numthreads=10, server_name=None,
                 max=-1, request_queue_size=5, timeout=10, shutdown_timeout=5):
        self.requests = ThreadPool(self, min=numthreads or 1, max=max)
        self.wsgi_app = wsgi_app
        self.gateway = wsgi_gateways[self.wsgi_version]
        
        self.bind_addr = bind_addr
        if not server_name:
            server_name = socket.gethostname()
        self.server_name = server_name
        self.request_queue_size = request_queue_size
        
        self.timeout = timeout
        self.shutdown_timeout = shutdown_timeout
        self.clear_stats()
    
    def _get_numthreads(self):
        return self.requests.min
    def _set_numthreads(self, value):
        self.requests.min = value
    numthreads = property(_get_numthreads, _set_numthreads)


class WSGIGateway(Gateway):
    """A base class to interface HTTPServer with WSGI."""
    
    def __init__(self, req):
        self.req = req
        self.started_response = False
        self.env = self.get_environ()
        self.remaining_bytes_out = None
    
    def get_environ(self):
        """Return a new environ dict targeting the given wsgi.version"""
        raise NotImplemented
    
    def respond(self):
        """Process the current request."""
        response = self.req.server.wsgi_app(self.env, self.start_response)
        try:
            for chunk in response:
                # "The start_response callable must not actually transmit
                # the response headers. Instead, it must store them for the
                # server or gateway to transmit only after the first
                # iteration of the application return value that yields
                # a NON-EMPTY string, or upon the application's first
                # invocation of the write() callable." (PEP 333)
                if chunk:
                    if isinstance(chunk, unicodestr):
                        chunk = chunk.encode('ISO-8859-1')
                    self.write(chunk)
        finally:
            if hasattr(response, "close"):
                response.close()
    
    def start_response(self, status, headers, exc_info = None):
        """WSGI callable to begin the HTTP response."""
        # "The application may call start_response more than once,
        # if and only if the exc_info argument is provided."
        if self.started_response and not exc_info:
            raise AssertionError("WSGI start_response called a second "
                                 "time with no exc_info.")
        self.started_response = True
        
        # "if exc_info is provided, and the HTTP headers have already been
        # sent, start_response must raise an error, and should raise the
        # exc_info tuple."
        if self.req.sent_headers:
            try:
                raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None
        
        self.req.status = status
        for k, v in headers:
            if not isinstance(k, str):
                raise TypeError("WSGI response header key %r is not of type str." % k)
            if not isinstance(v, str):
                raise TypeError("WSGI response header value %r is not of type str." % v)
            if k.lower() == 'content-length':
                self.remaining_bytes_out = int(v)
        self.req.outheaders.extend(headers)
        
        return self.write
    
    def write(self, chunk):
        """WSGI callable to write unbuffered data to the client.
        
        This method is also used internally by start_response (to write
        data from the iterable returned by the WSGI application).
        """
        if not self.started_response:
            raise AssertionError("WSGI write called before start_response.")
        
        chunklen = len(chunk)
        rbo = self.remaining_bytes_out
        if rbo is not None and chunklen > rbo:
            if not self.req.sent_headers:
                # Whew. We can send a 500 to the client.
                self.req.simple_response("500 Internal Server Error",
                    "The requested resource returned more bytes than the "
                    "declared Content-Length.")
            else:
                # Dang. We have probably already sent data. Truncate the chunk
                # to fit (so the client doesn't hang) and raise an error later.
                chunk = chunk[:rbo]
        
        if not self.req.sent_headers:
            self.req.sent_headers = True
            self.req.send_headers()
        
        self.req.write(chunk)
        
        if rbo is not None:
            rbo -= chunklen
            if rbo < 0:
                raise ValueError(
                    "Response body exceeds the declared Content-Length.")


class WSGIGateway_10(WSGIGateway):
    """A Gateway class to interface HTTPServer with WSGI 1.0.x."""
    
    def get_environ(self):
        """Return a new environ dict targeting the given wsgi.version"""
        req = self.req
        env = {
            # set a non-standard environ entry so the WSGI app can know what
            # the *real* server protocol is (and what features to support).
            # See http://www.faqs.org/rfcs/rfc2145.html.
            'ACTUAL_SERVER_PROTOCOL': req.server.protocol,
            'PATH_INFO': req.path,
            'QUERY_STRING': req.qs,
            'REMOTE_ADDR': req.conn.remote_addr or '',
            'REMOTE_PORT': str(req.conn.remote_port or ''),
            'REQUEST_METHOD': req.method,
            'REQUEST_URI': req.uri,
            'SCRIPT_NAME': '',
            'SERVER_NAME': req.server.server_name,
            # Bah. "SERVER_PROTOCOL" is actually the REQUEST protocol.
            'SERVER_PROTOCOL': req.request_protocol,
            'SERVER_SOFTWARE': req.server.software,
            'wsgi.errors': sys.stderr,
            'wsgi.input': req.rfile,
            'wsgi.multiprocess': False,
            'wsgi.multithread': True,
            'wsgi.run_once': False,
            'wsgi.url_scheme': req.scheme,
            'wsgi.version': (1, 0),
            }
        
        if isinstance(req.server.bind_addr, basestring):
            # AF_UNIX. This isn't really allowed by WSGI, which doesn't
            # address unix domain sockets. But it's better than nothing.
            env["SERVER_PORT"] = ""
        else:
            env["SERVER_PORT"] = str(req.server.bind_addr[1])
        
        # Request headers
        for k, v in req.inheaders.iteritems():
            env["HTTP_" + k.upper().replace("-", "_")] = v
        
        # CONTENT_TYPE/CONTENT_LENGTH
        ct = env.pop("HTTP_CONTENT_TYPE", None)
        if ct is not None:
            env["CONTENT_TYPE"] = ct
        cl = env.pop("HTTP_CONTENT_LENGTH", None)
        if cl is not None:
            env["CONTENT_LENGTH"] = cl
        
        if req.conn.ssl_env:
            env.update(req.conn.ssl_env)
        
        return env


class WSGIGateway_u0(WSGIGateway_10):
    """A Gateway class to interface HTTPServer with WSGI u.0.
    
    WSGI u.0 is an experimental protocol, which uses unicode for keys and values
    in both Python 2 and Python 3.
    """
    
    def get_environ(self):
        """Return a new environ dict targeting the given wsgi.version"""
        req = self.req
        env_10 = WSGIGateway_10.get_environ(self)
        env = dict([(k.decode('ISO-8859-1'), v) for k, v in env_10.iteritems()])
        env[u'wsgi.version'] = ('u', 0)
        
        # Request-URI
        env.setdefault(u'wsgi.url_encoding', u'utf-8')
        try:
            for key in [u"PATH_INFO", u"SCRIPT_NAME", u"QUERY_STRING"]:
                env[key] = env_10[str(key)].decode(env[u'wsgi.url_encoding'])
        except UnicodeDecodeError:
            # Fall back to latin 1 so apps can transcode if needed.
            env[u'wsgi.url_encoding'] = u'ISO-8859-1'
            for key in [u"PATH_INFO", u"SCRIPT_NAME", u"QUERY_STRING"]:
                env[key] = env_10[str(key)].decode(env[u'wsgi.url_encoding'])
        
        for k, v in sorted(env.items()):
            if isinstance(v, str) and k not in ('REQUEST_URI', 'wsgi.input'):
                env[k] = v.decode('ISO-8859-1')
        
        return env

wsgi_gateways = {
    (1, 0): WSGIGateway_10,
    ('u', 0): WSGIGateway_u0,
}

class WSGIPathInfoDispatcher(object):
    """A WSGI dispatcher for dispatch based on the PATH_INFO.
    
    apps: a dict or list of (path_prefix, app) pairs.
    """
    
    def __init__(self, apps):
        try:
            apps = list(apps.items())
        except AttributeError:
            pass
        
        # Sort the apps by len(path), descending
        apps.sort(cmp=lambda x,y: cmp(len(x[0]), len(y[0])))
        apps.reverse()
        
        # The path_prefix strings must start, but not end, with a slash.
        # Use "" instead of "/".
        self.apps = [(p.rstrip("/"), a) for p, a in apps]
    
    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"] or "/"
        for p, app in self.apps:
            # The apps list should be sorted by length, descending.
            if path.startswith(p + "/") or path == p:
                environ = environ.copy()
                environ["SCRIPT_NAME"] = environ["SCRIPT_NAME"] + p
                environ["PATH_INFO"] = path[len(p):]
                return app(environ, start_response)
        
        start_response('404 Not Found', [('Content-Type', 'text/plain'),
                                         ('Content-Length', '0')])
        return ['']


########NEW FILE########
__FILENAME__ = wsgiserver3
"""A high-speed, production ready, thread pooled, generic HTTP server.

Simplest example on how to use this module directly
(without using CherryPy's application machinery)::

    from cherrypy import wsgiserver
    
    def my_crazy_app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type','text/plain')]
        start_response(status, response_headers)
        return ['Hello world!']
    
    server = wsgiserver.CherryPyWSGIServer(
                ('0.0.0.0', 8070), my_crazy_app,
                server_name='www.cherrypy.example')
    server.start()
    
The CherryPy WSGI server can serve as many WSGI applications 
as you want in one instance by using a WSGIPathInfoDispatcher::
    
    d = WSGIPathInfoDispatcher({'/': my_crazy_app, '/blog': my_blog_app})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 80), d)
    
Want SSL support? Just set server.ssl_adapter to an SSLAdapter instance.

This won't call the CherryPy engine (application side) at all, only the
HTTP server, which is independent from the rest of CherryPy. Don't
let the name "CherryPyWSGIServer" throw you; the name merely reflects
its origin, not its coupling.

For those of you wanting to understand internals of this module, here's the
basic call flow. The server's listening thread runs a very tight loop,
sticking incoming connections onto a Queue::

    server = CherryPyWSGIServer(...)
    server.start()
    while True:
        tick()
        # This blocks until a request comes in:
        child = socket.accept()
        conn = HTTPConnection(child, ...)
        server.requests.put(conn)

Worker threads are kept in a pool and poll the Queue, popping off and then
handling each connection in turn. Each connection can consist of an arbitrary
number of requests and their responses, so we run a nested loop::

    while True:
        conn = server.requests.get()
        conn.communicate()
        ->  while True:
                req = HTTPRequest(...)
                req.parse_request()
                ->  # Read the Request-Line, e.g. "GET /page HTTP/1.1"
                    req.rfile.readline()
                    read_headers(req.rfile, req.inheaders)
                req.respond()
                ->  response = app(...)
                    try:
                        for chunk in response:
                            if chunk:
                                req.write(chunk)
                    finally:
                        if hasattr(response, "close"):
                            response.close()
                if req.close_connection:
                    return
"""

__all__ = ['HTTPRequest', 'HTTPConnection', 'HTTPServer',
           'SizeCheckWrapper', 'KnownLengthRFile', 'ChunkedRFile',
           'CP_makefile',
           'MaxSizeExceeded', 'NoSSLError', 'FatalSSLAlert',
           'WorkerThread', 'ThreadPool', 'SSLAdapter',
           'CherryPyWSGIServer',
           'Gateway', 'WSGIGateway', 'WSGIGateway_10', 'WSGIGateway_u0',
           'WSGIPathInfoDispatcher', 'get_ssl_adapter_class']

import os
try:
    import queue
except:
    import Queue as queue
import re
import email.utils
import socket
import sys
if 'win' in sys.platform and not hasattr(socket, 'IPPROTO_IPV6'):
    socket.IPPROTO_IPV6 = 41
if sys.version_info < (3,1):
    import io
else:
    import _pyio as io
DEFAULT_BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE

import threading
import time
from traceback import format_exc
from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.parse import scheme_chars
import warnings

if sys.version_info >= (3, 0):
    bytestr = bytes
    unicodestr = str
    basestring = (bytes, str)
    def ntob(n, encoding='ISO-8859-1'):
        """Return the given native string as a byte string in the given encoding."""
        # In Python 3, the native string type is unicode
        return n.encode(encoding)
else:
    bytestr = str
    unicodestr = unicode
    basestring = basestring
    def ntob(n, encoding='ISO-8859-1'):
        """Return the given native string as a byte string in the given encoding."""
        # In Python 2, the native string type is bytes. Assume it's already
        # in the given encoding, which for ISO-8859-1 is almost always what
        # was intended.
        return n

LF = ntob('\n')
CRLF = ntob('\r\n')
TAB = ntob('\t')
SPACE = ntob(' ')
COLON = ntob(':')
SEMICOLON = ntob(';')
EMPTY = ntob('')
NUMBER_SIGN = ntob('#')
QUESTION_MARK = ntob('?')
ASTERISK = ntob('*')
FORWARD_SLASH = ntob('/')
quoted_slash = re.compile(ntob("(?i)%2F"))

import errno

def plat_specific_errors(*errnames):
    """Return error numbers for all errors in errnames on this platform.
    
    The 'errno' module contains different global constants depending on
    the specific platform (OS). This function will return the list of
    numeric values for a given list of potential names.
    """
    errno_names = dir(errno)
    nums = [getattr(errno, k) for k in errnames if k in errno_names]
    # de-dupe the list
    return list(dict.fromkeys(nums).keys())

socket_error_eintr = plat_specific_errors("EINTR", "WSAEINTR")

socket_errors_to_ignore = plat_specific_errors(
    "EPIPE",
    "EBADF", "WSAEBADF",
    "ENOTSOCK", "WSAENOTSOCK",
    "ETIMEDOUT", "WSAETIMEDOUT",
    "ECONNREFUSED", "WSAECONNREFUSED",
    "ECONNRESET", "WSAECONNRESET",
    "ECONNABORTED", "WSAECONNABORTED",
    "ENETRESET", "WSAENETRESET",
    "EHOSTDOWN", "EHOSTUNREACH",
    )
socket_errors_to_ignore.append("timed out")
socket_errors_to_ignore.append("The read operation timed out")

socket_errors_nonblocking = plat_specific_errors(
    'EAGAIN', 'EWOULDBLOCK', 'WSAEWOULDBLOCK')

comma_separated_headers = [ntob(h) for h in
    ['Accept', 'Accept-Charset', 'Accept-Encoding',
     'Accept-Language', 'Accept-Ranges', 'Allow', 'Cache-Control',
     'Connection', 'Content-Encoding', 'Content-Language', 'Expect',
     'If-Match', 'If-None-Match', 'Pragma', 'Proxy-Authenticate', 'TE',
     'Trailer', 'Transfer-Encoding', 'Upgrade', 'Vary', 'Via', 'Warning',
     'WWW-Authenticate']]


import logging
if not hasattr(logging, 'statistics'): logging.statistics = {}


def read_headers(rfile, hdict=None):
    """Read headers from the given stream into the given header dict.
    
    If hdict is None, a new header dict is created. Returns the populated
    header dict.
    
    Headers which are repeated are folded together using a comma if their
    specification so dictates.
    
    This function raises ValueError when the read bytes violate the HTTP spec.
    You should probably return "400 Bad Request" if this happens.
    """
    if hdict is None:
        hdict = {}
    
    while True:
        line = rfile.readline()
        if not line:
            # No more data--illegal end of headers
            raise ValueError("Illegal end of headers.")
        
        if line == CRLF:
            # Normal end of headers
            break
        if not line.endswith(CRLF):
            raise ValueError("HTTP requires CRLF terminators")
        
        if line[0] in (SPACE, TAB):
            # It's a continuation line.
            v = line.strip()
        else:
            try:
                k, v = line.split(COLON, 1)
            except ValueError:
                raise ValueError("Illegal header line.")
            # TODO: what about TE and WWW-Authenticate?
            k = k.strip().title()
            v = v.strip()
            hname = k
        
        if k in comma_separated_headers:
            existing = hdict.get(hname)
            if existing:
                v = b", ".join((existing, v))
        hdict[hname] = v
    
    return hdict


class MaxSizeExceeded(Exception):
    pass

class SizeCheckWrapper(object):
    """Wraps a file-like object, raising MaxSizeExceeded if too large."""
    
    def __init__(self, rfile, maxlen):
        self.rfile = rfile
        self.maxlen = maxlen
        self.bytes_read = 0
    
    def _check_length(self):
        if self.maxlen and self.bytes_read > self.maxlen:
            raise MaxSizeExceeded()
    
    def read(self, size=None):
        data = self.rfile.read(size)
        self.bytes_read += len(data)
        self._check_length()
        return data
    
    def readline(self, size=None):
        if size is not None:
            data = self.rfile.readline(size)
            self.bytes_read += len(data)
            self._check_length()
            return data
        
        # User didn't specify a size ...
        # We read the line in chunks to make sure it's not a 100MB line !
        res = []
        while True:
            data = self.rfile.readline(256)
            self.bytes_read += len(data)
            self._check_length()
            res.append(data)
            # See http://www.cherrypy.org/ticket/421
            if len(data) < 256 or data[-1:] == "\n":
                return EMPTY.join(res)
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline()
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline()
        return lines
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        data = next(self.rfile)
        self.bytes_read += len(data)
        self._check_length()
        return data
    
    def next(self):
        data = self.rfile.next()
        self.bytes_read += len(data)
        self._check_length()
        return data


class KnownLengthRFile(object):
    """Wraps a file-like object, returning an empty string when exhausted."""
    
    def __init__(self, rfile, content_length):
        self.rfile = rfile
        self.remaining = content_length
    
    def read(self, size=None):
        if self.remaining == 0:
            return b''
        if size is None:
            size = self.remaining
        else:
            size = min(size, self.remaining)
        
        data = self.rfile.read(size)
        self.remaining -= len(data)
        return data
    
    def readline(self, size=None):
        if self.remaining == 0:
            return b''
        if size is None:
            size = self.remaining
        else:
            size = min(size, self.remaining)
        
        data = self.rfile.readline(size)
        self.remaining -= len(data)
        return data
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline(sizehint)
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline(sizehint)
        return lines
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        data = next(self.rfile)
        self.remaining -= len(data)
        return data


class ChunkedRFile(object):
    """Wraps a file-like object, returning an empty string when exhausted.
    
    This class is intended to provide a conforming wsgi.input value for
    request entities that have been encoded with the 'chunked' transfer
    encoding.
    """
    
    def __init__(self, rfile, maxlen, bufsize=8192):
        self.rfile = rfile
        self.maxlen = maxlen
        self.bytes_read = 0
        self.buffer = EMPTY
        self.bufsize = bufsize
        self.closed = False
    
    def _fetch(self):
        if self.closed:
            return
        
        line = self.rfile.readline()
        self.bytes_read += len(line)
        
        if self.maxlen and self.bytes_read > self.maxlen:
            raise MaxSizeExceeded("Request Entity Too Large", self.maxlen)
        
        line = line.strip().split(SEMICOLON, 1)
        
        try:
            chunk_size = line.pop(0)
            chunk_size = int(chunk_size, 16)
        except ValueError:
            raise ValueError("Bad chunked transfer size: " + repr(chunk_size))
        
        if chunk_size <= 0:
            self.closed = True
            return
        
##            if line: chunk_extension = line[0]
        
        if self.maxlen and self.bytes_read + chunk_size > self.maxlen:
            raise IOError("Request Entity Too Large")
        
        chunk = self.rfile.read(chunk_size)
        self.bytes_read += len(chunk)
        self.buffer += chunk
        
        crlf = self.rfile.read(2)
        if crlf != CRLF:
            raise ValueError(
                 "Bad chunked transfer coding (expected '\\r\\n', "
                 "got " + repr(crlf) + ")")
    
    def read(self, size=None):
        data = EMPTY
        while True:
            if size and len(data) >= size:
                return data
            
            if not self.buffer:
                self._fetch()
                if not self.buffer:
                    # EOF
                    return data
            
            if size:
                remaining = size - len(data)
                data += self.buffer[:remaining]
                self.buffer = self.buffer[remaining:]
            else:
                data += self.buffer
    
    def readline(self, size=None):
        data = EMPTY
        while True:
            if size and len(data) >= size:
                return data
            
            if not self.buffer:
                self._fetch()
                if not self.buffer:
                    # EOF
                    return data
            
            newline_pos = self.buffer.find(LF)
            if size:
                if newline_pos == -1:
                    remaining = size - len(data)
                    data += self.buffer[:remaining]
                    self.buffer = self.buffer[remaining:]
                else:
                    remaining = min(size - len(data), newline_pos)
                    data += self.buffer[:remaining]
                    self.buffer = self.buffer[remaining:]
            else:
                if newline_pos == -1:
                    data += self.buffer
                else:
                    data += self.buffer[:newline_pos]
                    self.buffer = self.buffer[newline_pos:]
    
    def readlines(self, sizehint=0):
        # Shamelessly stolen from StringIO
        total = 0
        lines = []
        line = self.readline(sizehint)
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline(sizehint)
        return lines
    
    def read_trailer_lines(self):
        if not self.closed:
            raise ValueError(
                "Cannot read trailers until the request body has been read.")
        
        while True:
            line = self.rfile.readline()
            if not line:
                # No more data--illegal end of headers
                raise ValueError("Illegal end of headers.")
            
            self.bytes_read += len(line)
            if self.maxlen and self.bytes_read > self.maxlen:
                raise IOError("Request Entity Too Large")
            
            if line == CRLF:
                # Normal end of headers
                break
            if not line.endswith(CRLF):
                raise ValueError("HTTP requires CRLF terminators")
            
            yield line
    
    def close(self):
        self.rfile.close()
    
    def __iter__(self):
        # Shamelessly stolen from StringIO
        total = 0
        line = self.readline(sizehint)
        while line:
            yield line
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline(sizehint)


class HTTPRequest(object):
    """An HTTP Request (and response).
    
    A single HTTP connection may consist of multiple request/response pairs.
    """
    
    server = None
    """The HTTPServer object which is receiving this request."""
    
    conn = None
    """The HTTPConnection object on which this request connected."""
    
    inheaders = {}
    """A dict of request headers."""
    
    outheaders = []
    """A list of header tuples to write in the response."""
    
    ready = False
    """When True, the request has been parsed and is ready to begin generating
    the response. When False, signals the calling Connection that the response
    should not be generated and the connection should close."""
    
    close_connection = False
    """Signals the calling Connection that the request should close. This does
    not imply an error! The client and/or server may each request that the
    connection be closed."""
    
    chunked_write = False
    """If True, output will be encoded with the "chunked" transfer-coding.
    
    This value is set automatically inside send_headers."""
    
    def __init__(self, server, conn):
        self.server= server
        self.conn = conn
        
        self.ready = False
        self.started_request = False
        self.scheme = ntob("http")
        if self.server.ssl_adapter is not None:
            self.scheme = ntob("https")
        # Use the lowest-common protocol in case read_request_line errors.
        self.response_protocol = 'HTTP/1.0'
        self.inheaders = {}
        
        self.status = ""
        self.outheaders = []
        self.sent_headers = False
        self.close_connection = self.__class__.close_connection
        self.chunked_read = False
        self.chunked_write = self.__class__.chunked_write
    
    def parse_request(self):
        """Parse the next HTTP request start-line and message-headers."""
        self.rfile = SizeCheckWrapper(self.conn.rfile,
                                      self.server.max_request_header_size)
        try:
            success = self.read_request_line()
        except MaxSizeExceeded:
            self.simple_response("414 Request-URI Too Long",
                "The Request-URI sent with the request exceeds the maximum "
                "allowed bytes.")
            return
        else:
            if not success:
                return
        
        try:
            success = self.read_request_headers()
        except MaxSizeExceeded:
            self.simple_response("413 Request Entity Too Large",
                "The headers sent with the request exceed the maximum "
                "allowed bytes.")
            return
        else:
            if not success:
                return
        
        self.ready = True
    
    def read_request_line(self):
        # HTTP/1.1 connections are persistent by default. If a client
        # requests a page, then idles (leaves the connection open),
        # then rfile.readline() will raise socket.error("timed out").
        # Note that it does this based on the value given to settimeout(),
        # and doesn't need the client to request or acknowledge the close
        # (although your TCP stack might suffer for it: cf Apache's history
        # with FIN_WAIT_2).
        request_line = self.rfile.readline()
        
        # Set started_request to True so communicate() knows to send 408
        # from here on out.
        self.started_request = True
        if not request_line:
            return False
        
        if request_line == CRLF:
            # RFC 2616 sec 4.1: "...if the server is reading the protocol
            # stream at the beginning of a message and receives a CRLF
            # first, it should ignore the CRLF."
            # But only ignore one leading line! else we enable a DoS.
            request_line = self.rfile.readline()
            if not request_line:
                return False
        
        if not request_line.endswith(CRLF):
            self.simple_response("400 Bad Request", "HTTP requires CRLF terminators")
            return False
        
        try:
            method, uri, req_protocol = request_line.strip().split(SPACE, 2)
            # The [x:y] slicing is necessary for byte strings to avoid getting ord's
            rp = int(req_protocol[5:6]), int(req_protocol[7:8])
        except ValueError:
            self.simple_response("400 Bad Request", "Malformed Request-Line")
            return False
        
        self.uri = uri
        self.method = method
        
        # uri may be an abs_path (including "http://host.domain.tld");
        scheme, authority, path = self.parse_request_uri(uri)
        if NUMBER_SIGN in path:
            self.simple_response("400 Bad Request",
                                 "Illegal #fragment in Request-URI.")
            return False
        
        if scheme:
            self.scheme = scheme
        
        qs = EMPTY
        if QUESTION_MARK in path:
            path, qs = path.split(QUESTION_MARK, 1)
        
        # Unquote the path+params (e.g. "/this%20path" -> "/this path").
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.1.2
        #
        # But note that "...a URI must be separated into its components
        # before the escaped characters within those components can be
        # safely decoded." http://www.ietf.org/rfc/rfc2396.txt, sec 2.4.2
        # Therefore, "/this%2Fpath" becomes "/this%2Fpath", not "/this/path".
        try:
            atoms = [self.unquote_bytes(x) for x in quoted_slash.split(path)]
        except ValueError:
            ex = sys.exc_info()[1]
            self.simple_response("400 Bad Request", ex.args[0])
            return False
        path = b"%2F".join(atoms)
        self.path = path
        
        # Note that, like wsgiref and most other HTTP servers,
        # we "% HEX HEX"-unquote the path but not the query string.
        self.qs = qs
        
        # Compare request and server HTTP protocol versions, in case our
        # server does not support the requested protocol. Limit our output
        # to min(req, server). We want the following output:
        #     request    server     actual written   supported response
        #     protocol   protocol  response protocol    feature set
        # a     1.0        1.0           1.0                1.0
        # b     1.0        1.1           1.1                1.0
        # c     1.1        1.0           1.0                1.0
        # d     1.1        1.1           1.1                1.1
        # Notice that, in (b), the response will be "HTTP/1.1" even though
        # the client only understands 1.0. RFC 2616 10.5.6 says we should
        # only return 505 if the _major_ version is different.
        # The [x:y] slicing is necessary for byte strings to avoid getting ord's
        sp = int(self.server.protocol[5:6]), int(self.server.protocol[7:8])
        
        if sp[0] != rp[0]:
            self.simple_response("505 HTTP Version Not Supported")
            return False

        self.request_protocol = req_protocol
        self.response_protocol = "HTTP/%s.%s" % min(rp, sp)
        return True

    def read_request_headers(self):
        """Read self.rfile into self.inheaders. Return success."""
        
        # then all the http headers
        try:
            read_headers(self.rfile, self.inheaders)
        except ValueError:
            ex = sys.exc_info()[1]
            self.simple_response("400 Bad Request", ex.args[0])
            return False
        
        mrbs = self.server.max_request_body_size
        if mrbs and int(self.inheaders.get(b"Content-Length", 0)) > mrbs:
            self.simple_response("413 Request Entity Too Large",
                "The entity sent with the request exceeds the maximum "
                "allowed bytes.")
            return False
        
        # Persistent connection support
        if self.response_protocol == "HTTP/1.1":
            # Both server and client are HTTP/1.1
            if self.inheaders.get(b"Connection", b"") == b"close":
                self.close_connection = True
        else:
            # Either the server or client (or both) are HTTP/1.0
            if self.inheaders.get(b"Connection", b"") != b"Keep-Alive":
                self.close_connection = True
        
        # Transfer-Encoding support
        te = None
        if self.response_protocol == "HTTP/1.1":
            te = self.inheaders.get(b"Transfer-Encoding")
            if te:
                te = [x.strip().lower() for x in te.split(b",") if x.strip()]
        
        self.chunked_read = False
        
        if te:
            for enc in te:
                if enc == b"chunked":
                    self.chunked_read = True
                else:
                    # Note that, even if we see "chunked", we must reject
                    # if there is an extension we don't recognize.
                    self.simple_response("501 Unimplemented")
                    self.close_connection = True
                    return False
        
        # From PEP 333:
        # "Servers and gateways that implement HTTP 1.1 must provide
        # transparent support for HTTP 1.1's "expect/continue" mechanism.
        # This may be done in any of several ways:
        #   1. Respond to requests containing an Expect: 100-continue request
        #      with an immediate "100 Continue" response, and proceed normally.
        #   2. Proceed with the request normally, but provide the application
        #      with a wsgi.input stream that will send the "100 Continue"
        #      response if/when the application first attempts to read from
        #      the input stream. The read request must then remain blocked
        #      until the client responds.
        #   3. Wait until the client decides that the server does not support
        #      expect/continue, and sends the request body on its own.
        #      (This is suboptimal, and is not recommended.)
        #
        # We used to do 3, but are now doing 1. Maybe we'll do 2 someday,
        # but it seems like it would be a big slowdown for such a rare case.
        if self.inheaders.get(b"Expect", b"") == b"100-continue":
            # Don't use simple_response here, because it emits headers
            # we don't want. See http://www.cherrypy.org/ticket/951
            msg = self.server.protocol.encode('ascii') + b" 100 Continue\r\n\r\n"
            try:
                self.conn.wfile.write(msg)
            except socket.error:
                x = sys.exc_info()[1]
                if x.args[0] not in socket_errors_to_ignore:
                    raise
        return True
    
    def parse_request_uri(self, uri):
        """Parse a Request-URI into (scheme, authority, path).
        
        Note that Request-URI's must be one of::
            
            Request-URI    = "*" | absoluteURI | abs_path | authority
        
        Therefore, a Request-URI which starts with a double forward-slash
        cannot be a "net_path"::
        
            net_path      = "//" authority [ abs_path ]
        
        Instead, it must be interpreted as an "abs_path" with an empty first
        path segment::
        
            abs_path      = "/"  path_segments
            path_segments = segment *( "/" segment )
            segment       = *pchar *( ";" param )
            param         = *pchar
        """
        if uri == ASTERISK:
            return None, None, uri

        scheme, sep, remainder = uri.partition(b'://')
        if sep and QUESTION_MARK not in scheme:
            # An absoluteURI.
            # If there's a scheme (and it must be http or https), then:
            # http_URL = "http:" "//" host [ ":" port ] [ abs_path [ "?" query ]]
            authority, path_a, path_b = remainder.partition(FORWARD_SLASH)
            return scheme.lower(), authority, path_a+path_b

        if uri.startswith(FORWARD_SLASH):
            # An abs_path.
            return None, None, uri
        else:
            # An authority.
            return None, uri, None
    
    def unquote_bytes(self, path):
        """takes quoted string and unquotes % encoded values""" 
        res = path.split(b'%')
        
        for i in range(1, len(res)):
            item = res[i]
            try:
                res[i] = bytes([int(item[:2], 16)]) + item[2:]
            except ValueError:
                raise
        return b''.join(res)
    
    def respond(self):
        """Call the gateway and write its iterable output."""
        mrbs = self.server.max_request_body_size
        if self.chunked_read:
            self.rfile = ChunkedRFile(self.conn.rfile, mrbs)
        else:
            cl = int(self.inheaders.get(b"Content-Length", 0))
            if mrbs and mrbs < cl:
                if not self.sent_headers:
                    self.simple_response("413 Request Entity Too Large",
                        "The entity sent with the request exceeds the maximum "
                        "allowed bytes.")
                return
            self.rfile = KnownLengthRFile(self.conn.rfile, cl)
        
        self.server.gateway(self).respond()
        
        if (self.ready and not self.sent_headers):
            self.sent_headers = True
            self.send_headers()
        if self.chunked_write:
            self.conn.wfile.write(b"0\r\n\r\n")
    
    def simple_response(self, status, msg=""):
        """Write a simple response back to the client."""
        status = str(status)
        buf = [bytes(self.server.protocol, "ascii") + SPACE +
               bytes(status, "ISO-8859-1") + CRLF,
               bytes("Content-Length: %s\r\n" % len(msg), "ISO-8859-1"),
               b"Content-Type: text/plain\r\n"]
        
        if status[:3] in ("413", "414"):
            # Request Entity Too Large / Request-URI Too Long
            self.close_connection = True
            if self.response_protocol == 'HTTP/1.1':
                # This will not be true for 414, since read_request_line
                # usually raises 414 before reading the whole line, and we
                # therefore cannot know the proper response_protocol.
                buf.append(b"Connection: close\r\n")
            else:
                # HTTP/1.0 had no 413/414 status nor Connection header.
                # Emit 400 instead and trust the message body is enough.
                status = "400 Bad Request"
        
        buf.append(CRLF)
        if msg:
            if isinstance(msg, unicodestr):
                msg = msg.encode("ISO-8859-1")
            buf.append(msg)
        
        try:
            self.conn.wfile.write(b"".join(buf))
        except socket.error:
            x = sys.exc_info()[1]
            if x.args[0] not in socket_errors_to_ignore:
                raise
    
    def write(self, chunk):
        """Write unbuffered data to the client."""
        if self.chunked_write and chunk:
            buf = [bytes(hex(len(chunk)), 'ASCII')[2:], CRLF, chunk, CRLF]
            self.conn.wfile.write(EMPTY.join(buf))
        else:
            self.conn.wfile.write(chunk)
    
    def send_headers(self):
        """Assert, process, and send the HTTP response message-headers.
        
        You must set self.status, and self.outheaders before calling this.
        """
        hkeys = [key.lower() for key, value in self.outheaders]
        status = int(self.status[:3])
        
        if status == 413:
            # Request Entity Too Large. Close conn to avoid garbage.
            self.close_connection = True
        elif b"content-length" not in hkeys:
            # "All 1xx (informational), 204 (no content),
            # and 304 (not modified) responses MUST NOT
            # include a message-body." So no point chunking.
            if status < 200 or status in (204, 205, 304):
                pass
            else:
                if (self.response_protocol == 'HTTP/1.1'
                    and self.method != b'HEAD'):
                    # Use the chunked transfer-coding
                    self.chunked_write = True
                    self.outheaders.append((b"Transfer-Encoding", b"chunked"))
                else:
                    # Closing the conn is the only way to determine len.
                    self.close_connection = True
        
        if b"connection" not in hkeys:
            if self.response_protocol == 'HTTP/1.1':
                # Both server and client are HTTP/1.1 or better
                if self.close_connection:
                    self.outheaders.append((b"Connection", b"close"))
            else:
                # Server and/or client are HTTP/1.0
                if not self.close_connection:
                    self.outheaders.append((b"Connection", b"Keep-Alive"))
        
        if (not self.close_connection) and (not self.chunked_read):
            # Read any remaining request body data on the socket.
            # "If an origin server receives a request that does not include an
            # Expect request-header field with the "100-continue" expectation,
            # the request includes a request body, and the server responds
            # with a final status code before reading the entire request body
            # from the transport connection, then the server SHOULD NOT close
            # the transport connection until it has read the entire request,
            # or until the client closes the connection. Otherwise, the client
            # might not reliably receive the response message. However, this
            # requirement is not be construed as preventing a server from
            # defending itself against denial-of-service attacks, or from
            # badly broken client implementations."
            remaining = getattr(self.rfile, 'remaining', 0)
            if remaining > 0:
                self.rfile.read(remaining)
        
        if b"date" not in hkeys:
            self.outheaders.append(
                (b"Date", email.utils.formatdate(usegmt=True).encode('ISO-8859-1')))
        
        if b"server" not in hkeys:
            self.outheaders.append(
                (b"Server", self.server.server_name.encode('ISO-8859-1')))
        
        buf = [self.server.protocol.encode('ascii') + SPACE + self.status + CRLF]
        for k, v in self.outheaders:
            buf.append(k + COLON + SPACE + v + CRLF)
        buf.append(CRLF)
        self.conn.wfile.write(EMPTY.join(buf))


class NoSSLError(Exception):
    """Exception raised when a client speaks HTTP to an HTTPS socket."""
    pass


class FatalSSLAlert(Exception):
    """Exception raised when the SSL implementation signals a fatal alert."""
    pass


class CP_BufferedWriter(io.BufferedWriter):
    """Faux file object attached to a socket object."""

    def write(self, b):
        self._checkClosed()
        if isinstance(b, str):
            raise TypeError("can't write str to binary stream")
        
        with self._write_lock:
            self._write_buf.extend(b)
            self._flush_unlocked()
            return len(b)
    
    def _flush_unlocked(self):
        self._checkClosed("flush of closed file")
        while self._write_buf:
            try:
                # ssl sockets only except 'bytes', not bytearrays
                # so perhaps we should conditionally wrap this for perf?
                n = self.raw.write(bytes(self._write_buf))
            except io.BlockingIOError as e:
                n = e.characters_written
            del self._write_buf[:n]


def CP_makefile(sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
    if 'r' in mode:
        return io.BufferedReader(socket.SocketIO(sock, mode), bufsize)
    else:
        return CP_BufferedWriter(socket.SocketIO(sock, mode), bufsize)

class HTTPConnection(object):
    """An HTTP connection (active socket).
    
    server: the Server object which received this connection.
    socket: the raw socket object (usually TCP) for this connection.
    makefile: a fileobject class for reading from the socket.
    """
    
    remote_addr = None
    remote_port = None
    ssl_env = None
    rbufsize = DEFAULT_BUFFER_SIZE
    wbufsize = DEFAULT_BUFFER_SIZE
    RequestHandlerClass = HTTPRequest
    
    def __init__(self, server, sock, makefile=CP_makefile):
        self.server = server
        self.socket = sock
        self.rfile = makefile(sock, "rb", self.rbufsize)
        self.wfile = makefile(sock, "wb", self.wbufsize)
        self.requests_seen = 0
    
    def communicate(self):
        """Read each request and respond appropriately."""
        request_seen = False
        try:
            while True:
                # (re)set req to None so that if something goes wrong in
                # the RequestHandlerClass constructor, the error doesn't
                # get written to the previous request.
                req = None
                req = self.RequestHandlerClass(self.server, self)
                
                # This order of operations should guarantee correct pipelining.
                req.parse_request()
                if self.server.stats['Enabled']:
                    self.requests_seen += 1
                if not req.ready:
                    # Something went wrong in the parsing (and the server has
                    # probably already made a simple_response). Return and
                    # let the conn close.
                    return
                
                request_seen = True
                req.respond()
                if req.close_connection:
                    return
        except socket.error:
            e = sys.exc_info()[1]
            errnum = e.args[0]
            # sadly SSL sockets return a different (longer) time out string
            if errnum == 'timed out' or errnum == 'The read operation timed out':
                # Don't error if we're between requests; only error
                # if 1) no request has been started at all, or 2) we're
                # in the middle of a request.
                # See http://www.cherrypy.org/ticket/853
                if (not request_seen) or (req and req.started_request):
                    # Don't bother writing the 408 if the response
                    # has already started being written.
                    if req and not req.sent_headers:
                        try:
                            req.simple_response("408 Request Timeout")
                        except FatalSSLAlert:
                            # Close the connection.
                            return
            elif errnum not in socket_errors_to_ignore:
                self.server.error_log("socket.error %s" % repr(errnum),
                                      level=logging.WARNING, traceback=True)
                if req and not req.sent_headers:
                    try:
                        req.simple_response("500 Internal Server Error")
                    except FatalSSLAlert:
                        # Close the connection.
                        return
            return
        except (KeyboardInterrupt, SystemExit):
            raise
        except FatalSSLAlert:
            # Close the connection.
            return
        except NoSSLError:
            if req and not req.sent_headers:
                # Unwrap our wfile
                self.wfile = CP_makefile(self.socket._sock, "wb", self.wbufsize)
                req.simple_response("400 Bad Request",
                    "The client sent a plain HTTP request, but "
                    "this server only speaks HTTPS on this port.")
                self.linger = True
        except Exception:
            e = sys.exc_info()[1]
            self.server.error_log(repr(e), level=logging.ERROR, traceback=True)
            if req and not req.sent_headers:
                try:
                    req.simple_response("500 Internal Server Error")
                except FatalSSLAlert:
                    # Close the connection.
                    return
    
    linger = False
    
    def close(self):
        """Close the socket underlying this connection."""
        self.rfile.close()
        
        if not self.linger:
            # Python's socket module does NOT call close on the kernel socket
            # when you call socket.close(). We do so manually here because we
            # want this server to send a FIN TCP segment immediately. Note this
            # must be called *before* calling socket.close(), because the latter
            # drops its reference to the kernel socket.
            # Python 3 *probably* fixed this with socket._real_close; hard to tell.
##            self.socket._sock.close()
            self.socket.close()
        else:
            # On the other hand, sometimes we want to hang around for a bit
            # to make sure the client has a chance to read our entire
            # response. Skipping the close() calls here delays the FIN
            # packet until the socket object is garbage-collected later.
            # Someday, perhaps, we'll do the full lingering_close that
            # Apache does, but not today.
            pass


class TrueyZero(object):
    """An object which equals and does math like the integer '0' but evals True."""
    def __add__(self, other):
        return other
    def __radd__(self, other):
        return other
trueyzero = TrueyZero()


_SHUTDOWNREQUEST = None

class WorkerThread(threading.Thread):
    """Thread which continuously polls a Queue for Connection objects.
    
    Due to the timing issues of polling a Queue, a WorkerThread does not
    check its own 'ready' flag after it has started. To stop the thread,
    it is necessary to stick a _SHUTDOWNREQUEST object onto the Queue
    (one for each running WorkerThread).
    """
    
    conn = None
    """The current connection pulled off the Queue, or None."""
    
    server = None
    """The HTTP Server which spawned this thread, and which owns the
    Queue and is placing active connections into it."""
    
    ready = False
    """A simple flag for the calling server to know when this thread
    has begun polling the Queue."""
    
    
    def __init__(self, server):
        self.ready = False
        self.server = server
        
        self.requests_seen = 0
        self.bytes_read = 0
        self.bytes_written = 0
        self.start_time = None
        self.work_time = 0
        self.stats = {
            'Requests': lambda s: self.requests_seen + ((self.start_time is None) and trueyzero or self.conn.requests_seen),
            'Bytes Read': lambda s: self.bytes_read + ((self.start_time is None) and trueyzero or self.conn.rfile.bytes_read),
            'Bytes Written': lambda s: self.bytes_written + ((self.start_time is None) and trueyzero or self.conn.wfile.bytes_written),
            'Work Time': lambda s: self.work_time + ((self.start_time is None) and trueyzero or time.time() - self.start_time),
            'Read Throughput': lambda s: s['Bytes Read'](s) / (s['Work Time'](s) or 1e-6),
            'Write Throughput': lambda s: s['Bytes Written'](s) / (s['Work Time'](s) or 1e-6),
        }
        threading.Thread.__init__(self)
    
    def run(self):
        self.server.stats['Worker Threads'][self.getName()] = self.stats
        try:
            self.ready = True
            while True:
                conn = self.server.requests.get()
                if conn is _SHUTDOWNREQUEST:
                    return
                
                self.conn = conn
                if self.server.stats['Enabled']:
                    self.start_time = time.time()
                try:
                    conn.communicate()
                finally:
                    conn.close()
                    if self.server.stats['Enabled']:
                        self.requests_seen += self.conn.requests_seen
                        self.bytes_read += self.conn.rfile.bytes_read
                        self.bytes_written += self.conn.wfile.bytes_written
                        self.work_time += time.time() - self.start_time
                        self.start_time = None
                    self.conn = None
        except (KeyboardInterrupt, SystemExit):
            exc = sys.exc_info()[1]
            self.server.interrupt = exc


class ThreadPool(object):
    """A Request Queue for an HTTPServer which pools threads.
    
    ThreadPool objects must provide min, get(), put(obj), start()
    and stop(timeout) attributes.
    """
    
    def __init__(self, server, min=10, max=-1):
        self.server = server
        self.min = min
        self.max = max
        self._threads = []
        self._queue = queue.Queue()
        self.get = self._queue.get
    
    def start(self):
        """Start the pool of threads."""
        for i in range(self.min):
            self._threads.append(WorkerThread(self.server))
        for worker in self._threads:
            worker.setName("CP Server " + worker.getName())
            worker.start()
        for worker in self._threads:
            while not worker.ready:
                time.sleep(.1)
    
    def _get_idle(self):
        """Number of worker threads which are idle. Read-only."""
        return len([t for t in self._threads if t.conn is None])
    idle = property(_get_idle, doc=_get_idle.__doc__)
    
    def put(self, obj):
        self._queue.put(obj)
        if obj is _SHUTDOWNREQUEST:
            return
    
    def grow(self, amount):
        """Spawn new worker threads (not above self.max)."""
        for i in range(amount):
            if self.max > 0 and len(self._threads) >= self.max:
                break
            worker = WorkerThread(self.server)
            worker.setName("CP Server " + worker.getName())
            self._threads.append(worker)
            worker.start()
    
    def shrink(self, amount):
        """Kill off worker threads (not below self.min)."""
        # Grow/shrink the pool if necessary.
        # Remove any dead threads from our list
        for t in self._threads:
            if not t.isAlive():
                self._threads.remove(t)
                amount -= 1
        
        if amount > 0:
            for i in range(min(amount, len(self._threads) - self.min)):
                # Put a number of shutdown requests on the queue equal
                # to 'amount'. Once each of those is processed by a worker,
                # that worker will terminate and be culled from our list
                # in self.put.
                self._queue.put(_SHUTDOWNREQUEST)
    
    def stop(self, timeout=5):
        # Must shut down threads here so the code that calls
        # this method can know when all threads are stopped.
        for worker in self._threads:
            self._queue.put(_SHUTDOWNREQUEST)
        
        # Don't join currentThread (when stop is called inside a request).
        current = threading.currentThread()
        if timeout and timeout >= 0:
            endtime = time.time() + timeout
        while self._threads:
            worker = self._threads.pop()
            if worker is not current and worker.isAlive():
                try:
                    if timeout is None or timeout < 0:
                        worker.join()
                    else:
                        remaining_time = endtime - time.time()
                        if remaining_time > 0:
                            worker.join(remaining_time)
                        if worker.isAlive():
                            # We exhausted the timeout.
                            # Forcibly shut down the socket.
                            c = worker.conn
                            if c and not c.rfile.closed:
                                try:
                                    c.socket.shutdown(socket.SHUT_RD)
                                except TypeError:
                                    # pyOpenSSL sockets don't take an arg
                                    c.socket.shutdown()
                            worker.join()
                except (AssertionError,
                        # Ignore repeated Ctrl-C.
                        # See http://www.cherrypy.org/ticket/691.
                        KeyboardInterrupt):
                    pass
    
    def _get_qsize(self):
        return self._queue.qsize()
    qsize = property(_get_qsize)



try:
    import fcntl
except ImportError:
    try:
        from ctypes import windll, WinError
    except ImportError:
        def prevent_socket_inheritance(sock):
            """Dummy function, since neither fcntl nor ctypes are available."""
            pass
    else:
        def prevent_socket_inheritance(sock):
            """Mark the given socket fd as non-inheritable (Windows)."""
            if not windll.kernel32.SetHandleInformation(sock.fileno(), 1, 0):
                raise WinError()
else:
    def prevent_socket_inheritance(sock):
        """Mark the given socket fd as non-inheritable (POSIX)."""
        fd = sock.fileno()
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        fcntl.fcntl(fd, fcntl.F_SETFD, old_flags | fcntl.FD_CLOEXEC)


class SSLAdapter(object):
    """Base class for SSL driver library adapters.
    
    Required methods:
    
        * ``wrap(sock) -> (wrapped socket, ssl environ dict)``
        * ``makefile(sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE) -> socket file object``
    """
    
    def __init__(self, certificate, private_key, certificate_chain=None):
        self.certificate = certificate
        self.private_key = private_key
        self.certificate_chain = certificate_chain
    
    def wrap(self, sock):
        raise NotImplemented
    
    def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
        raise NotImplemented


class HTTPServer(object):
    """An HTTP server."""
    
    _bind_addr = "127.0.0.1"
    _interrupt = None
    
    gateway = None
    """A Gateway instance."""
    
    minthreads = None
    """The minimum number of worker threads to create (default 10)."""
    
    maxthreads = None
    """The maximum number of worker threads to create (default -1 = no limit)."""
    
    server_name = None
    """The name of the server; defaults to socket.gethostname()."""
    
    protocol = "HTTP/1.1"
    """The version string to write in the Status-Line of all HTTP responses.
    
    For example, "HTTP/1.1" is the default. This also limits the supported
    features used in the response."""
    
    request_queue_size = 5
    """The 'backlog' arg to socket.listen(); max queued connections (default 5)."""
    
    shutdown_timeout = 5
    """The total time, in seconds, to wait for worker threads to cleanly exit."""
    
    timeout = 10
    """The timeout in seconds for accepted connections (default 10)."""
    
    version = "CherryPy/3.2.2"
    """A version string for the HTTPServer."""
    
    software = None
    """The value to set for the SERVER_SOFTWARE entry in the WSGI environ.
    
    If None, this defaults to ``'%s Server' % self.version``."""
    
    ready = False
    """An internal flag which marks whether the socket is accepting connections."""
    
    max_request_header_size = 0
    """The maximum size, in bytes, for request headers, or 0 for no limit."""
    
    max_request_body_size = 0
    """The maximum size, in bytes, for request bodies, or 0 for no limit."""
    
    nodelay = True
    """If True (the default since 3.1), sets the TCP_NODELAY socket option."""
    
    ConnectionClass = HTTPConnection
    """The class to use for handling HTTP connections."""
    
    ssl_adapter = None
    """An instance of SSLAdapter (or a subclass).
    
    You must have the corresponding SSL driver library installed."""
    
    def __init__(self, bind_addr, gateway, minthreads=10, maxthreads=-1,
                 server_name=None):
        self.bind_addr = bind_addr
        self.gateway = gateway
        
        self.requests = ThreadPool(self, min=minthreads or 1, max=maxthreads)
        
        if not server_name:
            server_name = socket.gethostname()
        self.server_name = server_name
        self.clear_stats()
    
    def clear_stats(self):
        self._start_time = None
        self._run_time = 0
        self.stats = {
            'Enabled': False,
            'Bind Address': lambda s: repr(self.bind_addr),
            'Run time': lambda s: (not s['Enabled']) and -1 or self.runtime(),
            'Accepts': 0,
            'Accepts/sec': lambda s: s['Accepts'] / self.runtime(),
            'Queue': lambda s: getattr(self.requests, "qsize", None),
            'Threads': lambda s: len(getattr(self.requests, "_threads", [])),
            'Threads Idle': lambda s: getattr(self.requests, "idle", None),
            'Socket Errors': 0,
            'Requests': lambda s: (not s['Enabled']) and -1 or sum([w['Requests'](w) for w
                                       in s['Worker Threads'].values()], 0),
            'Bytes Read': lambda s: (not s['Enabled']) and -1 or sum([w['Bytes Read'](w) for w
                                         in s['Worker Threads'].values()], 0),
            'Bytes Written': lambda s: (not s['Enabled']) and -1 or sum([w['Bytes Written'](w) for w
                                            in s['Worker Threads'].values()], 0),
            'Work Time': lambda s: (not s['Enabled']) and -1 or sum([w['Work Time'](w) for w
                                         in s['Worker Threads'].values()], 0),
            'Read Throughput': lambda s: (not s['Enabled']) and -1 or sum(
                [w['Bytes Read'](w) / (w['Work Time'](w) or 1e-6)
                 for w in s['Worker Threads'].values()], 0),
            'Write Throughput': lambda s: (not s['Enabled']) and -1 or sum(
                [w['Bytes Written'](w) / (w['Work Time'](w) or 1e-6)
                 for w in s['Worker Threads'].values()], 0),
            'Worker Threads': {},
            }
        logging.statistics["CherryPy HTTPServer %d" % id(self)] = self.stats
    
    def runtime(self):
        if self._start_time is None:
            return self._run_time
        else:
            return self._run_time + (time.time() - self._start_time)
    
    def __str__(self):
        return "%s.%s(%r)" % (self.__module__, self.__class__.__name__,
                              self.bind_addr)
    
    def _get_bind_addr(self):
        return self._bind_addr
    def _set_bind_addr(self, value):
        if isinstance(value, tuple) and value[0] in ('', None):
            # Despite the socket module docs, using '' does not
            # allow AI_PASSIVE to work. Passing None instead
            # returns '0.0.0.0' like we want. In other words:
            #     host    AI_PASSIVE     result
            #      ''         Y         192.168.x.y
            #      ''         N         192.168.x.y
            #     None        Y         0.0.0.0
            #     None        N         127.0.0.1
            # But since you can get the same effect with an explicit
            # '0.0.0.0', we deny both the empty string and None as values.
            raise ValueError("Host values of '' or None are not allowed. "
                             "Use '0.0.0.0' (IPv4) or '::' (IPv6) instead "
                             "to listen on all active interfaces.")
        self._bind_addr = value
    bind_addr = property(_get_bind_addr, _set_bind_addr,
        doc="""The interface on which to listen for connections.
        
        For TCP sockets, a (host, port) tuple. Host values may be any IPv4
        or IPv6 address, or any valid hostname. The string 'localhost' is a
        synonym for '127.0.0.1' (or '::1', if your hosts file prefers IPv6).
        The string '0.0.0.0' is a special IPv4 entry meaning "any active
        interface" (INADDR_ANY), and '::' is the similar IN6ADDR_ANY for
        IPv6. The empty string or None are not allowed.
        
        For UNIX sockets, supply the filename as a string.""")
    
    def start(self):
        """Run the server forever."""
        # We don't have to trap KeyboardInterrupt or SystemExit here,
        # because cherrpy.server already does so, calling self.stop() for us.
        # If you're using this server with another framework, you should
        # trap those exceptions in whatever code block calls start().
        self._interrupt = None
        
        if self.software is None:
            self.software = "%s Server" % self.version
        
        # Select the appropriate socket
        if isinstance(self.bind_addr, basestring):
            # AF_UNIX socket
            
            # So we can reuse the socket...
            try: os.unlink(self.bind_addr)
            except: pass
            
            # So everyone can access the socket...
            try: os.chmod(self.bind_addr, 511) # 0777
            except: pass
            
            info = [(socket.AF_UNIX, socket.SOCK_STREAM, 0, "", self.bind_addr)]
        else:
            # AF_INET or AF_INET6 socket
            # Get the correct address family for our host (allows IPv6 addresses)
            host, port = self.bind_addr
            try:
                info = socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
            except socket.gaierror:
                if ':' in self.bind_addr[0]:
                    info = [(socket.AF_INET6, socket.SOCK_STREAM,
                             0, "", self.bind_addr + (0, 0))]
                else:
                    info = [(socket.AF_INET, socket.SOCK_STREAM,
                             0, "", self.bind_addr)]
        
        self.socket = None
        msg = "No socket could be created"
        for res in info:
            af, socktype, proto, canonname, sa = res
            try:
                self.bind(af, socktype, proto)
            except socket.error:
                if self.socket:
                    self.socket.close()
                self.socket = None
                continue
            break
        if not self.socket:
            raise socket.error(msg)
        
        # Timeout so KeyboardInterrupt can be caught on Win32
        self.socket.settimeout(1)
        self.socket.listen(self.request_queue_size)
        
        # Create worker threads
        self.requests.start()
        
        self.ready = True
        self._start_time = time.time()
        while self.ready:
            try:
                self.tick()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.error_log("Error in HTTPServer.tick", level=logging.ERROR,
                               traceback=True)
            if self.interrupt:
                while self.interrupt is True:
                    # Wait for self.stop() to complete. See _set_interrupt.
                    time.sleep(0.1)
                if self.interrupt:
                    raise self.interrupt

    def error_log(self, msg="", level=20, traceback=False):
        # Override this in subclasses as desired
        sys.stderr.write(msg + '\n')
        sys.stderr.flush()
        if traceback:
            tblines = format_exc()
            sys.stderr.write(tblines)
            sys.stderr.flush()

    def bind(self, family, type, proto=0):
        """Create (or recreate) the actual socket object."""
        self.socket = socket.socket(family, type, proto)
        prevent_socket_inheritance(self.socket)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.nodelay and not isinstance(self.bind_addr, str):
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        if self.ssl_adapter is not None:
            self.socket = self.ssl_adapter.bind(self.socket)
        
        # If listening on the IPV6 any address ('::' = IN6ADDR_ANY),
        # activate dual-stack. See http://www.cherrypy.org/ticket/871.
        if (hasattr(socket, 'AF_INET6') and family == socket.AF_INET6
            and self.bind_addr[0] in ('::', '::0', '::0.0.0.0')):
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except (AttributeError, socket.error):
                # Apparently, the socket option is not available in
                # this machine's TCP stack
                pass
        
        self.socket.bind(self.bind_addr)
    
    def tick(self):
        """Accept a new connection and put it on the Queue."""
        try:
            s, addr = self.socket.accept()
            if self.stats['Enabled']:
                self.stats['Accepts'] += 1
            if not self.ready:
                return
            
            prevent_socket_inheritance(s)
            if hasattr(s, 'settimeout'):
                s.settimeout(self.timeout)
            
            makefile = CP_makefile
            ssl_env = {}
            # if ssl cert and key are set, we try to be a secure HTTP server
            if self.ssl_adapter is not None:
                try:
                    s, ssl_env = self.ssl_adapter.wrap(s)
                except NoSSLError:
                    msg = ("The client sent a plain HTTP request, but "
                           "this server only speaks HTTPS on this port.")
                    buf = ["%s 400 Bad Request\r\n" % self.protocol,
                           "Content-Length: %s\r\n" % len(msg),
                           "Content-Type: text/plain\r\n\r\n",
                           msg]
                    
                    wfile = makefile(s, "wb", DEFAULT_BUFFER_SIZE)
                    try:
                        wfile.write("".join(buf).encode('ISO-8859-1'))
                    except socket.error:
                        x = sys.exc_info()[1]
                        if x.args[0] not in socket_errors_to_ignore:
                            raise
                    return
                if not s:
                    return
                makefile = self.ssl_adapter.makefile
                # Re-apply our timeout since we may have a new socket object
                if hasattr(s, 'settimeout'):
                    s.settimeout(self.timeout)
            
            conn = self.ConnectionClass(self, s, makefile)
            
            if not isinstance(self.bind_addr, basestring):
                # optional values
                # Until we do DNS lookups, omit REMOTE_HOST
                if addr is None: # sometimes this can happen
                    # figure out if AF_INET or AF_INET6.
                    if len(s.getsockname()) == 2:
                        # AF_INET
                        addr = ('0.0.0.0', 0)
                    else:
                        # AF_INET6
                        addr = ('::', 0)
                conn.remote_addr = addr[0]
                conn.remote_port = addr[1]
            
            conn.ssl_env = ssl_env
            
            self.requests.put(conn)
        except socket.timeout:
            # The only reason for the timeout in start() is so we can
            # notice keyboard interrupts on Win32, which don't interrupt
            # accept() by default
            return
        except socket.error:
            x = sys.exc_info()[1]
            if self.stats['Enabled']:
                self.stats['Socket Errors'] += 1
            if x.args[0] in socket_error_eintr:
                # I *think* this is right. EINTR should occur when a signal
                # is received during the accept() call; all docs say retry
                # the call, and I *think* I'm reading it right that Python
                # will then go ahead and poll for and handle the signal
                # elsewhere. See http://www.cherrypy.org/ticket/707.
                return
            if x.args[0] in socket_errors_nonblocking:
                # Just try again. See http://www.cherrypy.org/ticket/479.
                return
            if x.args[0] in socket_errors_to_ignore:
                # Our socket was closed.
                # See http://www.cherrypy.org/ticket/686.
                return
            raise
    
    def _get_interrupt(self):
        return self._interrupt
    def _set_interrupt(self, interrupt):
        self._interrupt = True
        self.stop()
        self._interrupt = interrupt
    interrupt = property(_get_interrupt, _set_interrupt,
                         doc="Set this to an Exception instance to "
                             "interrupt the server.")
    
    def stop(self):
        """Gracefully shutdown a server that is serving forever."""
        self.ready = False
        if self._start_time is not None:
            self._run_time += (time.time() - self._start_time)
        self._start_time = None
        
        sock = getattr(self, "socket", None)
        if sock:
            if not isinstance(self.bind_addr, basestring):
                # Touch our own socket to make accept() return immediately.
                try:
                    host, port = sock.getsockname()[:2]
                except socket.error:
                    x = sys.exc_info()[1]
                    if x.args[0] not in socket_errors_to_ignore:
                        # Changed to use error code and not message
                        # See http://www.cherrypy.org/ticket/860.
                        raise
                else:
                    # Note that we're explicitly NOT using AI_PASSIVE,
                    # here, because we want an actual IP to touch.
                    # localhost won't work if we've bound to a public IP,
                    # but it will if we bound to '0.0.0.0' (INADDR_ANY).
                    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                                  socket.SOCK_STREAM):
                        af, socktype, proto, canonname, sa = res
                        s = None
                        try:
                            s = socket.socket(af, socktype, proto)
                            # See http://groups.google.com/group/cherrypy-users/
                            #        browse_frm/thread/bbfe5eb39c904fe0
                            s.settimeout(1.0)
                            s.connect((host, port))
                            s.close()
                        except socket.error:
                            if s:
                                s.close()
            if hasattr(sock, "close"):
                sock.close()
            self.socket = None
        
        self.requests.stop(self.shutdown_timeout)


class Gateway(object):
    """A base class to interface HTTPServer with other systems, such as WSGI."""
    
    def __init__(self, req):
        self.req = req
    
    def respond(self):
        """Process the current request. Must be overridden in a subclass."""
        raise NotImplemented


# These may either be wsgiserver.SSLAdapter subclasses or the string names
# of such classes (in which case they will be lazily loaded).
ssl_adapters = {
    'builtin': 'cherrypy.wsgiserver.ssl_builtin.BuiltinSSLAdapter',
    }

def get_ssl_adapter_class(name='builtin'):
    """Return an SSL adapter class for the given name."""
    adapter = ssl_adapters[name.lower()]
    if isinstance(adapter, basestring):
        last_dot = adapter.rfind(".")
        attr_name = adapter[last_dot + 1:]
        mod_path = adapter[:last_dot]
        
        try:
            mod = sys.modules[mod_path]
            if mod is None:
                raise KeyError()
        except KeyError:
            # The last [''] is important.
            mod = __import__(mod_path, globals(), locals(), [''])
        
        # Let an AttributeError propagate outward.
        try:
            adapter = getattr(mod, attr_name)
        except AttributeError:
            raise AttributeError("'%s' object has no attribute '%s'"
                                 % (mod_path, attr_name))
    
    return adapter

# -------------------------------- WSGI Stuff -------------------------------- #


class CherryPyWSGIServer(HTTPServer):
    """A subclass of HTTPServer which calls a WSGI application."""
    
    wsgi_version = (1, 0)
    """The version of WSGI to produce."""
    
    def __init__(self, bind_addr, wsgi_app, numthreads=10, server_name=None,
                 max=-1, request_queue_size=5, timeout=10, shutdown_timeout=5):
        self.requests = ThreadPool(self, min=numthreads or 1, max=max)
        self.wsgi_app = wsgi_app
        self.gateway = wsgi_gateways[self.wsgi_version]
        
        self.bind_addr = bind_addr
        if not server_name:
            server_name = socket.gethostname()
        self.server_name = server_name
        self.request_queue_size = request_queue_size
        
        self.timeout = timeout
        self.shutdown_timeout = shutdown_timeout
        self.clear_stats()
    
    def _get_numthreads(self):
        return self.requests.min
    def _set_numthreads(self, value):
        self.requests.min = value
    numthreads = property(_get_numthreads, _set_numthreads)


class WSGIGateway(Gateway):
    """A base class to interface HTTPServer with WSGI."""
    
    def __init__(self, req):
        self.req = req
        self.started_response = False
        self.env = self.get_environ()
        self.remaining_bytes_out = None
    
    def get_environ(self):
        """Return a new environ dict targeting the given wsgi.version"""
        raise NotImplemented
    
    def respond(self):
        """Process the current request."""
        response = self.req.server.wsgi_app(self.env, self.start_response)
        try:
            for chunk in response:
                # "The start_response callable must not actually transmit
                # the response headers. Instead, it must store them for the
                # server or gateway to transmit only after the first
                # iteration of the application return value that yields
                # a NON-EMPTY string, or upon the application's first
                # invocation of the write() callable." (PEP 333)
                if chunk:
                    if isinstance(chunk, unicodestr):
                        chunk = chunk.encode('ISO-8859-1')
                    self.write(chunk)
        finally:
            if hasattr(response, "close"):
                response.close()
    
    def start_response(self, status, headers, exc_info = None):
        """WSGI callable to begin the HTTP response."""
        # "The application may call start_response more than once,
        # if and only if the exc_info argument is provided."
        if self.started_response and not exc_info:
            raise AssertionError("WSGI start_response called a second "
                                 "time with no exc_info.")
        self.started_response = True
        
        # "if exc_info is provided, and the HTTP headers have already been
        # sent, start_response must raise an error, and should raise the
        # exc_info tuple."
        if self.req.sent_headers:
            try:
                raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
            finally:
                exc_info = None

        # According to PEP 3333, when using Python 3, the response status
        # and headers must be bytes masquerading as unicode; that is, they
        # must be of type "str" but are restricted to code points in the
        # "latin-1" set.
        if not isinstance(status, str):
            raise TypeError("WSGI response status is not of type str.")
        self.req.status = status.encode('ISO-8859-1')

        for k, v in headers:
            if not isinstance(k, str):
                raise TypeError("WSGI response header key %r is not of type str." % k)
            if not isinstance(v, str):
                raise TypeError("WSGI response header value %r is not of type str." % v)
            if k.lower() == 'content-length':
                self.remaining_bytes_out = int(v)
            self.req.outheaders.append((k.encode('ISO-8859-1'), v.encode('ISO-8859-1')))
        
        return self.write
    
    def write(self, chunk):
        """WSGI callable to write unbuffered data to the client.
        
        This method is also used internally by start_response (to write
        data from the iterable returned by the WSGI application).
        """
        if not self.started_response:
            raise AssertionError("WSGI write called before start_response.")
        
        chunklen = len(chunk)
        rbo = self.remaining_bytes_out
        if rbo is not None and chunklen > rbo:
            if not self.req.sent_headers:
                # Whew. We can send a 500 to the client.
                self.req.simple_response("500 Internal Server Error",
                    "The requested resource returned more bytes than the "
                    "declared Content-Length.")
            else:
                # Dang. We have probably already sent data. Truncate the chunk
                # to fit (so the client doesn't hang) and raise an error later.
                chunk = chunk[:rbo]
        
        if not self.req.sent_headers:
            self.req.sent_headers = True
            self.req.send_headers()
        
        self.req.write(chunk)
        
        if rbo is not None:
            rbo -= chunklen
            if rbo < 0:
                raise ValueError(
                    "Response body exceeds the declared Content-Length.")


class WSGIGateway_10(WSGIGateway):
    """A Gateway class to interface HTTPServer with WSGI 1.0.x."""
    
    def get_environ(self):
        """Return a new environ dict targeting the given wsgi.version"""
        req = self.req
        env = {
            # set a non-standard environ entry so the WSGI app can know what
            # the *real* server protocol is (and what features to support).
            # See http://www.faqs.org/rfcs/rfc2145.html.
            'ACTUAL_SERVER_PROTOCOL': req.server.protocol,
            'PATH_INFO': req.path.decode('ISO-8859-1'),
            'QUERY_STRING': req.qs.decode('ISO-8859-1'),
            'REMOTE_ADDR': req.conn.remote_addr or '',
            'REMOTE_PORT': str(req.conn.remote_port or ''),
            'REQUEST_METHOD': req.method.decode('ISO-8859-1'),
            'REQUEST_URI': req.uri,
            'SCRIPT_NAME': '',
            'SERVER_NAME': req.server.server_name,
            # Bah. "SERVER_PROTOCOL" is actually the REQUEST protocol.
            'SERVER_PROTOCOL': req.request_protocol.decode('ISO-8859-1'),
            'SERVER_SOFTWARE': req.server.software,
            'wsgi.errors': sys.stderr,
            'wsgi.input': req.rfile,
            'wsgi.multiprocess': False,
            'wsgi.multithread': True,
            'wsgi.run_once': False,
            'wsgi.url_scheme': req.scheme.decode('ISO-8859-1'),
            'wsgi.version': (1, 0),
            }
        
        if isinstance(req.server.bind_addr, basestring):
            # AF_UNIX. This isn't really allowed by WSGI, which doesn't
            # address unix domain sockets. But it's better than nothing.
            env["SERVER_PORT"] = ""
        else:
            env["SERVER_PORT"] = str(req.server.bind_addr[1])
        
        # Request headers
        for k, v in req.inheaders.items():
            k = k.decode('ISO-8859-1').upper().replace("-", "_")
            env["HTTP_" + k] = v.decode('ISO-8859-1')
        
        # CONTENT_TYPE/CONTENT_LENGTH
        ct = env.pop("HTTP_CONTENT_TYPE", None)
        if ct is not None:
            env["CONTENT_TYPE"] = ct
        cl = env.pop("HTTP_CONTENT_LENGTH", None)
        if cl is not None:
            env["CONTENT_LENGTH"] = cl
        
        if req.conn.ssl_env:
            env.update(req.conn.ssl_env)
        
        return env


class WSGIGateway_u0(WSGIGateway_10):
    """A Gateway class to interface HTTPServer with WSGI u.0.
    
    WSGI u.0 is an experimental protocol, which uses unicode for keys and values
    in both Python 2 and Python 3.
    """
    
    def get_environ(self):
        """Return a new environ dict targeting the given wsgi.version"""
        req = self.req
        env_10 = WSGIGateway_10.get_environ(self)
        env = env_10.copy()
        env['wsgi.version'] = ('u', 0)
        
        # Request-URI
        env.setdefault('wsgi.url_encoding', 'utf-8')
        try:
            # SCRIPT_NAME is the empty string, who cares what encoding it is?
            env["PATH_INFO"] = req.path.decode(env['wsgi.url_encoding'])
            env["QUERY_STRING"] = req.qs.decode(env['wsgi.url_encoding'])
        except UnicodeDecodeError:
            # Fall back to latin 1 so apps can transcode if needed.
            env['wsgi.url_encoding'] = 'ISO-8859-1'
            env["PATH_INFO"] = env_10["PATH_INFO"]
            env["QUERY_STRING"] = env_10["QUERY_STRING"]
        
        return env

wsgi_gateways = {
    (1, 0): WSGIGateway_10,
    ('u', 0): WSGIGateway_u0,
}

class WSGIPathInfoDispatcher(object):
    """A WSGI dispatcher for dispatch based on the PATH_INFO.
    
    apps: a dict or list of (path_prefix, app) pairs.
    """
    
    def __init__(self, apps):
        try:
            apps = list(apps.items())
        except AttributeError:
            pass
        
        # Sort the apps by len(path), descending
        apps.sort()
        apps.reverse()
        
        # The path_prefix strings must start, but not end, with a slash.
        # Use "" instead of "/".
        self.apps = [(p.rstrip("/"), a) for p, a in apps]
    
    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"] or "/"
        for p, app in self.apps:
            # The apps list should be sorted by length, descending.
            if path.startswith(p + "/") or path == p:
                environ = environ.copy()
                environ["SCRIPT_NAME"] = environ["SCRIPT_NAME"] + p
                environ["PATH_INFO"] = path[len(p):]
                return app(environ, start_response)
        
        start_response('404 Not Found', [('Content-Type', 'text/plain'),
                                         ('Content-Length', '0')])
        return ['']


########NEW FILE########
__FILENAME__ = _cpchecker
import os
import warnings

import cherrypy
from cherrypy._cpcompat import iteritems, copykeys, builtins


class Checker(object):
    """A checker for CherryPy sites and their mounted applications.
    
    When this object is called at engine startup, it executes each
    of its own methods whose names start with ``check_``. If you wish
    to disable selected checks, simply add a line in your global
    config which sets the appropriate method to False::
    
        [global]
        checker.check_skipped_app_config = False
    
    You may also dynamically add or replace ``check_*`` methods in this way.
    """
    
    on = True
    """If True (the default), run all checks; if False, turn off all checks."""
    
    
    def __init__(self):
        self._populate_known_types()
    
    def __call__(self):
        """Run all check_* methods."""
        if self.on:
            oldformatwarning = warnings.formatwarning
            warnings.formatwarning = self.formatwarning
            try:
                for name in dir(self):
                    if name.startswith("check_"):
                        method = getattr(self, name)
                        if method and hasattr(method, '__call__'):
                            method()
            finally:
                warnings.formatwarning = oldformatwarning
    
    def formatwarning(self, message, category, filename, lineno, line=None):
        """Function to format a warning."""
        return "CherryPy Checker:\n%s\n\n" % message
    
    # This value should be set inside _cpconfig.
    global_config_contained_paths = False
    
    def check_app_config_entries_dont_start_with_script_name(self):
        """Check for Application config with sections that repeat script_name."""
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            if not app.config:
                continue
            if sn == '':
                continue
            sn_atoms = sn.strip("/").split("/")
            for key in app.config.keys():
                key_atoms = key.strip("/").split("/")
                if key_atoms[:len(sn_atoms)] == sn_atoms:
                    warnings.warn(
                        "The application mounted at %r has config " \
                        "entries that start with its script name: %r" % (sn, key))
    
    def check_site_config_entries_in_app_config(self):
        """Check for mounted Applications that have site-scoped config."""
        for sn, app in iteritems(cherrypy.tree.apps):
            if not isinstance(app, cherrypy.Application):
                continue
            
            msg = []
            for section, entries in iteritems(app.config):
                if section.startswith('/'):
                    for key, value in iteritems(entries):
                        for n in ("engine.", "server.", "tree.", "checker."):
                            if key.startswith(n):
                                msg.append("[%s] %s = %s" % (section, key, value))
            if msg:
                msg.insert(0,
                    "The application mounted at %r contains the following "
                    "config entries, which are only allowed in site-wide "
                    "config. Move them to a [global] section and pass them "
                    "to cherrypy.config.update() instead of tree.mount()." % sn)
                warnings.warn(os.linesep.join(msg))
    
    def check_skipped_app_config(self):
        """Check for mounted Applications that have no config."""
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            if not app.config:
                msg = "The Application mounted at %r has an empty config." % sn
                if self.global_config_contained_paths:
                    msg += (" It looks like the config you passed to "
                            "cherrypy.config.update() contains application-"
                            "specific sections. You must explicitly pass "
                            "application config via "
                            "cherrypy.tree.mount(..., config=app_config)")
                warnings.warn(msg)
                return
    
    def check_app_config_brackets(self):
        """Check for Application config with extraneous brackets in section names."""
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            if not app.config:
                continue
            for key in app.config.keys():
                if key.startswith("[") or key.endswith("]"):
                    warnings.warn(
                        "The application mounted at %r has config " \
                        "section names with extraneous brackets: %r. "
                        "Config *files* need brackets; config *dicts* "
                        "(e.g. passed to tree.mount) do not." % (sn, key))
    
    def check_static_paths(self):
        """Check Application config for incorrect static paths."""
        # Use the dummy Request object in the main thread.
        request = cherrypy.request
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            request.app = app
            for section in app.config:
                # get_resource will populate request.config
                request.get_resource(section + "/dummy.html")
                conf = request.config.get
                
                if conf("tools.staticdir.on", False):
                    msg = ""
                    root = conf("tools.staticdir.root")
                    dir = conf("tools.staticdir.dir")
                    if dir is None:
                        msg = "tools.staticdir.dir is not set."
                    else:
                        fulldir = ""
                        if os.path.isabs(dir):
                            fulldir = dir
                            if root:
                                msg = ("dir is an absolute path, even "
                                       "though a root is provided.")
                                testdir = os.path.join(root, dir[1:])
                                if os.path.exists(testdir):
                                    msg += ("\nIf you meant to serve the "
                                            "filesystem folder at %r, remove "
                                            "the leading slash from dir." % testdir)
                        else:
                            if not root:
                                msg = "dir is a relative path and no root provided."
                            else:
                                fulldir = os.path.join(root, dir)
                                if not os.path.isabs(fulldir):
                                    msg = "%r is not an absolute path." % fulldir
                        
                        if fulldir and not os.path.exists(fulldir):
                            if msg:
                                msg += "\n"
                            msg += ("%r (root + dir) is not an existing "
                                    "filesystem path." % fulldir)
                    
                    if msg:
                        warnings.warn("%s\nsection: [%s]\nroot: %r\ndir: %r"
                                      % (msg, section, root, dir))
    
    
    # -------------------------- Compatibility -------------------------- #
    
    obsolete = {
        'server.default_content_type': 'tools.response_headers.headers',
        'log_access_file': 'log.access_file',
        'log_config_options': None,
        'log_file': 'log.error_file',
        'log_file_not_found': None,
        'log_request_headers': 'tools.log_headers.on',
        'log_to_screen': 'log.screen',
        'show_tracebacks': 'request.show_tracebacks',
        'throw_errors': 'request.throw_errors',
        'profiler.on': ('cherrypy.tree.mount(profiler.make_app('
                        'cherrypy.Application(Root())))'),
        }
    
    deprecated = {}
    
    def _compat(self, config):
        """Process config and warn on each obsolete or deprecated entry."""
        for section, conf in config.items():
            if isinstance(conf, dict):
                for k, v in conf.items():
                    if k in self.obsolete:
                        warnings.warn("%r is obsolete. Use %r instead.\n"
                                      "section: [%s]" %
                                      (k, self.obsolete[k], section))
                    elif k in self.deprecated:
                        warnings.warn("%r is deprecated. Use %r instead.\n"
                                      "section: [%s]" %
                                      (k, self.deprecated[k], section))
            else:
                if section in self.obsolete:
                    warnings.warn("%r is obsolete. Use %r instead."
                                  % (section, self.obsolete[section]))
                elif section in self.deprecated:
                    warnings.warn("%r is deprecated. Use %r instead."
                                  % (section, self.deprecated[section]))
    
    def check_compatibility(self):
        """Process config and warn on each obsolete or deprecated entry."""
        self._compat(cherrypy.config)
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            self._compat(app.config)
    
    
    # ------------------------ Known Namespaces ------------------------ #
    
    extra_config_namespaces = []
    
    def _known_ns(self, app):
        ns = ["wsgi"]
        ns.extend(copykeys(app.toolboxes))
        ns.extend(copykeys(app.namespaces))
        ns.extend(copykeys(app.request_class.namespaces))
        ns.extend(copykeys(cherrypy.config.namespaces))
        ns += self.extra_config_namespaces
        
        for section, conf in app.config.items():
            is_path_section = section.startswith("/")
            if is_path_section and isinstance(conf, dict):
                for k, v in conf.items():
                    atoms = k.split(".")
                    if len(atoms) > 1:
                        if atoms[0] not in ns:
                            # Spit out a special warning if a known
                            # namespace is preceded by "cherrypy."
                            if (atoms[0] == "cherrypy" and atoms[1] in ns):
                                msg = ("The config entry %r is invalid; "
                                       "try %r instead.\nsection: [%s]"
                                       % (k, ".".join(atoms[1:]), section))
                            else:
                                msg = ("The config entry %r is invalid, because "
                                       "the %r config namespace is unknown.\n"
                                       "section: [%s]" % (k, atoms[0], section))
                            warnings.warn(msg)
                        elif atoms[0] == "tools":
                            if atoms[1] not in dir(cherrypy.tools):
                                msg = ("The config entry %r may be invalid, "
                                       "because the %r tool was not found.\n"
                                       "section: [%s]" % (k, atoms[1], section))
                                warnings.warn(msg)
    
    def check_config_namespaces(self):
        """Process config and warn on each unknown config namespace."""
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            self._known_ns(app)


    
    
    # -------------------------- Config Types -------------------------- #
    
    known_config_types = {}
    
    def _populate_known_types(self):
        b = [x for x in vars(builtins).values()
             if type(x) is type(str)]
        
        def traverse(obj, namespace):
            for name in dir(obj):
                # Hack for 3.2's warning about body_params
                if name == 'body_params':
                    continue
                vtype = type(getattr(obj, name, None))
                if vtype in b:
                    self.known_config_types[namespace + "." + name] = vtype
        
        traverse(cherrypy.request, "request")
        traverse(cherrypy.response, "response")
        traverse(cherrypy.server, "server")
        traverse(cherrypy.engine, "engine")
        traverse(cherrypy.log, "log")
    
    def _known_types(self, config):
        msg = ("The config entry %r in section %r is of type %r, "
               "which does not match the expected type %r.")
        
        for section, conf in config.items():
            if isinstance(conf, dict):
                for k, v in conf.items():
                    if v is not None:
                        expected_type = self.known_config_types.get(k, None)
                        vtype = type(v)
                        if expected_type and vtype != expected_type:
                            warnings.warn(msg % (k, section, vtype.__name__,
                                                 expected_type.__name__))
            else:
                k, v = section, conf
                if v is not None:
                    expected_type = self.known_config_types.get(k, None)
                    vtype = type(v)
                    if expected_type and vtype != expected_type:
                        warnings.warn(msg % (k, section, vtype.__name__,
                                             expected_type.__name__))
    
    def check_config_types(self):
        """Assert that config values are of the same type as default values."""
        self._known_types(cherrypy.config)
        for sn, app in cherrypy.tree.apps.items():
            if not isinstance(app, cherrypy.Application):
                continue
            self._known_types(app.config)
    
    
    # -------------------- Specific config warnings -------------------- #
    
    def check_localhost(self):
        """Warn if any socket_host is 'localhost'. See #711."""
        for k, v in cherrypy.config.items():
            if k == 'server.socket_host' and v == 'localhost':
                warnings.warn("The use of 'localhost' as a socket host can "
                    "cause problems on newer systems, since 'localhost' can "
                    "map to either an IPv4 or an IPv6 address. You should "
                    "use '127.0.0.1' or '[::1]' instead.")

########NEW FILE########
__FILENAME__ = _cpcompat
"""Compatibility code for using CherryPy with various versions of Python.

CherryPy 3.2 is compatible with Python versions 2.3+. This module provides a
useful abstraction over the differences between Python versions, sometimes by
preferring a newer idiom, sometimes an older one, and sometimes a custom one.

In particular, Python 2 uses str and '' for byte strings, while Python 3
uses str and '' for unicode strings. We will call each of these the 'native
string' type for each version. Because of this major difference, this module
provides new 'bytestr', 'unicodestr', and 'nativestr' attributes, as well as
two functions: 'ntob', which translates native strings (of type 'str') into
byte strings regardless of Python version, and 'ntou', which translates native
strings to unicode strings. This also provides a 'BytesIO' name for dealing
specifically with bytes, and a 'StringIO' name for dealing with native strings.
It also provides a 'base64_decode' function with native strings as input and
output.
"""
import os
import re
import sys

if sys.version_info >= (3, 0):
    py3k = True
    bytestr = bytes
    unicodestr = str
    nativestr = unicodestr
    basestring = (bytes, str)
    def ntob(n, encoding='ISO-8859-1'):
        """Return the given native string as a byte string in the given encoding."""
        # In Python 3, the native string type is unicode
        return n.encode(encoding)
    def ntou(n, encoding='ISO-8859-1'):
        """Return the given native string as a unicode string with the given encoding."""
        # In Python 3, the native string type is unicode
        return n
    def tonative(n, encoding='ISO-8859-1'):
        """Return the given string as a native string in the given encoding."""
        # In Python 3, the native string type is unicode
        if isinstance(n, bytes):
            return n.decode(encoding)
        return n
    # type("")
    from io import StringIO
    # bytes:
    from io import BytesIO as BytesIO
else:
    # Python 2
    py3k = False
    bytestr = str
    unicodestr = unicode
    nativestr = bytestr
    basestring = basestring
    def ntob(n, encoding='ISO-8859-1'):
        """Return the given native string as a byte string in the given encoding."""
        # In Python 2, the native string type is bytes. Assume it's already
        # in the given encoding, which for ISO-8859-1 is almost always what
        # was intended.
        return n
    def ntou(n, encoding='ISO-8859-1'):
        """Return the given native string as a unicode string with the given encoding."""
        # In Python 2, the native string type is bytes.
        # First, check for the special encoding 'escape'. The test suite uses this
        # to signal that it wants to pass a string with embedded \uXXXX escapes,
        # but without having to prefix it with u'' for Python 2, but no prefix
        # for Python 3.
        if encoding == 'escape':
            return unicode(
                re.sub(r'\\u([0-9a-zA-Z]{4})',
                       lambda m: unichr(int(m.group(1), 16)),
                       n.decode('ISO-8859-1')))
        # Assume it's already in the given encoding, which for ISO-8859-1 is almost
        # always what was intended.
        return n.decode(encoding)
    def tonative(n, encoding='ISO-8859-1'):
        """Return the given string as a native string in the given encoding."""
        # In Python 2, the native string type is bytes.
        if isinstance(n, unicode):
            return n.encode(encoding)
        return n
    try:
        # type("")
        from cStringIO import StringIO
    except ImportError:
        # type("")
        from StringIO import StringIO
    # bytes:
    BytesIO = StringIO

try:
    set = set
except NameError:
    from sets import Set as set

try:
    # Python 3.1+
    from base64 import decodebytes as _base64_decodebytes
except ImportError:
    # Python 3.0-
    # since CherryPy claims compability with Python 2.3, we must use
    # the legacy API of base64
    from base64 import decodestring as _base64_decodebytes

def base64_decode(n, encoding='ISO-8859-1'):
    """Return the native string base64-decoded (as a native string)."""
    if isinstance(n, unicodestr):
        b = n.encode(encoding)
    else:
        b = n
    b = _base64_decodebytes(b)
    if nativestr is unicodestr:
        return b.decode(encoding)
    else:
        return b

try:
    # Python 2.5+
    from hashlib import md5
except ImportError:
    from md5 import new as md5

try:
    # Python 2.5+
    from hashlib import sha1 as sha
except ImportError:
    from sha import new as sha

try:
    sorted = sorted
except NameError:
    def sorted(i):
        i = i[:]
        i.sort()
        return i

try:
    reversed = reversed
except NameError:
    def reversed(x):
        i = len(x)
        while i > 0:
            i -= 1
            yield x[i]

try:
    # Python 3
    from urllib.parse import urljoin, urlencode
    from urllib.parse import quote, quote_plus
    from urllib.request import unquote, urlopen
    from urllib.request import parse_http_list, parse_keqv_list
except ImportError:
    # Python 2
    from urlparse import urljoin
    from urllib import urlencode, urlopen
    from urllib import quote, quote_plus
    from urllib import unquote
    from urllib2 import parse_http_list, parse_keqv_list

try:
    from threading import local as threadlocal
except ImportError:
    from cherrypy._cpthreadinglocal import local as threadlocal

try:
    dict.iteritems
    # Python 2
    iteritems = lambda d: d.iteritems()
    copyitems = lambda d: d.items()
except AttributeError:
    # Python 3
    iteritems = lambda d: d.items()
    copyitems = lambda d: list(d.items())

try:
    dict.iterkeys
    # Python 2
    iterkeys = lambda d: d.iterkeys()
    copykeys = lambda d: d.keys()
except AttributeError:
    # Python 3
    iterkeys = lambda d: d.keys()
    copykeys = lambda d: list(d.keys())

try:
    dict.itervalues
    # Python 2
    itervalues = lambda d: d.itervalues()
    copyvalues = lambda d: d.values()
except AttributeError:
    # Python 3
    itervalues = lambda d: d.values()
    copyvalues = lambda d: list(d.values())

try:
    # Python 3
    import builtins
except ImportError:
    # Python 2
    import __builtin__ as builtins

try:
    # Python 2. We have to do it in this order so Python 2 builds
    # don't try to import the 'http' module from cherrypy.lib
    from Cookie import SimpleCookie, CookieError
    from httplib import BadStatusLine, HTTPConnection, HTTPSConnection, IncompleteRead, NotConnected
    from BaseHTTPServer import BaseHTTPRequestHandler
except ImportError:
    # Python 3
    from http.cookies import SimpleCookie, CookieError
    from http.client import BadStatusLine, HTTPConnection, HTTPSConnection, IncompleteRead, NotConnected
    from http.server import BaseHTTPRequestHandler

try:
    # Python 2. We have to do it in this order so Python 2 builds
    # don't try to import the 'http' module from cherrypy.lib
    from httplib import HTTPSConnection
except ImportError:
    try:
        # Python 3
        from http.client import HTTPSConnection
    except ImportError:
        # Some platforms which don't have SSL don't expose HTTPSConnection
        HTTPSConnection = None

try:
    # Python 2
    xrange = xrange
except NameError:
    # Python 3
    xrange = range

import threading
if hasattr(threading.Thread, "daemon"):
    # Python 2.6+
    def get_daemon(t):
        return t.daemon
    def set_daemon(t, val):
        t.daemon = val
else:
    def get_daemon(t):
        return t.isDaemon()
    def set_daemon(t, val):
        t.setDaemon(val)

try:
    from email.utils import formatdate
    def HTTPDate(timeval=None):
        return formatdate(timeval, usegmt=True)
except ImportError:
    from rfc822 import formatdate as HTTPDate

try:
    # Python 3
    from urllib.parse import unquote as parse_unquote
    def unquote_qs(atom, encoding, errors='strict'):
        return parse_unquote(atom.replace('+', ' '), encoding=encoding, errors=errors)
except ImportError:
    # Python 2
    from urllib import unquote as parse_unquote
    def unquote_qs(atom, encoding, errors='strict'):
        return parse_unquote(atom.replace('+', ' ')).decode(encoding, errors)

try:
    # Prefer simplejson, which is usually more advanced than the builtin module.
    import simplejson as json
    json_decode = json.JSONDecoder().decode
    json_encode = json.JSONEncoder().iterencode
except ImportError:
    if py3k:
        # Python 3.0: json is part of the standard library,
        # but outputs unicode. We need bytes.
        import json
        json_decode = json.JSONDecoder().decode
        _json_encode = json.JSONEncoder().iterencode
        def json_encode(value):
            for chunk in _json_encode(value):
                yield chunk.encode('utf8')
    elif sys.version_info >= (2, 6):
        # Python 2.6: json is part of the standard library
        import json
        json_decode = json.JSONDecoder().decode
        json_encode = json.JSONEncoder().iterencode
    else:
        json = None
        def json_decode(s):
            raise ValueError('No JSON library is available')
        def json_encode(s):
            raise ValueError('No JSON library is available')

try:
    import cPickle as pickle
except ImportError:
    # In Python 2, pickle is a Python version.
    # In Python 3, pickle is the sped-up C version.
    import pickle

try:
    os.urandom(20)
    import binascii
    def random20():
        return binascii.hexlify(os.urandom(20)).decode('ascii')
except (AttributeError, NotImplementedError):
    import random
    # os.urandom not available until Python 2.4. Fall back to random.random.
    def random20():
        return sha('%s' % random.random()).hexdigest()

try:
    from _thread import get_ident as get_thread_ident
except ImportError:
    from thread import get_ident as get_thread_ident

try:
    # Python 3
    next = next
except NameError:
    # Python 2
    def next(i):
        return i.next()

########NEW FILE########
__FILENAME__ = _cpconfig
"""
Configuration system for CherryPy.

Configuration in CherryPy is implemented via dictionaries. Keys are strings
which name the mapped value, which may be of any type.


Architecture
------------

CherryPy Requests are part of an Application, which runs in a global context,
and configuration data may apply to any of those three scopes:

Global
    Configuration entries which apply everywhere are stored in
    cherrypy.config.

Application
    Entries which apply to each mounted application are stored
    on the Application object itself, as 'app.config'. This is a two-level
    dict where each key is a path, or "relative URL" (for example, "/" or
    "/path/to/my/page"), and each value is a config dict. Usually, this
    data is provided in the call to tree.mount(root(), config=conf),
    although you may also use app.merge(conf).

Request
    Each Request object possesses a single 'Request.config' dict.
    Early in the request process, this dict is populated by merging global
    config entries, Application entries (whose path equals or is a parent
    of Request.path_info), and any config acquired while looking up the
    page handler (see next).


Declaration
-----------

Configuration data may be supplied as a Python dictionary, as a filename,
or as an open file object. When you supply a filename or file, CherryPy
uses Python's builtin ConfigParser; you declare Application config by
writing each path as a section header::

    [/path/to/my/page]
    request.stream = True

To declare global configuration entries, place them in a [global] section.

You may also declare config entries directly on the classes and methods
(page handlers) that make up your CherryPy application via the ``_cp_config``
attribute. For example::

    class Demo:
        _cp_config = {'tools.gzip.on': True}
        
        def index(self):
            return "Hello world"
        index.exposed = True
        index._cp_config = {'request.show_tracebacks': False}

.. note::
    
    This behavior is only guaranteed for the default dispatcher.
    Other dispatchers may have different restrictions on where
    you can attach _cp_config attributes.


Namespaces
----------

Configuration keys are separated into namespaces by the first "." in the key.
Current namespaces:

engine
    Controls the 'application engine', including autoreload.
    These can only be declared in the global config.

tree
    Grafts cherrypy.Application objects onto cherrypy.tree.
    These can only be declared in the global config.

hooks
    Declares additional request-processing functions.

log
    Configures the logging for each application.
    These can only be declared in the global or / config.

request
    Adds attributes to each Request.

response
    Adds attributes to each Response.

server
    Controls the default HTTP server via cherrypy.server.
    These can only be declared in the global config.

tools
    Runs and configures additional request-processing packages.

wsgi
    Adds WSGI middleware to an Application's "pipeline".
    These can only be declared in the app's root config ("/").

checker
    Controls the 'checker', which looks for common errors in
    app state (including config) when the engine starts.
    Global config only.

The only key that does not exist in a namespace is the "environment" entry.
This special entry 'imports' other config entries from a template stored in
cherrypy._cpconfig.environments[environment]. It only applies to the global
config, and only when you use cherrypy.config.update.

You can define your own namespaces to be called at the Global, Application,
or Request level, by adding a named handler to cherrypy.config.namespaces,
app.namespaces, or app.request_class.namespaces. The name can
be any string, and the handler must be either a callable or a (Python 2.5
style) context manager.
"""

import cherrypy
from cherrypy._cpcompat import set, basestring
from cherrypy.lib import reprconf

# Deprecated in  CherryPy 3.2--remove in 3.3
NamespaceSet = reprconf.NamespaceSet

def merge(base, other):
    """Merge one app config (from a dict, file, or filename) into another.
    
    If the given config is a filename, it will be appended to
    the list of files to monitor for "autoreload" changes.
    """
    if isinstance(other, basestring):
        cherrypy.engine.autoreload.files.add(other)
    
    # Load other into base
    for section, value_map in reprconf.as_dict(other).items():
        if not isinstance(value_map, dict):
            raise ValueError(
                "Application config must include section headers, but the "
                "config you tried to merge doesn't have any sections. "
                "Wrap your config in another dict with paths as section "
                "headers, for example: {'/': config}.")
        base.setdefault(section, {}).update(value_map)


class Config(reprconf.Config):
    """The 'global' configuration data for the entire CherryPy process."""

    def update(self, config):
        """Update self from a dict, file or filename."""
        if isinstance(config, basestring):
            # Filename
            cherrypy.engine.autoreload.files.add(config)
        reprconf.Config.update(self, config)

    def _apply(self, config):
        """Update self from a dict."""
        if isinstance(config.get("global", None), dict):
            if len(config) > 1:
                cherrypy.checker.global_config_contained_paths = True
            config = config["global"]
        if 'tools.staticdir.dir' in config:
            config['tools.staticdir.section'] = "global"
        reprconf.Config._apply(self, config)
    
    def __call__(self, *args, **kwargs):
        """Decorator for page handlers to set _cp_config."""
        if args:
            raise TypeError(
                "The cherrypy.config decorator does not accept positional "
                "arguments; you must use keyword arguments.")
        def tool_decorator(f):
            if not hasattr(f, "_cp_config"):
                f._cp_config = {}
            for k, v in kwargs.items():
                f._cp_config[k] = v
            return f
        return tool_decorator


Config.environments = environments = {
    "staging": {
        'engine.autoreload_on': False,
        'checker.on': False,
        'tools.log_headers.on': False,
        'request.show_tracebacks': False,
        'request.show_mismatched_params': False,
        },
    "production": {
        'engine.autoreload_on': False,
        'checker.on': False,
        'tools.log_headers.on': False,
        'request.show_tracebacks': False,
        'request.show_mismatched_params': False,
        'log.screen': False,
        },
    "embedded": {
        # For use with CherryPy embedded in another deployment stack.
        'engine.autoreload_on': False,
        'checker.on': False,
        'tools.log_headers.on': False,
        'request.show_tracebacks': False,
        'request.show_mismatched_params': False,
        'log.screen': False,
        'engine.SIGHUP': None,
        'engine.SIGTERM': None,
        },
    "test_suite": {
        'engine.autoreload_on': False,
        'checker.on': False,
        'tools.log_headers.on': False,
        'request.show_tracebacks': True,
        'request.show_mismatched_params': True,
        'log.screen': False,
        },
    }


def _server_namespace_handler(k, v):
    """Config handler for the "server" namespace."""
    atoms = k.split(".", 1)
    if len(atoms) > 1:
        # Special-case config keys of the form 'server.servername.socket_port'
        # to configure additional HTTP servers.
        if not hasattr(cherrypy, "servers"):
            cherrypy.servers = {}
        
        servername, k = atoms
        if servername not in cherrypy.servers:
            from cherrypy import _cpserver
            cherrypy.servers[servername] = _cpserver.Server()
            # On by default, but 'on = False' can unsubscribe it (see below).
            cherrypy.servers[servername].subscribe()
        
        if k == 'on':
            if v:
                cherrypy.servers[servername].subscribe()
            else:
                cherrypy.servers[servername].unsubscribe()
        else:
            setattr(cherrypy.servers[servername], k, v)
    else:
        setattr(cherrypy.server, k, v)
Config.namespaces["server"] = _server_namespace_handler

def _engine_namespace_handler(k, v):
    """Backward compatibility handler for the "engine" namespace."""
    engine = cherrypy.engine
    if k == 'autoreload_on':
        if v:
            engine.autoreload.subscribe()
        else:
            engine.autoreload.unsubscribe()
    elif k == 'autoreload_frequency':
        engine.autoreload.frequency = v
    elif k == 'autoreload_match':
        engine.autoreload.match = v
    elif k == 'reload_files':
        engine.autoreload.files = set(v)
    elif k == 'deadlock_poll_freq':
        engine.timeout_monitor.frequency = v
    elif k == 'SIGHUP':
        engine.listeners['SIGHUP'] = set([v])
    elif k == 'SIGTERM':
        engine.listeners['SIGTERM'] = set([v])
    elif "." in k:
        plugin, attrname = k.split(".", 1)
        plugin = getattr(engine, plugin)
        if attrname == 'on':
            if v and hasattr(getattr(plugin, 'subscribe', None), '__call__'):
                plugin.subscribe()
                return
            elif (not v) and hasattr(getattr(plugin, 'unsubscribe', None), '__call__'):
                plugin.unsubscribe()
                return
        setattr(plugin, attrname, v)
    else:
        setattr(engine, k, v)
Config.namespaces["engine"] = _engine_namespace_handler


def _tree_namespace_handler(k, v):
    """Namespace handler for the 'tree' config namespace."""
    if isinstance(v, dict):
        for script_name, app in v.items():
            cherrypy.tree.graft(app, script_name)
            cherrypy.engine.log("Mounted: %s on %s" % (app, script_name or "/"))
    else:
        cherrypy.tree.graft(v, v.script_name)
        cherrypy.engine.log("Mounted: %s on %s" % (v, v.script_name or "/"))
Config.namespaces["tree"] = _tree_namespace_handler



########NEW FILE########
__FILENAME__ = _cpdispatch
"""CherryPy dispatchers.

A 'dispatcher' is the object which looks up the 'page handler' callable
and collects config for the current request based on the path_info, other
request attributes, and the application architecture. The core calls the
dispatcher as early as possible, passing it a 'path_info' argument.

The default dispatcher discovers the page handler by matching path_info
to a hierarchical arrangement of objects, starting at request.app.root.
"""

import string
import sys
import types
try:
    classtype = (type, types.ClassType)
except AttributeError:
    classtype = type

import cherrypy
from cherrypy._cpcompat import set


class PageHandler(object):
    """Callable which sets response.body."""
    
    def __init__(self, callable, *args, **kwargs):
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self):
        try:
            return self.callable(*self.args, **self.kwargs)
        except TypeError:
            x = sys.exc_info()[1]
            try:
                test_callable_spec(self.callable, self.args, self.kwargs)
            except cherrypy.HTTPError:
                raise sys.exc_info()[1]
            except:
                raise x
            raise


def test_callable_spec(callable, callable_args, callable_kwargs):
    """
    Inspect callable and test to see if the given args are suitable for it.

    When an error occurs during the handler's invoking stage there are 2
    erroneous cases:
    1.  Too many parameters passed to a function which doesn't define
        one of *args or **kwargs.
    2.  Too little parameters are passed to the function.

    There are 3 sources of parameters to a cherrypy handler.
    1.  query string parameters are passed as keyword parameters to the handler.
    2.  body parameters are also passed as keyword parameters.
    3.  when partial matching occurs, the final path atoms are passed as
        positional args.
    Both the query string and path atoms are part of the URI.  If they are
    incorrect, then a 404 Not Found should be raised. Conversely the body
    parameters are part of the request; if they are invalid a 400 Bad Request.
    """
    show_mismatched_params = getattr(
        cherrypy.serving.request, 'show_mismatched_params', False)
    try:
        (args, varargs, varkw, defaults) = inspect.getargspec(callable)
    except TypeError:
        if isinstance(callable, object) and hasattr(callable, '__call__'):
            (args, varargs, varkw, defaults) = inspect.getargspec(callable.__call__)
        else:
            # If it wasn't one of our own types, re-raise 
            # the original error
            raise

    if args and args[0] == 'self':
        args = args[1:]

    arg_usage = dict([(arg, 0,) for arg in args])
    vararg_usage = 0
    varkw_usage = 0
    extra_kwargs = set()

    for i, value in enumerate(callable_args):
        try:
            arg_usage[args[i]] += 1
        except IndexError:
            vararg_usage += 1

    for key in callable_kwargs.keys():
        try:
            arg_usage[key] += 1
        except KeyError:
            varkw_usage += 1
            extra_kwargs.add(key)

    # figure out which args have defaults.
    args_with_defaults = args[-len(defaults or []):]
    for i, val in enumerate(defaults or []):
        # Defaults take effect only when the arg hasn't been used yet.
        if arg_usage[args_with_defaults[i]] == 0:
            arg_usage[args_with_defaults[i]] += 1

    missing_args = []
    multiple_args = []
    for key, usage in arg_usage.items():
        if usage == 0:
            missing_args.append(key)
        elif usage > 1:
            multiple_args.append(key)

    if missing_args:
        # In the case where the method allows body arguments
        # there are 3 potential errors:
        # 1. not enough query string parameters -> 404
        # 2. not enough body parameters -> 400
        # 3. not enough path parts (partial matches) -> 404
        #
        # We can't actually tell which case it is, 
        # so I'm raising a 404 because that covers 2/3 of the
        # possibilities
        # 
        # In the case where the method does not allow body
        # arguments it's definitely a 404.
        message = None
        if show_mismatched_params:
            message="Missing parameters: %s" % ",".join(missing_args)
        raise cherrypy.HTTPError(404, message=message)

    # the extra positional arguments come from the path - 404 Not Found
    if not varargs and vararg_usage > 0:
        raise cherrypy.HTTPError(404)

    body_params = cherrypy.serving.request.body.params or {}
    body_params = set(body_params.keys())
    qs_params = set(callable_kwargs.keys()) - body_params

    if multiple_args:
        if qs_params.intersection(set(multiple_args)):
            # If any of the multiple parameters came from the query string then
            # it's a 404 Not Found
            error = 404
        else:
            # Otherwise it's a 400 Bad Request
            error = 400

        message = None
        if show_mismatched_params:
            message="Multiple values for parameters: "\
                    "%s" % ",".join(multiple_args)
        raise cherrypy.HTTPError(error, message=message)

    if not varkw and varkw_usage > 0:

        # If there were extra query string parameters, it's a 404 Not Found
        extra_qs_params = set(qs_params).intersection(extra_kwargs)
        if extra_qs_params:
            message = None
            if show_mismatched_params:
                message="Unexpected query string "\
                        "parameters: %s" % ", ".join(extra_qs_params)
            raise cherrypy.HTTPError(404, message=message)

        # If there were any extra body parameters, it's a 400 Not Found
        extra_body_params = set(body_params).intersection(extra_kwargs)
        if extra_body_params:
            message = None
            if show_mismatched_params:
                message="Unexpected body parameters: "\
                        "%s" % ", ".join(extra_body_params)
            raise cherrypy.HTTPError(400, message=message)


try:
    import inspect
except ImportError:
    test_callable_spec = lambda callable, args, kwargs: None



class LateParamPageHandler(PageHandler):
    """When passing cherrypy.request.params to the page handler, we do not
    want to capture that dict too early; we want to give tools like the
    decoding tool a chance to modify the params dict in-between the lookup
    of the handler and the actual calling of the handler. This subclass
    takes that into account, and allows request.params to be 'bound late'
    (it's more complicated than that, but that's the effect).
    """
    
    def _get_kwargs(self):
        kwargs = cherrypy.serving.request.params.copy()
        if self._kwargs:
            kwargs.update(self._kwargs)
        return kwargs
    
    def _set_kwargs(self, kwargs):
        self._kwargs = kwargs
    
    kwargs = property(_get_kwargs, _set_kwargs,
                      doc='page handler kwargs (with '
                      'cherrypy.request.params copied in)')


if sys.version_info < (3, 0):
    punctuation_to_underscores = string.maketrans(
        string.punctuation, '_' * len(string.punctuation))
    def validate_translator(t):
        if not isinstance(t, str) or len(t) != 256:
            raise ValueError("The translate argument must be a str of len 256.")
else:
    punctuation_to_underscores = str.maketrans(
        string.punctuation, '_' * len(string.punctuation))
    def validate_translator(t):
        if not isinstance(t, dict):
            raise ValueError("The translate argument must be a dict.")

class Dispatcher(object):
    """CherryPy Dispatcher which walks a tree of objects to find a handler.
    
    The tree is rooted at cherrypy.request.app.root, and each hierarchical
    component in the path_info argument is matched to a corresponding nested
    attribute of the root object. Matching handlers must have an 'exposed'
    attribute which evaluates to True. The special method name "index"
    matches a URI which ends in a slash ("/"). The special method name
    "default" may match a portion of the path_info (but only when no longer
    substring of the path_info matches some other object).
    
    This is the default, built-in dispatcher for CherryPy.
    """
    
    dispatch_method_name = '_cp_dispatch'
    """
    The name of the dispatch method that nodes may optionally implement
    to provide their own dynamic dispatch algorithm.
    """
    
    def __init__(self, dispatch_method_name=None,
                 translate=punctuation_to_underscores):
        validate_translator(translate)
        self.translate = translate
        if dispatch_method_name:
            self.dispatch_method_name = dispatch_method_name

    def __call__(self, path_info):
        """Set handler and config for the current request."""
        request = cherrypy.serving.request
        func, vpath = self.find_handler(path_info)
        
        if func:
            # Decode any leftover %2F in the virtual_path atoms.
            vpath = [x.replace("%2F", "/") for x in vpath]
            request.handler = LateParamPageHandler(func, *vpath)
        else:
            request.handler = cherrypy.NotFound()
    
    def find_handler(self, path):
        """Return the appropriate page handler, plus any virtual path.
        
        This will return two objects. The first will be a callable,
        which can be used to generate page output. Any parameters from
        the query string or request body will be sent to that callable
        as keyword arguments.
        
        The callable is found by traversing the application's tree,
        starting from cherrypy.request.app.root, and matching path
        components to successive objects in the tree. For example, the
        URL "/path/to/handler" might return root.path.to.handler.
        
        The second object returned will be a list of names which are
        'virtual path' components: parts of the URL which are dynamic,
        and were not used when looking up the handler.
        These virtual path components are passed to the handler as
        positional arguments.
        """
        request = cherrypy.serving.request
        app = request.app
        root = app.root
        dispatch_name = self.dispatch_method_name
        
        # Get config for the root object/path.
        fullpath = [x for x in path.strip('/').split('/') if x] + ['index']
        fullpath_len = len(fullpath)
        segleft = fullpath_len
        nodeconf = {}
        if hasattr(root, "_cp_config"):
            nodeconf.update(root._cp_config)
        if "/" in app.config:
            nodeconf.update(app.config["/"])
        object_trail = [['root', root, nodeconf, segleft]]
        
        node = root
        iternames = fullpath[:]
        while iternames:
            name = iternames[0]
            # map to legal Python identifiers (e.g. replace '.' with '_')
            objname = name.translate(self.translate)
            
            nodeconf = {}
            subnode = getattr(node, objname, None)
            pre_len = len(iternames)
            if subnode is None:
                dispatch = getattr(node, dispatch_name, None)
                if dispatch and hasattr(dispatch, '__call__') and not \
                        getattr(dispatch, 'exposed', False) and \
                        pre_len > 1:
                    #Don't expose the hidden 'index' token to _cp_dispatch
                    #We skip this if pre_len == 1 since it makes no sense
                    #to call a dispatcher when we have no tokens left.
                    index_name = iternames.pop()
                    subnode = dispatch(vpath=iternames)
                    iternames.append(index_name)
                else:
                    #We didn't find a path, but keep processing in case there
                    #is a default() handler.
                    iternames.pop(0)
            else:
                #We found the path, remove the vpath entry
                iternames.pop(0)
            segleft = len(iternames)
            if segleft > pre_len:
                #No path segment was removed.  Raise an error.
                raise cherrypy.CherryPyException(
                    "A vpath segment was added.  Custom dispatchers may only "
                    + "remove elements.  While trying to process "
                    + "{0} in {1}".format(name, fullpath)
                    )
            elif segleft == pre_len:
                #Assume that the handler used the current path segment, but
                #did not pop it.  This allows things like 
                #return getattr(self, vpath[0], None)
                iternames.pop(0)
                segleft -= 1
            node = subnode

            if node is not None:
                # Get _cp_config attached to this node.
                if hasattr(node, "_cp_config"):
                    nodeconf.update(node._cp_config)
            
            # Mix in values from app.config for this path.
            existing_len = fullpath_len - pre_len
            if existing_len != 0:
                curpath = '/' + '/'.join(fullpath[0:existing_len])
            else:
                curpath = ''
            new_segs = fullpath[fullpath_len - pre_len:fullpath_len - segleft]
            for seg in new_segs:
                curpath += '/' + seg
                if curpath in app.config:
                    nodeconf.update(app.config[curpath])
            
            object_trail.append([name, node, nodeconf, segleft])
            
        def set_conf():
            """Collapse all object_trail config into cherrypy.request.config."""
            base = cherrypy.config.copy()
            # Note that we merge the config from each node
            # even if that node was None.
            for name, obj, conf, segleft in object_trail:
                base.update(conf)
                if 'tools.staticdir.dir' in conf:
                    base['tools.staticdir.section'] = '/' + '/'.join(fullpath[0:fullpath_len - segleft])
            return base
        
        # Try successive objects (reverse order)
        num_candidates = len(object_trail) - 1
        for i in range(num_candidates, -1, -1):
            
            name, candidate, nodeconf, segleft = object_trail[i]
            if candidate is None:
                continue
            
            # Try a "default" method on the current leaf.
            if hasattr(candidate, "default"):
                defhandler = candidate.default
                if getattr(defhandler, 'exposed', False):
                    # Insert any extra _cp_config from the default handler.
                    conf = getattr(defhandler, "_cp_config", {})
                    object_trail.insert(i+1, ["default", defhandler, conf, segleft])
                    request.config = set_conf()
                    # See http://www.cherrypy.org/ticket/613
                    request.is_index = path.endswith("/")
                    return defhandler, fullpath[fullpath_len - segleft:-1]
            
            # Uncomment the next line to restrict positional params to "default".
            # if i < num_candidates - 2: continue
            
            # Try the current leaf.
            if getattr(candidate, 'exposed', False):
                request.config = set_conf()
                if i == num_candidates:
                    # We found the extra ".index". Mark request so tools
                    # can redirect if path_info has no trailing slash.
                    request.is_index = True
                else:
                    # We're not at an 'index' handler. Mark request so tools
                    # can redirect if path_info has NO trailing slash.
                    # Note that this also includes handlers which take
                    # positional parameters (virtual paths).
                    request.is_index = False
                return candidate, fullpath[fullpath_len - segleft:-1]
        
        # We didn't find anything
        request.config = set_conf()
        return None, []


class MethodDispatcher(Dispatcher):
    """Additional dispatch based on cherrypy.request.method.upper().
    
    Methods named GET, POST, etc will be called on an exposed class.
    The method names must be all caps; the appropriate Allow header
    will be output showing all capitalized method names as allowable
    HTTP verbs.
    
    Note that the containing class must be exposed, not the methods.
    """
    
    def __call__(self, path_info):
        """Set handler and config for the current request."""
        request = cherrypy.serving.request
        resource, vpath = self.find_handler(path_info)
        
        if resource:
            # Set Allow header
            avail = [m for m in dir(resource) if m.isupper()]
            if "GET" in avail and "HEAD" not in avail:
                avail.append("HEAD")
            avail.sort()
            cherrypy.serving.response.headers['Allow'] = ", ".join(avail)
            
            # Find the subhandler
            meth = request.method.upper()
            func = getattr(resource, meth, None)
            if func is None and meth == "HEAD":
                func = getattr(resource, "GET", None)
            if func:
                # Grab any _cp_config on the subhandler.
                if hasattr(func, "_cp_config"):
                    request.config.update(func._cp_config)
                
                # Decode any leftover %2F in the virtual_path atoms.
                vpath = [x.replace("%2F", "/") for x in vpath]
                request.handler = LateParamPageHandler(func, *vpath)
            else:
                request.handler = cherrypy.HTTPError(405)
        else:
            request.handler = cherrypy.NotFound()


class RoutesDispatcher(object):
    """A Routes based dispatcher for CherryPy."""
    
    def __init__(self, full_result=False):
        """
        Routes dispatcher

        Set full_result to True if you wish the controller
        and the action to be passed on to the page handler
        parameters. By default they won't be.
        """
        import routes
        self.full_result = full_result
        self.controllers = {}
        self.mapper = routes.Mapper()
        self.mapper.controller_scan = self.controllers.keys
        
    def connect(self, name, route, controller, **kwargs):
        self.controllers[name] = controller
        self.mapper.connect(name, route, controller=name, **kwargs)
    
    def redirect(self, url):
        raise cherrypy.HTTPRedirect(url)
    
    def __call__(self, path_info):
        """Set handler and config for the current request."""
        func = self.find_handler(path_info)
        if func:
            cherrypy.serving.request.handler = LateParamPageHandler(func)
        else:
            cherrypy.serving.request.handler = cherrypy.NotFound()
    
    def find_handler(self, path_info):
        """Find the right page handler, and set request.config."""
        import routes
        
        request = cherrypy.serving.request
        
        config = routes.request_config()
        config.mapper = self.mapper
        if hasattr(request, 'wsgi_environ'):
            config.environ = request.wsgi_environ
        config.host = request.headers.get('Host', None)
        config.protocol = request.scheme
        config.redirect = self.redirect
        
        result = self.mapper.match(path_info)
        
        config.mapper_dict = result
        params = {}
        if result:
            params = result.copy()
        if not self.full_result:
            params.pop('controller', None)
            params.pop('action', None)
        request.params.update(params)
        
        # Get config for the root object/path.
        request.config = base = cherrypy.config.copy()
        curpath = ""
        
        def merge(nodeconf):
            if 'tools.staticdir.dir' in nodeconf:
                nodeconf['tools.staticdir.section'] = curpath or "/"
            base.update(nodeconf)
        
        app = request.app
        root = app.root
        if hasattr(root, "_cp_config"):
            merge(root._cp_config)
        if "/" in app.config:
            merge(app.config["/"])
        
        # Mix in values from app.config.
        atoms = [x for x in path_info.split("/") if x]
        if atoms:
            last = atoms.pop()
        else:
            last = None
        for atom in atoms:
            curpath = "/".join((curpath, atom))
            if curpath in app.config:
                merge(app.config[curpath])
        
        handler = None
        if result:
            controller = result.get('controller')
            controller = self.controllers.get(controller, controller)
            if controller:
                if isinstance(controller, classtype):
                    controller = controller()
                # Get config from the controller.
                if hasattr(controller, "_cp_config"):
                    merge(controller._cp_config)
            
            action = result.get('action')
            if action is not None:
                handler = getattr(controller, action, None)
                # Get config from the handler 
                if hasattr(handler, "_cp_config"): 
                    merge(handler._cp_config)
            else:
                handler = controller
        
        # Do the last path atom here so it can
        # override the controller's _cp_config.
        if last:
            curpath = "/".join((curpath, last))
            if curpath in app.config:
                merge(app.config[curpath])
        
        return handler


def XMLRPCDispatcher(next_dispatcher=Dispatcher()):
    from cherrypy.lib import xmlrpcutil
    def xmlrpc_dispatch(path_info):
        path_info = xmlrpcutil.patched_path(path_info)
        return next_dispatcher(path_info)
    return xmlrpc_dispatch


def VirtualHost(next_dispatcher=Dispatcher(), use_x_forwarded_host=True, **domains):
    """
    Select a different handler based on the Host header.
    
    This can be useful when running multiple sites within one CP server.
    It allows several domains to point to different parts of a single
    website structure. For example::
    
        http://www.domain.example  ->  root
        http://www.domain2.example  ->  root/domain2/
        http://www.domain2.example:443  ->  root/secure
    
    can be accomplished via the following config::
    
        [/]
        request.dispatch = cherrypy.dispatch.VirtualHost(
            **{'www.domain2.example': '/domain2',
               'www.domain2.example:443': '/secure',
              })
    
    next_dispatcher
        The next dispatcher object in the dispatch chain.
        The VirtualHost dispatcher adds a prefix to the URL and calls
        another dispatcher. Defaults to cherrypy.dispatch.Dispatcher().
    
    use_x_forwarded_host
        If True (the default), any "X-Forwarded-Host"
        request header will be used instead of the "Host" header. This
        is commonly added by HTTP servers (such as Apache) when proxying.
    
    ``**domains``
        A dict of {host header value: virtual prefix} pairs.
        The incoming "Host" request header is looked up in this dict,
        and, if a match is found, the corresponding "virtual prefix"
        value will be prepended to the URL path before calling the
        next dispatcher. Note that you often need separate entries
        for "example.com" and "www.example.com". In addition, "Host"
        headers may contain the port number.
    """
    from cherrypy.lib import httputil
    def vhost_dispatch(path_info):
        request = cherrypy.serving.request
        header = request.headers.get
        
        domain = header('Host', '')
        if use_x_forwarded_host:
            domain = header("X-Forwarded-Host", domain)
        
        prefix = domains.get(domain, "")
        if prefix:
            path_info = httputil.urljoin(prefix, path_info)
        
        result = next_dispatcher(path_info)
        
        # Touch up staticdir config. See http://www.cherrypy.org/ticket/614.
        section = request.config.get('tools.staticdir.section')
        if section:
            section = section[len(prefix):]
            request.config['tools.staticdir.section'] = section
        
        return result
    return vhost_dispatch


########NEW FILE########
__FILENAME__ = _cperror
"""Exception classes for CherryPy.

CherryPy provides (and uses) exceptions for declaring that the HTTP response
should be a status other than the default "200 OK". You can ``raise`` them like
normal Python exceptions. You can also call them and they will raise themselves;
this means you can set an :class:`HTTPError<cherrypy._cperror.HTTPError>`
or :class:`HTTPRedirect<cherrypy._cperror.HTTPRedirect>` as the
:attr:`request.handler<cherrypy._cprequest.Request.handler>`.

.. _redirectingpost:

Redirecting POST
================

When you GET a resource and are redirected by the server to another Location,
there's generally no problem since GET is both a "safe method" (there should
be no side-effects) and an "idempotent method" (multiple calls are no different
than a single call).

POST, however, is neither safe nor idempotent--if you
charge a credit card, you don't want to be charged twice by a redirect!

For this reason, *none* of the 3xx responses permit a user-agent (browser) to
resubmit a POST on redirection without first confirming the action with the user:

=====    =================================    ===========
300      Multiple Choices                     Confirm with the user
301      Moved Permanently                    Confirm with the user
302      Found (Object moved temporarily)     Confirm with the user
303      See Other                            GET the new URI--no confirmation
304      Not modified                         (for conditional GET only--POST should not raise this error)
305      Use Proxy                            Confirm with the user
307      Temporary Redirect                   Confirm with the user
=====    =================================    ===========

However, browsers have historically implemented these restrictions poorly;
in particular, many browsers do not force the user to confirm 301, 302
or 307 when redirecting POST. For this reason, CherryPy defaults to 303,
which most user-agents appear to have implemented correctly. Therefore, if
you raise HTTPRedirect for a POST request, the user-agent will most likely
attempt to GET the new URI (without asking for confirmation from the user).
We realize this is confusing for developers, but it's the safest thing we
could do. You are of course free to raise ``HTTPRedirect(uri, status=302)``
or any other 3xx status if you know what you're doing, but given the
environment, we couldn't let any of those be the default.

Custom Error Handling
=====================

.. image:: /refman/cperrors.gif

Anticipated HTTP responses
--------------------------

The 'error_page' config namespace can be used to provide custom HTML output for
expected responses (like 404 Not Found). Supply a filename from which the output
will be read. The contents will be interpolated with the values %(status)s,
%(message)s, %(traceback)s, and %(version)s using plain old Python
`string formatting <http://www.python.org/doc/2.6.4/library/stdtypes.html#string-formatting-operations>`_.

::

    _cp_config = {'error_page.404': os.path.join(localDir, "static/index.html")}


Beginning in version 3.1, you may also provide a function or other callable as
an error_page entry. It will be passed the same status, message, traceback and
version arguments that are interpolated into templates::

    def error_page_402(status, message, traceback, version):
        return "Error %s - Well, I'm very sorry but you haven't paid!" % status
    cherrypy.config.update({'error_page.402': error_page_402})

Also in 3.1, in addition to the numbered error codes, you may also supply
"error_page.default" to handle all codes which do not have their own error_page entry.



Unanticipated errors
--------------------

CherryPy also has a generic error handling mechanism: whenever an unanticipated
error occurs in your code, it will call
:func:`Request.error_response<cherrypy._cprequest.Request.error_response>` to set
the response status, headers, and body. By default, this is the same output as
:class:`HTTPError(500) <cherrypy._cperror.HTTPError>`. If you want to provide
some other behavior, you generally replace "request.error_response".

Here is some sample code that shows how to display a custom error message and
send an e-mail containing the error::

    from cherrypy import _cperror

    def handle_error():
        cherrypy.response.status = 500
        cherrypy.response.body = ["<html><body>Sorry, an error occured</body></html>"]
        sendMail('error@domain.com', 'Error in your web app', _cperror.format_exc())

    class Root:
        _cp_config = {'request.error_response': handle_error}


Note that you have to explicitly set :attr:`response.body <cherrypy._cprequest.Response.body>`
and not simply return an error message as a result.
"""

from cgi import escape as _escape
from sys import exc_info as _exc_info
from traceback import format_exception as _format_exception
from cherrypy._cpcompat import basestring, bytestr, iteritems, ntob, tonative, urljoin as _urljoin
from cherrypy.lib import httputil as _httputil


class CherryPyException(Exception):
    """A base class for CherryPy exceptions."""
    pass


class TimeoutError(CherryPyException):
    """Exception raised when Response.timed_out is detected."""
    pass


class InternalRedirect(CherryPyException):
    """Exception raised to switch to the handler for a different URL.
    
    This exception will redirect processing to another path within the site
    (without informing the client). Provide the new path as an argument when
    raising the exception. Provide any params in the querystring for the new URL.
    """
    
    def __init__(self, path, query_string=""):
        import cherrypy
        self.request = cherrypy.serving.request
        
        self.query_string = query_string
        if "?" in path:
            # Separate any params included in the path
            path, self.query_string = path.split("?", 1)
        
        # Note that urljoin will "do the right thing" whether url is:
        #  1. a URL relative to root (e.g. "/dummy")
        #  2. a URL relative to the current path
        # Note that any query string will be discarded.
        path = _urljoin(self.request.path_info, path)
        
        # Set a 'path' member attribute so that code which traps this
        # error can have access to it.
        self.path = path
        
        CherryPyException.__init__(self, path, self.query_string)


class HTTPRedirect(CherryPyException):
    """Exception raised when the request should be redirected.
    
    This exception will force a HTTP redirect to the URL or URL's you give it.
    The new URL must be passed as the first argument to the Exception,
    e.g., HTTPRedirect(newUrl). Multiple URLs are allowed in a list.
    If a URL is absolute, it will be used as-is. If it is relative, it is
    assumed to be relative to the current cherrypy.request.path_info.

    If one of the provided URL is a unicode object, it will be encoded
    using the default encoding or the one passed in parameter.
    
    There are multiple types of redirect, from which you can select via the
    ``status`` argument. If you do not provide a ``status`` arg, it defaults to
    303 (or 302 if responding with HTTP/1.0).
    
    Examples::
    
        raise cherrypy.HTTPRedirect("")
        raise cherrypy.HTTPRedirect("/abs/path", 307)
        raise cherrypy.HTTPRedirect(["path1", "path2?a=1&b=2"], 301)
    
    See :ref:`redirectingpost` for additional caveats.
    """
    
    status = None
    """The integer HTTP status code to emit."""
    
    urls = None
    """The list of URL's to emit."""

    encoding = 'utf-8'
    """The encoding when passed urls are not native strings"""
    
    def __init__(self, urls, status=None, encoding=None):
        import cherrypy
        request = cherrypy.serving.request
        
        if isinstance(urls, basestring):
            urls = [urls]
        
        abs_urls = []
        for url in urls:
            url = tonative(url, encoding or self.encoding)
                
            # Note that urljoin will "do the right thing" whether url is:
            #  1. a complete URL with host (e.g. "http://www.example.com/test")
            #  2. a URL relative to root (e.g. "/dummy")
            #  3. a URL relative to the current path
            # Note that any query string in cherrypy.request is discarded.
            url = _urljoin(cherrypy.url(), url)
            abs_urls.append(url)
        self.urls = abs_urls
        
        # RFC 2616 indicates a 301 response code fits our goal; however,
        # browser support for 301 is quite messy. Do 302/303 instead. See
        # http://www.alanflavell.org.uk/www/post-redirect.html
        if status is None:
            if request.protocol >= (1, 1):
                status = 303
            else:
                status = 302
        else:
            status = int(status)
            if status < 300 or status > 399:
                raise ValueError("status must be between 300 and 399.")
        
        self.status = status
        CherryPyException.__init__(self, abs_urls, status)
    
    def set_response(self):
        """Modify cherrypy.response status, headers, and body to represent self.
        
        CherryPy uses this internally, but you can also use it to create an
        HTTPRedirect object and set its output without *raising* the exception.
        """
        import cherrypy
        response = cherrypy.serving.response
        response.status = status = self.status
        
        if status in (300, 301, 302, 303, 307):
            response.headers['Content-Type'] = "text/html;charset=utf-8"
            # "The ... URI SHOULD be given by the Location field
            # in the response."
            response.headers['Location'] = self.urls[0]
            
            # "Unless the request method was HEAD, the entity of the response
            # SHOULD contain a short hypertext note with a hyperlink to the
            # new URI(s)."
            msg = {300: "This resource can be found at <a href='%s'>%s</a>.",
                   301: "This resource has permanently moved to <a href='%s'>%s</a>.",
                   302: "This resource resides temporarily at <a href='%s'>%s</a>.",
                   303: "This resource can be found at <a href='%s'>%s</a>.",
                   307: "This resource has moved temporarily to <a href='%s'>%s</a>.",
                   }[status]
            msgs = [msg % (u, u) for u in self.urls]
            response.body = ntob("<br />\n".join(msgs), 'utf-8')
            # Previous code may have set C-L, so we have to reset it
            # (allow finalize to set it).
            response.headers.pop('Content-Length', None)
        elif status == 304:
            # Not Modified.
            # "The response MUST include the following header fields:
            # Date, unless its omission is required by section 14.18.1"
            # The "Date" header should have been set in Response.__init__
            
            # "...the response SHOULD NOT include other entity-headers."
            for key in ('Allow', 'Content-Encoding', 'Content-Language',
                        'Content-Length', 'Content-Location', 'Content-MD5',
                        'Content-Range', 'Content-Type', 'Expires',
                        'Last-Modified'):
                if key in response.headers:
                    del response.headers[key]
            
            # "The 304 response MUST NOT contain a message-body."
            response.body = None
            # Previous code may have set C-L, so we have to reset it.
            response.headers.pop('Content-Length', None)
        elif status == 305:
            # Use Proxy.
            # self.urls[0] should be the URI of the proxy.
            response.headers['Location'] = self.urls[0]
            response.body = None
            # Previous code may have set C-L, so we have to reset it.
            response.headers.pop('Content-Length', None)
        else:
            raise ValueError("The %s status code is unknown." % status)
    
    def __call__(self):
        """Use this exception as a request.handler (raise self)."""
        raise self


def clean_headers(status):
    """Remove any headers which should not apply to an error response."""
    import cherrypy
    
    response = cherrypy.serving.response
    
    # Remove headers which applied to the original content,
    # but do not apply to the error page.
    respheaders = response.headers
    for key in ["Accept-Ranges", "Age", "ETag", "Location", "Retry-After",
                "Vary", "Content-Encoding", "Content-Length", "Expires",
                "Content-Location", "Content-MD5", "Last-Modified"]:
        if key in respheaders:
            del respheaders[key]
    
    if status != 416:
        # A server sending a response with status code 416 (Requested
        # range not satisfiable) SHOULD include a Content-Range field
        # with a byte-range-resp-spec of "*". The instance-length
        # specifies the current length of the selected resource.
        # A response with status code 206 (Partial Content) MUST NOT
        # include a Content-Range field with a byte-range- resp-spec of "*".
        if "Content-Range" in respheaders:
            del respheaders["Content-Range"]


class HTTPError(CherryPyException):
    """Exception used to return an HTTP error code (4xx-5xx) to the client.
    
    This exception can be used to automatically send a response using a http status
    code, with an appropriate error page. It takes an optional
    ``status`` argument (which must be between 400 and 599); it defaults to 500
    ("Internal Server Error"). It also takes an optional ``message`` argument,
    which will be returned in the response body. See
    `RFC 2616 <http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4>`_
    for a complete list of available error codes and when to use them.
    
    Examples::
        
        raise cherrypy.HTTPError(403)
        raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
    """
    
    status = None
    """The HTTP status code. May be of type int or str (with a Reason-Phrase)."""
    
    code = None
    """The integer HTTP status code."""
    
    reason = None
    """The HTTP Reason-Phrase string."""
    
    def __init__(self, status=500, message=None):
        self.status = status
        try:
            self.code, self.reason, defaultmsg = _httputil.valid_status(status)
        except ValueError:
            raise self.__class__(500, _exc_info()[1].args[0])
        
        if self.code < 400 or self.code > 599:
            raise ValueError("status must be between 400 and 599.")
        
        # See http://www.python.org/dev/peps/pep-0352/
        # self.message = message
        self._message = message or defaultmsg
        CherryPyException.__init__(self, status, message)
    
    def set_response(self):
        """Modify cherrypy.response status, headers, and body to represent self.
        
        CherryPy uses this internally, but you can also use it to create an
        HTTPError object and set its output without *raising* the exception.
        """
        import cherrypy
        
        response = cherrypy.serving.response
        
        clean_headers(self.code)
        
        # In all cases, finalize will be called after this method,
        # so don't bother cleaning up response values here.
        response.status = self.status
        tb = None
        if cherrypy.serving.request.show_tracebacks:
            tb = format_exc()
        response.headers['Content-Type'] = "text/html;charset=utf-8"
        response.headers.pop('Content-Length', None)
        
        content = ntob(self.get_error_page(self.status, traceback=tb,
                                           message=self._message), 'utf-8')
        response.body = content
        
        _be_ie_unfriendly(self.code)
    
    def get_error_page(self, *args, **kwargs):
        return get_error_page(*args, **kwargs)
    
    def __call__(self):
        """Use this exception as a request.handler (raise self)."""
        raise self


class NotFound(HTTPError):
    """Exception raised when a URL could not be mapped to any handler (404).
    
    This is equivalent to raising
    :class:`HTTPError("404 Not Found") <cherrypy._cperror.HTTPError>`.
    """
    
    def __init__(self, path=None):
        if path is None:
            import cherrypy
            request = cherrypy.serving.request
            path = request.script_name + request.path_info
        self.args = (path,)
        HTTPError.__init__(self, 404, "The path '%s' was not found." % path)


_HTTPErrorTemplate = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>
    <title>%(status)s</title>
    <style type="text/css">
    #powered_by {
        margin-top: 20px;
        border-top: 2px solid black;
        font-style: italic;
    }

    #traceback {
        color: red;
    }
    </style>
</head>
    <body>
        <h2>%(status)s</h2>
        <p>%(message)s</p>
        <pre id="traceback">%(traceback)s</pre>
    <div id="powered_by">
    <span>Powered by <a href="http://www.cherrypy.org">CherryPy %(version)s</a></span>
    </div>
    </body>
</html>
'''

def get_error_page(status, **kwargs):
    """Return an HTML page, containing a pretty error response.
    
    status should be an int or a str.
    kwargs will be interpolated into the page template.
    """
    import cherrypy
    
    try:
        code, reason, message = _httputil.valid_status(status)
    except ValueError:
        raise cherrypy.HTTPError(500, _exc_info()[1].args[0])
    
    # We can't use setdefault here, because some
    # callers send None for kwarg values.
    if kwargs.get('status') is None:
        kwargs['status'] = "%s %s" % (code, reason)
    if kwargs.get('message') is None:
        kwargs['message'] = message
    if kwargs.get('traceback') is None:
        kwargs['traceback'] = ''
    if kwargs.get('version') is None:
        kwargs['version'] = cherrypy.__version__
    
    for k, v in iteritems(kwargs):
        if v is None:
            kwargs[k] = ""
        else:
            kwargs[k] = _escape(kwargs[k])
    
    # Use a custom template or callable for the error page?
    pages = cherrypy.serving.request.error_page
    error_page = pages.get(code) or pages.get('default')
    if error_page:
        try:
            if hasattr(error_page, '__call__'):
                return error_page(**kwargs)
            else:
                data = open(error_page, 'rb').read()
                return tonative(data) % kwargs
        except:
            e = _format_exception(*_exc_info())[-1]
            m = kwargs['message']
            if m:
                m += "<br />"
            m += "In addition, the custom error page failed:\n<br />%s" % e
            kwargs['message'] = m
    
    return _HTTPErrorTemplate % kwargs


_ie_friendly_error_sizes = {
    400: 512, 403: 256, 404: 512, 405: 256,
    406: 512, 408: 512, 409: 512, 410: 256,
    500: 512, 501: 512, 505: 512,
    }


def _be_ie_unfriendly(status):
    import cherrypy
    response = cherrypy.serving.response
    
    # For some statuses, Internet Explorer 5+ shows "friendly error
    # messages" instead of our response.body if the body is smaller
    # than a given size. Fix this by returning a body over that size
    # (by adding whitespace).
    # See http://support.microsoft.com/kb/q218155/
    s = _ie_friendly_error_sizes.get(status, 0)
    if s:
        s += 1
        # Since we are issuing an HTTP error status, we assume that
        # the entity is short, and we should just collapse it.
        content = response.collapse_body()
        l = len(content)
        if l and l < s:
            # IN ADDITION: the response must be written to IE
            # in one chunk or it will still get replaced! Bah.
            content = content + (ntob(" ") * (s - l))
        response.body = content
        response.headers['Content-Length'] = str(len(content))


def format_exc(exc=None):
    """Return exc (or sys.exc_info if None), formatted."""
    try:
        if exc is None:
            exc = _exc_info()
        if exc == (None, None, None):
            return ""
        import traceback
        return "".join(traceback.format_exception(*exc))
    finally:
        del exc

def bare_error(extrabody=None):
    """Produce status, headers, body for a critical error.
    
    Returns a triple without calling any other questionable functions,
    so it should be as error-free as possible. Call it from an HTTP server
    if you get errors outside of the request.
    
    If extrabody is None, a friendly but rather unhelpful error message
    is set in the body. If extrabody is a string, it will be appended
    as-is to the body.
    """
    
    # The whole point of this function is to be a last line-of-defense
    # in handling errors. That is, it must not raise any errors itself;
    # it cannot be allowed to fail. Therefore, don't add to it!
    # In particular, don't call any other CP functions.
    
    body = ntob("Unrecoverable error in the server.")
    if extrabody is not None:
        if not isinstance(extrabody, bytestr):
            extrabody = extrabody.encode('utf-8')
        body += ntob("\n") + extrabody
    
    return (ntob("500 Internal Server Error"),
            [(ntob('Content-Type'), ntob('text/plain')),
             (ntob('Content-Length'), ntob(str(len(body)),'ISO-8859-1'))],
            [body])



########NEW FILE########
__FILENAME__ = _cplogging
"""
Simple config
=============

Although CherryPy uses the :mod:`Python logging module <logging>`, it does so
behind the scenes so that simple logging is simple, but complicated logging
is still possible. "Simple" logging means that you can log to the screen
(i.e. console/stdout) or to a file, and that you can easily have separate
error and access log files.

Here are the simplified logging settings. You use these by adding lines to
your config file or dict. You should set these at either the global level or
per application (see next), but generally not both.

 * ``log.screen``: Set this to True to have both "error" and "access" messages
   printed to stdout.
 * ``log.access_file``: Set this to an absolute filename where you want
   "access" messages written.
 * ``log.error_file``: Set this to an absolute filename where you want "error"
   messages written.

Many events are automatically logged; to log your own application events, call
:func:`cherrypy.log`.

Architecture
============

Separate scopes
---------------

CherryPy provides log managers at both the global and application layers.
This means you can have one set of logging rules for your entire site,
and another set of rules specific to each application. The global log
manager is found at :func:`cherrypy.log`, and the log manager for each
application is found at :attr:`app.log<cherrypy._cptree.Application.log>`.
If you're inside a request, the latter is reachable from
``cherrypy.request.app.log``; if you're outside a request, you'll have to obtain
a reference to the ``app``: either the return value of
:func:`tree.mount()<cherrypy._cptree.Tree.mount>` or, if you used
:func:`quickstart()<cherrypy.quickstart>` instead, via ``cherrypy.tree.apps['/']``.

By default, the global logs are named "cherrypy.error" and "cherrypy.access",
and the application logs are named "cherrypy.error.2378745" and
"cherrypy.access.2378745" (the number is the id of the Application object).
This means that the application logs "bubble up" to the site logs, so if your
application has no log handlers, the site-level handlers will still log the
messages.

Errors vs. Access
-----------------

Each log manager handles both "access" messages (one per HTTP request) and
"error" messages (everything else). Note that the "error" log is not just for
errors! The format of access messages is highly formalized, but the error log
isn't--it receives messages from a variety of sources (including full error
tracebacks, if enabled).


Custom Handlers
===============

The simple settings above work by manipulating Python's standard :mod:`logging`
module. So when you need something more complex, the full power of the standard
module is yours to exploit. You can borrow or create custom handlers, formats,
filters, and much more. Here's an example that skips the standard FileHandler
and uses a RotatingFileHandler instead:

::

    #python
    log = app.log
    
    # Remove the default FileHandlers if present.
    log.error_file = ""
    log.access_file = ""
    
    maxBytes = getattr(log, "rot_maxBytes", 10000000)
    backupCount = getattr(log, "rot_backupCount", 1000)
    
    # Make a new RotatingFileHandler for the error log.
    fname = getattr(log, "rot_error_file", "error.log")
    h = handlers.RotatingFileHandler(fname, 'a', maxBytes, backupCount)
    h.setLevel(DEBUG)
    h.setFormatter(_cplogging.logfmt)
    log.error_log.addHandler(h)
    
    # Make a new RotatingFileHandler for the access log.
    fname = getattr(log, "rot_access_file", "access.log")
    h = handlers.RotatingFileHandler(fname, 'a', maxBytes, backupCount)
    h.setLevel(DEBUG)
    h.setFormatter(_cplogging.logfmt)
    log.access_log.addHandler(h)


The ``rot_*`` attributes are pulled straight from the application log object.
Since "log.*" config entries simply set attributes on the log object, you can
add custom attributes to your heart's content. Note that these handlers are
used ''instead'' of the default, simple handlers outlined above (so don't set
the "log.error_file" config entry, for example).
"""

import datetime
import logging
# Silence the no-handlers "warning" (stderr write!) in stdlib logging
logging.Logger.manager.emittedNoHandlerWarning = 1
logfmt = logging.Formatter("%(message)s")
import os
import sys

import cherrypy
from cherrypy import _cperror
from cherrypy._cpcompat import ntob, py3k


class NullHandler(logging.Handler):
    """A no-op logging handler to silence the logging.lastResort handler."""

    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None


class LogManager(object):
    """An object to assist both simple and advanced logging.
    
    ``cherrypy.log`` is an instance of this class.
    """
    
    appid = None
    """The id() of the Application object which owns this log manager. If this
    is a global log manager, appid is None."""
   
    error_log = None
    """The actual :class:`logging.Logger` instance for error messages."""
    
    access_log = None
    """The actual :class:`logging.Logger` instance for access messages."""
    
    if py3k:
        access_log_format = \
            '{h} {l} {u} {t} "{r}" {s} {b} "{f}" "{a}"'
    else:
        access_log_format = \
            '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
    
    logger_root = None
    """The "top-level" logger name.
    
    This string will be used as the first segment in the Logger names.
    The default is "cherrypy", for example, in which case the Logger names
    will be of the form::
    
        cherrypy.error.<appid>
        cherrypy.access.<appid>
    """
    
    def __init__(self, appid=None, logger_root="cherrypy"):
        self.logger_root = logger_root
        self.appid = appid
        if appid is None:
            self.error_log = logging.getLogger("%s.error" % logger_root)
            self.access_log = logging.getLogger("%s.access" % logger_root)
        else:
            self.error_log = logging.getLogger("%s.error.%s" % (logger_root, appid))
            self.access_log = logging.getLogger("%s.access.%s" % (logger_root, appid))
        self.error_log.setLevel(logging.INFO)
        self.access_log.setLevel(logging.INFO)

        # Silence the no-handlers "warning" (stderr write!) in stdlib logging
        self.error_log.addHandler(NullHandler())
        self.access_log.addHandler(NullHandler())

        cherrypy.engine.subscribe('graceful', self.reopen_files)

    def reopen_files(self):
        """Close and reopen all file handlers."""
        for log in (self.error_log, self.access_log):
            for h in log.handlers:
                if isinstance(h, logging.FileHandler):
                    h.acquire()
                    h.stream.close()
                    h.stream = open(h.baseFilename, h.mode)
                    h.release()
    
    def error(self, msg='', context='', severity=logging.INFO, traceback=False):
        """Write the given ``msg`` to the error log.
        
        This is not just for errors! Applications may call this at any time
        to log application-specific information.
        
        If ``traceback`` is True, the traceback of the current exception
        (if any) will be appended to ``msg``.
        """
        if traceback:
            msg += _cperror.format_exc()
        self.error_log.log(severity, ' '.join((self.time(), context, msg)))
    
    def __call__(self, *args, **kwargs):
        """An alias for ``error``."""
        return self.error(*args, **kwargs)
    
    def access(self):
        """Write to the access log (in Apache/NCSA Combined Log format).
        
        See http://httpd.apache.org/docs/2.0/logs.html#combined for format
        details.
        
        CherryPy calls this automatically for you. Note there are no arguments;
        it collects the data itself from
        :class:`cherrypy.request<cherrypy._cprequest.Request>`.
        
        Like Apache started doing in 2.0.46, non-printable and other special
        characters in %r (and we expand that to all parts) are escaped using
        \\xhh sequences, where hh stands for the hexadecimal representation
        of the raw byte. Exceptions from this rule are " and \\, which are
        escaped by prepending a backslash, and all whitespace characters,
        which are written in their C-style notation (\\n, \\t, etc).
        """
        request = cherrypy.serving.request
        remote = request.remote
        response = cherrypy.serving.response
        outheaders = response.headers
        inheaders = request.headers
        if response.output_status is None:
            status = "-"
        else:
            status = response.output_status.split(ntob(" "), 1)[0]
            if py3k:
                status = status.decode('ISO-8859-1')
        
        atoms = {'h': remote.name or remote.ip,
                 'l': '-',
                 'u': getattr(request, "login", None) or "-",
                 't': self.time(),
                 'r': request.request_line,
                 's': status,
                 'b': dict.get(outheaders, 'Content-Length', '') or "-",
                 'f': dict.get(inheaders, 'Referer', ''),
                 'a': dict.get(inheaders, 'User-Agent', ''),
                 }
        if py3k:
            for k, v in atoms.items():
                if not isinstance(v, str):
                    v = str(v)
                v = v.replace('"', '\\"').encode('utf8')
                # Fortunately, repr(str) escapes unprintable chars, \n, \t, etc
                # and backslash for us. All we have to do is strip the quotes.
                v = repr(v)[2:-1]
                
                # in python 3.0 the repr of bytes (as returned by encode) 
                # uses double \'s.  But then the logger escapes them yet, again
                # resulting in quadruple slashes.  Remove the extra one here.
                v = v.replace('\\\\', '\\')
                
                # Escape double-quote.
                atoms[k] = v
            
            try:
                self.access_log.log(logging.INFO, self.access_log_format.format(**atoms))
            except:
                self(traceback=True)
        else:
            for k, v in atoms.items():
                if isinstance(v, unicode):
                    v = v.encode('utf8')
                elif not isinstance(v, str):
                    v = str(v)
                # Fortunately, repr(str) escapes unprintable chars, \n, \t, etc
                # and backslash for us. All we have to do is strip the quotes.
                v = repr(v)[1:-1]
                # Escape double-quote.
                atoms[k] = v.replace('"', '\\"')
            
            try:
                self.access_log.log(logging.INFO, self.access_log_format % atoms)
            except:
                self(traceback=True)
    
    def time(self):
        """Return now() in Apache Common Log Format (no timezone)."""
        now = datetime.datetime.now()
        monthnames = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        month = monthnames[now.month - 1].capitalize()
        return ('[%02d/%s/%04d:%02d:%02d:%02d]' %
                (now.day, month, now.year, now.hour, now.minute, now.second))
    
    def _get_builtin_handler(self, log, key):
        for h in log.handlers:
            if getattr(h, "_cpbuiltin", None) == key:
                return h
    
    
    # ------------------------- Screen handlers ------------------------- #
    
    def _set_screen_handler(self, log, enable, stream=None):
        h = self._get_builtin_handler(log, "screen")
        if enable:
            if not h:
                if stream is None:
                    stream=sys.stderr
                h = logging.StreamHandler(stream)
                h.setFormatter(logfmt)
                h._cpbuiltin = "screen"
                log.addHandler(h)
        elif h:
            log.handlers.remove(h)
    
    def _get_screen(self):
        h = self._get_builtin_handler
        has_h = h(self.error_log, "screen") or h(self.access_log, "screen")
        return bool(has_h)
    
    def _set_screen(self, newvalue):
        self._set_screen_handler(self.error_log, newvalue, stream=sys.stderr)
        self._set_screen_handler(self.access_log, newvalue, stream=sys.stdout)
    screen = property(_get_screen, _set_screen,
        doc="""Turn stderr/stdout logging on or off.
        
        If you set this to True, it'll add the appropriate StreamHandler for
        you. If you set it to False, it will remove the handler.
        """)
    
    # -------------------------- File handlers -------------------------- #
    
    def _add_builtin_file_handler(self, log, fname):
        h = logging.FileHandler(fname)
        h.setFormatter(logfmt)
        h._cpbuiltin = "file"
        log.addHandler(h)
    
    def _set_file_handler(self, log, filename):
        h = self._get_builtin_handler(log, "file")
        if filename:
            if h:
                if h.baseFilename != os.path.abspath(filename):
                    h.close()
                    log.handlers.remove(h)
                    self._add_builtin_file_handler(log, filename)
            else:
                self._add_builtin_file_handler(log, filename)
        else:
            if h:
                h.close()
                log.handlers.remove(h)
    
    def _get_error_file(self):
        h = self._get_builtin_handler(self.error_log, "file")
        if h:
            return h.baseFilename
        return ''
    def _set_error_file(self, newvalue):
        self._set_file_handler(self.error_log, newvalue)
    error_file = property(_get_error_file, _set_error_file,
        doc="""The filename for self.error_log.
        
        If you set this to a string, it'll add the appropriate FileHandler for
        you. If you set it to ``None`` or ``''``, it will remove the handler.
        """)
    
    def _get_access_file(self):
        h = self._get_builtin_handler(self.access_log, "file")
        if h:
            return h.baseFilename
        return ''
    def _set_access_file(self, newvalue):
        self._set_file_handler(self.access_log, newvalue)
    access_file = property(_get_access_file, _set_access_file,
        doc="""The filename for self.access_log.
        
        If you set this to a string, it'll add the appropriate FileHandler for
        you. If you set it to ``None`` or ``''``, it will remove the handler.
        """)
    
    # ------------------------- WSGI handlers ------------------------- #
    
    def _set_wsgi_handler(self, log, enable):
        h = self._get_builtin_handler(log, "wsgi")
        if enable:
            if not h:
                h = WSGIErrorHandler()
                h.setFormatter(logfmt)
                h._cpbuiltin = "wsgi"
                log.addHandler(h)
        elif h:
            log.handlers.remove(h)
    
    def _get_wsgi(self):
        return bool(self._get_builtin_handler(self.error_log, "wsgi"))
    
    def _set_wsgi(self, newvalue):
        self._set_wsgi_handler(self.error_log, newvalue)
    wsgi = property(_get_wsgi, _set_wsgi,
        doc="""Write errors to wsgi.errors.
        
        If you set this to True, it'll add the appropriate
        :class:`WSGIErrorHandler<cherrypy._cplogging.WSGIErrorHandler>` for you
        (which writes errors to ``wsgi.errors``).
        If you set it to False, it will remove the handler.
        """)


class WSGIErrorHandler(logging.Handler):
    "A handler class which writes logging records to environ['wsgi.errors']."
    
    def flush(self):
        """Flushes the stream."""
        try:
            stream = cherrypy.serving.request.wsgi_environ.get('wsgi.errors')
        except (AttributeError, KeyError):
            pass
        else:
            stream.flush()
    
    def emit(self, record):
        """Emit a record."""
        try:
            stream = cherrypy.serving.request.wsgi_environ.get('wsgi.errors')
        except (AttributeError, KeyError):
            pass
        else:
            try:
                msg = self.format(record)
                fs = "%s\n"
                import types
                if not hasattr(types, "UnicodeType"): #if no unicode support...
                    stream.write(fs % msg)
                else:
                    try:
                        stream.write(fs % msg)
                    except UnicodeError:
                        stream.write(fs % msg.encode("UTF-8"))
                self.flush()
            except:
                self.handleError(record)

########NEW FILE########
__FILENAME__ = _cpmodpy
"""Native adapter for serving CherryPy via mod_python

Basic usage:

##########################################
# Application in a module called myapp.py
##########################################

import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        return 'Hi there, Ho there, Hey there'


# We will use this method from the mod_python configuration
# as the entry point to our application
def setup_server():
    cherrypy.tree.mount(Root())
    cherrypy.config.update({'environment': 'production',
                            'log.screen': False,
                            'show_tracebacks': False})

##########################################
# mod_python settings for apache2
# This should reside in your httpd.conf
# or a file that will be loaded at
# apache startup
##########################################

# Start
DocumentRoot "/"
Listen 8080
LoadModule python_module /usr/lib/apache2/modules/mod_python.so

<Location "/">
	PythonPath "sys.path+['/path/to/my/application']" 
	SetHandler python-program
	PythonHandler cherrypy._cpmodpy::handler
	PythonOption cherrypy.setup myapp::setup_server
	PythonDebug On
</Location> 
# End

The actual path to your mod_python.so is dependent on your
environment. In this case we suppose a global mod_python
installation on a Linux distribution such as Ubuntu.

We do set the PythonPath configuration setting so that
your application can be found by from the user running
the apache2 instance. Of course if your application
resides in the global site-package this won't be needed.

Then restart apache2 and access http://127.0.0.1:8080
"""

import logging
import sys

import cherrypy
from cherrypy._cpcompat import BytesIO, copyitems, ntob
from cherrypy._cperror import format_exc, bare_error
from cherrypy.lib import httputil


# ------------------------------ Request-handling



def setup(req):
    from mod_python import apache
    
    # Run any setup functions defined by a "PythonOption cherrypy.setup" directive.
    options = req.get_options()
    if 'cherrypy.setup' in options:
        for function in options['cherrypy.setup'].split():
            atoms = function.split('::', 1)
            if len(atoms) == 1:
                mod = __import__(atoms[0], globals(), locals())
            else:
                modname, fname = atoms
                mod = __import__(modname, globals(), locals(), [fname])
                func = getattr(mod, fname)
                func()
    
    cherrypy.config.update({'log.screen': False,
                            "tools.ignore_headers.on": True,
                            "tools.ignore_headers.headers": ['Range'],
                            })
    
    engine = cherrypy.engine
    if hasattr(engine, "signal_handler"):
        engine.signal_handler.unsubscribe()
    if hasattr(engine, "console_control_handler"):
        engine.console_control_handler.unsubscribe()
    engine.autoreload.unsubscribe()
    cherrypy.server.unsubscribe()
    
    def _log(msg, level):
        newlevel = apache.APLOG_ERR
        if logging.DEBUG >= level:
            newlevel = apache.APLOG_DEBUG
        elif logging.INFO >= level:
            newlevel = apache.APLOG_INFO
        elif logging.WARNING >= level:
            newlevel = apache.APLOG_WARNING
        # On Windows, req.server is required or the msg will vanish. See
        # http://www.modpython.org/pipermail/mod_python/2003-October/014291.html.
        # Also, "When server is not specified...LogLevel does not apply..."
        apache.log_error(msg, newlevel, req.server)
    engine.subscribe('log', _log)
    
    engine.start()
    
    def cherrypy_cleanup(data):
        engine.exit()
    try:
        # apache.register_cleanup wasn't available until 3.1.4.
        apache.register_cleanup(cherrypy_cleanup)
    except AttributeError:
        req.server.register_cleanup(req, cherrypy_cleanup)


class _ReadOnlyRequest:
    expose = ('read', 'readline', 'readlines')
    def __init__(self, req):
        for method in self.expose:
            self.__dict__[method] = getattr(req, method)


recursive = False

_isSetUp = False
def handler(req):
    from mod_python import apache
    try:
        global _isSetUp
        if not _isSetUp:
            setup(req)
            _isSetUp = True
        
        # Obtain a Request object from CherryPy
        local = req.connection.local_addr
        local = httputil.Host(local[0], local[1], req.connection.local_host or "")
        remote = req.connection.remote_addr
        remote = httputil.Host(remote[0], remote[1], req.connection.remote_host or "")
        
        scheme = req.parsed_uri[0] or 'http'
        req.get_basic_auth_pw()
        
        try:
            # apache.mpm_query only became available in mod_python 3.1
            q = apache.mpm_query
            threaded = q(apache.AP_MPMQ_IS_THREADED)
            forked = q(apache.AP_MPMQ_IS_FORKED)
        except AttributeError:
            bad_value = ("You must provide a PythonOption '%s', "
                         "either 'on' or 'off', when running a version "
                         "of mod_python < 3.1")
            
            threaded = options.get('multithread', '').lower()
            if threaded == 'on':
                threaded = True
            elif threaded == 'off':
                threaded = False
            else:
                raise ValueError(bad_value % "multithread")
            
            forked = options.get('multiprocess', '').lower()
            if forked == 'on':
                forked = True
            elif forked == 'off':
                forked = False
            else:
                raise ValueError(bad_value % "multiprocess")
        
        sn = cherrypy.tree.script_name(req.uri or "/")
        if sn is None:
            send_response(req, '404 Not Found', [], '')
        else:
            app = cherrypy.tree.apps[sn]
            method = req.method
            path = req.uri
            qs = req.args or ""
            reqproto = req.protocol
            headers = copyitems(req.headers_in)
            rfile = _ReadOnlyRequest(req)
            prev = None
            
            try:
                redirections = []
                while True:
                    request, response = app.get_serving(local, remote, scheme,
                                                        "HTTP/1.1")
                    request.login = req.user
                    request.multithread = bool(threaded)
                    request.multiprocess = bool(forked)
                    request.app = app
                    request.prev = prev
                    
                    # Run the CherryPy Request object and obtain the response
                    try:
                        request.run(method, path, qs, reqproto, headers, rfile)
                        break
                    except cherrypy.InternalRedirect:
                        ir = sys.exc_info()[1]
                        app.release_serving()
                        prev = request
                        
                        if not recursive:
                            if ir.path in redirections:
                                raise RuntimeError("InternalRedirector visited the "
                                                   "same URL twice: %r" % ir.path)
                            else:
                                # Add the *previous* path_info + qs to redirections.
                                if qs:
                                    qs = "?" + qs
                                redirections.append(sn + path + qs)
                        
                        # Munge environment and try again.
                        method = "GET"
                        path = ir.path
                        qs = ir.query_string
                        rfile = BytesIO()
                
                send_response(req, response.output_status, response.header_list,
                              response.body, response.stream)
            finally:
                app.release_serving()
    except:
        tb = format_exc()
        cherrypy.log(tb, 'MOD_PYTHON', severity=logging.ERROR)
        s, h, b = bare_error()
        send_response(req, s, h, b)
    return apache.OK


def send_response(req, status, headers, body, stream=False):
    # Set response status
    req.status = int(status[:3])
    
    # Set response headers
    req.content_type = "text/plain"
    for header, value in headers:
        if header.lower() == 'content-type':
            req.content_type = value
            continue
        req.headers_out.add(header, value)
    
    if stream:
        # Flush now so the status and headers are sent immediately.
        req.flush()
    
    # Set response body
    if isinstance(body, basestring):
        req.write(body)
    else:
        for seg in body:
            req.write(seg)



# --------------- Startup tools for CherryPy + mod_python --------------- #


import os
import re
try:
    import subprocess
    def popen(fullcmd):
        p = subprocess.Popen(fullcmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             close_fds=True)
        return p.stdout
except ImportError:
    def popen(fullcmd):
        pipein, pipeout = os.popen4(fullcmd)
        return pipeout


def read_process(cmd, args=""):
    fullcmd = "%s %s" % (cmd, args)
    pipeout = popen(fullcmd)
    try:
        firstline = pipeout.readline()
        if (re.search(ntob("(not recognized|No such file|not found)"), firstline,
                      re.IGNORECASE)):
            raise IOError('%s must be on your system path.' % cmd)
        output = firstline + pipeout.read()
    finally:
        pipeout.close()
    return output


class ModPythonServer(object):
    
    template = """
# Apache2 server configuration file for running CherryPy with mod_python.

DocumentRoot "/"
Listen %(port)s
LoadModule python_module modules/mod_python.so

<Location %(loc)s>
    SetHandler python-program
    PythonHandler %(handler)s
    PythonDebug On
%(opts)s
</Location>
"""
    
    def __init__(self, loc="/", port=80, opts=None, apache_path="apache",
                 handler="cherrypy._cpmodpy::handler"):
        self.loc = loc
        self.port = port
        self.opts = opts
        self.apache_path = apache_path
        self.handler = handler
    
    def start(self):
        opts = "".join(["    PythonOption %s %s\n" % (k, v)
                        for k, v in self.opts])
        conf_data = self.template % {"port": self.port,
                                     "loc": self.loc,
                                     "opts": opts,
                                     "handler": self.handler,
                                     }
        
        mpconf = os.path.join(os.path.dirname(__file__), "cpmodpy.conf")
        f = open(mpconf, 'wb')
        try:
            f.write(conf_data)
        finally:
            f.close()
        
        response = read_process(self.apache_path, "-k start -f %s" % mpconf)
        self.ready = True
        return response
    
    def stop(self):
        os.popen("apache -k stop")
        self.ready = False


########NEW FILE########
__FILENAME__ = _cpnative_server
"""Native adapter for serving CherryPy via its builtin server."""

import logging
import sys

import cherrypy
from cherrypy._cpcompat import BytesIO
from cherrypy._cperror import format_exc, bare_error
from cherrypy.lib import httputil
from cherrypy import wsgiserver


class NativeGateway(wsgiserver.Gateway):
    
    recursive = False
    
    def respond(self):
        req = self.req
        try:
            # Obtain a Request object from CherryPy
            local = req.server.bind_addr
            local = httputil.Host(local[0], local[1], "")
            remote = req.conn.remote_addr, req.conn.remote_port
            remote = httputil.Host(remote[0], remote[1], "")
            
            scheme = req.scheme
            sn = cherrypy.tree.script_name(req.uri or "/")
            if sn is None:
                self.send_response('404 Not Found', [], [''])
            else:
                app = cherrypy.tree.apps[sn]
                method = req.method
                path = req.path
                qs = req.qs or ""
                headers = req.inheaders.items()
                rfile = req.rfile
                prev = None
                
                try:
                    redirections = []
                    while True:
                        request, response = app.get_serving(
                            local, remote, scheme, "HTTP/1.1")
                        request.multithread = True
                        request.multiprocess = False
                        request.app = app
                        request.prev = prev
                        
                        # Run the CherryPy Request object and obtain the response
                        try:
                            request.run(method, path, qs, req.request_protocol, headers, rfile)
                            break
                        except cherrypy.InternalRedirect:
                            ir = sys.exc_info()[1]
                            app.release_serving()
                            prev = request
                            
                            if not self.recursive:
                                if ir.path in redirections:
                                    raise RuntimeError("InternalRedirector visited the "
                                                       "same URL twice: %r" % ir.path)
                                else:
                                    # Add the *previous* path_info + qs to redirections.
                                    if qs:
                                        qs = "?" + qs
                                    redirections.append(sn + path + qs)
                            
                            # Munge environment and try again.
                            method = "GET"
                            path = ir.path
                            qs = ir.query_string
                            rfile = BytesIO()
                    
                    self.send_response(
                        response.output_status, response.header_list,
                        response.body)
                finally:
                    app.release_serving()
        except:
            tb = format_exc()
            #print tb
            cherrypy.log(tb, 'NATIVE_ADAPTER', severity=logging.ERROR)
            s, h, b = bare_error()
            self.send_response(s, h, b)
    
    def send_response(self, status, headers, body):
        req = self.req
        
        # Set response status
        req.status = str(status or "500 Server Error")
        
        # Set response headers
        for header, value in headers:
            req.outheaders.append((header, value))
        if (req.ready and not req.sent_headers):
            req.sent_headers = True
            req.send_headers()
        
        # Set response body
        for seg in body:
            req.write(seg)


class CPHTTPServer(wsgiserver.HTTPServer):
    """Wrapper for wsgiserver.HTTPServer.
    
    wsgiserver has been designed to not reference CherryPy in any way,
    so that it can be used in other frameworks and applications.
    Therefore, we wrap it here, so we can apply some attributes
    from config -> cherrypy.server -> HTTPServer.
    """
    
    def __init__(self, server_adapter=cherrypy.server):
        self.server_adapter = server_adapter
        
        server_name = (self.server_adapter.socket_host or
                       self.server_adapter.socket_file or
                       None)
        
        wsgiserver.HTTPServer.__init__(
            self, server_adapter.bind_addr, NativeGateway,
            minthreads=server_adapter.thread_pool,
            maxthreads=server_adapter.thread_pool_max,
            server_name=server_name)
        
        self.max_request_header_size = self.server_adapter.max_request_header_size or 0
        self.max_request_body_size = self.server_adapter.max_request_body_size or 0
        self.request_queue_size = self.server_adapter.socket_queue_size
        self.timeout = self.server_adapter.socket_timeout
        self.shutdown_timeout = self.server_adapter.shutdown_timeout
        self.protocol = self.server_adapter.protocol_version
        self.nodelay = self.server_adapter.nodelay
        
        ssl_module = self.server_adapter.ssl_module or 'pyopenssl'
        if self.server_adapter.ssl_context:
            adapter_class = wsgiserver.get_ssl_adapter_class(ssl_module)
            self.ssl_adapter = adapter_class(
                self.server_adapter.ssl_certificate,
                self.server_adapter.ssl_private_key,
                self.server_adapter.ssl_certificate_chain)
            self.ssl_adapter.context = self.server_adapter.ssl_context
        elif self.server_adapter.ssl_certificate:
            adapter_class = wsgiserver.get_ssl_adapter_class(ssl_module)
            self.ssl_adapter = adapter_class(
                self.server_adapter.ssl_certificate,
                self.server_adapter.ssl_private_key,
                self.server_adapter.ssl_certificate_chain)



########NEW FILE########
__FILENAME__ = _cpreqbody
"""Request body processing for CherryPy.

.. versionadded:: 3.2

Application authors have complete control over the parsing of HTTP request
entities. In short, :attr:`cherrypy.request.body<cherrypy._cprequest.Request.body>`
is now always set to an instance of :class:`RequestBody<cherrypy._cpreqbody.RequestBody>`,
and *that* class is a subclass of :class:`Entity<cherrypy._cpreqbody.Entity>`.

When an HTTP request includes an entity body, it is often desirable to
provide that information to applications in a form other than the raw bytes.
Different content types demand different approaches. Examples:

 * For a GIF file, we want the raw bytes in a stream.
 * An HTML form is better parsed into its component fields, and each text field
   decoded from bytes to unicode.
 * A JSON body should be deserialized into a Python dict or list.

When the request contains a Content-Type header, the media type is used as a
key to look up a value in the
:attr:`request.body.processors<cherrypy._cpreqbody.Entity.processors>` dict.
If the full media
type is not found, then the major type is tried; for example, if no processor
is found for the 'image/jpeg' type, then we look for a processor for the 'image'
types altogether. If neither the full type nor the major type has a matching
processor, then a default processor is used
(:func:`default_proc<cherrypy._cpreqbody.Entity.default_proc>`). For most
types, this means no processing is done, and the body is left unread as a
raw byte stream. Processors are configurable in an 'on_start_resource' hook.

Some processors, especially those for the 'text' types, attempt to decode bytes
to unicode. If the Content-Type request header includes a 'charset' parameter,
this is used to decode the entity. Otherwise, one or more default charsets may
be attempted, although this decision is up to each processor. If a processor
successfully decodes an Entity or Part, it should set the
:attr:`charset<cherrypy._cpreqbody.Entity.charset>` attribute
on the Entity or Part to the name of the successful charset, so that
applications can easily re-encode or transcode the value if they wish.

If the Content-Type of the request entity is of major type 'multipart', then
the above parsing process, and possibly a decoding process, is performed for
each part.

For both the full entity and multipart parts, a Content-Disposition header may
be used to fill :attr:`name<cherrypy._cpreqbody.Entity.name>` and
:attr:`filename<cherrypy._cpreqbody.Entity.filename>` attributes on the
request.body or the Part.

.. _custombodyprocessors:

Custom Processors
=================

You can add your own processors for any specific or major MIME type. Simply add
it to the :attr:`processors<cherrypy._cprequest.Entity.processors>` dict in a
hook/tool that runs at ``on_start_resource`` or ``before_request_body``. 
Here's the built-in JSON tool for an example::

    def json_in(force=True, debug=False):
        request = cherrypy.serving.request
        def json_processor(entity):
            \"""Read application/json data into request.json.\"""
            if not entity.headers.get("Content-Length", ""):
                raise cherrypy.HTTPError(411)
            
            body = entity.fp.read()
            try:
                request.json = json_decode(body)
            except ValueError:
                raise cherrypy.HTTPError(400, 'Invalid JSON document')
        if force:
            request.body.processors.clear()
            request.body.default_proc = cherrypy.HTTPError(
                415, 'Expected an application/json content type')
        request.body.processors['application/json'] = json_processor

We begin by defining a new ``json_processor`` function to stick in the ``processors``
dictionary. All processor functions take a single argument, the ``Entity`` instance
they are to process. It will be called whenever a request is received (for those
URI's where the tool is turned on) which has a ``Content-Type`` of
"application/json".

First, it checks for a valid ``Content-Length`` (raising 411 if not valid), then
reads the remaining bytes on the socket. The ``fp`` object knows its own length, so
it won't hang waiting for data that never arrives. It will return when all data
has been read. Then, we decode those bytes using Python's built-in ``json`` module,
and stick the decoded result onto ``request.json`` . If it cannot be decoded, we
raise 400.

If the "force" argument is True (the default), the ``Tool`` clears the ``processors``
dict so that request entities of other ``Content-Types`` aren't parsed at all. Since
there's no entry for those invalid MIME types, the ``default_proc`` method of ``cherrypy.request.body``
is called. But this does nothing by default (usually to provide the page handler an opportunity to handle it.)
But in our case, we want to raise 415, so we replace ``request.body.default_proc``
with the error (``HTTPError`` instances, when called, raise themselves).

If we were defining a custom processor, we can do so without making a ``Tool``. Just add the config entry::

    request.body.processors = {'application/json': json_processor}

Note that you can only replace the ``processors`` dict wholesale this way, not update the existing one.
"""

try:
    from io import DEFAULT_BUFFER_SIZE
except ImportError:
    DEFAULT_BUFFER_SIZE = 8192
import re
import sys
import tempfile
try:
    from urllib import unquote_plus
except ImportError:
    def unquote_plus(bs):
        """Bytes version of urllib.parse.unquote_plus."""
        bs = bs.replace(ntob('+'), ntob(' '))
        atoms = bs.split(ntob('%'))
        for i in range(1, len(atoms)):
            item = atoms[i]
            try:
                pct = int(item[:2], 16)
                atoms[i] = bytes([pct]) + item[2:]
            except ValueError:
                pass
        return ntob('').join(atoms)

import cherrypy
from cherrypy._cpcompat import basestring, ntob, ntou
from cherrypy.lib import httputil


# -------------------------------- Processors -------------------------------- #

def process_urlencoded(entity):
    """Read application/x-www-form-urlencoded data into entity.params."""
    qs = entity.fp.read()
    for charset in entity.attempt_charsets:
        try:
            params = {}
            for aparam in qs.split(ntob('&')):
                for pair in aparam.split(ntob(';')):
                    if not pair:
                        continue
                    
                    atoms = pair.split(ntob('='), 1)
                    if len(atoms) == 1:
                        atoms.append(ntob(''))
                    
                    key = unquote_plus(atoms[0]).decode(charset)
                    value = unquote_plus(atoms[1]).decode(charset)
                    
                    if key in params:
                        if not isinstance(params[key], list):
                            params[key] = [params[key]]
                        params[key].append(value)
                    else:
                        params[key] = value
        except UnicodeDecodeError:
            pass
        else:
            entity.charset = charset
            break
    else:
        raise cherrypy.HTTPError(
            400, "The request entity could not be decoded. The following "
            "charsets were attempted: %s" % repr(entity.attempt_charsets))
        
    # Now that all values have been successfully parsed and decoded,
    # apply them to the entity.params dict.
    for key, value in params.items():
        if key in entity.params:
            if not isinstance(entity.params[key], list):
                entity.params[key] = [entity.params[key]]
            entity.params[key].append(value)
        else:
            entity.params[key] = value


def process_multipart(entity):
    """Read all multipart parts into entity.parts."""
    ib = ""
    if 'boundary' in entity.content_type.params:
        # http://tools.ietf.org/html/rfc2046#section-5.1.1
        # "The grammar for parameters on the Content-type field is such that it
        # is often necessary to enclose the boundary parameter values in quotes
        # on the Content-type line"
        ib = entity.content_type.params['boundary'].strip('"')
    
    if not re.match("^[ -~]{0,200}[!-~]$", ib):
        raise ValueError('Invalid boundary in multipart form: %r' % (ib,))
    
    ib = ('--' + ib).encode('ascii')
    
    # Find the first marker
    while True:
        b = entity.readline()
        if not b:
            return
        
        b = b.strip()
        if b == ib:
            break
    
    # Read all parts
    while True:
        part = entity.part_class.from_fp(entity.fp, ib)
        entity.parts.append(part)
        part.process()
        if part.fp.done:
            break

def process_multipart_form_data(entity):
    """Read all multipart/form-data parts into entity.parts or entity.params."""
    process_multipart(entity)
    
    kept_parts = []
    for part in entity.parts:
        if part.name is None:
            kept_parts.append(part)
        else:
            if part.filename is None:
                # It's a regular field
                value = part.fullvalue()
            else:
                # It's a file upload. Retain the whole part so consumer code
                # has access to its .file and .filename attributes.
                value = part
            
            if part.name in entity.params:
                if not isinstance(entity.params[part.name], list):
                    entity.params[part.name] = [entity.params[part.name]]
                entity.params[part.name].append(value)
            else:
                entity.params[part.name] = value
    
    entity.parts = kept_parts

def _old_process_multipart(entity):
    """The behavior of 3.2 and lower. Deprecated and will be changed in 3.3."""
    process_multipart(entity)
    
    params = entity.params
    
    for part in entity.parts:
        if part.name is None:
            key = ntou('parts')
        else:
            key = part.name
        
        if part.filename is None:
            # It's a regular field
            value = part.fullvalue()
        else:
            # It's a file upload. Retain the whole part so consumer code
            # has access to its .file and .filename attributes.
            value = part
        
        if key in params:
            if not isinstance(params[key], list):
                params[key] = [params[key]]
            params[key].append(value)
        else:
            params[key] = value



# --------------------------------- Entities --------------------------------- #


class Entity(object):
    """An HTTP request body, or MIME multipart body.
    
    This class collects information about the HTTP request entity. When a
    given entity is of MIME type "multipart", each part is parsed into its own
    Entity instance, and the set of parts stored in
    :attr:`entity.parts<cherrypy._cpreqbody.Entity.parts>`.
    
    Between the ``before_request_body`` and ``before_handler`` tools, CherryPy
    tries to process the request body (if any) by calling
    :func:`request.body.process<cherrypy._cpreqbody.RequestBody.process`.
    This uses the ``content_type`` of the Entity to look up a suitable processor
    in :attr:`Entity.processors<cherrypy._cpreqbody.Entity.processors>`, a dict.
    If a matching processor cannot be found for the complete Content-Type,
    it tries again using the major type. For example, if a request with an
    entity of type "image/jpeg" arrives, but no processor can be found for
    that complete type, then one is sought for the major type "image". If a
    processor is still not found, then the
    :func:`default_proc<cherrypy._cpreqbody.Entity.default_proc>` method of the
    Entity is called (which does nothing by default; you can override this too).
    
    CherryPy includes processors for the "application/x-www-form-urlencoded"
    type, the "multipart/form-data" type, and the "multipart" major type.
    CherryPy 3.2 processes these types almost exactly as older versions.
    Parts are passed as arguments to the page handler using their
    ``Content-Disposition.name`` if given, otherwise in a generic "parts"
    argument. Each such part is either a string, or the
    :class:`Part<cherrypy._cpreqbody.Part>` itself if it's a file. (In this
    case it will have ``file`` and ``filename`` attributes, or possibly a
    ``value`` attribute). Each Part is itself a subclass of
    Entity, and has its own ``process`` method and ``processors`` dict.
    
    There is a separate processor for the "multipart" major type which is more
    flexible, and simply stores all multipart parts in
    :attr:`request.body.parts<cherrypy._cpreqbody.Entity.parts>`. You can
    enable it with::
    
        cherrypy.request.body.processors['multipart'] = _cpreqbody.process_multipart
    
    in an ``on_start_resource`` tool.
    """
    
    # http://tools.ietf.org/html/rfc2046#section-4.1.2:
    # "The default character set, which must be assumed in the
    # absence of a charset parameter, is US-ASCII."
    # However, many browsers send data in utf-8 with no charset.
    attempt_charsets = ['utf-8']
    """A list of strings, each of which should be a known encoding.
    
    When the Content-Type of the request body warrants it, each of the given
    encodings will be tried in order. The first one to successfully decode the
    entity without raising an error is stored as
    :attr:`entity.charset<cherrypy._cpreqbody.Entity.charset>`. This defaults
    to ``['utf-8']`` (plus 'ISO-8859-1' for "text/\*" types, as required by 
    `HTTP/1.1 <http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.7.1>`_), 
    but ``['us-ascii', 'utf-8']`` for multipart parts.
    """
    
    charset = None
    """The successful decoding; see "attempt_charsets" above."""
    
    content_type = None
    """The value of the Content-Type request header.
    
    If the Entity is part of a multipart payload, this will be the Content-Type
    given in the MIME headers for this part.
    """
    
    default_content_type = 'application/x-www-form-urlencoded'
    """This defines a default ``Content-Type`` to use if no Content-Type header
    is given. The empty string is used for RequestBody, which results in the
    request body not being read or parsed at all. This is by design; a missing
    ``Content-Type`` header in the HTTP request entity is an error at best,
    and a security hole at worst. For multipart parts, however, the MIME spec
    declares that a part with no Content-Type defaults to "text/plain"
    (see :class:`Part<cherrypy._cpreqbody.Part>`).
    """
    
    filename = None
    """The ``Content-Disposition.filename`` header, if available."""
    
    fp = None
    """The readable socket file object."""
    
    headers = None
    """A dict of request/multipart header names and values.
    
    This is a copy of the ``request.headers`` for the ``request.body``;
    for multipart parts, it is the set of headers for that part.
    """
    
    length = None
    """The value of the ``Content-Length`` header, if provided."""
    
    name = None
    """The "name" parameter of the ``Content-Disposition`` header, if any."""
    
    params = None
    """
    If the request Content-Type is 'application/x-www-form-urlencoded' or
    multipart, this will be a dict of the params pulled from the entity
    body; that is, it will be the portion of request.params that come
    from the message body (sometimes called "POST params", although they
    can be sent with various HTTP method verbs). This value is set between
    the 'before_request_body' and 'before_handler' hooks (assuming that
    process_request_body is True)."""
    
    processors = {'application/x-www-form-urlencoded': process_urlencoded,
                  'multipart/form-data': process_multipart_form_data,
                  'multipart': process_multipart,
                  }
    """A dict of Content-Type names to processor methods."""
    
    parts = None
    """A list of Part instances if ``Content-Type`` is of major type "multipart"."""
    
    part_class = None
    """The class used for multipart parts.
    
    You can replace this with custom subclasses to alter the processing of
    multipart parts.
    """
    
    def __init__(self, fp, headers, params=None, parts=None):
        # Make an instance-specific copy of the class processors
        # so Tools, etc. can replace them per-request.
        self.processors = self.processors.copy()
        
        self.fp = fp
        self.headers = headers
        
        if params is None:
            params = {}
        self.params = params
        
        if parts is None:
            parts = []
        self.parts = parts
        
        # Content-Type
        self.content_type = headers.elements('Content-Type')
        if self.content_type:
            self.content_type = self.content_type[0]
        else:
            self.content_type = httputil.HeaderElement.from_str(
                self.default_content_type)
        
        # Copy the class 'attempt_charsets', prepending any Content-Type charset
        dec = self.content_type.params.get("charset", None)
        if dec:
            self.attempt_charsets = [dec] + [c for c in self.attempt_charsets
                                             if c != dec]
        else:
            self.attempt_charsets = self.attempt_charsets[:]
        
        # Length
        self.length = None
        clen = headers.get('Content-Length', None)
        # If Transfer-Encoding is 'chunked', ignore any Content-Length.
        if clen is not None and 'chunked' not in headers.get('Transfer-Encoding', ''):
            try:
                self.length = int(clen)
            except ValueError:
                pass
        
        # Content-Disposition
        self.name = None
        self.filename = None
        disp = headers.elements('Content-Disposition')
        if disp:
            disp = disp[0]
            if 'name' in disp.params:
                self.name = disp.params['name']
                if self.name.startswith('"') and self.name.endswith('"'):
                    self.name = self.name[1:-1]
            if 'filename' in disp.params:
                self.filename = disp.params['filename']
                if self.filename.startswith('"') and self.filename.endswith('"'):
                    self.filename = self.filename[1:-1]
    
    # The 'type' attribute is deprecated in 3.2; remove it in 3.3.
    type = property(lambda self: self.content_type,
        doc="""A deprecated alias for :attr:`content_type<cherrypy._cpreqbody.Entity.content_type>`.""")
    
    def read(self, size=None, fp_out=None):
        return self.fp.read(size, fp_out)
    
    def readline(self, size=None):
        return self.fp.readline(size)
    
    def readlines(self, sizehint=None):
        return self.fp.readlines(sizehint)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def next(self):
        return self.__next__()
    
    def read_into_file(self, fp_out=None):
        """Read the request body into fp_out (or make_file() if None). Return fp_out."""
        if fp_out is None:
            fp_out = self.make_file()
        self.read(fp_out=fp_out)
        return fp_out
    
    def make_file(self):
        """Return a file-like object into which the request body will be read.
        
        By default, this will return a TemporaryFile. Override as needed.
        See also :attr:`cherrypy._cpreqbody.Part.maxrambytes`."""
        return tempfile.TemporaryFile()
    
    def fullvalue(self):
        """Return this entity as a string, whether stored in a file or not."""
        if self.file:
            # It was stored in a tempfile. Read it.
            self.file.seek(0)
            value = self.file.read()
            self.file.seek(0)
        else:
            value = self.value
        return value
    
    def process(self):
        """Execute the best-match processor for the given media type."""
        proc = None
        ct = self.content_type.value
        try:
            proc = self.processors[ct]
        except KeyError:
            toptype = ct.split('/', 1)[0]
            try:
                proc = self.processors[toptype]
            except KeyError:
                pass
        if proc is None:
            self.default_proc()
        else:
            proc(self)
    
    def default_proc(self):
        """Called if a more-specific processor is not found for the ``Content-Type``."""
        # Leave the fp alone for someone else to read. This works fine
        # for request.body, but the Part subclasses need to override this
        # so they can move on to the next part.
        pass


class Part(Entity):
    """A MIME part entity, part of a multipart entity."""
    
    # "The default character set, which must be assumed in the absence of a
    # charset parameter, is US-ASCII."
    attempt_charsets = ['us-ascii', 'utf-8']
    """A list of strings, each of which should be a known encoding.
    
    When the Content-Type of the request body warrants it, each of the given
    encodings will be tried in order. The first one to successfully decode the
    entity without raising an error is stored as
    :attr:`entity.charset<cherrypy._cpreqbody.Entity.charset>`. This defaults
    to ``['utf-8']`` (plus 'ISO-8859-1' for "text/\*" types, as required by 
    `HTTP/1.1 <http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.7.1>`_), 
    but ``['us-ascii', 'utf-8']`` for multipart parts.
    """
    
    boundary = None
    """The MIME multipart boundary."""
    
    default_content_type = 'text/plain'
    """This defines a default ``Content-Type`` to use if no Content-Type header
    is given. The empty string is used for RequestBody, which results in the
    request body not being read or parsed at all. This is by design; a missing
    ``Content-Type`` header in the HTTP request entity is an error at best,
    and a security hole at worst. For multipart parts, however (this class),
    the MIME spec declares that a part with no Content-Type defaults to
    "text/plain".
    """
    
    # This is the default in stdlib cgi. We may want to increase it.
    maxrambytes = 1000
    """The threshold of bytes after which point the ``Part`` will store its data
    in a file (generated by :func:`make_file<cherrypy._cprequest.Entity.make_file>`)
    instead of a string. Defaults to 1000, just like the :mod:`cgi` module in
    Python's standard library.
    """
    
    def __init__(self, fp, headers, boundary):
        Entity.__init__(self, fp, headers)
        self.boundary = boundary
        self.file = None
        self.value = None
    
    def from_fp(cls, fp, boundary):
        headers = cls.read_headers(fp)
        return cls(fp, headers, boundary)
    from_fp = classmethod(from_fp)
    
    def read_headers(cls, fp):
        headers = httputil.HeaderMap()
        while True:
            line = fp.readline()
            if not line:
                # No more data--illegal end of headers
                raise EOFError("Illegal end of headers.")
            
            if line == ntob('\r\n'):
                # Normal end of headers
                break
            if not line.endswith(ntob('\r\n')):
                raise ValueError("MIME requires CRLF terminators: %r" % line)
            
            if line[0] in ntob(' \t'):
                # It's a continuation line.
                v = line.strip().decode('ISO-8859-1')
            else:
                k, v = line.split(ntob(":"), 1)
                k = k.strip().decode('ISO-8859-1')
                v = v.strip().decode('ISO-8859-1')
            
            existing = headers.get(k)
            if existing:
                v = ", ".join((existing, v))
            headers[k] = v
        
        return headers
    read_headers = classmethod(read_headers)
    
    def read_lines_to_boundary(self, fp_out=None):
        """Read bytes from self.fp and return or write them to a file.
        
        If the 'fp_out' argument is None (the default), all bytes read are
        returned in a single byte string.
        
        If the 'fp_out' argument is not None, it must be a file-like object that
        supports the 'write' method; all bytes read will be written to the fp,
        and that fp is returned.
        """
        endmarker = self.boundary + ntob("--")
        delim = ntob("")
        prev_lf = True
        lines = []
        seen = 0
        while True:
            line = self.fp.readline(1<<16)
            if not line:
                raise EOFError("Illegal end of multipart body.")
            if line.startswith(ntob("--")) and prev_lf:
                strippedline = line.strip()
                if strippedline == self.boundary:
                    break
                if strippedline == endmarker:
                    self.fp.finish()
                    break
            
            line = delim + line
            
            if line.endswith(ntob("\r\n")):
                delim = ntob("\r\n")
                line = line[:-2]
                prev_lf = True
            elif line.endswith(ntob("\n")):
                delim = ntob("\n")
                line = line[:-1]
                prev_lf = True
            else:
                delim = ntob("")
                prev_lf = False
            
            if fp_out is None:
                lines.append(line)
                seen += len(line)
                if seen > self.maxrambytes:
                    fp_out = self.make_file()
                    for line in lines:
                        fp_out.write(line)
            else:
                fp_out.write(line)
        
        if fp_out is None:
            result = ntob('').join(lines)
            for charset in self.attempt_charsets:
                try:
                    result = result.decode(charset)
                except UnicodeDecodeError:
                    pass
                else:
                    self.charset = charset
                    return result
            else:
                raise cherrypy.HTTPError(
                    400, "The request entity could not be decoded. The following "
                    "charsets were attempted: %s" % repr(self.attempt_charsets))
        else:
            fp_out.seek(0)
            return fp_out
    
    def default_proc(self):
        """Called if a more-specific processor is not found for the ``Content-Type``."""
        if self.filename:
            # Always read into a file if a .filename was given.
            self.file = self.read_into_file()
        else:
            result = self.read_lines_to_boundary()
            if isinstance(result, basestring):
                self.value = result
            else:
                self.file = result
    
    def read_into_file(self, fp_out=None):
        """Read the request body into fp_out (or make_file() if None). Return fp_out."""
        if fp_out is None:
            fp_out = self.make_file()
        self.read_lines_to_boundary(fp_out=fp_out)
        return fp_out

Entity.part_class = Part

try:
    inf = float('inf')
except ValueError:
    # Python 2.4 and lower
    class Infinity(object):
        def __cmp__(self, other):
            return 1
        def __sub__(self, other):
            return self
    inf = Infinity()


comma_separated_headers = ['Accept', 'Accept-Charset', 'Accept-Encoding',
    'Accept-Language', 'Accept-Ranges', 'Allow', 'Cache-Control', 'Connection',
    'Content-Encoding', 'Content-Language', 'Expect', 'If-Match',
    'If-None-Match', 'Pragma', 'Proxy-Authenticate', 'Te', 'Trailer',
    'Transfer-Encoding', 'Upgrade', 'Vary', 'Via', 'Warning', 'Www-Authenticate']


class SizedReader:
    
    def __init__(self, fp, length, maxbytes, bufsize=DEFAULT_BUFFER_SIZE, has_trailers=False):
        # Wrap our fp in a buffer so peek() works
        self.fp = fp
        self.length = length
        self.maxbytes = maxbytes
        self.buffer = ntob('')
        self.bufsize = bufsize
        self.bytes_read = 0
        self.done = False
        self.has_trailers = has_trailers
    
    def read(self, size=None, fp_out=None):
        """Read bytes from the request body and return or write them to a file.
        
        A number of bytes less than or equal to the 'size' argument are read
        off the socket. The actual number of bytes read are tracked in
        self.bytes_read. The number may be smaller than 'size' when 1) the
        client sends fewer bytes, 2) the 'Content-Length' request header
        specifies fewer bytes than requested, or 3) the number of bytes read
        exceeds self.maxbytes (in which case, 413 is raised).
        
        If the 'fp_out' argument is None (the default), all bytes read are
        returned in a single byte string.
        
        If the 'fp_out' argument is not None, it must be a file-like object that
        supports the 'write' method; all bytes read will be written to the fp,
        and None is returned.
        """
        
        if self.length is None:
            if size is None:
                remaining = inf
            else:
                remaining = size
        else:
            remaining = self.length - self.bytes_read
            if size and size < remaining:
                remaining = size
        if remaining == 0:
            self.finish()
            if fp_out is None:
                return ntob('')
            else:
                return None
        
        chunks = []
        
        # Read bytes from the buffer.
        if self.buffer:
            if remaining is inf:
                data = self.buffer
                self.buffer = ntob('')
            else:
                data = self.buffer[:remaining]
                self.buffer = self.buffer[remaining:]
            datalen = len(data)
            remaining -= datalen
            
            # Check lengths.
            self.bytes_read += datalen
            if self.maxbytes and self.bytes_read > self.maxbytes:
                raise cherrypy.HTTPError(413)
            
            # Store the data.
            if fp_out is None:
                chunks.append(data)
            else:
                fp_out.write(data)
        
        # Read bytes from the socket.
        while remaining > 0:
            chunksize = min(remaining, self.bufsize)
            try:
                data = self.fp.read(chunksize)
            except Exception:
                e = sys.exc_info()[1]
                if e.__class__.__name__ == 'MaxSizeExceeded':
                    # Post data is too big
                    raise cherrypy.HTTPError(
                        413, "Maximum request length: %r" % e.args[1])
                else:
                    raise
            if not data:
                self.finish()
                break
            datalen = len(data)
            remaining -= datalen
            
            # Check lengths.
            self.bytes_read += datalen
            if self.maxbytes and self.bytes_read > self.maxbytes:
                raise cherrypy.HTTPError(413)
            
            # Store the data.
            if fp_out is None:
                chunks.append(data)
            else:
                fp_out.write(data)
        
        if fp_out is None:
            return ntob('').join(chunks)
    
    def readline(self, size=None):
        """Read a line from the request body and return it."""
        chunks = []
        while size is None or size > 0:
            chunksize = self.bufsize
            if size is not None and size < self.bufsize:
                chunksize = size
            data = self.read(chunksize)
            if not data:
                break
            pos = data.find(ntob('\n')) + 1
            if pos:
                chunks.append(data[:pos])
                remainder = data[pos:]
                self.buffer += remainder
                self.bytes_read -= len(remainder)
                break
            else:
                chunks.append(data)
        return ntob('').join(chunks)
    
    def readlines(self, sizehint=None):
        """Read lines from the request body and return them."""
        if self.length is not None:
            if sizehint is None:
                sizehint = self.length - self.bytes_read
            else:
                sizehint = min(sizehint, self.length - self.bytes_read)
        
        lines = []
        seen = 0
        while True:
            line = self.readline()
            if not line:
                break
            lines.append(line)
            seen += len(line)
            if seen >= sizehint:
                break
        return lines
    
    def finish(self):
        self.done = True
        if self.has_trailers and hasattr(self.fp, 'read_trailer_lines'):
            self.trailers = {}
            
            try:
                for line in self.fp.read_trailer_lines():
                    if line[0] in ntob(' \t'):
                        # It's a continuation line.
                        v = line.strip()
                    else:
                        try:
                            k, v = line.split(ntob(":"), 1)
                        except ValueError:
                            raise ValueError("Illegal header line.")
                        k = k.strip().title()
                        v = v.strip()
                    
                    if k in comma_separated_headers:
                        existing = self.trailers.get(envname)
                        if existing:
                            v = ntob(", ").join((existing, v))
                    self.trailers[k] = v
            except Exception:
                e = sys.exc_info()[1]
                if e.__class__.__name__ == 'MaxSizeExceeded':
                    # Post data is too big
                    raise cherrypy.HTTPError(
                        413, "Maximum request length: %r" % e.args[1])
                else:
                    raise


class RequestBody(Entity):
    """The entity of the HTTP request."""
    
    bufsize = 8 * 1024
    """The buffer size used when reading the socket."""
    
    # Don't parse the request body at all if the client didn't provide
    # a Content-Type header. See http://www.cherrypy.org/ticket/790
    default_content_type = ''
    """This defines a default ``Content-Type`` to use if no Content-Type header
    is given. The empty string is used for RequestBody, which results in the
    request body not being read or parsed at all. This is by design; a missing
    ``Content-Type`` header in the HTTP request entity is an error at best,
    and a security hole at worst. For multipart parts, however, the MIME spec
    declares that a part with no Content-Type defaults to "text/plain"
    (see :class:`Part<cherrypy._cpreqbody.Part>`).
    """
    
    maxbytes = None
    """Raise ``MaxSizeExceeded`` if more bytes than this are read from the socket."""
    
    def __init__(self, fp, headers, params=None, request_params=None):
        Entity.__init__(self, fp, headers, params)
        
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.7.1
        # When no explicit charset parameter is provided by the
        # sender, media subtypes of the "text" type are defined
        # to have a default charset value of "ISO-8859-1" when
        # received via HTTP.
        if self.content_type.value.startswith('text/'):
            for c in ('ISO-8859-1', 'iso-8859-1', 'Latin-1', 'latin-1'):
                if c in self.attempt_charsets:
                    break
            else:
                self.attempt_charsets.append('ISO-8859-1')
        
        # Temporary fix while deprecating passing .parts as .params.
        self.processors['multipart'] = _old_process_multipart
        
        if request_params is None:
            request_params = {}
        self.request_params = request_params
    
    def process(self):
        """Process the request entity based on its Content-Type."""
        # "The presence of a message-body in a request is signaled by the
        # inclusion of a Content-Length or Transfer-Encoding header field in
        # the request's message-headers."
        # It is possible to send a POST request with no body, for example;
        # however, app developers are responsible in that case to set
        # cherrypy.request.process_body to False so this method isn't called.
        h = cherrypy.serving.request.headers
        if 'Content-Length' not in h and 'Transfer-Encoding' not in h:
            raise cherrypy.HTTPError(411)
        
        self.fp = SizedReader(self.fp, self.length,
                              self.maxbytes, bufsize=self.bufsize,
                              has_trailers='Trailer' in h)
        super(RequestBody, self).process()
        
        # Body params should also be a part of the request_params
        # add them in here.
        request_params = self.request_params
        for key, value in self.params.items():
            # Python 2 only: keyword arguments must be byte strings (type 'str').
            if sys.version_info < (3, 0):
                if isinstance(key, unicode):
                    key = key.encode('ISO-8859-1')
            
            if key in request_params:
                if not isinstance(request_params[key], list):
                    request_params[key] = [request_params[key]]
                request_params[key].append(value)
            else:
                request_params[key] = value

########NEW FILE########
__FILENAME__ = _cprequest

import os
import sys
import time
import warnings

import cherrypy
from cherrypy._cpcompat import basestring, copykeys, ntob, unicodestr
from cherrypy._cpcompat import SimpleCookie, CookieError, py3k
from cherrypy import _cpreqbody, _cpconfig
from cherrypy._cperror import format_exc, bare_error
from cherrypy.lib import httputil, file_generator


class Hook(object):
    """A callback and its metadata: failsafe, priority, and kwargs."""
    
    callback = None
    """
    The bare callable that this Hook object is wrapping, which will
    be called when the Hook is called."""
    
    failsafe = False
    """
    If True, the callback is guaranteed to run even if other callbacks
    from the same call point raise exceptions."""
    
    priority = 50
    """
    Defines the order of execution for a list of Hooks. Priority numbers
    should be limited to the closed interval [0, 100], but values outside
    this range are acceptable, as are fractional values."""
    
    kwargs = {}
    """
    A set of keyword arguments that will be passed to the
    callable on each call."""
    
    def __init__(self, callback, failsafe=None, priority=None, **kwargs):
        self.callback = callback
        
        if failsafe is None:
            failsafe = getattr(callback, "failsafe", False)
        self.failsafe = failsafe
        
        if priority is None:
            priority = getattr(callback, "priority", 50)
        self.priority = priority
        
        self.kwargs = kwargs
    
    def __lt__(self, other):
        # Python 3
        return self.priority < other.priority

    def __cmp__(self, other):
        # Python 2
        return cmp(self.priority, other.priority)
    
    def __call__(self):
        """Run self.callback(**self.kwargs)."""
        return self.callback(**self.kwargs)
    
    def __repr__(self):
        cls = self.__class__
        return ("%s.%s(callback=%r, failsafe=%r, priority=%r, %s)"
                % (cls.__module__, cls.__name__, self.callback,
                   self.failsafe, self.priority,
                   ", ".join(['%s=%r' % (k, v)
                              for k, v in self.kwargs.items()])))


class HookMap(dict):
    """A map of call points to lists of callbacks (Hook objects)."""
    
    def __new__(cls, points=None):
        d = dict.__new__(cls)
        for p in points or []:
            d[p] = []
        return d
    
    def __init__(self, *a, **kw):
        pass
    
    def attach(self, point, callback, failsafe=None, priority=None, **kwargs):
        """Append a new Hook made from the supplied arguments."""
        self[point].append(Hook(callback, failsafe, priority, **kwargs))
    
    def run(self, point):
        """Execute all registered Hooks (callbacks) for the given point."""
        exc = None
        hooks = self[point]
        hooks.sort()
        for hook in hooks:
            # Some hooks are guaranteed to run even if others at
            # the same hookpoint fail. We will still log the failure,
            # but proceed on to the next hook. The only way
            # to stop all processing from one of these hooks is
            # to raise SystemExit and stop the whole server.
            if exc is None or hook.failsafe:
                try:
                    hook()
                except (KeyboardInterrupt, SystemExit):
                    raise
                except (cherrypy.HTTPError, cherrypy.HTTPRedirect,
                        cherrypy.InternalRedirect):
                    exc = sys.exc_info()[1]
                except:
                    exc = sys.exc_info()[1]
                    cherrypy.log(traceback=True, severity=40)
        if exc:
            raise exc
    
    def __copy__(self):
        newmap = self.__class__()
        # We can't just use 'update' because we want copies of the
        # mutable values (each is a list) as well.
        for k, v in self.items():
            newmap[k] = v[:]
        return newmap
    copy = __copy__
    
    def __repr__(self):
        cls = self.__class__
        return "%s.%s(points=%r)" % (cls.__module__, cls.__name__, copykeys(self))


# Config namespace handlers

def hooks_namespace(k, v):
    """Attach bare hooks declared in config."""
    # Use split again to allow multiple hooks for a single
    # hookpoint per path (e.g. "hooks.before_handler.1").
    # Little-known fact you only get from reading source ;)
    hookpoint = k.split(".", 1)[0]
    if isinstance(v, basestring):
        v = cherrypy.lib.attributes(v)
    if not isinstance(v, Hook):
        v = Hook(v)
    cherrypy.serving.request.hooks[hookpoint].append(v)

def request_namespace(k, v):
    """Attach request attributes declared in config."""
    # Provides config entries to set request.body attrs (like attempt_charsets).
    if k[:5] == 'body.':
        setattr(cherrypy.serving.request.body, k[5:], v)
    else:
        setattr(cherrypy.serving.request, k, v)

def response_namespace(k, v):
    """Attach response attributes declared in config."""
    # Provides config entries to set default response headers
    # http://cherrypy.org/ticket/889
    if k[:8] == 'headers.':
        cherrypy.serving.response.headers[k.split('.', 1)[1]] = v
    else:
        setattr(cherrypy.serving.response, k, v)

def error_page_namespace(k, v):
    """Attach error pages declared in config."""
    if k != 'default':
        k = int(k)
    cherrypy.serving.request.error_page[k] = v


hookpoints = ['on_start_resource', 'before_request_body',
              'before_handler', 'before_finalize',
              'on_end_resource', 'on_end_request',
              'before_error_response', 'after_error_response']


class Request(object):
    """An HTTP request.
    
    This object represents the metadata of an HTTP request message;
    that is, it contains attributes which describe the environment
    in which the request URL, headers, and body were sent (if you
    want tools to interpret the headers and body, those are elsewhere,
    mostly in Tools). This 'metadata' consists of socket data,
    transport characteristics, and the Request-Line. This object
    also contains data regarding the configuration in effect for
    the given URL, and the execution plan for generating a response.
    """
    
    prev = None
    """
    The previous Request object (if any). This should be None
    unless we are processing an InternalRedirect."""
    
    # Conversation/connection attributes
    local = httputil.Host("127.0.0.1", 80)
    "An httputil.Host(ip, port, hostname) object for the server socket."
    
    remote = httputil.Host("127.0.0.1", 1111)
    "An httputil.Host(ip, port, hostname) object for the client socket."
    
    scheme = "http"
    """
    The protocol used between client and server. In most cases,
    this will be either 'http' or 'https'."""
    
    server_protocol = "HTTP/1.1"
    """
    The HTTP version for which the HTTP server is at least
    conditionally compliant."""
    
    base = ""
    """The (scheme://host) portion of the requested URL.
    In some cases (e.g. when proxying via mod_rewrite), this may contain
    path segments which cherrypy.url uses when constructing url's, but
    which otherwise are ignored by CherryPy. Regardless, this value
    MUST NOT end in a slash."""
    
    # Request-Line attributes
    request_line = ""
    """
    The complete Request-Line received from the client. This is a
    single string consisting of the request method, URI, and protocol
    version (joined by spaces). Any final CRLF is removed."""
    
    method = "GET"
    """
    Indicates the HTTP method to be performed on the resource identified
    by the Request-URI. Common methods include GET, HEAD, POST, PUT, and
    DELETE. CherryPy allows any extension method; however, various HTTP
    servers and gateways may restrict the set of allowable methods.
    CherryPy applications SHOULD restrict the set (on a per-URI basis)."""
    
    query_string = ""
    """
    The query component of the Request-URI, a string of information to be
    interpreted by the resource. The query portion of a URI follows the
    path component, and is separated by a '?'. For example, the URI
    'http://www.cherrypy.org/wiki?a=3&b=4' has the query component,
    'a=3&b=4'."""
    
    query_string_encoding = 'utf8'
    """
    The encoding expected for query string arguments after % HEX HEX decoding).
    If a query string is provided that cannot be decoded with this encoding,
    404 is raised (since technically it's a different URI). If you want
    arbitrary encodings to not error, set this to 'Latin-1'; you can then
    encode back to bytes and re-decode to whatever encoding you like later.
    """
    
    protocol = (1, 1)
    """The HTTP protocol version corresponding to the set
    of features which should be allowed in the response. If BOTH
    the client's request message AND the server's level of HTTP
    compliance is HTTP/1.1, this attribute will be the tuple (1, 1).
    If either is 1.0, this attribute will be the tuple (1, 0).
    Lower HTTP protocol versions are not explicitly supported."""
    
    params = {}
    """
    A dict which combines query string (GET) and request entity (POST)
    variables. This is populated in two stages: GET params are added
    before the 'on_start_resource' hook, and POST params are added
    between the 'before_request_body' and 'before_handler' hooks."""
    
    # Message attributes
    header_list = []
    """
    A list of the HTTP request headers as (name, value) tuples.
    In general, you should use request.headers (a dict) instead."""
    
    headers = httputil.HeaderMap()
    """
    A dict-like object containing the request headers. Keys are header
    names (in Title-Case format); however, you may get and set them in
    a case-insensitive manner. That is, headers['Content-Type'] and
    headers['content-type'] refer to the same value. Values are header
    values (decoded according to :rfc:`2047` if necessary). See also:
    httputil.HeaderMap, httputil.HeaderElement."""
    
    cookie = SimpleCookie()
    """See help(Cookie)."""
    
    rfile = None
    """
    If the request included an entity (body), it will be available
    as a stream in this attribute. However, the rfile will normally
    be read for you between the 'before_request_body' hook and the
    'before_handler' hook, and the resulting string is placed into
    either request.params or the request.body attribute.
    
    You may disable the automatic consumption of the rfile by setting
    request.process_request_body to False, either in config for the desired
    path, or in an 'on_start_resource' or 'before_request_body' hook.
    
    WARNING: In almost every case, you should not attempt to read from the
    rfile stream after CherryPy's automatic mechanism has read it. If you
    turn off the automatic parsing of rfile, you should read exactly the
    number of bytes specified in request.headers['Content-Length'].
    Ignoring either of these warnings may result in a hung request thread
    or in corruption of the next (pipelined) request.
    """
    
    process_request_body = True
    """
    If True, the rfile (if any) is automatically read and parsed,
    and the result placed into request.params or request.body."""
    
    methods_with_bodies = ("POST", "PUT")
    """
    A sequence of HTTP methods for which CherryPy will automatically
    attempt to read a body from the rfile."""
    
    body = None
    """
    If the request Content-Type is 'application/x-www-form-urlencoded'
    or multipart, this will be None. Otherwise, this will be an instance
    of :class:`RequestBody<cherrypy._cpreqbody.RequestBody>` (which you
    can .read()); this value is set between the 'before_request_body' and
    'before_handler' hooks (assuming that process_request_body is True)."""
    
    # Dispatch attributes
    dispatch = cherrypy.dispatch.Dispatcher()
    """
    The object which looks up the 'page handler' callable and collects
    config for the current request based on the path_info, other
    request attributes, and the application architecture. The core
    calls the dispatcher as early as possible, passing it a 'path_info'
    argument.
    
    The default dispatcher discovers the page handler by matching path_info
    to a hierarchical arrangement of objects, starting at request.app.root.
    See help(cherrypy.dispatch) for more information."""
    
    script_name = ""
    """
    The 'mount point' of the application which is handling this request.
    
    This attribute MUST NOT end in a slash. If the script_name refers to
    the root of the URI, it MUST be an empty string (not "/").
    """
    
    path_info = "/"
    """
    The 'relative path' portion of the Request-URI. This is relative
    to the script_name ('mount point') of the application which is
    handling this request."""

    login = None
    """
    When authentication is used during the request processing this is
    set to 'False' if it failed and to the 'username' value if it succeeded.
    The default 'None' implies that no authentication happened."""
    
    # Note that cherrypy.url uses "if request.app:" to determine whether
    # the call is during a real HTTP request or not. So leave this None.
    app = None
    """The cherrypy.Application object which is handling this request."""
    
    handler = None
    """
    The function, method, or other callable which CherryPy will call to
    produce the response. The discovery of the handler and the arguments
    it will receive are determined by the request.dispatch object.
    By default, the handler is discovered by walking a tree of objects
    starting at request.app.root, and is then passed all HTTP params
    (from the query string and POST body) as keyword arguments."""
    
    toolmaps = {}
    """
    A nested dict of all Toolboxes and Tools in effect for this request,
    of the form: {Toolbox.namespace: {Tool.name: config dict}}."""
    
    config = None
    """
    A flat dict of all configuration entries which apply to the
    current request. These entries are collected from global config,
    application config (based on request.path_info), and from handler
    config (exactly how is governed by the request.dispatch object in
    effect for this request; by default, handler config can be attached
    anywhere in the tree between request.app.root and the final handler,
    and inherits downward)."""
    
    is_index = None
    """
    This will be True if the current request is mapped to an 'index'
    resource handler (also, a 'default' handler if path_info ends with
    a slash). The value may be used to automatically redirect the
    user-agent to a 'more canonical' URL which either adds or removes
    the trailing slash. See cherrypy.tools.trailing_slash."""
    
    hooks = HookMap(hookpoints)
    """
    A HookMap (dict-like object) of the form: {hookpoint: [hook, ...]}.
    Each key is a str naming the hook point, and each value is a list
    of hooks which will be called at that hook point during this request.
    The list of hooks is generally populated as early as possible (mostly
    from Tools specified in config), but may be extended at any time.
    See also: _cprequest.Hook, _cprequest.HookMap, and cherrypy.tools."""
    
    error_response = cherrypy.HTTPError(500).set_response
    """
    The no-arg callable which will handle unexpected, untrapped errors
    during request processing. This is not used for expected exceptions
    (like NotFound, HTTPError, or HTTPRedirect) which are raised in
    response to expected conditions (those should be customized either
    via request.error_page or by overriding HTTPError.set_response).
    By default, error_response uses HTTPError(500) to return a generic
    error response to the user-agent."""
    
    error_page = {}
    """
    A dict of {error code: response filename or callable} pairs.
    
    The error code must be an int representing a given HTTP error code,
    or the string 'default', which will be used if no matching entry
    is found for a given numeric code.
    
    If a filename is provided, the file should contain a Python string-
    formatting template, and can expect by default to receive format 
    values with the mapping keys %(status)s, %(message)s, %(traceback)s,
    and %(version)s. The set of format mappings can be extended by
    overriding HTTPError.set_response.
    
    If a callable is provided, it will be called by default with keyword
    arguments 'status', 'message', 'traceback', and 'version', as for a
    string-formatting template. The callable must return a string or iterable of
    strings which will be set to response.body. It may also override headers or
    perform any other processing.
    
    If no entry is given for an error code, and no 'default' entry exists,
    a default template will be used.
    """
    
    show_tracebacks = True
    """
    If True, unexpected errors encountered during request processing will
    include a traceback in the response body."""

    show_mismatched_params = True
    """
    If True, mismatched parameters encountered during PageHandler invocation
    processing will be included in the response body."""
    
    throws = (KeyboardInterrupt, SystemExit, cherrypy.InternalRedirect)
    """The sequence of exceptions which Request.run does not trap."""
    
    throw_errors = False
    """
    If True, Request.run will not trap any errors (except HTTPRedirect and
    HTTPError, which are more properly called 'exceptions', not errors)."""
    
    closed = False
    """True once the close method has been called, False otherwise."""
    
    stage = None
    """
    A string containing the stage reached in the request-handling process.
    This is useful when debugging a live server with hung requests."""
    
    namespaces = _cpconfig.NamespaceSet(
        **{"hooks": hooks_namespace,
           "request": request_namespace,
           "response": response_namespace,
           "error_page": error_page_namespace,
           "tools": cherrypy.tools,
           })
    
    def __init__(self, local_host, remote_host, scheme="http",
                 server_protocol="HTTP/1.1"):
        """Populate a new Request object.
        
        local_host should be an httputil.Host object with the server info.
        remote_host should be an httputil.Host object with the client info.
        scheme should be a string, either "http" or "https".
        """
        self.local = local_host
        self.remote = remote_host
        self.scheme = scheme
        self.server_protocol = server_protocol
        
        self.closed = False
        
        # Put a *copy* of the class error_page into self.
        self.error_page = self.error_page.copy()
        
        # Put a *copy* of the class namespaces into self.
        self.namespaces = self.namespaces.copy()
        
        self.stage = None
    
    def close(self):
        """Run cleanup code. (Core)"""
        if not self.closed:
            self.closed = True
            self.stage = 'on_end_request'
            self.hooks.run('on_end_request')
            self.stage = 'close'
    
    def run(self, method, path, query_string, req_protocol, headers, rfile):
        r"""Process the Request. (Core)
        
        method, path, query_string, and req_protocol should be pulled directly
        from the Request-Line (e.g. "GET /path?key=val HTTP/1.0").
        
        path
            This should be %XX-unquoted, but query_string should not be.
            
            When using Python 2, they both MUST be byte strings,
            not unicode strings.
            
            When using Python 3, they both MUST be unicode strings,
            not byte strings, and preferably not bytes \x00-\xFF
            disguised as unicode.
        
        headers
            A list of (name, value) tuples.
        
        rfile
            A file-like object containing the HTTP request entity.
        
        When run() is done, the returned object should have 3 attributes:
        
          * status, e.g. "200 OK"
          * header_list, a list of (name, value) tuples
          * body, an iterable yielding strings
        
        Consumer code (HTTP servers) should then access these response
        attributes to build the outbound stream.
        
        """
        response = cherrypy.serving.response
        self.stage = 'run'
        try:
            self.error_response = cherrypy.HTTPError(500).set_response
            
            self.method = method
            path = path or "/"
            self.query_string = query_string or ''
            self.params = {}
            
            # Compare request and server HTTP protocol versions, in case our
            # server does not support the requested protocol. Limit our output
            # to min(req, server). We want the following output:
            #     request    server     actual written   supported response
            #     protocol   protocol  response protocol    feature set
            # a     1.0        1.0           1.0                1.0
            # b     1.0        1.1           1.1                1.0
            # c     1.1        1.0           1.0                1.0
            # d     1.1        1.1           1.1                1.1
            # Notice that, in (b), the response will be "HTTP/1.1" even though
            # the client only understands 1.0. RFC 2616 10.5.6 says we should
            # only return 505 if the _major_ version is different.
            rp = int(req_protocol[5]), int(req_protocol[7])
            sp = int(self.server_protocol[5]), int(self.server_protocol[7])
            self.protocol = min(rp, sp)
            response.headers.protocol = self.protocol
            
            # Rebuild first line of the request (e.g. "GET /path HTTP/1.0").
            url = path
            if query_string:
                url += '?' + query_string
            self.request_line = '%s %s %s' % (method, url, req_protocol)
            
            self.header_list = list(headers)
            self.headers = httputil.HeaderMap()
            
            self.rfile = rfile
            self.body = None
            
            self.cookie = SimpleCookie()
            self.handler = None
            
            # path_info should be the path from the
            # app root (script_name) to the handler.
            self.script_name = self.app.script_name
            self.path_info = pi = path[len(self.script_name):]
            
            self.stage = 'respond'
            self.respond(pi)
            
        except self.throws:
            raise
        except:
            if self.throw_errors:
                raise
            else:
                # Failure in setup, error handler or finalize. Bypass them.
                # Can't use handle_error because we may not have hooks yet.
                cherrypy.log(traceback=True, severity=40)
                if self.show_tracebacks:
                    body = format_exc()
                else:
                    body = ""
                r = bare_error(body)
                response.output_status, response.header_list, response.body = r
        
        if self.method == "HEAD":
            # HEAD requests MUST NOT return a message-body in the response.
            response.body = []
        
        try:
            cherrypy.log.access()
        except:
            cherrypy.log.error(traceback=True)
        
        if response.timed_out:
            raise cherrypy.TimeoutError()
        
        return response
    
    # Uncomment for stage debugging
    # stage = property(lambda self: self._stage, lambda self, v: print(v))
    
    def respond(self, path_info):
        """Generate a response for the resource at self.path_info. (Core)"""
        response = cherrypy.serving.response
        try:
            try:
                try:
                    if self.app is None:
                        raise cherrypy.NotFound()
                    
                    # Get the 'Host' header, so we can HTTPRedirect properly.
                    self.stage = 'process_headers'
                    self.process_headers()
                    
                    # Make a copy of the class hooks
                    self.hooks = self.__class__.hooks.copy()
                    self.toolmaps = {}
                    
                    self.stage = 'get_resource'
                    self.get_resource(path_info)
                    
                    self.body = _cpreqbody.RequestBody(
                        self.rfile, self.headers, request_params=self.params)
                    
                    self.namespaces(self.config)
                    
                    self.stage = 'on_start_resource'
                    self.hooks.run('on_start_resource')
                    
                    # Parse the querystring
                    self.stage = 'process_query_string'
                    self.process_query_string()
                    
                    # Process the body
                    if self.process_request_body:
                        if self.method not in self.methods_with_bodies:
                            self.process_request_body = False
                    self.stage = 'before_request_body'
                    self.hooks.run('before_request_body')
                    if self.process_request_body:
                        self.body.process()
                    
                    # Run the handler
                    self.stage = 'before_handler'
                    self.hooks.run('before_handler')
                    if self.handler:
                        self.stage = 'handler'
                        response.body = self.handler()
                    
                    # Finalize
                    self.stage = 'before_finalize'
                    self.hooks.run('before_finalize')
                    response.finalize()
                except (cherrypy.HTTPRedirect, cherrypy.HTTPError):
                    inst = sys.exc_info()[1]
                    inst.set_response()
                    self.stage = 'before_finalize (HTTPError)'
                    self.hooks.run('before_finalize')
                    response.finalize()
            finally:
                self.stage = 'on_end_resource'
                self.hooks.run('on_end_resource')
        except self.throws:
            raise
        except:
            if self.throw_errors:
                raise
            self.handle_error()
    
    def process_query_string(self):
        """Parse the query string into Python structures. (Core)"""
        try:
            p = httputil.parse_query_string(
                self.query_string, encoding=self.query_string_encoding)
        except UnicodeDecodeError:
            raise cherrypy.HTTPError(
                404, "The given query string could not be processed. Query "
                "strings for this resource must be encoded with %r." %
                self.query_string_encoding)
        
        # Python 2 only: keyword arguments must be byte strings (type 'str').
        if not py3k:
            for key, value in p.items():
                if isinstance(key, unicode):
                    del p[key]
                    p[key.encode(self.query_string_encoding)] = value
        self.params.update(p)
    
    def process_headers(self):
        """Parse HTTP header data into Python structures. (Core)"""
        # Process the headers into self.headers
        headers = self.headers
        for name, value in self.header_list:
            # Call title() now (and use dict.__method__(headers))
            # so title doesn't have to be called twice.
            name = name.title()
            value = value.strip()
            
            # Warning: if there is more than one header entry for cookies (AFAIK,
            # only Konqueror does that), only the last one will remain in headers
            # (but they will be correctly stored in request.cookie).
            if "=?" in value:
                dict.__setitem__(headers, name, httputil.decode_TEXT(value))
            else:
                dict.__setitem__(headers, name, value)
            
            # Handle cookies differently because on Konqueror, multiple
            # cookies come on different lines with the same key
            if name == 'Cookie':
                try:
                    self.cookie.load(value)
                except CookieError:
                    msg = "Illegal cookie name %s" % value.split('=')[0]
                    raise cherrypy.HTTPError(400, msg)
        
        if not dict.__contains__(headers, 'Host'):
            # All Internet-based HTTP/1.1 servers MUST respond with a 400
            # (Bad Request) status code to any HTTP/1.1 request message
            # which lacks a Host header field.
            if self.protocol >= (1, 1):
                msg = "HTTP/1.1 requires a 'Host' request header."
                raise cherrypy.HTTPError(400, msg)
        host = dict.get(headers, 'Host')
        if not host:
            host = self.local.name or self.local.ip
        self.base = "%s://%s" % (self.scheme, host)
    
    def get_resource(self, path):
        """Call a dispatcher (which sets self.handler and .config). (Core)"""
        # First, see if there is a custom dispatch at this URI. Custom
        # dispatchers can only be specified in app.config, not in _cp_config
        # (since custom dispatchers may not even have an app.root).
        dispatch = self.app.find_config(path, "request.dispatch", self.dispatch)
        
        # dispatch() should set self.handler and self.config
        dispatch(path)
    
    def handle_error(self):
        """Handle the last unanticipated exception. (Core)"""
        try:
            self.hooks.run("before_error_response")
            if self.error_response:
                self.error_response()
            self.hooks.run("after_error_response")
            cherrypy.serving.response.finalize()
        except cherrypy.HTTPRedirect:
            inst = sys.exc_info()[1]
            inst.set_response()
            cherrypy.serving.response.finalize()
    
    # ------------------------- Properties ------------------------- #
    
    def _get_body_params(self):
        warnings.warn(
                "body_params is deprecated in CherryPy 3.2, will be removed in "
                "CherryPy 3.3.",
                DeprecationWarning
            )
        return self.body.params
    body_params = property(_get_body_params,
                      doc= """
    If the request Content-Type is 'application/x-www-form-urlencoded' or
    multipart, this will be a dict of the params pulled from the entity
    body; that is, it will be the portion of request.params that come
    from the message body (sometimes called "POST params", although they
    can be sent with various HTTP method verbs). This value is set between
    the 'before_request_body' and 'before_handler' hooks (assuming that
    process_request_body is True).
    
    Deprecated in 3.2, will be removed for 3.3 in favor of
    :attr:`request.body.params<cherrypy._cprequest.RequestBody.params>`.""")


class ResponseBody(object):
    """The body of the HTTP response (the response entity)."""
    
    if py3k:
        unicode_err = ("Page handlers MUST return bytes. Use tools.encode "
                       "if you wish to return unicode.")
    
    def __get__(self, obj, objclass=None):
        if obj is None:
            # When calling on the class instead of an instance...
            return self
        else:
            return obj._body
    
    def __set__(self, obj, value):
        # Convert the given value to an iterable object.
        if py3k and isinstance(value, str):
            raise ValueError(self.unicode_err)
        
        if isinstance(value, basestring):
            # strings get wrapped in a list because iterating over a single
            # item list is much faster than iterating over every character
            # in a long string.
            if value:
                value = [value]
            else:
                # [''] doesn't evaluate to False, so replace it with [].
                value = []
        elif py3k and isinstance(value, list):
            # every item in a list must be bytes... 
            for i, item in enumerate(value):
                if isinstance(item, str):
                    raise ValueError(self.unicode_err)
        # Don't use isinstance here; io.IOBase which has an ABC takes
        # 1000 times as long as, say, isinstance(value, str)
        elif hasattr(value, 'read'):
            value = file_generator(value)
        elif value is None:
            value = []
        obj._body = value


class Response(object):
    """An HTTP Response, including status, headers, and body."""
    
    status = ""
    """The HTTP Status-Code and Reason-Phrase."""
    
    header_list = []
    """
    A list of the HTTP response headers as (name, value) tuples.
    In general, you should use response.headers (a dict) instead. This
    attribute is generated from response.headers and is not valid until
    after the finalize phase."""
    
    headers = httputil.HeaderMap()
    """
    A dict-like object containing the response headers. Keys are header
    names (in Title-Case format); however, you may get and set them in
    a case-insensitive manner. That is, headers['Content-Type'] and
    headers['content-type'] refer to the same value. Values are header
    values (decoded according to :rfc:`2047` if necessary).
    
    .. seealso:: classes :class:`HeaderMap`, :class:`HeaderElement`
    """
    
    cookie = SimpleCookie()
    """See help(Cookie)."""
    
    body = ResponseBody()
    """The body (entity) of the HTTP response."""
    
    time = None
    """The value of time.time() when created. Use in HTTP dates."""
    
    timeout = 300
    """Seconds after which the response will be aborted."""
    
    timed_out = False
    """
    Flag to indicate the response should be aborted, because it has
    exceeded its timeout."""
    
    stream = False
    """If False, buffer the response body."""
    
    def __init__(self):
        self.status = None
        self.header_list = None
        self._body = []
        self.time = time.time()
        
        self.headers = httputil.HeaderMap()
        # Since we know all our keys are titled strings, we can
        # bypass HeaderMap.update and get a big speed boost.
        dict.update(self.headers, {
            "Content-Type": 'text/html',
            "Server": "CherryPy/" + cherrypy.__version__,
            "Date": httputil.HTTPDate(self.time),
        })
        self.cookie = SimpleCookie()
    
    def collapse_body(self):
        """Collapse self.body to a single string; replace it and return it."""
        if isinstance(self.body, basestring):
            return self.body
        
        newbody = []
        for chunk in self.body:
            if py3k and not isinstance(chunk, bytes):
                raise TypeError("Chunk %s is not of type 'bytes'." % repr(chunk))
            newbody.append(chunk)
        newbody = ntob('').join(newbody)
        
        self.body = newbody
        return newbody
    
    def finalize(self):
        """Transform headers (and cookies) into self.header_list. (Core)"""
        try:
            code, reason, _ = httputil.valid_status(self.status)
        except ValueError:
            raise cherrypy.HTTPError(500, sys.exc_info()[1].args[0])
        
        headers = self.headers
        
        self.status = "%s %s" % (code, reason)
        self.output_status = ntob(str(code), 'ascii') + ntob(" ") + headers.encode(reason)
        
        if self.stream:
            # The upshot: wsgiserver will chunk the response if
            # you pop Content-Length (or set it explicitly to None).
            # Note that lib.static sets C-L to the file's st_size.
            if dict.get(headers, 'Content-Length') is None:
                dict.pop(headers, 'Content-Length', None)
        elif code < 200 or code in (204, 205, 304):
            # "All 1xx (informational), 204 (no content),
            # and 304 (not modified) responses MUST NOT
            # include a message-body."
            dict.pop(headers, 'Content-Length', None)
            self.body = ntob("")
        else:
            # Responses which are not streamed should have a Content-Length,
            # but allow user code to set Content-Length if desired.
            if dict.get(headers, 'Content-Length') is None:
                content = self.collapse_body()
                dict.__setitem__(headers, 'Content-Length', len(content))
        
        # Transform our header dict into a list of tuples.
        self.header_list = h = headers.output()
        
        cookie = self.cookie.output()
        if cookie:
            for line in cookie.split("\n"):
                if line.endswith("\r"):
                    # Python 2.4 emits cookies joined by LF but 2.5+ by CRLF.
                    line = line[:-1]
                name, value = line.split(": ", 1)
                if isinstance(name, unicodestr):
                    name = name.encode("ISO-8859-1")
                if isinstance(value, unicodestr):
                    value = headers.encode(value)
                h.append((name, value))
    
    def check_timeout(self):
        """If now > self.time + self.timeout, set self.timed_out.
        
        This purposefully sets a flag, rather than raising an error,
        so that a monitor thread can interrupt the Response thread.
        """
        if time.time() > self.time + self.timeout:
            self.timed_out = True




########NEW FILE########
__FILENAME__ = _cpserver
"""Manage HTTP servers with CherryPy."""

import warnings

import cherrypy
from cherrypy.lib import attributes
from cherrypy._cpcompat import basestring, py3k

# We import * because we want to export check_port
# et al as attributes of this module.
from cherrypy.process.servers import *


class Server(ServerAdapter):
    """An adapter for an HTTP server.
    
    You can set attributes (like socket_host and socket_port)
    on *this* object (which is probably cherrypy.server), and call
    quickstart. For example::
    
        cherrypy.server.socket_port = 80
        cherrypy.quickstart()
    """
    
    socket_port = 8080
    """The TCP port on which to listen for connections."""
    
    _socket_host = '127.0.0.1'
    def _get_socket_host(self):
        return self._socket_host
    def _set_socket_host(self, value):
        if value == '':
            raise ValueError("The empty string ('') is not an allowed value. "
                             "Use '0.0.0.0' instead to listen on all active "
                             "interfaces (INADDR_ANY).")
        self._socket_host = value
    socket_host = property(_get_socket_host, _set_socket_host,
        doc="""The hostname or IP address on which to listen for connections.
        
        Host values may be any IPv4 or IPv6 address, or any valid hostname.
        The string 'localhost' is a synonym for '127.0.0.1' (or '::1', if
        your hosts file prefers IPv6). The string '0.0.0.0' is a special
        IPv4 entry meaning "any active interface" (INADDR_ANY), and '::'
        is the similar IN6ADDR_ANY for IPv6. The empty string or None are
        not allowed.""")
    
    socket_file = None
    """If given, the name of the UNIX socket to use instead of TCP/IP.
    
    When this option is not None, the `socket_host` and `socket_port` options
    are ignored."""
    
    socket_queue_size = 5
    """The 'backlog' argument to socket.listen(); specifies the maximum number
    of queued connections (default 5)."""
    
    socket_timeout = 10
    """The timeout in seconds for accepted connections (default 10)."""
    
    shutdown_timeout = 5
    """The time to wait for HTTP worker threads to clean up."""
    
    protocol_version = 'HTTP/1.1'
    """The version string to write in the Status-Line of all HTTP responses,
    for example, "HTTP/1.1" (the default). Depending on the HTTP server used,
    this should also limit the supported features used in the response."""
    
    thread_pool = 10
    """The number of worker threads to start up in the pool."""
    
    thread_pool_max = -1
    """The maximum size of the worker-thread pool. Use -1 to indicate no limit."""
    
    max_request_header_size = 500 * 1024
    """The maximum number of bytes allowable in the request headers. If exceeded,
    the HTTP server should return "413 Request Entity Too Large"."""
    
    max_request_body_size = 100 * 1024 * 1024
    """The maximum number of bytes allowable in the request body. If exceeded,
    the HTTP server should return "413 Request Entity Too Large"."""
    
    instance = None
    """If not None, this should be an HTTP server instance (such as
    CPWSGIServer) which cherrypy.server will control. Use this when you need
    more control over object instantiation than is available in the various
    configuration options."""
    
    ssl_context = None
    """When using PyOpenSSL, an instance of SSL.Context."""
    
    ssl_certificate = None
    """The filename of the SSL certificate to use."""
    
    ssl_certificate_chain = None
    """When using PyOpenSSL, the certificate chain to pass to
    Context.load_verify_locations."""
    
    ssl_private_key = None
    """The filename of the private key to use with SSL."""
    
    if py3k:
        ssl_module = 'builtin'
        """The name of a registered SSL adaptation module to use with the builtin
        WSGI server. Builtin options are: 'builtin' (to use the SSL library built
        into recent versions of Python). You may also register your
        own classes in the wsgiserver.ssl_adapters dict."""
    else:
        ssl_module = 'pyopenssl'
        """The name of a registered SSL adaptation module to use with the builtin
        WSGI server. Builtin options are 'builtin' (to use the SSL library built
        into recent versions of Python) and 'pyopenssl' (to use the PyOpenSSL
        project, which you must install separately). You may also register your
        own classes in the wsgiserver.ssl_adapters dict."""
    
    statistics = False
    """Turns statistics-gathering on or off for aware HTTP servers."""
    
    nodelay = True
    """If True (the default since 3.1), sets the TCP_NODELAY socket option."""
    
    wsgi_version = (1, 0)
    """The WSGI version tuple to use with the builtin WSGI server.
    The provided options are (1, 0) [which includes support for PEP 3333,
    which declares it covers WSGI version 1.0.1 but still mandates the
    wsgi.version (1, 0)] and ('u', 0), an experimental unicode version.
    You may create and register your own experimental versions of the WSGI
    protocol by adding custom classes to the wsgiserver.wsgi_gateways dict."""
    
    def __init__(self):
        self.bus = cherrypy.engine
        self.httpserver = None
        self.interrupt = None
        self.running = False
    
    def httpserver_from_self(self, httpserver=None):
        """Return a (httpserver, bind_addr) pair based on self attributes."""
        if httpserver is None:
            httpserver = self.instance
        if httpserver is None:
            from cherrypy import _cpwsgi_server
            httpserver = _cpwsgi_server.CPWSGIServer(self)
        if isinstance(httpserver, basestring):
            # Is anyone using this? Can I add an arg?
            httpserver = attributes(httpserver)(self)
        return httpserver, self.bind_addr
    
    def start(self):
        """Start the HTTP server."""
        if not self.httpserver:
            self.httpserver, self.bind_addr = self.httpserver_from_self()
        ServerAdapter.start(self)
    start.priority = 75
    
    def _get_bind_addr(self):
        if self.socket_file:
            return self.socket_file
        if self.socket_host is None and self.socket_port is None:
            return None
        return (self.socket_host, self.socket_port)
    def _set_bind_addr(self, value):
        if value is None:
            self.socket_file = None
            self.socket_host = None
            self.socket_port = None
        elif isinstance(value, basestring):
            self.socket_file = value
            self.socket_host = None
            self.socket_port = None
        else:
            try:
                self.socket_host, self.socket_port = value
                self.socket_file = None
            except ValueError:
                raise ValueError("bind_addr must be a (host, port) tuple "
                                 "(for TCP sockets) or a string (for Unix "
                                 "domain sockets), not %r" % value)
    bind_addr = property(_get_bind_addr, _set_bind_addr,
        doc='A (host, port) tuple for TCP sockets or a str for Unix domain sockets.')
    
    def base(self):
        """Return the base (scheme://host[:port] or sock file) for this server."""
        if self.socket_file:
            return self.socket_file
        
        host = self.socket_host
        if host in ('0.0.0.0', '::'):
            # 0.0.0.0 is INADDR_ANY and :: is IN6ADDR_ANY.
            # Look up the host name, which should be the
            # safest thing to spit out in a URL.
            import socket
            host = socket.gethostname()
        
        port = self.socket_port
        
        if self.ssl_certificate:
            scheme = "https"
            if port != 443:
                host += ":%s" % port
        else:
            scheme = "http"
            if port != 80:
                host += ":%s" % port
        
        return "%s://%s" % (scheme, host)


########NEW FILE########
__FILENAME__ = _cpthreadinglocal
# This is a backport of Python-2.4's threading.local() implementation

"""Thread-local objects

(Note that this module provides a Python version of thread
 threading.local class.  Depending on the version of Python you're
 using, there may be a faster one available.  You should always import
 the local class from threading.)

Thread-local objects support the management of thread-local data.
If you have data that you want to be local to a thread, simply create
a thread-local object and use its attributes:

  >>> mydata = local()
  >>> mydata.number = 42
  >>> mydata.number
  42

You can also access the local-object's dictionary:

  >>> mydata.__dict__
  {'number': 42}
  >>> mydata.__dict__.setdefault('widgets', [])
  []
  >>> mydata.widgets
  []

What's important about thread-local objects is that their data are
local to a thread. If we access the data in a different thread:

  >>> log = []
  >>> def f():
  ...     items = mydata.__dict__.items()
  ...     items.sort()
  ...     log.append(items)
  ...     mydata.number = 11
  ...     log.append(mydata.number)

  >>> import threading
  >>> thread = threading.Thread(target=f)
  >>> thread.start()
  >>> thread.join()
  >>> log
  [[], 11]

we get different data.  Furthermore, changes made in the other thread
don't affect data seen in this thread:

  >>> mydata.number
  42

Of course, values you get from a local object, including a __dict__
attribute, are for whatever thread was current at the time the
attribute was read.  For that reason, you generally don't want to save
these values across threads, as they apply only to the thread they
came from.

You can create custom local objects by subclassing the local class:

  >>> class MyLocal(local):
  ...     number = 2
  ...     initialized = False
  ...     def __init__(self, **kw):
  ...         if self.initialized:
  ...             raise SystemError('__init__ called too many times')
  ...         self.initialized = True
  ...         self.__dict__.update(kw)
  ...     def squared(self):
  ...         return self.number ** 2

This can be useful to support default values, methods and
initialization.  Note that if you define an __init__ method, it will be
called each time the local object is used in a separate thread.  This
is necessary to initialize each thread's dictionary.

Now if we create a local object:

  >>> mydata = MyLocal(color='red')

Now we have a default number:

  >>> mydata.number
  2

an initial color:

  >>> mydata.color
  'red'
  >>> del mydata.color

And a method that operates on the data:

  >>> mydata.squared()
  4

As before, we can access the data in a separate thread:

  >>> log = []
  >>> thread = threading.Thread(target=f)
  >>> thread.start()
  >>> thread.join()
  >>> log
  [[('color', 'red'), ('initialized', True)], 11]

without affecting this thread's data:

  >>> mydata.number
  2
  >>> mydata.color
  Traceback (most recent call last):
  ...
  AttributeError: 'MyLocal' object has no attribute 'color'

Note that subclasses can define slots, but they are not thread
local. They are shared across threads:

  >>> class MyLocal(local):
  ...     __slots__ = 'number'

  >>> mydata = MyLocal()
  >>> mydata.number = 42
  >>> mydata.color = 'red'

So, the separate thread:

  >>> thread = threading.Thread(target=f)
  >>> thread.start()
  >>> thread.join()

affects what we see:

  >>> mydata.number
  11

>>> del mydata
"""

# Threading import is at end

class _localbase(object):
    __slots__ = '_local__key', '_local__args', '_local__lock'

    def __new__(cls, *args, **kw):
        self = object.__new__(cls)
        key = 'thread.local.' + str(id(self))
        object.__setattr__(self, '_local__key', key)
        object.__setattr__(self, '_local__args', (args, kw))
        object.__setattr__(self, '_local__lock', RLock())

        if args or kw and (cls.__init__ is object.__init__):
            raise TypeError("Initialization arguments are not supported")

        # We need to create the thread dict in anticipation of
        # __init__ being called, to make sure we don't call it
        # again ourselves.
        dict = object.__getattribute__(self, '__dict__')
        currentThread().__dict__[key] = dict

        return self

def _patch(self):
    key = object.__getattribute__(self, '_local__key')
    d = currentThread().__dict__.get(key)
    if d is None:
        d = {}
        currentThread().__dict__[key] = d
        object.__setattr__(self, '__dict__', d)

        # we have a new instance dict, so call out __init__ if we have
        # one
        cls = type(self)
        if cls.__init__ is not object.__init__:
            args, kw = object.__getattribute__(self, '_local__args')
            cls.__init__(self, *args, **kw)
    else:
        object.__setattr__(self, '__dict__', d)

class local(_localbase):

    def __getattribute__(self, name):
        lock = object.__getattribute__(self, '_local__lock')
        lock.acquire()
        try:
            _patch(self)
            return object.__getattribute__(self, name)
        finally:
            lock.release()

    def __setattr__(self, name, value):
        lock = object.__getattribute__(self, '_local__lock')
        lock.acquire()
        try:
            _patch(self)
            return object.__setattr__(self, name, value)
        finally:
            lock.release()

    def __delattr__(self, name):
        lock = object.__getattribute__(self, '_local__lock')
        lock.acquire()
        try:
            _patch(self)
            return object.__delattr__(self, name)
        finally:
            lock.release()


    def __del__():
        threading_enumerate = enumerate
        __getattribute__ = object.__getattribute__

        def __del__(self):
            key = __getattribute__(self, '_local__key')

            try:
                threads = list(threading_enumerate())
            except:
                # if enumerate fails, as it seems to do during
                # shutdown, we'll skip cleanup under the assumption
                # that there is nothing to clean up
                return

            for thread in threads:
                try:
                    __dict__ = thread.__dict__
                except AttributeError:
                    # Thread is dying, rest in peace
                    continue

                if key in __dict__:
                    try:
                        del __dict__[key]
                    except KeyError:
                        pass # didn't have anything in this thread

        return __del__
    __del__ = __del__()

from threading import currentThread, enumerate, RLock

########NEW FILE########
__FILENAME__ = _cptools
"""CherryPy tools. A "tool" is any helper, adapted to CP.

Tools are usually designed to be used in a variety of ways (although some
may only offer one if they choose):
    
    Library calls
        All tools are callables that can be used wherever needed.
        The arguments are straightforward and should be detailed within the
        docstring.
    
    Function decorators
        All tools, when called, may be used as decorators which configure
        individual CherryPy page handlers (methods on the CherryPy tree).
        That is, "@tools.anytool()" should "turn on" the tool via the
        decorated function's _cp_config attribute.
    
    CherryPy config
        If a tool exposes a "_setup" callable, it will be called
        once per Request (if the feature is "turned on" via config).

Tools may be implemented as any object with a namespace. The builtins
are generally either modules or instances of the tools.Tool class.
"""

import sys
import warnings

import cherrypy


def _getargs(func):
    """Return the names of all static arguments to the given function."""
    # Use this instead of importing inspect for less mem overhead.
    import types
    if sys.version_info >= (3, 0):
        if isinstance(func, types.MethodType):
            func = func.__func__
        co = func.__code__
    else:
        if isinstance(func, types.MethodType):
            func = func.im_func
        co = func.func_code
    return co.co_varnames[:co.co_argcount]


_attr_error = ("CherryPy Tools cannot be turned on directly. Instead, turn them "
               "on via config, or use them as decorators on your page handlers.")

class Tool(object):
    """A registered function for use with CherryPy request-processing hooks.
    
    help(tool.callable) should give you more information about this Tool.
    """
    
    namespace = "tools"
    
    def __init__(self, point, callable, name=None, priority=50):
        self._point = point
        self.callable = callable
        self._name = name
        self._priority = priority
        self.__doc__ = self.callable.__doc__
        self._setargs()
    
    def _get_on(self):
        raise AttributeError(_attr_error)
    def _set_on(self, value):
        raise AttributeError(_attr_error)
    on = property(_get_on, _set_on)
    
    def _setargs(self):
        """Copy func parameter names to obj attributes."""
        try:
            for arg in _getargs(self.callable):
                setattr(self, arg, None)
        except (TypeError, AttributeError):
            if hasattr(self.callable, "__call__"):
                for arg in _getargs(self.callable.__call__):
                    setattr(self, arg, None)
        # IronPython 1.0 raises NotImplementedError because
        # inspect.getargspec tries to access Python bytecode
        # in co_code attribute.
        except NotImplementedError:
            pass
        # IronPython 1B1 may raise IndexError in some cases,
        # but if we trap it here it doesn't prevent CP from working.
        except IndexError:
            pass
    
    def _merged_args(self, d=None):
        """Return a dict of configuration entries for this Tool."""
        if d:
            conf = d.copy()
        else:
            conf = {}
        
        tm = cherrypy.serving.request.toolmaps[self.namespace]
        if self._name in tm:
            conf.update(tm[self._name])
        
        if "on" in conf:
            del conf["on"]
        
        return conf
    
    def __call__(self, *args, **kwargs):
        """Compile-time decorator (turn on the tool in config).
        
        For example::
        
            @tools.proxy()
            def whats_my_base(self):
                return cherrypy.request.base
            whats_my_base.exposed = True
        """
        if args:
            raise TypeError("The %r Tool does not accept positional "
                            "arguments; you must use keyword arguments."
                            % self._name)
        def tool_decorator(f):
            if not hasattr(f, "_cp_config"):
                f._cp_config = {}
            subspace = self.namespace + "." + self._name + "."
            f._cp_config[subspace + "on"] = True
            for k, v in kwargs.items():
                f._cp_config[subspace + k] = v
            return f
        return tool_decorator
    
    def _setup(self):
        """Hook this tool into cherrypy.request.
        
        The standard CherryPy request object will automatically call this
        method when the tool is "turned on" in config.
        """
        conf = self._merged_args()
        p = conf.pop("priority", None)
        if p is None:
            p = getattr(self.callable, "priority", self._priority)
        cherrypy.serving.request.hooks.attach(self._point, self.callable,
                                              priority=p, **conf)


class HandlerTool(Tool):
    """Tool which is called 'before main', that may skip normal handlers.
    
    If the tool successfully handles the request (by setting response.body),
    if should return True. This will cause CherryPy to skip any 'normal' page
    handler. If the tool did not handle the request, it should return False
    to tell CherryPy to continue on and call the normal page handler. If the
    tool is declared AS a page handler (see the 'handler' method), returning
    False will raise NotFound.
    """
    
    def __init__(self, callable, name=None):
        Tool.__init__(self, 'before_handler', callable, name)
    
    def handler(self, *args, **kwargs):
        """Use this tool as a CherryPy page handler.
        
        For example::
        
            class Root:
                nav = tools.staticdir.handler(section="/nav", dir="nav",
                                              root=absDir)
        """
        def handle_func(*a, **kw):
            handled = self.callable(*args, **self._merged_args(kwargs))
            if not handled:
                raise cherrypy.NotFound()
            return cherrypy.serving.response.body
        handle_func.exposed = True
        return handle_func
    
    def _wrapper(self, **kwargs):
        if self.callable(**kwargs):
            cherrypy.serving.request.handler = None
    
    def _setup(self):
        """Hook this tool into cherrypy.request.
        
        The standard CherryPy request object will automatically call this
        method when the tool is "turned on" in config.
        """
        conf = self._merged_args()
        p = conf.pop("priority", None)
        if p is None:
            p = getattr(self.callable, "priority", self._priority)
        cherrypy.serving.request.hooks.attach(self._point, self._wrapper,
                                              priority=p, **conf)


class HandlerWrapperTool(Tool):
    """Tool which wraps request.handler in a provided wrapper function.
    
    The 'newhandler' arg must be a handler wrapper function that takes a
    'next_handler' argument, plus ``*args`` and ``**kwargs``. Like all
    page handler
    functions, it must return an iterable for use as cherrypy.response.body.
    
    For example, to allow your 'inner' page handlers to return dicts
    which then get interpolated into a template::
    
        def interpolator(next_handler, *args, **kwargs):
            filename = cherrypy.request.config.get('template')
            cherrypy.response.template = env.get_template(filename)
            response_dict = next_handler(*args, **kwargs)
            return cherrypy.response.template.render(**response_dict)
        cherrypy.tools.jinja = HandlerWrapperTool(interpolator)
    """
    
    def __init__(self, newhandler, point='before_handler', name=None, priority=50):
        self.newhandler = newhandler
        self._point = point
        self._name = name
        self._priority = priority
    
    def callable(self, debug=False):
        innerfunc = cherrypy.serving.request.handler
        def wrap(*args, **kwargs):
            return self.newhandler(innerfunc, *args, **kwargs)
        cherrypy.serving.request.handler = wrap


class ErrorTool(Tool):
    """Tool which is used to replace the default request.error_response."""
    
    def __init__(self, callable, name=None):
        Tool.__init__(self, None, callable, name)
    
    def _wrapper(self):
        self.callable(**self._merged_args())
    
    def _setup(self):
        """Hook this tool into cherrypy.request.
        
        The standard CherryPy request object will automatically call this
        method when the tool is "turned on" in config.
        """
        cherrypy.serving.request.error_response = self._wrapper


#                              Builtin tools                              #

from cherrypy.lib import cptools, encoding, auth, static, jsontools
from cherrypy.lib import sessions as _sessions, xmlrpcutil as _xmlrpc
from cherrypy.lib import caching as _caching
from cherrypy.lib import auth_basic, auth_digest


class SessionTool(Tool):
    """Session Tool for CherryPy.
    
    sessions.locking
        When 'implicit' (the default), the session will be locked for you,
        just before running the page handler.
        
        When 'early', the session will be locked before reading the request
        body. This is off by default for safety reasons; for example,
        a large upload would block the session, denying an AJAX
        progress meter (see http://www.cherrypy.org/ticket/630).
        
        When 'explicit' (or any other value), you need to call
        cherrypy.session.acquire_lock() yourself before using
        session data.
    """
    
    def __init__(self):
        # _sessions.init must be bound after headers are read
        Tool.__init__(self, 'before_request_body', _sessions.init)
    
    def _lock_session(self):
        cherrypy.serving.session.acquire_lock()
    
    def _setup(self):
        """Hook this tool into cherrypy.request.
        
        The standard CherryPy request object will automatically call this
        method when the tool is "turned on" in config.
        """
        hooks = cherrypy.serving.request.hooks
        
        conf = self._merged_args()
        
        p = conf.pop("priority", None)
        if p is None:
            p = getattr(self.callable, "priority", self._priority)
        
        hooks.attach(self._point, self.callable, priority=p, **conf)
        
        locking = conf.pop('locking', 'implicit')
        if locking == 'implicit':
            hooks.attach('before_handler', self._lock_session)
        elif locking == 'early':
            # Lock before the request body (but after _sessions.init runs!)
            hooks.attach('before_request_body', self._lock_session,
                         priority=60)
        else:
            # Don't lock
            pass
        
        hooks.attach('before_finalize', _sessions.save)
        hooks.attach('on_end_request', _sessions.close)
        
    def regenerate(self):
        """Drop the current session and make a new one (with a new id)."""
        sess = cherrypy.serving.session
        sess.regenerate()
        
        # Grab cookie-relevant tool args
        conf = dict([(k, v) for k, v in self._merged_args().items()
                     if k in ('path', 'path_header', 'name', 'timeout',
                              'domain', 'secure')])
        _sessions.set_response_cookie(**conf)




class XMLRPCController(object):
    """A Controller (page handler collection) for XML-RPC.
    
    To use it, have your controllers subclass this base class (it will
    turn on the tool for you).
    
    You can also supply the following optional config entries::
    
        tools.xmlrpc.encoding: 'utf-8'
        tools.xmlrpc.allow_none: 0
    
    XML-RPC is a rather discontinuous layer over HTTP; dispatching to the
    appropriate handler must first be performed according to the URL, and
    then a second dispatch step must take place according to the RPC method
    specified in the request body. It also allows a superfluous "/RPC2"
    prefix in the URL, supplies its own handler args in the body, and
    requires a 200 OK "Fault" response instead of 404 when the desired
    method is not found.
    
    Therefore, XML-RPC cannot be implemented for CherryPy via a Tool alone.
    This Controller acts as the dispatch target for the first half (based
    on the URL); it then reads the RPC method from the request body and
    does its own second dispatch step based on that method. It also reads
    body params, and returns a Fault on error.
    
    The XMLRPCDispatcher strips any /RPC2 prefix; if you aren't using /RPC2
    in your URL's, you can safely skip turning on the XMLRPCDispatcher.
    Otherwise, you need to use declare it in config::
    
        request.dispatch: cherrypy.dispatch.XMLRPCDispatcher()
    """
    
    # Note we're hard-coding this into the 'tools' namespace. We could do
    # a huge amount of work to make it relocatable, but the only reason why
    # would be if someone actually disabled the default_toolbox. Meh.
    _cp_config = {'tools.xmlrpc.on': True}
    
    def default(self, *vpath, **params):
        rpcparams, rpcmethod = _xmlrpc.process_body()
        
        subhandler = self
        for attr in str(rpcmethod).split('.'):
            subhandler = getattr(subhandler, attr, None)
         
        if subhandler and getattr(subhandler, "exposed", False):
            body = subhandler(*(vpath + rpcparams), **params)
        
        else:
            # http://www.cherrypy.org/ticket/533
            # if a method is not found, an xmlrpclib.Fault should be returned
            # raising an exception here will do that; see
            # cherrypy.lib.xmlrpcutil.on_error
            raise Exception('method "%s" is not supported' % attr)
        
        conf = cherrypy.serving.request.toolmaps['tools'].get("xmlrpc", {})
        _xmlrpc.respond(body,
                        conf.get('encoding', 'utf-8'),
                        conf.get('allow_none', 0))
        return cherrypy.serving.response.body
    default.exposed = True


class SessionAuthTool(HandlerTool):
    
    def _setargs(self):
        for name in dir(cptools.SessionAuth):
            if not name.startswith("__"):
                setattr(self, name, None)


class CachingTool(Tool):
    """Caching Tool for CherryPy."""
    
    def _wrapper(self, **kwargs):
        request = cherrypy.serving.request
        if _caching.get(**kwargs):
            request.handler = None
        else:
            if request.cacheable:
                # Note the devious technique here of adding hooks on the fly
                request.hooks.attach('before_finalize', _caching.tee_output,
                                     priority = 90)
    _wrapper.priority = 20
    
    def _setup(self):
        """Hook caching into cherrypy.request."""
        conf = self._merged_args()
        
        p = conf.pop("priority", None)
        cherrypy.serving.request.hooks.attach('before_handler', self._wrapper,
                                              priority=p, **conf)



class Toolbox(object):
    """A collection of Tools.
    
    This object also functions as a config namespace handler for itself.
    Custom toolboxes should be added to each Application's toolboxes dict.
    """
    
    def __init__(self, namespace):
        self.namespace = namespace
    
    def __setattr__(self, name, value):
        # If the Tool._name is None, supply it from the attribute name.
        if isinstance(value, Tool):
            if value._name is None:
                value._name = name
            value.namespace = self.namespace
        object.__setattr__(self, name, value)
    
    def __enter__(self):
        """Populate request.toolmaps from tools specified in config."""
        cherrypy.serving.request.toolmaps[self.namespace] = map = {}
        def populate(k, v):
            toolname, arg = k.split(".", 1)
            bucket = map.setdefault(toolname, {})
            bucket[arg] = v
        return populate
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Run tool._setup() for each tool in our toolmap."""
        map = cherrypy.serving.request.toolmaps.get(self.namespace)
        if map:
            for name, settings in map.items():
                if settings.get("on", False):
                    tool = getattr(self, name)
                    tool._setup()


class DeprecatedTool(Tool):
    
    _name = None
    warnmsg = "This Tool is deprecated."
    
    def __init__(self, point, warnmsg=None):
        self.point = point
        if warnmsg is not None:
            self.warnmsg = warnmsg
    
    def __call__(self, *args, **kwargs):
        warnings.warn(self.warnmsg)
        def tool_decorator(f):
            return f
        return tool_decorator
    
    def _setup(self):
        warnings.warn(self.warnmsg)


default_toolbox = _d = Toolbox("tools")
_d.session_auth = SessionAuthTool(cptools.session_auth)
_d.allow = Tool('on_start_resource', cptools.allow)
_d.proxy = Tool('before_request_body', cptools.proxy, priority=30)
_d.response_headers = Tool('on_start_resource', cptools.response_headers)
_d.log_tracebacks = Tool('before_error_response', cptools.log_traceback)
_d.log_headers = Tool('before_error_response', cptools.log_request_headers)
_d.log_hooks = Tool('on_end_request', cptools.log_hooks, priority=100)
_d.err_redirect = ErrorTool(cptools.redirect)
_d.etags = Tool('before_finalize', cptools.validate_etags, priority=75)
_d.decode = Tool('before_request_body', encoding.decode)
# the order of encoding, gzip, caching is important
_d.encode = Tool('before_handler', encoding.ResponseEncoder, priority=70)
_d.gzip = Tool('before_finalize', encoding.gzip, priority=80)
_d.staticdir = HandlerTool(static.staticdir)
_d.staticfile = HandlerTool(static.staticfile)
_d.sessions = SessionTool()
_d.xmlrpc = ErrorTool(_xmlrpc.on_error)
_d.caching = CachingTool('before_handler', _caching.get, 'caching')
_d.expires = Tool('before_finalize', _caching.expires)
_d.tidy = DeprecatedTool('before_finalize',
    "The tidy tool has been removed from the standard distribution of CherryPy. "
    "The most recent version can be found at http://tools.cherrypy.org/browser.")
_d.nsgmls = DeprecatedTool('before_finalize',
    "The nsgmls tool has been removed from the standard distribution of CherryPy. "
    "The most recent version can be found at http://tools.cherrypy.org/browser.")
_d.ignore_headers = Tool('before_request_body', cptools.ignore_headers)
_d.referer = Tool('before_request_body', cptools.referer)
_d.basic_auth = Tool('on_start_resource', auth.basic_auth)
_d.digest_auth = Tool('on_start_resource', auth.digest_auth)
_d.trailing_slash = Tool('before_handler', cptools.trailing_slash, priority=60)
_d.flatten = Tool('before_finalize', cptools.flatten)
_d.accept = Tool('on_start_resource', cptools.accept)
_d.redirect = Tool('on_start_resource', cptools.redirect)
_d.autovary = Tool('on_start_resource', cptools.autovary, priority=0)
_d.json_in = Tool('before_request_body', jsontools.json_in, priority=30)
_d.json_out = Tool('before_handler', jsontools.json_out, priority=30)
_d.auth_basic = Tool('before_handler', auth_basic.basic_auth, priority=1)
_d.auth_digest = Tool('before_handler', auth_digest.digest_auth, priority=1)

del _d, cptools, encoding, auth, static

########NEW FILE########
__FILENAME__ = _cptree
"""CherryPy Application and Tree objects."""

import os
import sys

import cherrypy
from cherrypy._cpcompat import ntou, py3k
from cherrypy import _cpconfig, _cplogging, _cprequest, _cpwsgi, tools
from cherrypy.lib import httputil


class Application(object):
    """A CherryPy Application.
    
    Servers and gateways should not instantiate Request objects directly.
    Instead, they should ask an Application object for a request object.
    
    An instance of this class may also be used as a WSGI callable
    (WSGI application object) for itself.
    """
    
    root = None
    """The top-most container of page handlers for this app. Handlers should
    be arranged in a hierarchy of attributes, matching the expected URI
    hierarchy; the default dispatcher then searches this hierarchy for a
    matching handler. When using a dispatcher other than the default,
    this value may be None."""
    
    config = {}
    """A dict of {path: pathconf} pairs, where 'pathconf' is itself a dict
    of {key: value} pairs."""
    
    namespaces = _cpconfig.NamespaceSet()
    toolboxes = {'tools': cherrypy.tools}
    
    log = None
    """A LogManager instance. See _cplogging."""
    
    wsgiapp = None
    """A CPWSGIApp instance. See _cpwsgi."""
    
    request_class = _cprequest.Request
    response_class = _cprequest.Response
    
    relative_urls = False
    
    def __init__(self, root, script_name="", config=None):
        self.log = _cplogging.LogManager(id(self), cherrypy.log.logger_root)
        self.root = root
        self.script_name = script_name
        self.wsgiapp = _cpwsgi.CPWSGIApp(self)
        
        self.namespaces = self.namespaces.copy()
        self.namespaces["log"] = lambda k, v: setattr(self.log, k, v)
        self.namespaces["wsgi"] = self.wsgiapp.namespace_handler
        
        self.config = self.__class__.config.copy()
        if config:
            self.merge(config)
    
    def __repr__(self):
        return "%s.%s(%r, %r)" % (self.__module__, self.__class__.__name__,
                                  self.root, self.script_name)
    
    script_name_doc = """The URI "mount point" for this app. A mount point is that portion of
    the URI which is constant for all URIs that are serviced by this
    application; it does not include scheme, host, or proxy ("virtual host")
    portions of the URI.
    
    For example, if script_name is "/my/cool/app", then the URL
    "http://www.example.com/my/cool/app/page1" might be handled by a
    "page1" method on the root object.
    
    The value of script_name MUST NOT end in a slash. If the script_name
    refers to the root of the URI, it MUST be an empty string (not "/").
    
    If script_name is explicitly set to None, then the script_name will be
    provided for each call from request.wsgi_environ['SCRIPT_NAME'].
    """
    def _get_script_name(self):
        if self._script_name is None:
            # None signals that the script name should be pulled from WSGI environ.
            return cherrypy.serving.request.wsgi_environ['SCRIPT_NAME'].rstrip("/")
        return self._script_name
    def _set_script_name(self, value):
        if value:
            value = value.rstrip("/")
        self._script_name = value
    script_name = property(fget=_get_script_name, fset=_set_script_name,
                           doc=script_name_doc)
    
    def merge(self, config):
        """Merge the given config into self.config."""
        _cpconfig.merge(self.config, config)
        
        # Handle namespaces specified in config.
        self.namespaces(self.config.get("/", {}))
    
    def find_config(self, path, key, default=None):
        """Return the most-specific value for key along path, or default."""
        trail = path or "/"
        while trail:
            nodeconf = self.config.get(trail, {})
            
            if key in nodeconf:
                return nodeconf[key]
            
            lastslash = trail.rfind("/")
            if lastslash == -1:
                break
            elif lastslash == 0 and trail != "/":
                trail = "/"
            else:
                trail = trail[:lastslash]
        
        return default
    
    def get_serving(self, local, remote, scheme, sproto):
        """Create and return a Request and Response object."""
        req = self.request_class(local, remote, scheme, sproto)
        req.app = self
        
        for name, toolbox in self.toolboxes.items():
            req.namespaces[name] = toolbox
        
        resp = self.response_class()
        cherrypy.serving.load(req, resp)
        cherrypy.engine.publish('acquire_thread')
        cherrypy.engine.publish('before_request')
        
        return req, resp
    
    def release_serving(self):
        """Release the current serving (request and response)."""
        req = cherrypy.serving.request
        
        cherrypy.engine.publish('after_request')
        
        try:
            req.close()
        except:
            cherrypy.log(traceback=True, severity=40)
        
        cherrypy.serving.clear()
    
    def __call__(self, environ, start_response):
        return self.wsgiapp(environ, start_response)


class Tree(object):
    """A registry of CherryPy applications, mounted at diverse points.
    
    An instance of this class may also be used as a WSGI callable
    (WSGI application object), in which case it dispatches to all
    mounted apps.
    """
    
    apps = {}
    """
    A dict of the form {script name: application}, where "script name"
    is a string declaring the URI mount point (no trailing slash), and
    "application" is an instance of cherrypy.Application (or an arbitrary
    WSGI callable if you happen to be using a WSGI server)."""
    
    def __init__(self):
        self.apps = {}
    
    def mount(self, root, script_name="", config=None):
        """Mount a new app from a root object, script_name, and config.
        
        root
            An instance of a "controller class" (a collection of page
            handler methods) which represents the root of the application.
            This may also be an Application instance, or None if using
            a dispatcher other than the default.
        
        script_name
            A string containing the "mount point" of the application.
            This should start with a slash, and be the path portion of the
            URL at which to mount the given root. For example, if root.index()
            will handle requests to "http://www.example.com:8080/dept/app1/",
            then the script_name argument would be "/dept/app1".
            
            It MUST NOT end in a slash. If the script_name refers to the
            root of the URI, it MUST be an empty string (not "/").
        
        config
            A file or dict containing application config.
        """
        if script_name is None:
            raise TypeError(
                "The 'script_name' argument may not be None. Application "
                "objects may, however, possess a script_name of None (in "
                "order to inpect the WSGI environ for SCRIPT_NAME upon each "
                "request). You cannot mount such Applications on this Tree; "
                "you must pass them to a WSGI server interface directly.")
        
        # Next line both 1) strips trailing slash and 2) maps "/" -> "".
        script_name = script_name.rstrip("/")
        
        if isinstance(root, Application):
            app = root
            if script_name != "" and script_name != app.script_name:
                raise ValueError("Cannot specify a different script name and "
                                 "pass an Application instance to cherrypy.mount")
            script_name = app.script_name
        else:
            app = Application(root, script_name)
            
            # If mounted at "", add favicon.ico
            if (script_name == "" and root is not None
                    and not hasattr(root, "favicon_ico")):
                favicon = os.path.join(os.getcwd(), os.path.dirname(__file__),
                                       "favicon.ico")
                root.favicon_ico = tools.staticfile.handler(favicon)
        
        if config:
            app.merge(config)
        
        self.apps[script_name] = app
        
        return app
    
    def graft(self, wsgi_callable, script_name=""):
        """Mount a wsgi callable at the given script_name."""
        # Next line both 1) strips trailing slash and 2) maps "/" -> "".
        script_name = script_name.rstrip("/")
        self.apps[script_name] = wsgi_callable
    
    def script_name(self, path=None):
        """The script_name of the app at the given path, or None.
        
        If path is None, cherrypy.request is used.
        """
        if path is None:
            try:
                request = cherrypy.serving.request
                path = httputil.urljoin(request.script_name,
                                        request.path_info)
            except AttributeError:
                return None
        
        while True:
            if path in self.apps:
                return path
            
            if path == "":
                return None
            
            # Move one node up the tree and try again.
            path = path[:path.rfind("/")]
    
    def __call__(self, environ, start_response):
        # If you're calling this, then you're probably setting SCRIPT_NAME
        # to '' (some WSGI servers always set SCRIPT_NAME to '').
        # Try to look up the app using the full path.
        env1x = environ
        if environ.get(ntou('wsgi.version')) == (ntou('u'), 0):
            env1x = _cpwsgi.downgrade_wsgi_ux_to_1x(environ)
        path = httputil.urljoin(env1x.get('SCRIPT_NAME', ''),
                                env1x.get('PATH_INFO', ''))
        sn = self.script_name(path or "/")
        if sn is None:
            start_response('404 Not Found', [])
            return []
        
        app = self.apps[sn]
        
        # Correct the SCRIPT_NAME and PATH_INFO environ entries.
        environ = environ.copy()
        if not py3k:
            if environ.get(ntou('wsgi.version')) == (ntou('u'), 0):
                # Python 2/WSGI u.0: all strings MUST be of type unicode
                enc = environ[ntou('wsgi.url_encoding')]
                environ[ntou('SCRIPT_NAME')] = sn.decode(enc)
                environ[ntou('PATH_INFO')] = path[len(sn.rstrip("/")):].decode(enc)
            else:
                # Python 2/WSGI 1.x: all strings MUST be of type str
                environ['SCRIPT_NAME'] = sn
                environ['PATH_INFO'] = path[len(sn.rstrip("/")):]
        else:
            if environ.get(ntou('wsgi.version')) == (ntou('u'), 0):
                # Python 3/WSGI u.0: all strings MUST be full unicode
                environ['SCRIPT_NAME'] = sn
                environ['PATH_INFO'] = path[len(sn.rstrip("/")):]
            else:
                # Python 3/WSGI 1.x: all strings MUST be ISO-8859-1 str
                environ['SCRIPT_NAME'] = sn.encode('utf-8').decode('ISO-8859-1')
                environ['PATH_INFO'] = path[len(sn.rstrip("/")):].encode('utf-8').decode('ISO-8859-1')
        return app(environ, start_response)

########NEW FILE########
__FILENAME__ = _cpwsgi
"""WSGI interface (see PEP 333 and 3333).

Note that WSGI environ keys and values are 'native strings'; that is,
whatever the type of "" is. For Python 2, that's a byte string; for Python 3,
it's a unicode string. But PEP 3333 says: "even if Python's str type is
actually Unicode "under the hood", the content of native strings must
still be translatable to bytes via the Latin-1 encoding!"
"""

import sys as _sys

import cherrypy as _cherrypy
from cherrypy._cpcompat import BytesIO, bytestr, ntob, ntou, py3k, unicodestr
from cherrypy import _cperror
from cherrypy.lib import httputil


def downgrade_wsgi_ux_to_1x(environ):
    """Return a new environ dict for WSGI 1.x from the given WSGI u.x environ."""
    env1x = {}
    
    url_encoding = environ[ntou('wsgi.url_encoding')]
    for k, v in list(environ.items()):
        if k in [ntou('PATH_INFO'), ntou('SCRIPT_NAME'), ntou('QUERY_STRING')]:
            v = v.encode(url_encoding)
        elif isinstance(v, unicodestr):
            v = v.encode('ISO-8859-1')
        env1x[k.encode('ISO-8859-1')] = v
    
    return env1x


class VirtualHost(object):
    """Select a different WSGI application based on the Host header.
    
    This can be useful when running multiple sites within one CP server.
    It allows several domains to point to different applications. For example::
    
        root = Root()
        RootApp = cherrypy.Application(root)
        Domain2App = cherrypy.Application(root)
        SecureApp = cherrypy.Application(Secure())
        
        vhost = cherrypy._cpwsgi.VirtualHost(RootApp,
            domains={'www.domain2.example': Domain2App,
                     'www.domain2.example:443': SecureApp,
                     })
        
        cherrypy.tree.graft(vhost)
    """
    default = None
    """Required. The default WSGI application."""
    
    use_x_forwarded_host = True
    """If True (the default), any "X-Forwarded-Host"
    request header will be used instead of the "Host" header. This
    is commonly added by HTTP servers (such as Apache) when proxying."""
    
    domains = {}
    """A dict of {host header value: application} pairs.
    The incoming "Host" request header is looked up in this dict,
    and, if a match is found, the corresponding WSGI application
    will be called instead of the default. Note that you often need
    separate entries for "example.com" and "www.example.com".
    In addition, "Host" headers may contain the port number.
    """
    
    def __init__(self, default, domains=None, use_x_forwarded_host=True):
        self.default = default
        self.domains = domains or {}
        self.use_x_forwarded_host = use_x_forwarded_host
    
    def __call__(self, environ, start_response):
        domain = environ.get('HTTP_HOST', '')
        if self.use_x_forwarded_host:
            domain = environ.get("HTTP_X_FORWARDED_HOST", domain)
        
        nextapp = self.domains.get(domain)
        if nextapp is None:
            nextapp = self.default
        return nextapp(environ, start_response)


class InternalRedirector(object):
    """WSGI middleware that handles raised cherrypy.InternalRedirect."""
    
    def __init__(self, nextapp, recursive=False):
        self.nextapp = nextapp
        self.recursive = recursive
    
    def __call__(self, environ, start_response):
        redirections = []
        while True:
            environ = environ.copy()
            try:
                return self.nextapp(environ, start_response)
            except _cherrypy.InternalRedirect:
                ir = _sys.exc_info()[1]
                sn = environ.get('SCRIPT_NAME', '')
                path = environ.get('PATH_INFO', '')
                qs = environ.get('QUERY_STRING', '')
                
                # Add the *previous* path_info + qs to redirections.
                old_uri = sn + path
                if qs:
                    old_uri += "?" + qs
                redirections.append(old_uri)
                
                if not self.recursive:
                    # Check to see if the new URI has been redirected to already
                    new_uri = sn + ir.path
                    if ir.query_string:
                        new_uri += "?" + ir.query_string
                    if new_uri in redirections:
                        ir.request.close()
                        raise RuntimeError("InternalRedirector visited the "
                                           "same URL twice: %r" % new_uri)
                
                # Munge the environment and try again.
                environ['REQUEST_METHOD'] = "GET"
                environ['PATH_INFO'] = ir.path
                environ['QUERY_STRING'] = ir.query_string
                environ['wsgi.input'] = BytesIO()
                environ['CONTENT_LENGTH'] = "0"
                environ['cherrypy.previous_request'] = ir.request


class ExceptionTrapper(object):
    """WSGI middleware that traps exceptions."""
    
    def __init__(self, nextapp, throws=(KeyboardInterrupt, SystemExit)):
        self.nextapp = nextapp
        self.throws = throws
    
    def __call__(self, environ, start_response):
        return _TrappedResponse(self.nextapp, environ, start_response, self.throws)


class _TrappedResponse(object):
    
    response = iter([])
    
    def __init__(self, nextapp, environ, start_response, throws):
        self.nextapp = nextapp
        self.environ = environ
        self.start_response = start_response
        self.throws = throws
        self.started_response = False
        self.response = self.trap(self.nextapp, self.environ, self.start_response)
        self.iter_response = iter(self.response)
    
    def __iter__(self):
        self.started_response = True
        return self
    
    if py3k:
        def __next__(self):
            return self.trap(next, self.iter_response)
    else:
        def next(self):
            return self.trap(self.iter_response.next)
    
    def close(self):
        if hasattr(self.response, 'close'):
            self.response.close()
    
    def trap(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except self.throws:
            raise
        except StopIteration:
            raise
        except:
            tb = _cperror.format_exc()
            #print('trapped (started %s):' % self.started_response, tb)
            _cherrypy.log(tb, severity=40)
            if not _cherrypy.request.show_tracebacks:
                tb = ""
            s, h, b = _cperror.bare_error(tb)
            if py3k:
                # What fun.
                s = s.decode('ISO-8859-1')
                h = [(k.decode('ISO-8859-1'), v.decode('ISO-8859-1'))
                     for k, v in h]
            if self.started_response:
                # Empty our iterable (so future calls raise StopIteration)
                self.iter_response = iter([])
            else:
                self.iter_response = iter(b)
            
            try:
                self.start_response(s, h, _sys.exc_info())
            except:
                # "The application must not trap any exceptions raised by
                # start_response, if it called start_response with exc_info.
                # Instead, it should allow such exceptions to propagate
                # back to the server or gateway."
                # But we still log and call close() to clean up ourselves.
                _cherrypy.log(traceback=True, severity=40)
                raise
            
            if self.started_response:
                return ntob("").join(b)
            else:
                return b


#                           WSGI-to-CP Adapter                           #


class AppResponse(object):
    """WSGI response iterable for CherryPy applications."""
    
    def __init__(self, environ, start_response, cpapp):
        self.cpapp = cpapp
        try:
            if not py3k:
                if environ.get(ntou('wsgi.version')) == (ntou('u'), 0):
                    environ = downgrade_wsgi_ux_to_1x(environ)
            self.environ = environ
            self.run()

            r = _cherrypy.serving.response

            outstatus = r.output_status
            if not isinstance(outstatus, bytestr):
                raise TypeError("response.output_status is not a byte string.")
            
            outheaders = []
            for k, v in r.header_list:
                if not isinstance(k, bytestr):
                    raise TypeError("response.header_list key %r is not a byte string." % k)
                if not isinstance(v, bytestr):
                    raise TypeError("response.header_list value %r is not a byte string." % v)
                outheaders.append((k, v))
            
            if py3k:
                # According to PEP 3333, when using Python 3, the response status
                # and headers must be bytes masquerading as unicode; that is, they
                # must be of type "str" but are restricted to code points in the
                # "latin-1" set.
                outstatus = outstatus.decode('ISO-8859-1')
                outheaders = [(k.decode('ISO-8859-1'), v.decode('ISO-8859-1'))
                              for k, v in outheaders]

            self.iter_response = iter(r.body)
            self.write = start_response(outstatus, outheaders)
        except:
            self.close()
            raise
    
    def __iter__(self):
        return self
    
    if py3k:
        def __next__(self):
            return next(self.iter_response)
    else:
        def next(self):
            return self.iter_response.next()
    
    def close(self):
        """Close and de-reference the current request and response. (Core)"""
        self.cpapp.release_serving()
    
    def run(self):
        """Create a Request object using environ."""
        env = self.environ.get
        
        local = httputil.Host('', int(env('SERVER_PORT', 80)),
                           env('SERVER_NAME', ''))
        remote = httputil.Host(env('REMOTE_ADDR', ''),
                               int(env('REMOTE_PORT', -1) or -1),
                               env('REMOTE_HOST', ''))
        scheme = env('wsgi.url_scheme')
        sproto = env('ACTUAL_SERVER_PROTOCOL', "HTTP/1.1")
        request, resp = self.cpapp.get_serving(local, remote, scheme, sproto)
        
        # LOGON_USER is served by IIS, and is the name of the
        # user after having been mapped to a local account.
        # Both IIS and Apache set REMOTE_USER, when possible.
        request.login = env('LOGON_USER') or env('REMOTE_USER') or None
        request.multithread = self.environ['wsgi.multithread']
        request.multiprocess = self.environ['wsgi.multiprocess']
        request.wsgi_environ = self.environ
        request.prev = env('cherrypy.previous_request', None)
        
        meth = self.environ['REQUEST_METHOD']
        
        path = httputil.urljoin(self.environ.get('SCRIPT_NAME', ''),
                                self.environ.get('PATH_INFO', ''))
        qs = self.environ.get('QUERY_STRING', '')

        if py3k:
            # This isn't perfect; if the given PATH_INFO is in the wrong encoding,
            # it may fail to match the appropriate config section URI. But meh.
            old_enc = self.environ.get('wsgi.url_encoding', 'ISO-8859-1')
            new_enc = self.cpapp.find_config(self.environ.get('PATH_INFO', ''),
                                             "request.uri_encoding", 'utf-8')
            if new_enc.lower() != old_enc.lower():
                # Even though the path and qs are unicode, the WSGI server is
                # required by PEP 3333 to coerce them to ISO-8859-1 masquerading
                # as unicode. So we have to encode back to bytes and then decode
                # again using the "correct" encoding.
                try:
                    u_path = path.encode(old_enc).decode(new_enc)
                    u_qs = qs.encode(old_enc).decode(new_enc)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    # Just pass them through without transcoding and hope.
                    pass
                else:
                    # Only set transcoded values if they both succeed.
                    path = u_path
                    qs = u_qs
        
        rproto = self.environ.get('SERVER_PROTOCOL')
        headers = self.translate_headers(self.environ)
        rfile = self.environ['wsgi.input']
        request.run(meth, path, qs, rproto, headers, rfile)
    
    headerNames = {'HTTP_CGI_AUTHORIZATION': 'Authorization',
                   'CONTENT_LENGTH': 'Content-Length',
                   'CONTENT_TYPE': 'Content-Type',
                   'REMOTE_HOST': 'Remote-Host',
                   'REMOTE_ADDR': 'Remote-Addr',
                   }
    
    def translate_headers(self, environ):
        """Translate CGI-environ header names to HTTP header names."""
        for cgiName in environ:
            # We assume all incoming header keys are uppercase already.
            if cgiName in self.headerNames:
                yield self.headerNames[cgiName], environ[cgiName]
            elif cgiName[:5] == "HTTP_":
                # Hackish attempt at recovering original header names.
                translatedHeader = cgiName[5:].replace("_", "-")
                yield translatedHeader, environ[cgiName]


class CPWSGIApp(object):
    """A WSGI application object for a CherryPy Application."""
    
    pipeline = [('ExceptionTrapper', ExceptionTrapper),
                ('InternalRedirector', InternalRedirector),
                ]
    """A list of (name, wsgiapp) pairs. Each 'wsgiapp' MUST be a
    constructor that takes an initial, positional 'nextapp' argument,
    plus optional keyword arguments, and returns a WSGI application
    (that takes environ and start_response arguments). The 'name' can
    be any you choose, and will correspond to keys in self.config."""
    
    head = None
    """Rather than nest all apps in the pipeline on each call, it's only
    done the first time, and the result is memoized into self.head. Set
    this to None again if you change self.pipeline after calling self."""
    
    config = {}
    """A dict whose keys match names listed in the pipeline. Each
    value is a further dict which will be passed to the corresponding
    named WSGI callable (from the pipeline) as keyword arguments."""
    
    response_class = AppResponse
    """The class to instantiate and return as the next app in the WSGI chain."""
    
    def __init__(self, cpapp, pipeline=None):
        self.cpapp = cpapp
        self.pipeline = self.pipeline[:]
        if pipeline:
            self.pipeline.extend(pipeline)
        self.config = self.config.copy()
    
    def tail(self, environ, start_response):
        """WSGI application callable for the actual CherryPy application.
        
        You probably shouldn't call this; call self.__call__ instead,
        so that any WSGI middleware in self.pipeline can run first.
        """
        return self.response_class(environ, start_response, self.cpapp)
    
    def __call__(self, environ, start_response):
        head = self.head
        if head is None:
            # Create and nest the WSGI apps in our pipeline (in reverse order).
            # Then memoize the result in self.head.
            head = self.tail
            for name, callable in self.pipeline[::-1]:
                conf = self.config.get(name, {})
                head = callable(head, **conf)
            self.head = head
        return head(environ, start_response)
    
    def namespace_handler(self, k, v):
        """Config handler for the 'wsgi' namespace."""
        if k == "pipeline":
            # Note this allows multiple 'wsgi.pipeline' config entries
            # (but each entry will be processed in a 'random' order).
            # It should also allow developers to set default middleware
            # in code (passed to self.__init__) that deployers can add to
            # (but not remove) via config.
            self.pipeline.extend(v)
        elif k == "response_class":
            self.response_class = v
        else:
            name, arg = k.split(".", 1)
            bucket = self.config.setdefault(name, {})
            bucket[arg] = v


########NEW FILE########
__FILENAME__ = _cpwsgi_server
"""WSGI server interface (see PEP 333). This adds some CP-specific bits to
the framework-agnostic wsgiserver package.
"""
import sys

import cherrypy
from cherrypy import wsgiserver


class CPWSGIServer(wsgiserver.CherryPyWSGIServer):
    """Wrapper for wsgiserver.CherryPyWSGIServer.
    
    wsgiserver has been designed to not reference CherryPy in any way,
    so that it can be used in other frameworks and applications. Therefore,
    we wrap it here, so we can set our own mount points from cherrypy.tree
    and apply some attributes from config -> cherrypy.server -> wsgiserver.
    """
    
    def __init__(self, server_adapter=cherrypy.server):
        self.server_adapter = server_adapter
        self.max_request_header_size = self.server_adapter.max_request_header_size or 0
        self.max_request_body_size = self.server_adapter.max_request_body_size or 0
        
        server_name = (self.server_adapter.socket_host or
                       self.server_adapter.socket_file or
                       None)
        
        self.wsgi_version = self.server_adapter.wsgi_version
        s = wsgiserver.CherryPyWSGIServer
        s.__init__(self, server_adapter.bind_addr, cherrypy.tree,
                   self.server_adapter.thread_pool,
                   server_name,
                   max = self.server_adapter.thread_pool_max,
                   request_queue_size = self.server_adapter.socket_queue_size,
                   timeout = self.server_adapter.socket_timeout,
                   shutdown_timeout = self.server_adapter.shutdown_timeout,
                   )
        self.protocol = self.server_adapter.protocol_version
        self.nodelay = self.server_adapter.nodelay

        if sys.version_info >= (3, 0):
            ssl_module = self.server_adapter.ssl_module or 'builtin'
        else:
            ssl_module = self.server_adapter.ssl_module or 'pyopenssl'
        if self.server_adapter.ssl_context:
            adapter_class = wsgiserver.get_ssl_adapter_class(ssl_module)
            self.ssl_adapter = adapter_class(
                self.server_adapter.ssl_certificate,
                self.server_adapter.ssl_private_key,
                self.server_adapter.ssl_certificate_chain)
            self.ssl_adapter.context = self.server_adapter.ssl_context
        elif self.server_adapter.ssl_certificate:
            adapter_class = wsgiserver.get_ssl_adapter_class(ssl_module)
            self.ssl_adapter = adapter_class(
                self.server_adapter.ssl_certificate,
                self.server_adapter.ssl_private_key,
                self.server_adapter.ssl_certificate_chain)
        
        self.stats['Enabled'] = getattr(self.server_adapter, 'statistics', False)

    def error_log(self, msg="", level=20, traceback=False):
        cherrypy.engine.log(msg, level, traceback)


########NEW FILE########
__FILENAME__ = fetch
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2013 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import socket
import urllib2
import shutil

socket.setdefaulttimeout(10)

import tmpname
import tools

def urlheadinfo(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent','Forban +http://www.foo.be/forban/')
    request.get_method = lambda: "HEAD"

    try:
        httphead = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False
    else:
        pass

    return (httphead.headers["last-modified"],httphead.headers["content-length"])

def urlget(url, localfile="testurlget"):
    httpreq = urllib2.Request(url)
    httpreq.add_header('User-Agent','Forban +http://www.foo.be/forban/')

    try:
        r = urllib2.urlopen(httpreq)
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False
    except socket.error,e:
        return False
    except socket.timeout:
        return False
    else:
        pass

    (lpath, lfile) = os.path.split(localfile)

    if not os.path.isdir(lpath) and not (lpath ==''):
        os.makedirs(lpath)

    # as url fetch is part of the Forban protocol interface
    # the Content-Disposition MUST be present even if it's
    # not used right now. The interface is used as file transfert
    # so the Content-Disposition is a requirement for any other
    # HTTP clients

    tlocalfile = tmpname.get(localfile)

    if r.info().has_key('Content-Disposition'):
        f = open (tlocalfile[1], "w")
        try:
            shutil.copyfileobj(r.fp,f)
        except:
            return False
        f.close()
        if os.path.exists(tlocalfile[1]):
            tools.rename(tlocalfile[1], tlocalfile[0])
        return True
    else:
        return False

def managetest():
    print urlget("http://127.0.0.1:12555/s/?g=forban/index")

if __name__ == "__main__":
    managetest()


########NEW FILE########
__FILENAME__ = fid
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# forban UUID

import uuid
import os.path

class manage:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.fidpath = os.path.join(dynpath,"fid")
        self.create()

    def create(self):

        if os.path.isdir(self.dynpath) and os.path.isfile(self.fidpath):
            fidfile = open(self.fidpath,'r')
            self.fid = fidfile.read()
            fidfile.close()
        else:
            self.fid = str(uuid.uuid4())
            if not os.path.isdir(self.dynpath):
                os.mkdir(self.dynpath)
            fidfile = open(self.fidpath,'w')
            fidfile.write(str(self.fid))
            fidfile.close()

    def get (self):
        return self.fid

    def regen (self):
        os.unlink(self.fidpath)
        self.create()

def managetest():
        fid = manage()
        print fid.get()
        fid.regen()
        print fid.get()

if __name__ == "__main__":

    managetest()


########NEW FILE########
__FILENAME__ = index
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2012 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import difflib
import re
import sys
try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1

import hmac

import fetch
import loot
import tmpname
import tools

class manage:

    def __init__ (self, sharedir="../var/share/",
    location="../var/share/forban/index", forbanglobal = "../"):
        self.location = sharedir+"/forban/index"
        self.sharedir = sharedir
        self.lootdir = os.path.join(forbanglobal,"var","loot/")
        self.dynpath = os.path.join(forbanglobal,"var")

    def build (self):
        self.index = ""
        for root, dirs, files in os.walk(self.sharedir, topdown=True, followlinks=True):
            for name in files:
                try:
                    self.index = self.index + os.path.join(root.split(self.sharedir)[1],name)+","+str(os.path.getsize(os.path.join(root,name)))+"\n"
                except:
                    pass

        pid = os.getpid()
        workingloc = self.location+"."+str(pid)
        f = open (workingloc,"w")
        f.write(self.index)
        f.close()
        hmacval = self.calchmac(filepath=workingloc)
        hmacpath = self.location+".hmac"
        self.save(value=hmacval, filepath=hmacpath)
        tools.rename(workingloc, self.location)

    def save (self, value=None, filepath=None):
        if value is None:
            return False
        if filepath is None:
            return False

        tlocalfile = tmpname.get(filepath, suff=str(os.getpid()))

        f = open(tlocalfile[1], "w")
        f.write(value)
        f.close()

        tools.rename(tlocalfile[1], tlocalfile[0])

    def gethmac (self):
        hmacpath = self.location+".hmac"
        if not os.path.exists(hmacpath):
            return False

        f = open(hmacpath, "r")
        val = f.read()
        f.close()
        return val

    def calchmac (self, filepath=None, key="forban"):

        if not os.path.exists(filepath):
            return False
        f = open (filepath,"r")
        auth = hmac.new(key, f.read(), sha1)
        f.close()

        return auth.hexdigest()

    def cache (self, uuid):
        cachepath = os.path.join (self.lootdir, uuid, "cache")
        if not os.path.exists(cachepath):
            os.makedirs(cachepath)
        lloot = loot.loot(self.dynpath)
        for url in lloot.getindexurl(uuid):
            hmacannounced = lloot.gethmac(uuid)
            hmaccalculated = self.calchmac(cachepath+"/forban/index")
            # only fetch the index if the HMAC is different
            if not hmacannounced == hmaccalculated:
                fetch.urlget(url, cachepath+"/forban/index")

    def search (self, query, uuid=None):
        queryresult = []
        pmatch = re.compile(query, re.I)
        if uuid is None:
            location = self.location
        else:
            location = self.lootdir + uuid + "/cache/forban/index"

        f = open(location, "r")
        for cacheline in f.readlines():
            if pmatch.search(cacheline):
                if re.search('/\.',cacheline):
                    continue
                if re.search('^\+\.',cacheline):
                    continue
                queryresult.append(cacheline)
        f.close()

        return queryresult

    def getfilesize (self, filename=None, uuid=None):

        if filename is None:
            return False

        # if uuid is None we use the local cache
        if uuid is None:
            location = self.location
        else:
            location = self.lootdir + uuid + "/cache/forban/index"
        f = open(location, "r")
        pmatch = re.compile(re.escape(filename))
        for line in f.readlines():
            if pmatch.search(line):
                v = line.rsplit(",",1)[1].rstrip('\n')
                return int(v)
        return False

    def totalfilesize (self, uuid=None, prettyprint = True):

        if uuid is None:
            return False
        cachepath = os.path.join(self.lootdir, uuid, "cache","forban","index")

        if not os.path.exists(cachepath):
            return False
        totalvalue = 0
        f = open (cachepath, "r")
        for line in f.readlines():
            val = line.rsplit(",",1)[1].rstrip('\n')
            totalvalue = totalvalue + int(val)

        f.close()

        if prettyprint is False:
            return totalvalue
        else:
            return tools.convertbytes(totalvalue)

    def howfar (self, uuid):
        cachepath = self.lootdir + uuid + "/cache/forban/index"
        # how can I compare my cache to the other, if the other
        # cache is missing...
        if not os.path.exists(cachepath):
            return False
        f1 = open(self.location,"r")
        f1v = f1.read()
        f1.close()
        f2 = open(cachepath,"r")
        f2v = f2.read()
        f2.close()
        f1vs = f1v.splitlines()
        f1vs.sort()
        f2vs = f2v.splitlines()
        f2vs.sort()
        mydiff = '\n'.join(list(difflib.unified_diff(f1vs,f2vs, lineterm="")))
        lmodified = []
        for l in mydiff.splitlines():
            if re.search("(^\+)",l) and not re.search("^\+\+",l) and not re.search("forban",l):
                #exclude temporary files or dot files
                if re.search('/\.',l):
                    continue
                if re.search('^\+\.',l):
                    continue
                missingfile = l.rsplit(",",1)[0]
                missingfile = re.sub("^(\+)","",missingfile)
                lmodified.append(missingfile)
        if lmodified:
            return lmodified
        else:
            return None

def test ():
    testindex = manage()
    testindex.build()
    print testindex.gethmac()

    testindex.cache("8d63025e-2f11-4c08-837a-08c44b122150")
    #print testindex.howfar("e2f05993-eba1-4b94-8e56-d2157d1ce552")
    #print testindex.search("^((?!forban).)*$","e2f05993-eba1-4b94-8e56-d2157d1ce552");
    print testindex.getfilesize(filename="forban/index")
    print testindex.getfilesize(filename="forban//index",uuid="8d63025e-2f11-4c08-837a-08c44b122150")
    print testindex.totalfilesize(uuid="d55727ed-5c6a-49a8-9d8d-28b4004aee0c")

if __name__ == "__main__":

    test()

########NEW FILE########
__FILENAME__ = loot
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import re
import datetime
import time
import sys

# forban internal junk
sys.path.append('.')
import fid
import tmpname
import tools

class loot:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.lootpath = os.path.join(dynpath,"loot")
        if not os.path.isdir(self.lootpath):
            os.mkdir(self.lootpath)

    def listall (self):
        lloot =  []
        for root, dirs, files in os.walk(self.lootpath, topdown=True):
            for name in dirs:
                if "cache" not in os.path.join(root,name):
                    lloot.append(name)
        return lloot

    def getname (self, uuid):

        pathname = os.path.join(self.lootpath,uuid,"name")

        if os.path.exists(pathname):
            f = open (pathname)
            rname = f.read()
            f.close();
            return rname
        else:
            return None

    def getipv4 (self, uuid):

        pathsourcev4 = os.path.join(self.lootpath,uuid,"sourcev4")

        if os.path.exists(pathsourcev4):
            f = open (pathsourcev4)
            rname = f.read()
            f.close()
            return rname
        else:
            return None

    def getlastseen (self, uuid):

        pathlastseen = os.path.join(self.lootpath,uuid,"last")
        defaultlastseen = 100
        if self.exist(uuid):

            if os.path.exists(pathlastseen):
                try:
                    f = open (pathlastseen)
                    rlastseen = f.read()
                    f.close()
                except:
                    rlastseen = defaultlastseen

                return rlastseen
            else:
                return defaultlastseen
        else:

            return defaultlastseen

    def lastannounced (self, uuid, timeago=300):

        lastseen = float(self.getlastseen(uuid))
        t = datetime.datetime.now()
        now = time.mktime(t.timetuple())
        gap = now-lastseen
        if gap < timeago:
            return gap
        else:
            return False

    def whoami (self):

        lfid = fid.manage(dynpath=self.dynpath)
        return lfid.get()

    def getipv6 (self, uuid):

        pathsourcev6 = os.path.join(self.lootpath,uuid,"sourcev6")

        if os.path.exists(pathsourcev6):
            f = open (pathsourcev6)
            rname = f.read()
            f.close()
            return rname
        else:
            return None

    def exist (self, uuid):

        aloot = os.path.join(self.lootpath,uuid)
        if os.path.isdir(aloot):
            return True
        else:
            return False

    def getindexurl (self, uuid, v4only=False):
        iurl = []

        if self.exist(uuid):
            ipv4 = self.getipv4(uuid)
            if ipv4 is not None:
                iurl.append("http://"+ipv4+":12555/s/?g=forban/index")
            ipv6 = self.getipv6(uuid)
            if not v4only:
                if ipv6 is not None:
                    iurl.append("http://["+ipv6+"]:12555/s/?g=forban/index")
            return iurl
        else:
            return False

    def add (self, dmessage, sip):

        mess = dmessage.split(";")
        self.hmac = None
        for i in range (1, len(mess)-1, 2):
            if mess[i] == "name":
                #name is REQUIRED
                self.lname = mess[i+1]
            elif mess[i] == "uuid":
                #uuid is REQUIRED
                self.luuid = mess[i+1]
            elif mess[i] == "hmac":
                #hmac is RECOMMENDED
                self.hmac = mess[i+1]
        self.lsource = sip

        if not self.exist(self.luuid):
            os.mkdir(os.path.join(self.lootpath,self.luuid))

        if self.hmac is not None:
            self.sethmac(lhmac=self.hmac)

        self.setfirstseen()
        self.setlastseen()

        if re.search(":",self.lsource):
            if re.match("^::ffff:",self.lsource):
                self.lsourcev4 = re.sub("^::ffff:","",self.lsource)
                self.lsourcev6 = None
            else:
                # IPv6 link-local regularly uses the interface source
                # to deduce where to send the request when multiple
                # interface with IPv6 link-local are enable.
                #self.lsourcev6 = self.lsource.split("%")[0]
                # we now keep the source interface too.
                # but in such case web url are only accessible to
                # the local machine or machine matching same interface name.
                self.lsourcev6 = self.lsource
                self.lsourcev4 = None
        else:
            self.lsourcev4 = self.lsource
            self.lsourcev6 = None

        self.setname(self.lname)
        self.setsource(self.lsourcev4, self.lsourcev6)

    def setname (self, lname):

        localfile =  os.path.join(self.lootpath,self.luuid,"name")
        tlocalfile = tmpname.get(localfile)

        f = open(tlocalfile[1], "w")
        f.write(lname)
        f.close()

        tools.rename(tlocalfile[1], tlocalfile[0])

        # self is added for the same forban doing the announce
        # and the discovery

        myid = fid.manage(dynpath=self.dynpath)
        if myid.get() == self.luuid:
            localfile = os.path.join(self.lootpath,self.luuid,"self")
            tlocalfile = tmpname.get(localfile)
            f = open (tlocalfile[1], "w")
            f.write("")
            f.close()
            tools.rename(tlocalfile[1], tlocalfile[0])

    def sethmac (self, lhmac = None):

        localfile = os.path.join(self.lootpath,self.luuid,"hmac")
        tlocalfile = tmpname.get(localfile)

        f = open(tlocalfile[1], "w")
        f.write(lhmac)
        f.close()

        tools.rename(tlocalfile[1], tlocalfile[0])


    def gethmac (self, uuid):

        pathhmac = os.path.join(self.lootpath,uuid,"hmac")

        if self.exist(uuid):
            if os.path.exists(pathhmac):
                f = open (pathhmac)
                rhmac = f.read()
                f.close()
                return rhmac
            else:
                return None
        else:

            return None

    def setsource (self, sourcev4 = None , sourcev6 = None):

        if sourcev4 is not None:
            f = open(os.path.join(self.lootpath,self.luuid,"sourcev4"), "w")
            f.write(sourcev4)
            f.close()
        if sourcev6 is not None:
            f = open(os.path.join(self.lootpath,self.luuid,"sourcev6"), "w")
            f.write(sourcev6)
            f.close()

    def setfirstseen (self):

        firstseenpath = os.path.join(self.lootpath,self.luuid,"first")
        if not os.path.exists(firstseenpath):
            f = open(firstseenpath, "w")
            t = datetime.datetime.now()
            f.write(str(time.mktime(t.timetuple())))
            f.close()

    def setlastseen (self):

        localfile =  os.path.join(self.lootpath,self.luuid,"last")
        tlocalfile = tmpname.get(localfile)
        f = open(tlocalfile[1], "w")
        t = datetime.datetime.now()
        f.write(str(time.mktime(t.timetuple())))
        f.close()
        if os.path.exists(tlocalfile[1]):
            tools.rename(tlocalfile[1], tlocalfile[0])

def loottest():

        myloot = loot()
        if not myloot.exist("1234"):
            print "not existing -> ok"
        #myloot.add("forban;name;notset;uuid;cb001bf2-1497-443c-9675-74de7027ecf9;hmac;59753cbda00f8c605aff6c4ceacd3f12caedddea","127.0.0.1")
        print myloot.getindexurl("cb001bf2-1497-443c-9675-74de7027ecf9")
        print myloot.getlastseen("cb001bf2-1497-443c-9675-74de7027ecf9")
        print myloot.lastannounced("cb001bf2-1497-443c-9675-74de7027ecf9")
        print myloot.listall()
        print myloot.gethmac("cb001bf2-1497-443c-9675-74de7027ecf9")

if __name__ == "__main__":

    loottest()

########NEW FILE########
__FILENAME__ = tmpname
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1

#
# return a tuple with the original filename and the temporary reverse name
# (should be unique but reversible per filename)
#

def get(filename=None, suff=None):

    if filename is None:
        return False

    (lpath, lfile) = os.path.split(filename)

    if suff is None:
        h = sha1()
        h.update(lfile)
        hv = h.hexdigest()[:8]
        lfile = "."+lfile+"-"+hv
    else :
        lfile = "."+lfile+"-"+str(suff)

    return (filename,os.path.join(lpath,lfile))

if __name__ == "__main__":
    
    print get("aest")[1]
    print get("/a/b/aestb")

########NEW FILE########
__FILENAME__ = tools
# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2012 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import platform
import re

def convertbytes (bytes=None):

    if bytes is None:
        return False

    bytes = float(bytes)

    if bytes >= 1099511627776:
        tera = bytes / 1099511627776
        cbytes = '%.2fTB' % tera
    elif bytes >= 1073741824:
        giga = bytes / 1073741824
        cbytes = '%.2fGB' % giga
    elif bytes >= 1048576:
        mega = bytes / 1048576
        cbytes = '%.2fMB' % mega
    elif bytes >= 1024:
        kilo = bytes / 1024
        cbytes = '%.2fKB' % kilo
    else:
        cbytes = '%.2fb' % bytes

    return cbytes

# Rename function to handle the platform specific case
# especially with Windows platform.

def rename(source=None, destination=None):

    if source is None or destination is None:
        return False

    if not os.path.exists(source):
        return False

    sys = platform.system()

    if sys == "Windows":
        if os.path.exists(destination):
            os.remove(destination)
        os.rename(source, destination)

    else:
        os.rename(source, destination)

# Guess local hostname on Unix and Windows
#

def guesshostname():
    guessedhostname = platform.node()
    return guessedhostname

# Return a list of tuple (filepath, size, mtime) for a directory
#

def dirtree(rootdir=None):
    if rootdir is None:
        return False
    if not os.path.exists(rootdir):
        return False

    index = []

    for root, dirs, files in os.walk(rootdir, topdown=True):
        for name in files:
            try:
                filename = os.path.join(root, name)
                filenamesize = str(os.path.getsize(os.path.join(root,name)))
                filenamemtime = str(os.path.getmtime(os.path.join(root,name)))
                index.append((filename,filenamesize,filenamemtime))
            except:
                pass

    return index

# Return a list of directories matching a pattern
#

def finddir(rootdir=None, dirmatch="forban"):
    if rootdir is None:
        return False
    if not os.path.exists(rootdir):
        return False

    dirfound = []

    for root, dirs, files in os.walk(rootdir, topdown=True):
        for name in dirs:
            if re.search(name, dirmatch):
                if os.path.isdir(os.path.join(root,name)):
                    dirpath = str(os.path.join(root,name))
                    dirfound.append(dirpath)

    return dirfound

if __name__ == "__main__":
   print convertbytes (1234567)
   print guesshostname()
   print finddir("/media")
   # print rename("x","xy")

########NEW FILE########
