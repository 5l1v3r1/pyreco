__FILENAME__ = conftest
option_doctestmodules = True

########NEW FILE########
__FILENAME__ = slate
from StringIO import StringIO

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter as PI
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

import utils

__all__ = ['PDF']

class PDFPageInterpreter(PI):
    def process_page(self, page):
        if 1 <= self.debug:
            print >>stderr, 'Processing page: %r' % page
        (x0,y0,x1,y1) = page.mediabox
        if page.rotate == 90:
            ctm = (0,-1,1,0, -y0,x1)
        elif page.rotate == 180:
            ctm = (-1,0,0,-1, x1,y1)
        elif page.rotate == 270:
            ctm = (0,1,-1,0, y1,-x0)
        else:
            ctm = (1,0,0,1, -x0,-y0)
        self.device.outfp.seek(0)
        self.device.outfp.buf = ''
        self.device.begin_page(page, ctm)
        self.render_contents(page.resources, page.contents, ctm=ctm)
        self.device.end_page(page)
        return self.device.outfp.getvalue()

class PDF(list):
    def __init__(self, file, password='', just_text=1):
        self.parser = PDFParser(file)
        self.doc = PDFDocument(self.parser)
        self.parser.set_document(self.doc)
        self.doc.initialize(password)
        if self.doc.is_extractable:
            self.resmgr = PDFResourceManager()
            self.device = TextConverter(self.resmgr, outfp=StringIO())
            self.interpreter = PDFPageInterpreter(
               self.resmgr, self.device)
            for page in PDFPage.create_pages(self.doc):
                self.append(self.interpreter.process_page(page))
            self.metadata = self.doc.info
        if just_text:
            self._cleanup()

    def _cleanup(self):
        """ 
        Frees lots of non-textual information, such as the fonts
        and images and the objects that were needed to parse the
        PDF.
        """
        del self.device
        del self.doc
        del self.parser
        del self.resmgr
        del self.interpreter

    def text(self, clean=True):
        """ 
        Returns the text of the PDF as a single string.
        Options:

          :clean:
            Removes misc cruft, like lots of whitespace.
        """
        if clean:
            return utils.normalise_whitespace(''.join(self))
        else:
            return ''.join(self) 

########NEW FILE########
__FILENAME__ = test_slate
""" 
  Tests for slate 
  http://pypi.python.org/slate

  Expected to be used with py.test:
  http://codespeak.net/py/dist/test/index.html
"""

from slate import PDF

def pytest_funcarg__doc(request):
    with open('example.pdf', 'rb') as f:
        return PDF(f)

def pytest_funcarg__passwd(request):
    with open('protected.pdf') as f:
        return PDF(f, 'a')

def test_basic(doc):
    assert doc[0] == 'This is a test.\x0c'

def test_metadata_extraction(doc):
    assert doc.metadata

def test_text_method(doc):
    assert "This is a test" in doc.text()

def test_text_method_unclean(doc):
    assert '\x0c' in doc.text(clean=0)

def test_password(passwd):
    assert passwd[0] == "Chamber of secrets.\x0c"

########NEW FILE########
__FILENAME__ = utils
import re

def normalise_whitespace(s):
    """ 
    Returns a string that has at most one whitespace
    character between non-whitespace characters. We
    leave a few extra spaces because most NLP parsers
    don't tend to care.

    >>> normalise_whitespace(' hi   there')
    ' hi there'
    >>> normalise_whitespace('meh\n\n\f')
    'meh '
    """
    return re.sub(r'\s+', ' ', s) 

########NEW FILE########
