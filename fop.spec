%define gcj_support 1

Name:           fop
Version:        0.94
Release:        %mkrel 0.2.1
Epoch:          0
Summary:        XSL-driven print formatter
License:        Apache License
Group:          Development/Java
Source0:        fop-%{version}-src.tar.gz
Source1:        %{name}.script
Patch0:         %{name}-build.patch
Patch1:         %{name}-manifest.patch
Patch2:         %{name}-main.patch
URL:            http://xmlgraphics.apache.org/fop

Requires:       xmlgraphics-commons >= 0:1.2
Requires:       avalon-framework >= 0:4.1.4
Requires:       batik >= 0:1.7
Requires:       xalan-j2 >= 0:2.7.0
Requires:       xml-commons-apis >= 0:1.3.04
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-io >= 0:1.2
Requires:       jakarta-commons-logging >= 0:1.0.4

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  java-rpmbuild
BuildRequires:  java-1.7.0-icedtea-devel
BuildRequires:  java-1.7.0-icedtea-javadoc
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
export JAVA_HOME=%{_jvmdir}/java-icedtea
export CLASSPATH=
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/trax`"
ant clean jar-main transcoder-pkg javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -a build/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -a build/%{name}-transcoder.jar $RPM_BUILD_ROOT%{_javadir}/pdf-transcoder.jar
pushd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}*
do ln -s ${jar} `echo $jar| sed "s|-%{version}||g"`
done
popd

# script
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop

# data
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a conf $RPM_BUILD_ROOT%{_datadir}/%{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
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
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

