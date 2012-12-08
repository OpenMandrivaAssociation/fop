%define gcj_support 0

Summary:	XSL-driven print formatter
Name:		fop
Version:	1.0
Release:	%mkrel 0.0.5
Epoch:		0
License:	Apache License
Group:		Development/Java
URL:		http://xmlgraphics.apache.org/fop
Source0:	fop-%{version}-src.tar.gz
Source1:	%{name}.script
Patch1:		%{name}-manifest.patch
Patch2:		%{name}-main.patch
Requires:	xmlgraphics-commons >= 0:1.2
Requires:	avalon-framework >= 0:4.1.4
Requires:	batik >= 0:1.7
Requires:	xalan-j2 >= 0:2.7.0
Requires:	xml-commons-apis >= 0:1.3.04
Requires:	jakarta-commons-httpclient
Requires:	jakarta-commons-io >= 0:1.2
Requires:	jakarta-commons-logging >= 0:1.0.4
BuildRequires:	ant
BuildRequires:	ant-trax
BuildRequires:	java-rpmbuild
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q
#%patch1 -p1
%patch2 -p0

%build
export JAVA_HOME=%{java_home}
export CLASSPATH=
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/trax`"

%ant clean jar-main transcoder-pkg javadocs

%install
rm -rf %{buildroot}

# jars
mkdir -p %{buildroot}%{_javadir}
cp -a build/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
cp -a build/%{name}-transcoder.jar %{buildroot}%{_javadir}/pdf-transcoder.jar
pushd %{buildroot}%{_javadir}
for jar in *-%{version}*
do ln -s ${jar} `echo $jar| sed "s|-%{version}||g"`
done
popd

# script
mkdir -p %{buildroot}%{_bindir}
cp -a %{SOURCE1} %{buildroot}%{_bindir}/fop

# data
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a conf %{buildroot}%{_datadir}/%{name}

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a build/javadocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%doc LICENSE README NOTICE
%{_javadir}/%{name}*.jar
%{_datadir}/%{name}
%{_javadir}/pdf-transcoder.jar
%attr(0755,root,root) %{_bindir}/fop
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.0-0.0.4mdv2011.0
+ Revision: 664348
- mass rebuild

* Thu Dec 09 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 0:1.0-0.0.3mdv2011.0
+ Revision: 617684
- Resubmit after moving

* Sat Sep 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0:1.0-0.0.2mdv2011.0
+ Revision: 576002
- rebuild for new xmlgraphics-commons

* Sun Aug 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0:1.0-0.0.1mdv2011.0
+ Revision: 574030
- update to new version 1.0
- disable patch 1
- disable gcj support

* Thu Apr 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0:0.95-0.0.3mdv2010.1
+ Revision: 540954
- rebuild

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0:0.95-0.0.2mdv2010.0
+ Revision: 437573
- rebuild

* Wed Dec 17 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0:0.95-0.0.1mdv2009.1
+ Revision: 315376
- update to new version 0.95
- drop patch0, not needed anymore
- spec file clean
- drop useles buildrequires
- use %%java_home

* Sat Dec 29 2007 David Walluck <walluck@mandriva.org> 0:0.94-0.2.1mdv2008.1
+ Revision: 139372
- spec cleanup
- import fop


* Fri Dec  7 2007 Lillian Angel <langel at redhat.com> - 0.94-2
- Updated Release.

* Thu Dec  6 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Removed ppc/64 conditions since IcedTea is now available for ppc/64.

* Tue Nov 27 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Fixed to build with gcj on ppc/64.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Fixed rpmlint errors.

* Tue Sep 18 2007 Joshua Sumali <jsumali at redhat.com> - 0:0.94-1
- Update to fop 0.94

* Thu Mar 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-9jpp
- First build for JPP-1.7
- Replace avalon-framework, avalon-logkit with their new excalibur-*
  counterparts
- Drop non-free jimi and jai BRs

* Tue Oct 11 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-8jpp
- Patch to Batik >= 1.5.1

* Fri Oct 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-7jpp
- Omit ant -d flag

* Mon Aug 23 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-6jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-5jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:0.20.5-4jpp
- Upgrade to Ant 1.6.X

* Thu Jan  8 2004 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-3jpp
- BuildRequires ant-optional.
- Crosslink with full J2SE javadocs instead of just JAXP/XML-commons.
- Add Main-Class back to manifest.

* Tue Sep 23 2003 Paul Nasrat <pauln at truemesh.com> - 0:0.20.5-2jpp
- Fix script and requires
- Remove class path in manifest
- New javadoc style

* Sat Jul 19 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-1jpp
- Update to 0.20.5.
- Crosslink with xml-commons-apis and batik javadocs.
- BuildRequires jai, jce and jimi.

* Sat Jun  7 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-0.rc3a.1jpp
- Update to 0.20.5rc3a.
- Include fop script.
- Non-versioned javadoc symlinks.

* Thu Apr 17 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-0.rc2.1jpp
- Update to 0.20.5rc2 and JPackage 1.5.

* Sun Mar 10 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.3-1jpp
- 0.20.3 final
- fixed missing symlink

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.3-0.rc.1jpp
- 0.20.3rc
- first unified release
- javadoc into javadoc package
- no dependencies for manual package
- s/jPackage/JPackage
- adaptation to new xalan-j2 package
- requires and buildrequires avalon-logkit

* Thu Aug 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.1-1mdk
- first release

