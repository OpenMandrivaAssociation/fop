%define gcj_support 0

Summary:	XSL-driven print formatter
Name:		fop
Version:	1.0
Release:	%mkrel 0.0.4
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
