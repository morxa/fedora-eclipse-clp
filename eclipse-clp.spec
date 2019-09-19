Name:		  eclipse-clp
Version:	7.0_49
Release:	2%{?dist}
Summary:	The ECLiPSe Constraint Programming System

License:	MPL
URL:		  http://eclipseclp.org/
Source0:	http://eclipseclp.org/Distribution/Builds/%{version}/src/eclipse_src.tgz#/eclipse-clp-%{version}.tar.gz
Source1:  eclipse-clp.sh
Source2:  tkeclipse-clp.sh
Patch0:   eclipse-clp.tclpath.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	gmp-devel
BuildRequires:	hostname
BuildRequires:	libtool
BuildRequires:	tcl-devel

%description
ECLiPSe is a software system for the cost-effective development and deployment
of constraint programming applications, e.g. in the areas of planning,
scheduling, resource allocation, timetabling, transport etc. It is also ideal
for teaching most aspects of combinatorial problem solving, e.g. problem
modelling, constraint programming, mathematical programming, and search
techniques. It contains several constraint solver libraries, a high-level
modelling and control language, interfaces to third-party solvers, an
integrated development environment and interfaces for embedding into host
environments.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n Eclipse_%{version}


# 'Install' to %%_builddir so we can manually copy files into %%buildroot.
# This is necessary as the install target installs files all over the place and
# not where they belong.
%global LOCALINSTALLDIR %{_builddir}/Eclipse_%{version}/install

%build
CFLAGS="%optflags -DUSE_INTERP_RESULT"
CXXFLAGS="%optflags -DUSE_INTERP_RESULT"

export PREFIX=%{LOCALINSTALLDIR}/%{_prefix}
export ECLIPSEARCH=%{_arch}_linux
export TCL_VERSION=8.6
export TCL_ARCH_DIR=$TCL_DIR
%configure --prefix=$PREFIX
%make_build -f Makefile.%{_arch}_linux -j1

%install

# Use a custom script to set up the environment. The original eclipse-clp has
# all paths wrong, so it's easier to write it from scratch.
rm -rf %{LOCALINSTALLDIR}/%{_bindir}/%{_arch}_linux/{eclipse,tkeclipse}
install -p -D -m755 %{SOURCE1} %{buildroot}/%{_bindir}/eclipse-clp
install -p -D -m755 %{SOURCE2} %{buildroot}/%{_bindir}/tkeclipse-clp
install -p -D -t %{buildroot}/%{_bindir} %{LOCALINSTALLDIR}/%{_bindir}/%{_arch}_linux/*

install -p -D -t %{buildroot}/%{_libdir} %{LOCALINSTALLDIR}/%{_prefix}/lib/%{_arch}_linux/*.so*
install -p -D -t %{buildroot}/%{_includedir}/%{name} %{LOCALINSTALLDIR}/%{_includedir}/%{_arch}_linux/*

# Install the actual binary in %%{_libexecdir}, as it's not supposed be called directly, but from the script in %%{_bindir}.
install -p -D %{LOCALINSTALLDIR}/%{_prefix}/lib/%{_arch}_linux/eclipse.exe %{buildroot}/%{_libexecdir}/%{name}/eclipse-clp
## Remove so we can glob lib
rm -rf %{LOCALINSTALLDIR}/%{_prefix}/lib/%{_arch}_linux
install -p -D -t %{buildroot}/%{_libexecdir}/%{name}/lib/chr %{LOCALINSTALLDIR}/%{_prefix}/lib/chr/*
## Remove so we can glob lib
rm -rf %{LOCALINSTALLDIR}/%{_prefix}/lib/chr
install -p -D -t %{buildroot}/%{_libexecdir}/%{name}/lib %{LOCALINSTALLDIR}/%{_prefix}/lib/*
ln -s %{_libdir}/tkeclipse.so %{buildroot}/%{_libexecdir}/%{name}/lib/
ln -s %{_libdir}/tkexdr.so %{buildroot}/%{_libexecdir}/%{name}/lib/
# Not needed
rm %{LOCALINSTALLDIR}/%{_prefix}/lib_tcl/eclipse_arch.tcl
mv %{LOCALINSTALLDIR}/%{_prefix}/lib_tcl %{buildroot}/%{_libexecdir}/%{name}/lib_tcl
chmod +x %{buildroot}/%{_libexecdir}/%{name}/lib_tcl/tkeclipse.tcl

%files
%{_bindir}/eclipse-clp
%{_bindir}/tkeclipse-clp
%{_bindir}/tktools
%{_libdir}/*.so
%{_libexecdir}/%{name}

%files devel
%{_includedir}/%{name}


%changelog
* Thu Sep 19 2019 Till Hofmann <thofmann@fedoraproject.org> - 7.0_49-2
- Install missing tcl files

* Thu Sep 19 2019 Till Hofmann <thofmann@fedoraproject.org> - 7.0_49-1
- Initial package
