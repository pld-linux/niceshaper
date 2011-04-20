
%define		_rc	rc8

Summary:	NiceShaper - bandwidth limiting
Summary(pl.UTF-8):	NiceShaper - dynamiczny podział łącza
Name:		niceshaper
Version:	0.6
Release:	0.%{_rc}.1
License:	GPL
Group:		Networking/Admin
Source0:	http://niceshaper.jedwabny.net/files/%{name}%{version}%{_rc}.tar.bz2
# Source0-md5:	32aab12fe08aa77c4244c9c3db1c082b
Source1:	%{name}.users
Source2:	%{name}.config
Source3:	%{name}.about
Source4:	%{name}.init
Patch0:		%{name}-includes.patch
Patch1:		%{name}-iptables-deprecated.patch
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
Program opierając się na HTB/IMQ dzieli dostępne pasmo na komputery w
sieci, dynamicznie dostosowując się do generowanego przez każdego z
użytkowników obciążenia.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

%build

%{__make} \
	CPP="%{__cxx} %{rpmcxxflags}"

install %{SOURCE1} ./users
install %{SOURCE2} ./config
install %{SOURCE3} ./about
install %{SOURCE4} .

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/niceshaper0.6,/etc/rc.d/init.d}

install niceshaper $RPM_BUILD_ROOT%{_bindir}
install etc/niceshaper0.6/* $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper0.6
install niceshaper.init $RPM_BUILD_ROOT/etc/rc.d/init.d/niceshaper

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
%dir %{_sysconfdir}/%{name}0.6
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}0.6/*
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/niceshaper
