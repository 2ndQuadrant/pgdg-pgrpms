%global sname	pgtap

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Unit testing for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.99.0
Release:	2%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
URL:		https://pgxn.org/dist/pgtap/
Source0:	https://api.pgxn.org/dist/pgtap/%{version}/pgtap-%{version}.zip
# Use this source for pg_prove and pg_tapgen
Source1:	https://search.cpan.org/CPAN/authors/id/D/DW/DWHEELER/TAP-Parser-SourceHandler-pgTAP-3.33.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion} perl-Test-Pod perl-Test-Pod-Coverage
%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:	perl-Module-Build
%endif
Requires:	postgresql%{pgmajorversion}-server, perl-Test-Harness >= 3.0
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

BuildArch:	noarch

%description
pgTAP is a unit testing framework for PostgreSQL written in PL/pgSQL and
PL/SQL. It includes a comprehensive collection of TAP-emitting assertion
functions, as well as the ability to integrate with other TAP-emitting
test frameworks. It can also be used in the xUnit testing style.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
%{__make} USE_PGXS=1 TAPSCHEMA=pgtap %{?_smp_mflags}

# Build pg_prove and pg_tapgen
tar zxf %{SOURCE1}
pushd TAP-Parser-SourceHandler-pgTAP-3.33
perl Build.PL
./Build
popd

%install
%{__rm} -rf  %{buildroot}
%{__make} install USE_PGXS=1 DESTDIR=%{buildroot} %{?_smp_mflags}

# Install pg_prove and pg_tapgen
pushd TAP-Parser-SourceHandler-pgTAP-3.33
%{__mkdir} -p  %{buildroot}%{_bindir}
%{__install} -m 755 bin/* %{buildroot}%{_bindir}
%{__mkdir} -p  %{buildroot}%{perl_privlib}/TAP/Parser/SourceHandler/
%{__install} lib/TAP/Parser/SourceHandler/pgTAP.pm %{buildroot}%{perl_privlib}/TAP/Parser/
popd

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/pgtap.mmd
%{_bindir}/pg_prove
%{_bindir}/pg_tapgen
%{pginstdir}/share/extension/*pgtap*.sql
%{pginstdir}/share/extension/pgtap.control
%{perl_privlib}/TAP/Parser/pgTAP.pm

%changelog
* Sun Oct 28 2018 Devrim Gündüz <devrim@gunduz.org> - 0.99.0-2
- Attempt to fix #3720

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.99.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Sep 24 2018 Devrim Gündüz <devrim@gunduz.org> 0.99.0-1
- Update to 0.99.0

* Sat Mar 17 2018 Devrim Gündüz <devrim@gunduz.org> 0.98.0-2
- Add pg_prove and pg_tapgen, per #3167

* Wed Nov 8 2017 Devrim Gündüz <devrim@gunduz.org> 0.98.0-1
- Update to 0.98.0

* Sat Dec 3 2016 Devrim Gündüz <devrim@gunduz.org> 0.97.0-1
- Update to 0.97.0

- Fri Mar 27 2015 Devrim Gündüz <devrim@gunduz.org> 0.95.0-1
- Update to 0.95.0

* Wed Jul 2 2014 Devrim Gündüz <devrim@gunduz.org> 0.94.0-1
- Update to 0.94.0

* Fri Apr 1 2011 Devrim Gündüz <devrim@gunduz.org> 0.25.0-1
- Update to 0.25.0

* Fri Oct 8 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-3
- Use alternatives method for binaries.
- Use %%{?_smp_mflags} macro for make.

* Thu Oct 7 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-2
- Update spec for 9.0 layout.
- TODO: Use alternatives.

* Tue Jun 15 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-1
- Update to 0.24

* Mon Dec 28 2009 Devrim Gündüz <devrim@gunduz.org> 0.23-1
- Update to 0.23

* Wed Aug 19 2009 Darrell Fuhriman <darrell@projectdx.com> 0.22-1
- initial RPM

