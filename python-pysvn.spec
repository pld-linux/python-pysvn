%bcond_with	tests

%define	module	pysvn
Summary:	Python SVN Tools
Name:		python-%{module}
Version:	1.3.0
Release:	1
License:	Apache Group License
Group:		Development/Languages/Python
Source0:	http://pysvn.tigris.org/files/documents/1233/25338/%{module}-%{version}.tar.gz
# Source0-md5:	f31d99a2fe9078f9b0501f8eb6364e18
URL:		http://pysvn.tigris.org/
BuildRequires:	apr-devel
BuildRequires:	subversion-devel
BuildRequires:	python-devel
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

%prep
%setup  -q -n %{module}-%{version}

%build
cd Source
python ./setup.py configure \
	--apr-inc-dir="$(apr-1-config --includedir)" \
	--svn-lib-dir=%{_libdir}
%{__make} \
	CC="%{__cc} -c" \
	CCC="%{__cxx} -c"

%{?with_tests:%{__make} -C ../Tests -f unix.mak PYTHON=%{_bindir}/python}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}/pysvn

install Source/pysvn/__init__.py Source/pysvn/*.so $RPM_BUILD_ROOT%{py_sitedir}/pysvn

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Docs/* Examples/*
%dir %{py_sitedir}/pysvn
%attr(755,root,root) %{py_sitedir}/pysvn/*.so
%{py_sitedir}/pysvn/*.py[co]
