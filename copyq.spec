#
# Conditional build
%bcond_with	qt6		# build againast Qt6

%define		qt5ver	5.8.0
%define		qt6ver	6.1.0

Summary:	Advanced clipboard manager with editing and scripting features
Name:		copyq
Version:	6.4.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/hluk/CopyQ/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	69972953a49d2a312463baa30dd5c50a
Patch0:		%{name}-plugindir.patch
URL:		https://hluk.github.io/CopyQ/
%if %{without qt6}
BuildRequires:	Qt5Core-devel >= %{qt5ver}
BuildRequires:	Qt5Gui-devel >= %{qt5ver}
BuildRequires:	Qt5Network-devel >= %{qt5ver}
BuildRequires:	Qt5Qml-devel >= %{qt5ver}
BuildRequires:	Qt5Svg-devel >= %{qt5ver}
BuildRequires:	Qt5WaylandClient-devel >= %{qt5ver}
BuildRequires:	Qt5Widgets-devel >= %{qt5ver}
BuildRequires:	Qt5X11Extras-devel >= %{qt5ver}
BuildRequires:	Qt5Xml-devel >= %{qt5ver}
BuildRequires:	qt5-linguist
%else
BuildRequires:	Qt6Core-devel >= %{qt6ver}
BuildRequires:	Qt6Gui-devel >= %{qt6ver}
BuildRequires:	Qt6Network-devel >= %{qt6ver}
BuildRequires:	Qt6Qml-devel >= %{qt6ver}
BuildRequires:	Qt6Svg-devel >= %{qt6ver}
BuildRequires:	Qt6WaylandClient-devel >= %{qt6ver}
BuildRequires:	Qt6Widgets-devel >= %{qt6ver}
BuildRequires:	Qt6Xml-devel >= %{qt6ver}
BuildRequires:	qt6-linguist
%endif
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 5.18.0
BuildRequires:	kf5-knotifications-devel >= 5.18.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libxcb-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	wayland-devel >= 1.15
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-proto-xproto-devel
%if %{without qt6}
Requires:	Qt5Core >= %{qt5ver}
Requires:	Qt5Gui >= %{qt5ver}
Requires:	Qt5Network >= %{qt5ver}
Requires:	Qt5Qml >= %{qt5ver}
Requires:	Qt5Script >= %{qt5ver}
Requires:	Qt5Svg >= %{qt5ver}
Requires:	Qt5WaylandClient >= %{qt5ver}
Requires:	Qt5Widgets >= %{qt5ver}
Requires:	Qt5X11Extras >= %{qt5ver}
Requires:	Qt5Xml >= %{qt5ver}
%else
Requires:	Qt6Core >= %{qt6ver}
Requires:	Qt6Gui >= %{qt6ver}
Requires:	Qt6Network >= %{qt6ver}
Requires:	Qt6Qml >= %{qt6ver}
Requires:	Qt6Script >= %{qt6ver}
Requires:	Qt6Svg >= %{qt6ver}
Requires:	Qt6WaylandClient >= %{qt6ver}
Requires:	Qt6Widgets >= %{qt6ver}
Requires:	Qt6Xml >= %{qt6ver}
%endif
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
Requires:	bash-completion >= 1:2.0
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
	%{cmake_on_off qt6 WITH_QT6} \
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
