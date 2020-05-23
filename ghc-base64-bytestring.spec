#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	base64-bytestring
Summary:	Fast base64 encoding and decoding for ByteStrings
Summary(pl.UTF-8):	Szybkie kodowanie i dekodowanie base64 wartości ByteString
Name:		ghc-%{pkgname}
Version:	1.1.0.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/base64-bytestring
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	f6a31309fd7891e65d1bc366405b4d8d
URL:		http://hackage.haskell.org/package/base64-bytestring
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9.0
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides a Haskell library for working with
base64-encoded data quickly and efficiently, using the ByteString
type.

%description -l pl.UTF-8
Ten pakiet dostarcza bibliotekę Haskella do szybkiej i wydajnej pracy
z danymi kodowanymi base64 przy użyciu typu ByteString.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9.0

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname} ghc package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname} ghc package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbase64-bytestring-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbase64-bytestring-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbase64-bytestring-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/URL
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/URL/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/URL/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbase64-bytestring-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base64/URL/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
