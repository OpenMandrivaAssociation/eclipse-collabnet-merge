%global eclipse_base     %{_libdir}/eclipse
%global eclipse_dropin   %{_datadir}/eclipse/dropins

Name:      eclipse-collabnet-merge
Version:   2.2.1
Release:   4
Summary:   CollabNet Merge Client for Subclipse
Group:     Development/Java
License:   EPL
URL:       https://desktop-eclipse.open.collab.net/servlets/ProjectProcess?pageID=MEuUjb&freeformpage=Merge%20Client

# source tarball and the script used to generate it from upstream's source control
# script usage:
# $ sh get-collabnet-merge.sh
Source0:   collabnet-merge-%{version}.tar.gz
Source1:   get-collabnet-merge.sh

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: eclipse-pde >= 0:3.5.0
BuildRequires: eclipse-subclipse >= 1.6.10
Requires:      java
Requires:      jpackage-utils
Requires:      eclipse-platform >= 0:3.5.0
Requires:      eclipse-subclipse >= 1.6.10

%description
The CollabNet Merge Client has been built on top of Eclipse and Subclipse.
This combination allowed us to support multiple client operating systems and
also allowed us to focus on the actual merge client and merge process while
leveraging the excellent Subversion capabilities that already exist in
Subclipse. This gives you a powerful client that allows you to perform all
Subversion operations from a single tool. Commit, History, Blame, Switch,
Tagging. Everything you need is available. You do not have to be an Eclipse
shop or even an Eclipse developer to use the client. Eclipse and Subclipse
make it easy to checkout and access any project in your repository. You can
just use the client as a general Subversion UI, or even just to perform merges.
Adopting the client does not require that you adopt Eclipse as your only
development tool.

%prep
%setup -q -n collabnet-merge-%{version}

# make sure upstream hasn't sneaked in any jars we don't know about
JARS=""
for j in `find -name "*.jar"`; do
  if [ ! -L $j ]; then
    JARS="$JARS $j"
  fi
done
if [ ! -z "$JARS" ]; then
   echo "These jars should be deleted and symlinked to system jars: $JARS"
   exit 1
fi

%build
# build collabnet-merge features
%{eclipse_base}/buildscripts/pdebuild -f com.collabnet.subversion.merge.feature \
  -d "subclipse svnkit"

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{eclipse_dropin}
unzip -q -n -d %{buildroot}%{eclipse_dropin}/collabnet-merge build/rpmBuild/com.collabnet.subversion.merge.feature.zip

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{eclipse_dropin}/collabnet-merge
%doc com.collabnet.subversion.merge.feature/license.html

