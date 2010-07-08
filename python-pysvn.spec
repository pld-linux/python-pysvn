%bcond_with	tests

%define	module	pysvn
Summary:	Python SVN Tools
Summary(pl.UTF-8):	Narzędzia do SVN w Pythonie
Name:		python-%{module}
Version:	1.7.2
Release:	2
License:	Apache Group License
Group:		Development/Languages/Python
Source0:	http://pysvn.barrys-emacs.org/source_kits/%{module}-%{version}.tar.gz
# Source0-md5:	b557a12bc34f0d6805e259d69b9f38ce
URL:		http://pysvn.tigris.org/
BuildRequires:	apr-devel
BuildRequires:	subversion
BuildRequires:	subversion-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python
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

%build
cd Source
%{__python} ./setup.py configure \
	--apr-inc-dir="$(apr-1-config --includedir)" \
	--svn-lib-dir=%{_libdir}
%{__make} \
	CC="%{__cc} -c" \
	CCC="%{__cxx} -c $(pkg-config apr-util-1 --cflags)"

%{?with_tests:%{__make} -C ../Tests -f unix.mak PYTHON=%{_bindir}/python}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}/pysvn

install Source/pysvn/__init__.py Source/pysvn/*.so $RPM_BUILD_ROOT%{py_sitedir}/pysvn
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Client
install Examples/Client/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Client

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
