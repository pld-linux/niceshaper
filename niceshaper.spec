# TODO:
# - make init.d script

Summary:	NiceShaper - bandwidth limiting
Summary(pl):	NiceShaper - dzielenie ³±cza
Name:		niceshaper
Version:	0.5rc3
Release:	0.1
License:	GPL
Group:		Networking/Admin
Source0:	http://www.niceshaper.mikule.net/files/%{name}-%{version}.tar.bz2
Source1:	niceshaper.users
Source2:	niceshaper.config
Source3:	niceshaper.about
URL:		http://www.niceshaper.mikule.net/
Requires:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program potrafi ograniczaæ przepustowo¶æ interfejsu ethernet/ppp oraz
dzieliæ dostêpne pasmo pomiêdzy komputery w sieci lokalnej.

%prep
%setup -q -c

%build
%{__cxx} %{rpmcflags} niceshaper.cpp -o niceshaper
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper

install niceshaper $RPM_BUILD_ROOT%{_bindir}
install etc/niceshaper/* $RPM_BUILD_ROOT%{_sysconfdir}/niceshaper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc niceshaper.users niceshaper.config niceshaper.about
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %verify(not size md5 mtime) %config(noreplace) %{_sysconfdir}/niceshaper/*
