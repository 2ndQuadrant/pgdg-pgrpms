%global	sname	periods

Summary:	PERIODs and SYSTEM VERSIONING for PostgreSQL

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2%{?dist}
License:	PostgreSQL
URL:		https://github.com/xocolatl/%{sname}
Source0:	https://github.com/xocolatl/%{sname}/archive/v%{version}.zip
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This extension recreates the behavior defined in SQL:2016 (originally in
SQL:2011) around periods and tables with SYSTEM VERSIONING. The idea is to
figure out all the rules that PostgreSQL would like to adopt (there are some
details missing in the standard) and to allow earlier versions of PostgreSQL
to simulate the behavior once the feature is finally integrated.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%doc %{pginstdir}/doc/extension/README.periods
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Fix OS versions in Makefile, the distro name in the packages changed.

* Fri Aug 30 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
