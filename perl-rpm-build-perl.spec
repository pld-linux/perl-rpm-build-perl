#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	rpm
%define	pnam	build-perl
Summary:	Calculate dependencies for Perl sources
Summary(pl.UTF-8):	Znajdź zależności dla źródeł perlowych
Name:		perl-rpm-build-perl
Version:	0.80
Release:	1
License:	Artistic/GPL
Group:		Development/Languages/Perl
Source0:	http://search.cpan.org/CPAN/authors/id/A/AT/ATOURBIN/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	0ce2716ea447362fa2879684b5daafe7
URL:		http://search.cpan.org/dist/rpm-build-perl/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Calculate dependencies for Perl sources.

%description -l pl.UTF-8
Moduł ten znajduje zależności dla źródeł perlowych.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%attr(755,root,root) %{_bindir}/perl.*
%dir %{perl_vendorlib}/B
%{perl_vendorlib}/B/*.pm
%dir %{perl_vendorlib}/PerlReq
%{perl_vendorlib}/PerlReq/*.pm
%{perl_vendorlib}/*.pm
%{_mandir}/man?/*
