__FILENAME__ = export2enex
# A script for exporting all starred items from Google Reader to Evernote,
# using exported JSON data from Google's Takeout and Evernote's
# bulk import feature (available in the desktop client).
#
# Copyright 2013 Paul Kerchen
#
# This program is distributed under the terms of the GNU General Public License v3.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
import smtplib
from xml.sax.saxutils import escape
import json
import io
import getopt, sys
import os.path
import codecs
import time

def usage():
   print "\nOptions:"
   print "-e, --encoding: The name of the character encoding codec to use.  The default"
   print "          is utf8.  For other possible values, see the table of standard"
   print "          python character encodings at "
   print "             http://docs.python.org/2/library/codecs.html#standard-encodings"
   print "-n, --notebook: The name of the Evernote notebook to put sent notes in."
   print "          If you do not specify a notebook, sent notes will be put in the default notebook."
   print "-m, --maximum: The maximum number of articles that should be converted."
   print "          If you do not specify a maximum, all messages will be converted."
   print "-h, --help: Print this message and exit."

try:
   opts, args = getopt.getopt( sys.argv[1:], "e:n:m:h", ["encoding=","notebook=","maximum=","help"])
except getopt.GetoptError as err:
   print str(err) 
   usage()
   sys.exit(2)

sender_user = ""
evernote_user = ""
notebook = ""
message_limit = -1 
skip_count = 0
continue_from_prev = False
char_encoding = "utf8"

for o, a in opts:
   if o in ("-e", "--encoding"):
      char_encoding = a
   elif o in ("-n", "--notebook"):
      notebook = a
   elif o in ("-m", "--maximum"):
      message_limit = int(a)
   elif o in ("-h", "--help"):
      usage()
      sys.exit()

#json_file = open("starred.json", "rb")
json_file = codecs.open( "starred.json", encoding=char_encoding )
json_dict = json.loads( json_file.read() )

item_list = json_dict[ "items" ]

if message_limit < 0:
   message_limit = len(item_list)

print('<?xml version="1.0" encoding="' + char_encoding + '"?>')
print('<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export2.dtd">')
print('<en-export export-date="20130320T150950Z" application="Evernote" version="Evernote Mac 5.0.6 (400960)">')

for s in item_list:
   subject = "none"
   if 'title' in s.keys():
      subject = s["title"].encode(char_encoding, 'replace')
   if 'published' in s.keys():
      published_epoch = s["published"]
      published_datetime = time.strftime("%Y%m%dT%H%M%SZ", time.localtime(published_epoch) )
   if 'updated' in s.keys():
      updated_epoch = s["updated"]
      updated_datetime = time.strftime("%Y%m%dT%H%M%SZ", time.localtime(updated_epoch) )
   if notebook:
      subject = subject + " @" + notebook

   msg_body = ""
   msg_body = msg_body + '<note><title>'+subject+'</title><content><![CDATA[<?xml version="1.0" encoding="'+char_encoding+'" standalone="no"?> <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"> <en-note>'
   msg_url = ""

   if 'canonical' in s.keys():
      d = s["canonical"][0]
      msg_url = d["href"].encode(char_encoding, 'replace')
   if 'alternate' in s.keys():
      d = s["alternate"][0]
      msg_url = d["href"].encode(char_encoding, 'replace')
   if 'summary' in s.keys():
      d = s["summary"]
      msg_body = msg_body + d["content"].encode(char_encoding, 'replace')
   if 'content' in s.keys():
      d = s["content"]
      msg_body = msg_body + d["content"].encode(char_encoding, 'replace')
   msg_body = msg_body + "</en-note>]]>\r\n</content>\r\n"
   if published_datetime:
      msg_body = msg_body + "<created>" + published_datetime + "</created>"
   if updated_datetime:
      msg_body = msg_body + "<updated>" + updated_datetime + "</updated>"
   msg_body = msg_body + "<note-attributes><source>web.clip</source><source-url>" + escape(msg_url) + "</source-url></note-attributes>"
   msg_body = msg_body + "</note>\r\n"

   print(msg_body)

   message_limit = message_limit - 1
   if message_limit < 1:
      break

print('</en-export>')


########NEW FILE########
__FILENAME__ = export2HTMLFiles
# A script for exporting all starred items from Google Reader to HTML files,
# using exported JSON data from Google's Takeout 
#
# Copyright 2013 Paul Kerchen, Davide Della Casa
#
# This program is distributed under the terms of the GNU General Public License v3.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
import smtplib
import json
import io
import getopt, sys
import os.path
import string

def usage():
   print "Converts exported starred articles from a Google Reader export file."
   print "The file 'starred.json' must be in the directory that this script is"
   print "invoked from.  Each article will be exported to its own HTML file."
   print "\nOptions:"
   print "-h, --help: Print this message and exit."

try:
   opts, args = getopt.getopt( sys.argv[1:], "h", ["help"])
except getopt.GetoptError as err:
   print str(err) 
   usage()
   sys.exit(2)

for o, a in opts:
   if o in ("-h", "--help"):
      usage()
      sys.exit()

# Provides a decent filename. A variation of: http://stackoverflow.com/a/295146/1318347
def cleanFileName(value):
  valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
  untrimmedFileName = ''.join(c for c in value if c in valid_chars)
  maximumFileNameLength = 200
  if len(untrimmedFileName) > maximumFileNameLength:
    trimmedFileName = (untrimmedFileName[:maximumFileNameLength] + '..')
  else:
    trimmedFileName = untrimmedFileName
  return trimmedFileName.strip()

json_file = open("starred.json")
json_dict = json.loads( unicode(json_file.read(), encoding="utf-8") )

item_list = json_dict[ "items" ]

articleCounter = 0
for s in item_list:
   articleCounter += 1
   title = str(articleCounter)
   if 'title' in s.keys():
      title = title + " " + s["title"]
   fileName = cleanFileName(title) + '.html'
   file = open(fileName, 'w+')

   html_body = ""

   if 'alternate' in s.keys():
      d = s["alternate"][0]
      alternateURL = d["href"]
      html_body = html_body + '<p>URL: <a href="'+alternateURL+'">'+alternateURL+'</a></p>'
   if 'canonical' in s.keys():
      d = s["canonical"][0]
      canonicalURL = d["href"]
      hintAboutSecondURL  = (' 2') if 'alternate' in s.keys() else ''
      html_body = html_body + '<p>URL'+hintAboutSecondURL+': <a href="'+canonicalURL+'">'+canonicalURL+'</a></p>'

   html_body = html_body + '<hr>'

   if 'summary' in s.keys():
      d = s["summary"]
      html_body = html_body + d["content"]
   if 'content' in s.keys():
      d = s["content"]
      html_body = html_body + d["content"]

   file.write(html_body.encode("UTF-8"))
   file.close()

   print('extracted: ' + fileName)

print('...done')


########NEW FILE########
__FILENAME__ = export_gr2evernote
# A script for exporting all starred items from Google Reader to Evernote,
# using exported JSON data from Google's Takeout and Evernote's
# note emailing feature. 
#
# Copyright 2013 Paul Kerchen
#
# This program is distributed under the terms of the GNU General Public License v3.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
import smtplib
import json
import io
import getopt, sys
import getpass
import os.path
import pickle

def usage():
   print "\nOptions:"
   print "-c, --continue: Pick up where the last export left off, using the same parameters from"
   print "          the last export.  If other options are specified, they will override any parameters"
   print "          from the last export."
   print "-e, --evernote-user: The Evernote email username (NOT the Evernote username) to send messages to. [required]"
   print "          Username only; do not include the '@m.evernote.com'!"
   print "-g, --gmail-user: The gmail username to send messages from. [required]"
   print "          Username only; do not include the '@gmail.com'!"
   print "-m, --maximum: The maximum number of messages that should be sent."
   print "          If you do not specify a maximum, all messages will be sent."
   print "          Note that Evernote limits the number of notes that can be added via e-mail in a single day."
   print "          For free accounts, the limit is 50; for premium accounts, it is 250."
   print "-n, --notebook: The name of the Evernote notebook to put sent notes in."
   print "          If you do not specify a notebook, sent notes will be put in the default notebook."
   print "-s, --skip: The number of articles to skip before sending the first e-mail message."
   print "          Useful for picking up where you left off from the previous day if you"
   print "          ran into Evernote's e-mail submission daily limit."
   print "-h, --help: Print this message and exit."
   print
   print "When prompted for a password, enter the password for the sender gmail address."
   print "It is expected that the exported starred items are in a file named 'starred_json' in the current working directory."

try:
   opts, args = getopt.getopt( sys.argv[1:], "ce:m:n:g:s:h", ["continue","evernote-user=","maximum=","notebook=","gmail-user=","skip=","help"])
except getopt.GetoptError as err:
   print str(err) 
   usage()
   sys.exit(2)

sender_user = ""
evernote_user = ""
notebook = ""
message_limit = -1 
skip_count = 0
continue_from_prev = False

for o, a in opts:
   if o in ("-c", "--continue"):
     continue_from_prev = True 
   elif o in ("-g", "--gmail-user"):
      sender_user = a
   elif o in ("-e", "--evernote-user"):
      evernote_user = a
   elif o in ("-m", "--maximum"):
      message_limit = int(a)
   elif o in ("-n", "--notebook"):
      notebook = a
   elif o in ("-s", "--skip"):
      skip_count = int(a)
   elif o in ("-h", "--help"):
      usage()
      sys.exit()

if continue_from_prev:
   if not os.path.exists("continuation.txt"):
      print "Continuation data file not found; cannot continue."
      sys.exit()

   last_session_data = open("continuation.txt")
   if not last_session_data.closed:
      val = pickle.load( last_session_data ) # skip count
      if skip_count == 0:
         skip_count = val
      val = pickle.load( last_session_data ) # limit 
      if message_limit == -1:
         message_limit = val
      val = pickle.load( last_session_data ) # notebook
      if not notebook:
         notebook = val
      val = pickle.load( last_session_data ) # sender
      if not sender_user:
         sender_user = val
      val = pickle.load( last_session_data ) # evernote username
      if not evernote_user:
         evernote_user = val
      print "Continuing with:"
      print "  Skip count: %d" % skip_count
      print "  Message limit: %d" % message_limit
      print "  Notebook: %s" % notebook
      print "  gmail username: %s" % sender_user
      print "  Evernote username: %s" % evernote_user
   else:
      print "Continuation data file cannot be opened; cannot continue."
      sys.exit()

if not sender_user or not evernote_user:
   print "Missing required parameter."
   usage()
   sys.exit()

sender_addr = sender_user + "@gmail.com"
evernote_addr = evernote_user + "@m.evernote.com"

FROM = sender_user
TO = [evernote_addr] #must be a list 

json_file = open("starred.json")
json_dict = json.loads( unicode(json_file.read(), encoding="utf-8") )

item_list = json_dict[ "items" ]
 
print "Number of articles found in json export: %d" % len(item_list)

if message_limit < 0:
   message_limit = len(item_list)

print "Number of notes to be added to Evernote: %d" % message_limit
if message_limit > 50:
   print "Warning: if you have a free account, adding more than 50 notes in one day will most likely fail."
if message_limit > 250:
   print "Warning: adding more than 250 notes in one day will most likely fail."

if skip_count > 0:
   print "The first %d articles will be skipped" % skip_count

sender_pwd = getpass.getpass()

original_message_limit = message_limit
sent_count = 0
fail_count = 0
article_num = 0
note_count = 0

for s in item_list:
   article_num = article_num + 1
   if skip_count > 0:
      skip_count = skip_count - 1
      continue

   note_count = note_count + 1
   subject = unicode(s["title"]).encode('ascii', 'replace')
   if notebook:
      subject = subject + " @" + notebook

   msg_body = ""
   if 'canonical' in s.keys():
      d = s["canonical"][0]
      msg_body = msg_body + "URL: " + unicode(d["href"]).encode('ascii', 'replace') + "\r\n"
   if 'alternate' in s.keys():
      d = s["alternate"][0]
      msg_body = msg_body + "Alt URL:" + unicode(d["href"]).encode('ascii', 'replace') + "\r\n"
   if 'summary' in s.keys():
      d = s["summary"]
      msg_body = msg_body + "Summary: " + unicode(d["content"]).encode('ascii', 'replace') + "\r\n"
   if 'content' in s.keys():
      d = s["content"]
      msg_body = msg_body + unicode(d["content"]).encode('ascii', 'replace')
   msg_body = msg_body + "</en-note>\r\n"


   # Prepare actual message
   message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
   """ % (FROM, ", ".join(TO), subject, msg_body)
   try:
         server = smtplib.SMTP("smtp.gmail.com", 587) 
         server.ehlo()
         server.starttls()
         server.login(sender_addr, sender_pwd)
         server.sendmail(FROM, TO, message)
         server.close()
         sent_count = sent_count + 1
         print ("Successfully sent note {0} for article {1} '{2}'").format( note_count, article_num, subject )
   except:
         print ("Failed to send note {0} for article {1} '{2}'").format( note_count, article_num, subject )
         fail_count = fail_count + 1

   message_limit = message_limit - 1
   if message_limit < 1:
      break

print ("Successfully sent {0} notes; {1} failed").format( sent_count, fail_count )

cont_file = open( "continuation.txt", "w" )

# Write new skip count, message count, 
pickle.dump( article_num, cont_file ) # New skip count = number of last-sent article
pickle.dump( original_message_limit, cont_file )
pickle.dump( notebook, cont_file )
pickle.dump( sender_user, cont_file )
pickle.dump( evernote_user, cont_file )

cont_file.close()
print "Continuation data saved to 'continuation.txt'"

########NEW FILE########
