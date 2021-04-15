%define		qtver	5.8.0

Summary:	Advanced clipboard manager with editing and scripting features
Name:		copyq
Version:	4.0.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/hluk/CopyQ/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2015c7772d2c3dec3608351a9a045c04
Patch0:		%{name}-plugindir.patch
URL:		https://hluk.github.io/CopyQ/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Script-devel >= %{qtver}
BuildRequires:	Qt5Svg-devel >= %{qtver}
BuildRequires:	Qt5WaylandClient-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 5.18.0
BuildRequires:	kf5-knotifications-devel >= 5.18.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libxcb-devel
BuildRequires:	qt5-linguist
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-proto-xproto-devel
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5Network >= %{qtver}
Requires:	Qt5Qml >= %{qtver}
Requires:	Qt5Script >= %{qtver}
Requires:	Qt5Svg >= %{qtver}
Requires:	Qt5WaylandClient >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
Requires:	Qt5Xml >= %{qtver}
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
Requires:	kf5-knotifications >= 5.18.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CopyQ monitors system clipboard and saves its content in customized
tabs. Saved clipboard can be later copied and pasted directly into any
application.

%package -n bash-completion-copyq
Summary:	Bash completion for CopyQ
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-copyq
Bash completion for CopyQ.

%prep
%setup -q -n CopyQ-%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DDATA_INSTALL_PREFIX:PATH=%{_datadir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database

%postun
%update_icon_cache hicolor
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/copyq
%dir %{_libdir}/copyq
%dir %{_libdir}/copyq/plugins
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemencrypted.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemfakevim.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemimage.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemnotes.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitempinned.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemsync.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemtags.so
%attr(755,root,root) %{_libdir}/copyq/plugins/libitemtext.so
%dir %{_datadir}/copyq
%{_datadir}/copyq/themes
%dir %{_datadir}/copyq/translations
%{_desktopdir}/com.github.hluk.copyq.desktop
%{_iconsdir}/hicolor/*x*/apps/copyq.png
%{_iconsdir}/hicolor/scalable/apps/copyq.svg
%{_iconsdir}/hicolor/scalable/apps/copyq_mask.svg
%{_mandir}/man1/copyq.1*
%{_datadir}/metainfo/com.github.hluk.copyq.appdata.xml

%files -n bash-completion-copyq
%defattr(644,root,root,755)
%{bash_compdir}/copyq
