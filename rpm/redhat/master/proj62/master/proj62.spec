%global sname proj
%global projinstdir /usr/%{sname}62

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Name:		%{sname}62
Version:	6.2.1
Release:	1%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source1:	http://download.osgeo.org/%{sname}/%{sname}-datumgrid-1.8.zip
Source2:	%{name}-pgdg-libs.conf


BuildRequires:	sqlite-devel >= 3.7 gcc-c++
%if 0%{?fedora} > 28 || 0%{?rhel} == 8
Requires:	sqlite-libs >= 3.7
%else
Requires:	sqlite
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%package static
Summary:	Development files for PROJ
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions. Proj docs: http://www.remotesensing.org/dl/new_docs/

%description devel
This package contains libproj and the appropriate header files and man pages.

%description static
This package contains libproj static library.

%prep
%setup -q -n %{sname}-%{version}

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

%build
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{projinstdir}/lib" ; export SHLIB_LINK

./configure --prefix=%{projinstdir} --without-jni
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%make_install
%{__install} -d %{buildroot}%{projinstdir}/share/%{sname}
%{__install} -d %{buildroot}%{projinstdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{projinstdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%clean
%{__rm} -rf %{buildroot}

%post
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%postun
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc %{projinstdir}/share/doc/*
%{projinstdir}/bin/*
%{projinstdir}/share/man/man1/*.1
%{projinstdir}/share/proj/*
%{projinstdir}/lib/libproj.so.15*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{projinstdir}/share/man/man3/*.3
%{projinstdir}/include/*.h
%{projinstdir}/include/proj/*
%{projinstdir}/include/proj_json_streaming_writer.hpp
%{projinstdir}/lib/*.so
%{projinstdir}/lib/*.a
%attr(0755,root,root) %{projinstdir}/lib/pkgconfig/%{sname}.pc
%exclude %{projinstdir}/lib/libproj.a
%exclude %{projinstdir}/lib/libproj.la
%{projinstdir}/include/proj/util.hpp

%files static
%defattr(-,root,root,-)
%{projinstdir}/lib/libproj.a
%{projinstdir}/lib/libproj.la

%changelog
* Thu Aug 29 2019 Devrim Gündüz <devrim@gunduz.org> - 0:6.2.1-1
- Update to 6.2.1

* Thu Aug 29 2019 Devrim Gündüz <devrim@gunduz.org> - 0:6.2.0-1
- Initial 6.2 packaging for PostgreSQL RPM Repository
