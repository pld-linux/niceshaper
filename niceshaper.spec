
%define		_rc	rc3

Summary:	NiceShaper - bandwidth limiting
Summary(pl.UTF-8):	NiceShaper - dynamiczny podział łącza
Name:		niceshaper
Version:	0.6
Release:	0.%{_rc}.1
License:	GPL
Group:		Networking/Admin
Source0:	http://niceshaper.jedwabny.net/files/%{name}%{version}%{_rc}.tar.bz2
# Source0-md5:	6657728212c61d9657bcbec637a51f5d
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

%description -l pl.UTF-8
Program opierając się na HTB/IMQ dzieli dostępne pasmo na komputery
w sieci, dynamicznie dostosowując się do generowanego przez każdego
z użytkowników obciążenia.


%prep
%setup -q -c

%build

%{__cxx} %{rpmcflags} src/ns_class.cc src/ns_container.cc src/ns_filter.cc src/ns_instance.cc src/ns_net.cc src/niceshaper.cc -o src/niceshaper
cp %{SOURCE1} ./users
cp %{SOURCE2} ./config
cp %{SOURCE3} ./about
cp %{SOURCE4} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/niceshaper,%{_initrddir}}

install src/niceshaper $RPM_BUILD_ROOT%{_bindir}
install etc/niceshaper0.6/* $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper
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
