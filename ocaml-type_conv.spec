#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Support library for preprocessor type conversions
Summary(pl.UTF-8):	Biblioteka wspierająca dla konwersji typów preprocesora
Name:		ocaml-type_conv
Version:	113.00.02
Release:	2
License:	Apache v2.0 and BSD
Group:		Libraries
#Source0Download: https://github.com/janestreet/type_conv/releases
Source0:	https://github.com/janestreet/type_conv/archive/%{version}/type_conv-%{version}.tar.gz
# Source0-md5:	62b64cf98ad2685a718dd7d1706497f5
URL:		https://github.com/janestreet/type_conv/
BuildRequires:	ocaml >= 4.00.0
BuildRequires:	ocaml-findlib >= 1.3.2
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
The type_conv mini-library factors out functionality needed by
different preprocessors that generate code from type specifications.

%description -l pl.UTF-8
Mini-biblioteka type_conv gromadzi wspólną funkcjonalność wymaganą
przez różne preprocesory generujące kod ze specyfikacji typów.

%package devel
Summary:	Support library for preprocessor type conversions - development part
Summary(pl.UTF-8):	Biblioteka wspierająca dla konwersji typów preprocesora - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
type_conv library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do tworzenia programów używających
biblioteki type_conv.

%prep
%setup -q -n type_conv-%{version}

%build
ocaml setup.ml -configure \
	--prefix %{_prefix} \
	--override bytecomp_c_compiler "%{__cc} %{rpmcflags} -fno-defer-pop -D_FILE_OFFSET_BITS=64 -D_REENTRANT -fPIC" \
	--override native_c_compiler "%{__cc} %{rpmcflags} -D_FILE_OFFSET_BITS=64 -D_REENTRANT"

ocaml setup.ml -all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml

export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
ocaml setup.ml -install

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/type_conv/*.{annot,cmt,cmti}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md COPYRIGHT.txt INRIA-DISCLAIMER.txt LICENSE.txt LICENSE-Tywith.txt README.md THIRD-PARTY.txt
%dir %{_libdir}/ocaml/type_conv
%{_libdir}/ocaml/type_conv/META
%{_libdir}/ocaml/type_conv/pa_type_conv.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/type_conv/pa_type_conv.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/type_conv/pa_type_conv.cmi
# doc?
%{_libdir}/ocaml/type_conv/pa_type_conv.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/type_conv/pa_type_conv.a
%{_libdir}/ocaml/type_conv/pa_type_conv.cmx
%{_libdir}/ocaml/type_conv/pa_type_conv.cmxa
%endif
