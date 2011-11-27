Summary:	XSL-driven print formatter
Name:		fop
Version:	1.0
Release:	18
License:	ASL 2.0
Group:		Text tools
URL:		http://xmlgraphics.apache.org/fop
Source0:	http://www.apache.org/dist/xmlgraphics/fop/source/%{name}-%{version}-src.tar.gz
Source1:	%{name}.script
Source2:	batik-pdf-MANIFEST.MF
Source3:	http://mirrors.ibiblio.org/pub/mirrors/maven2/org/apache/xmlgraphics/%{name}/%{version}/%{name}-%{version}.pom
Source4:	event-model.tgz
Patch0:		%{name}-manifest.patch
Patch1:		%{name}-main.patch
Patch2:		qdox-build.patch
BuildArch:  noarch
Requires:	xmlgraphics-commons >= 1.2
Requires:	avalon-framework >= 4.1.4
Requires:	batik >= 1.7
Requires:	xalan-j2 >= 2.7.0
Requires:	xml-commons-apis >= 1.3.04
Requires:	jakarta-commons-httpclient
Requires:	apache-commons-io >= 1.2
Requires:	apache-commons-logging >= 1.0.4
Requires:	java >= 0:1.6.0
Requires:   jpackage-utils

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

BuildRequires:	ant
BuildRequires:	java-devel >= 0:1.6.0
BuildRequires:	java-javadoc >= 0:1.6.0
BuildRequires:	jpackage-utils
BuildRequires:	apache-commons-logging
BuildRequires:	apache-commons-io
BuildRequires:	avalon-framework
BuildRequires:	xmlgraphics-commons
BuildRequires:	batik
BuildRequires:	servlet
BuildRequires:	qdox
BuildRequires:	xmlunit
BuildRequires:	zip
BuildRequires:	junit

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
Requires:	jpackage-utils

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -a 4
%patch0 -p1
%patch1 -p0
%patch2 -p0 -b .sav

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

sed -i -e "s|1.4|1.5|g" build.xml

%build
export CLASSPATH=$(build-classpath apache-commons-logging apache-commons-io xmlgraphics-commons batik-all avalon-framework-api avalon-framework-impl servlet batik/batik-svg-dom xml-commons-apis xml-commons-apis-ext qdox objectweb-asm/asm-all xmlunit)
ant jar-main transcoder-pkg javadocs

%install
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{name}.jar META-INF/MANIFEST.MF

# jars
mkdir -p %{buildroot}%{_javadir}
cp -a build/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar
cp -a build/%{name}-transcoder.jar %{buildroot}%{_javadir}/pdf-transcoder.jar

# script
mkdir -p %{buildroot}%{_bindir}
cp -a %{SOURCE1} %{buildroot}%{_bindir}/fop

# data
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a conf %{buildroot}%{_datadir}/%{name}

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -a build/javadocs/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.xmlgraphics %{name} %{version} JPP %{name} %{version}

%pre javadoc
# workaround for rpm bug 646523, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc LICENSE README NOTICE
%{_javadir}/%{name}.jar
%{_datadir}/%{name}
%{_javadir}/pdf-transcoder.jar
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*pom
%attr(0755,root,root) %{_bindir}/fop

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}
%doc LICENSE


