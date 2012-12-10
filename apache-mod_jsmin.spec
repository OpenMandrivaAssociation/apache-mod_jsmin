%define snap r7

#Module-Specific definitions
%define mod_name mod_jsmin
%define mod_conf B43_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module which 'minifies' javascript
Name:		apache-%{mod_name}
Version:	0
Release: 	0.%{snap}.7
Group:		System/Servers
License:	BSD
URL:		http://code.google.com/p/modjsmin/
Source0:	mod_jsmin.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0

%description
This is a port of Douglas Crockford's JSMin program so that it can be run as an
apache 2.x filter.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

head -27 %{mod_name}.c > LICENSE

%build
%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.7mdv2012.0
+ Revision: 772671
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.6
+ Revision: 678330
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.5mdv2011.0
+ Revision: 588014
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.4mdv2010.1
+ Revision: 516132
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.3mdv2010.0
+ Revision: 406601
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.2mdv2009.1
+ Revision: 325789
- rebuild

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.1mdv2009.0
+ Revision: 270300
- import apache-mod_jsmin


* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0-0.r7.1mdv2009.0
- initial Mandriva package
