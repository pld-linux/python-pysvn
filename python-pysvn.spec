# NOTE
# - The GUI is packaged in pysvn-workbench.spec
#
# Conditional build:
%bcond_with	tests		# build with tests

%define	module	pysvn
Summary:	Python SVN Tools
Summary(pl.UTF-8):	Narzędzia do SVN w Pythonie
Name:		python-%{module}
Version:	1.8.0
Release:	1
License:	Apache
Group:		Development/Languages/Python
Source0:	http://pysvn.barrys-emacs.org/source_kits/%{module}-%{version}.tar.gz
# Source0-md5:	3999a7680f4d3c4d3bddfc45edf65788
Patch1:		x32.patch
URL:		http://pysvn.tigris.org/
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	subversion
BuildRequires:	subversion-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pysvn Extension Features:
- Supports all svn client features
- Supports svn transaction features required to write svn pre-commit
  hooks
- Easy to learn and use
- Python like interface
- Good Documentation and examples
- No need to understand the Subversion C API

%description -l pl.UTF-8
Cechy pysvn:
- obsługuje wszystkie możliwości klienta svn
- obsługuje cechy transakcji svn wymagane do pisania procedur
  wywoływanych przed commitem do svn
- łatwy w nauce i użyciu
- pythonowy interfejs
- dobra dokumentacja i przykłady
- nie trzeba rozumieć API C do Subversion

%prep
%setup  -q -n %{module}-%{version}
%patch1 -p1

%build
cd Source
%{__python} ./setup.py configure \
	--apr-inc-dir="$(apr-1-config --includedir)" \
	--apu-inc-dir="$(apu-1-config --includedir)" \
	--svn-lib-dir=%{_libdir}

%{__make} \
	CC="%{__cc} -c $(pkg-config apr-util-1 --cflags)" \
	CCC="%{__cxx} -c $(pkg-config apr-util-1 --cflags)"

%{?with_tests:%{__make} -C ../Tests -f unix.mak PYTHON=%{__python}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}/pysvn
cp -a Source/pysvn/__init__.py Source/pysvn/*.so $RPM_BUILD_ROOT%{py_sitedir}/pysvn

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Client
cp -p Examples/Client/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Client

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Docs/*
%dir %{py_sitedir}/pysvn
%attr(755,root,root) %{py_sitedir}/pysvn/*.so
%{py_sitedir}/pysvn/*.py[co]
%{_examplesdir}/%{name}-%{version}
