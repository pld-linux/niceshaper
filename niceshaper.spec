# TODO:
# - look into niceshaper.init and remake it if needed

Summary:	NiceShaper - bandwidth limiting
Summary(pl):	NiceShaper - dynamiczny podzia³ ³±cza
Name:		niceshaper
Version:	0.5rc3
Release:	0.2
License:	GPL
Group:		Networking/Admin
Source0:	http://www.niceshaper.mikule.net/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.users
Source2:	%{name}.config
Source3:	%{name}.about
Source4:	%{name}.init
URL:		http://www.niceshaper.mikule.net/
Requires:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program opieraj±c siê na HTB dzieli dostêpne pasmo na komputery w
sieci, dynamicznie dostosowuj±c siê do generowanego przez ka¿dego z
u¿ytkowników obci±¿enia.

%prep
%setup -q -c

%build
%{__cxx} %{rpmcflags} niceshaper.cpp -o niceshaper
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
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

%files
%defattr(644,root,root,755)
%doc niceshaper.users niceshaper.config niceshaper.about
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/niceshaper
%attr(640,root,root) %verify(not size md5 mtime) %config(noreplace) %{_sysconfdir}/niceshaper/*
