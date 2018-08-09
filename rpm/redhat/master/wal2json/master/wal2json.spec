%global sname wal2json

Summary:	JSON output plugin for changeset extraction
Name:		%{sname}%{pgmajorversion}
Version:	1.0
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_1_0.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/eulerto/wal2json
# This is for older spec files (RHEL <= 6)
%if 0%{?rhel} && 0%{?rhel} <= 6
Group:		Application/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
wal2json is an output plugin for logical decoding. It means that the
plugin have access to tuples produced by INSERT and UPDATE. Also,
UPDATE/DELETE old row versions can be accessed depending on the
configured replica identity. Changes can be consumed using the streaming
protocol (logical replication slots) or by a special SQL API.

The wal2json output plugin produces a JSON object per transaction. All
of the new/old tuples are available in the JSON object. Also, there are
options to include properties such as transaction timestamp,
schema-qualified, data types, and transaction ids.

%prep
%setup -q -n %{sname}-%{sname}_1_0
%patch0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%make_install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}/%{pginstdir}/doc/extension/
%{__mv} README.md  %{buildroot}/%{pginstdir}/doc/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
 %if 0%{?rhel} && 0%{?rhel} <= 6
 %else
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
 %endif
%endif

%changelog
* Mon Jun 18 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.8-1
- Initial RPM packaging for yum.postgresql.org