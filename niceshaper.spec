Summary:	NiceShaper - bandwidth limiting
Summary(pl):	NiceShaper - dynamiczny podzia� ��cza
Name:		niceshaper
Version:	0.5
Release:	1
License:	GPL
Group:		Networking/Admin
Source0:	http://www.niceshaper.mikule.net/files/%{name}-%{version}.tar.bz2
# Source0-md5:	e33efd5a56e7d3f31d31a4b906fefbde
Source1:	%{name}.users
Source2:	%{name}.config
Source3:	%{name}.about
Source4:	%{name}.init
URL:		http://www.niceshaper.mikule.net/
PreReq:         rc-scripts
Requires(post,preun):   /sbin/chkconfig
Requires:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program opieraj�c si� na HTB dzieli dost�pne pasmo na komputery w
sieci, dynamicznie dostosowuj�c si� do generowanego przez ka�dego z
u�ytkownik�w obci��enia.

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
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper

install niceshaper $RPM_BUILD_ROOT%{_bindir}
install etc/niceshaper/* $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper
install niceshaper.init $RPM_BUILD_ROOT/etc/rc.d/init.d/niceshaper

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add niceshaper
if [ -f /var/run/niceshaper.pid ]; then
        /etc/rc.d/init.d/niceshaper restart >&2
else
        echo "Run \"/etc/rc.d/init.d/niceshaper start\" to start niceshaper daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/run/niceshaper.pid ]; then
                /etc/rc.d/init.d/niceshaper stop >&2
        fi
        /sbin/chkconfig --del niceshaper
fi

%files
%defattr(644,root,root,755)
%doc users config about
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/niceshaper
%attr(640,root,root) %verify(not size md5 mtime) %config(noreplace) %{_sysconfdir}/niceshaper/*
