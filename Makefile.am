SUFFIXES = .c .mod .def .o .obj .lo .a .m .mxm

SHELL=/bin/bash

prefix= @prefix@
datarootdir= @datarootdir@
srcdir= @srcdir@
mandir= @mandir@
exec_prefix=@exec_prefix@
bindir= @bindir@
INSTALL_PROGRAM = install

TEXI2HTML=python3 $(srcdir)/www/tools/texi2tr/src/texi2tr.py
PYTHON_VERSION=$(strip $(shell python3 -V 2>&1 | cut -b8- | cut -f1-2 -d'.'))

DISTFILES = Makefile.am configure.ac configure \
            README version.c COPYING examples doc

all: force
	echo "nothing to be done for all"

install: force
	if [ ! -f touchgui.py ] ; then cp $(srcdir)/touchgui.py . ; fi
	if [ ! -f touchguipalate.py ] ; then cp $(srcdir)/touchguipalate.py . ; fi
	PYTHONPATH=.:$(srcdir)/python python3 $(srcdir)/touchguisetup.py build
	python3 -m py_compile touchgui.py
	python3 -m py_compile touchguiconf.py
	python3 -m py_compile touchguipalate.py
	$(INSTALL_PROGRAM) -m 755 -d $(DESTDIR)/usr/lib/python$(PYTHON_VERSION)
	$(INSTALL_PROGRAM) -m 644 touchgui.py $(DESTDIR)/usr/lib/python$(PYTHON_VERSION)
	$(INSTALL_PROGRAM) -m 644 touchguiconf.py $(DESTDIR)/usr/lib/python$(PYTHON_VERSION)
	$(INSTALL_PROGRAM) -m 644 touchguipalate.py $(DESTDIR)/usr/lib/python$(PYTHON_VERSION)
	cd $(srcdir) && tar cf - images | (mkdir -p $(DESTDIR)/$(datarootdir)/touchgui && cd $(DESTDIR)/$(datarootdir)/touchgui && tar xf -)

documentation: touchgui.pdf touchgui.html texi2tr.css

touchgui.pdf: touchgui.ps
	gs -q -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=$@ $<

touchgui.ps: touchgui.dvi
	dvips -o $@ $<

touchgui.dvi: touchgui-api.texi $(srcdir)/doc/touchgui.texi
	texi2dvi -I $(srcdir)/ $(srcdir)/doc/touchgui.texi

touchgui-api.texi:  force
	python3 $(srcdir)/tools/py2texi.py -f$(srcdir)/touchgui.py > touchgui-api.texi

texi2tr.css: $(srcdir)/www/tools/texi2tr/html/texi2tr.css
	cp $< $@

touchgui.html: touchgui-api.texi $(srcdir)/doc/touchgui.texi
	cp $(srcdir)/www/tools/texi2tr/html/*.html .
	cp $(srcdir)/www/tools/texi2tr/png/*png .
	$(TEXI2HTML) -T$(srcdir)/www/tools/texi2tr/html -n -I.:$(srcdir)/doc:$(srcdir) -b touchgui-%d.html -r touchgui.html touchgui.texi

release: force
	pwd
	echo touchgui-`sed -e '/version_string/!d' \
          -e 's/[^0-9.]*\([0-9.]*\).*/\1/' -e q $(srcdir)/version.c` > .fname
	-rm -rf `cat .fname`
	mkdir `cat .fname`
	dst=`cat .fname`; for f in $(DISTFILES); do \
           cp -rp $(srcdir)/$$f $$dst/$$f ; \
        done
	tar --gzip -chf `cat .fname`.tar.gz `cat .fname`
	-rm -rf `cat .fname` .fname

clean: force
	$(RM) *.o *.m *.cpp *~ $(EXAMPLES) *.so *.lo *.la
	$(RM) -rf .libs *_m2.cpp

clear: force
	$(RM) *.png *.ms *.cpp

force:
