# Copyright (c) 2016-2019, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%global githubname   intel-cmt-cat
%global githubver    3.0.1

%if %{defined githubsubver}
%global githubfull   %{githubname}-%{githubver}.%{githubsubver}
%else
%global githubfull   %{githubname}-%{githubver}
%endif

# disable producing debuginfo for this package
%global debug_package %{nil}


Summary:            Provides command line interface to CMT, MBM, CAT, CDP and MBA technologies
Name:               %{githubname}
Release:            1%{?dist}
Version:            %{githubver}
License:            BSD
ExclusiveArch:      x86_64 i686 i586
%if %{defined githubsubver}
Source:             https://github.com/01org/%{githubname}/archive/v%{githubver}.%{githubsubver}.tar.gz
%else
Source:             https://github.com/01org/%{githubname}/archive/v%{githubver}.tar.gz
%endif
URL:                https://github.com/01org/%{githubname}
BuildRequires:      gcc, make

%description
This software package provides basic support for
Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring (MBM),
Cache Allocation Technology (CAT), Memory Bandwidth Allocation (MBA),
and Code Data Prioratization (CDP).

CMT, MBM and CAT are configured using Model Specific Registers (MSRs)
to measure last level cache occupancy, set up the class of service masks and
manage the association of the cores/logical threads to a class of service.
The software executes in user space, and access to the MSRs is
obtained through a standard Linux* interface. The virtual file system
provides an interface to read and write the MSR registers but
it requires root privileges.

%package -n intel-cmt-cat-devel
Summary:            Library and sample code to use CMT, MBM, CAT, CDP and MBA technologies
License:            BSD
Requires:           intel-cmt-cat == %{version}
ExclusiveArch:      x86_64 i686 i586

%description -n intel-cmt-cat-devel
This software package provides basic support for
Cache Monitoring Technology (CMT), Memory Bandwidth Monitoring (MBM),
Cache Allocation Technology (CAT), Memory Bandwidth Allocation (MBA),
and Code Data Prioratization (CDP).
The package includes library, header file and sample code.

For additional information please refer to:
https://github.com/01org/%{githubname}

%prep
%autosetup -n %{githubfull}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%build
make %{?_smp_mflags}

%install
# Not doing make install as it strips the symbols.
# Using files from the build directory.
install -d %{buildroot}/%{_bindir}
install -s %{_builddir}/%{githubfull}/pqos/pqos %{buildroot}/%{_bindir}
install %{_builddir}/%{githubfull}/pqos/pqos-os %{buildroot}/%{_bindir}
install %{_builddir}/%{githubfull}/pqos/pqos-msr %{buildroot}/%{_bindir}
sed -i "1s/.*/\#!\/usr\/bin\/bash/" %{buildroot}/%{_bindir}/pqos-*

install -d %{buildroot}/%{_mandir}/man8
install -m 0644 %{_builddir}/%{githubfull}/pqos/pqos.8  %{buildroot}/%{_mandir}/man8
ln -sf %{_mandir}/man8/pqos.8 %{buildroot}/%{_mandir}/man8/pqos-os.8
ln -sf %{_mandir}/man8/pqos.8 %{buildroot}/%{_mandir}/man8/pqos-msr.8

install -d %{buildroot}/%{_bindir}
install -s %{_builddir}/%{githubfull}/rdtset/rdtset %{buildroot}/%{_bindir}

install -d %{buildroot}/%{_mandir}/man8
install -m 0644 %{_builddir}/%{githubfull}/rdtset/rdtset.8  %{buildroot}/%{_mandir}/man8

install -d %{buildroot}/%{_licensedir}/%{name}-%{version}
install -m 0644 %{_builddir}/%{githubfull}/LICENSE %{buildroot}/%{_licensedir}/%{name}-%{version}

# Install the library
install -d %{buildroot}/%{_libdir}
install -s %{_builddir}/%{githubfull}/lib/libpqos.so.* %{buildroot}/%{_libdir}
cp -a %{_builddir}/%{githubfull}/lib/libpqos.so %{buildroot}/%{_libdir}
cp -a %{_builddir}/%{githubfull}/lib/libpqos.so.3 %{buildroot}/%{_libdir}

# Install the header file
install -d %{buildroot}/%{_includedir}
install -m 0644 %{_builddir}/%{githubfull}/lib/pqos.h %{buildroot}/%{_includedir}

# Install license and sample code
install -d %{buildroot}/%{_usrsrc}/%{githubfull}
install -m 0644 %{_builddir}/%{githubfull}/LICENSE %{buildroot}/%{_usrsrc}/%{githubfull}

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/Makefile          %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/reset_app.c       %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/allocation_app_l2cat.c  %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/allocation_app_l3cat.c  %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/allocation_app_mba.c  %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CAT_MBA/association_app.c %{buildroot}/%{_usrsrc}/%{githubfull}/c/CAT_MBA

install -d %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CMT_MBM/Makefile      %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM
install -m 0644 %{_builddir}/%{githubfull}/examples/c/CMT_MBM/monitor_app.c %{buildroot}/%{_usrsrc}/%{githubfull}/c/CMT_MBM

%files
%{_bindir}/pqos
%{_bindir}/pqos-os
%{_bindir}/pqos-msr
%{_mandir}/man8/pqos.8.gz
%{_mandir}/man8/pqos-os.8.gz
%{_mandir}/man8/pqos-msr.8.gz
%{_bindir}/rdtset
%{_mandir}/man8/rdtset.8.gz
%{_libdir}/libpqos.so.*

%{!?_licensedir:%global license %%doc}
%license %{_licensedir}/%{name}-%{version}/LICENSE
%doc ChangeLog README

%files -n intel-cmt-cat-devel
%{_libdir}/libpqos.so
%{_libdir}/libpqos.so.3
%{_includedir}/pqos.h
%{_usrsrc}/%{githubfull}/c/CAT_MBA/Makefile
%{_usrsrc}/%{githubfull}/c/CAT_MBA/reset_app.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/association_app.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/allocation_app_l2cat.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/allocation_app_l3cat.c
%{_usrsrc}/%{githubfull}/c/CAT_MBA/allocation_app_mba.c
%{_usrsrc}/%{githubfull}/c/CMT_MBM/Makefile
%{_usrsrc}/%{githubfull}/c/CMT_MBM/monitor_app.c
%doc %{_usrsrc}/%{githubfull}/LICENSE

%changelog
* Tue May 21 2019 Jiri Olsa <jolsa@redhat.com> 3.1.0-1
- new version 3.1.0
- change spec to follow fedora
- Resolves: rhbz#1643196

* Thu Nov 15 2018 Jiri Olsa <jolsa@redhat.com> 2.1.0-1
- new version 2.1.0
- change spec to follow fedora
- Resolves: rhbz#1643196

* Mon May 08 2017 Jiri Olsa <jolsa@redhat.com> 0.1.5-2
- new version 0.1.5-1
- change spec to follow fedora
- Resolves: rhbz#1448539

* Thu May 04 2017 Jiri Olsa <jolsa@redhat.com> 0.1.5-1
- Resolves: rhbz#1315489

* Thu Mar 30 2017 Jiri Olsa <jolsa@redhat.com> 0.1.4-5
- Resolves: rhbz#1315489

* Fri Feb 17 2017 Gopal Tiwari <gtiwari@redhat.com> 0.1.4-4
- Resolves: rhbz#1315489 

* Tue Apr 19 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-3
- global typo fix
- small edits in the description

* Mon Apr 18 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-2
- LICENSE file added to the package

* Thu Apr 7 2016 Tomasz Kantecki <tomasz.kantecki@intel.com> 0.1.4-1
- initial version of the package
