#
# Conditional build:
%bcond_without	tests	# unit tests
#
%define	pdir	rpm
%define	pnam	build-perl
Summary:	Calculate dependencies for Perl sources
Summary(pl.UTF-8):	Znajdowanie zależności dla źródeł perlowych
Name:		perl-rpm-build-perl
Version:	0.82
Release:	14
License:	GPL v2+
Group:		Development/Languages/Perl
Source0:	https://www.cpan.org/modules/by-authors/id/A/AT/ATOURBIN/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	1cfb4f6a0842d04ef39fd945abacce91
# https://rt.cpan.org/Ticket/Attachment/1513584/807128/rpm-build-perl-0.82-Adjust-to-perl-5.22.patch
Patch0:		%{name}-perl5.22.patch
# https://rt.cpan.org/Ticket/Attachment/1213691/640915/0001-Fix-non-deterministic-failures-on-newer-perls.patch
Patch1:		%{name}-non-deterministic-failures.patch
# CPAN RT#117350
Patch2:		rpm-build-perl-0.82-Port-to-OpSIBLING-like-macros-required-since-Perl-5..patch
# CPAN RT#142772
Patch3:		rpm-build-perl-Adapt-tests-to-Perl-5.35.12.patch
# from Fedora, CPAN RT #148982
Patch4:		rpm-build-perl-Adjust-to-Perl-5.38.0.patch
URL:		https://metacpan.org/dist/rpm-build-perl
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	perl-Encode
BuildRequires:	perl-Test-Simple
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Calculate dependencies for Perl sources.

%description -l pl.UTF-8
Moduł ten znajduje zależności dla źródeł perlowych.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

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
%attr(755,root,root) %{_bindir}/perl.clean
%attr(755,root,root) %{_bindir}/perl.prov
%attr(755,root,root) %{_bindir}/perl.prov.files
%attr(755,root,root) %{_bindir}/perl.req
%attr(755,root,root) %{_bindir}/perl.req.files
%{perl_vendorarch}/B/Clobbers.pm
%{perl_vendorarch}/B/ConstOptree.pm
%{perl_vendorarch}/B/PerlReq.pm
%{perl_vendorarch}/B/Walker.pm
%dir %{perl_vendorarch}/PerlReq
%{perl_vendorarch}/PerlReq/Utils.pm
%{perl_vendorarch}/fake.pm
%dir %{perl_vendorarch}/auto/B
%dir %{perl_vendorarch}/auto/B/ConstOptree
%attr(755,root,root) %{perl_vendorarch}/auto/B/ConstOptree/ConstOptree.so
%{_mandir}/man1/perl.prov.1p*
%{_mandir}/man1/perl.req.1p*
%{_mandir}/man3/B::Clobbers.3pm*
%{_mandir}/man3/B::ConstOptree.3pm*
%{_mandir}/man3/B::PerlReq.3pm*
%{_mandir}/man3/B::Walker.3pm*
%{_mandir}/man3/PerlReq::Utils.3pm*
