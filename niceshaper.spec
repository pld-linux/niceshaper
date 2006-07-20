Summary:	NiceShaper - bandwidth limiting
Summary(pl):	NiceShaper - dynamiczny podzia³ ³±cza
Name:		niceshaper
Version:	0.5.1
Release:	2
License:	GPL
Group:		Networking/Admin
Source0:	http://www.niceshaper.mikule.net/files/%{name}-%{version}.tar.bz2
# Source0-md5:	dd565b28a9cddeede8fe2966591961a0
Source1:	%{name}.users
Source2:	%{name}.config
Source3:	%{name}.about
Source4:	%{name}.init
URL:		http://niceshaper.jedwabny.net/
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	firewall-userspace-tool
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program opieraj±c siê na HTB/IMQ dzieli dostêpne pasmo na komputery w
sieci, dynamicznie dostosowuj±c siê do generowanego przez ka¿dego z
u¿ytkowników obci±¿enia.

%prep
%setup -q -c

%build
%{__cxx} %{rpmcflags} niceshaper.cpp -o niceshaper
cp %{SOURCE1} ./users
cp %{SOURCE2} ./config
cp %{SOURCE3} ./about
cp %{SOURCE4} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/niceshaper,%{_initrddir}}

install niceshaper $RPM_BUILD_ROOT%{_bindir}
install etc/niceshaper/* $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper
install niceshaper.init $RPM_BUILD_ROOT%{_initrddir}/niceshaper

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add niceshaper
%service niceshaper restart "niceshaper daemon"

%preun
if [ "$1" = "0" ]; then
	%service niceshaper stop
	/sbin/chkconfig --del niceshaper
fi

%files
%defattr(644,root,root,755)
%doc users config about
%dir %{_sysconfdir}/%{name}
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) %{_initrddir}/niceshaper
