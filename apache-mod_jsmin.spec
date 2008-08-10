%define snap r7

#Module-Specific definitions
%define mod_name mod_jsmin
%define mod_conf B43_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module which 'minifies' javascript
Name:		apache-%{mod_name}
Version:	0
Release: 	%mkrel 0.%{snap}.1
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a port of Douglas Crockford's JSMin program so that it can be run as an
apache 2.x filter.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

head -27 %{mod_name}.c > LICENSE

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

