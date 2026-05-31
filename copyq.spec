%define		qt6ver	6.2.0

Summary:	Advanced clipboard manager with editing and scripting features
Name:		copyq
Version:	16.0.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/hluk/CopyQ/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ba1b4e37e2d5e19a1ebbc0e117c2e1a1
Patch0:		%{name}-plugindir.patch
URL:		https://hluk.github.io/CopyQ/
BuildRequires:	Qt6Core-devel >= %{qt6ver}
BuildRequires:	Qt6DBus-devel >= %{qt6ver}
BuildRequires:	Qt6Gui-devel >= %{qt6ver}
BuildRequires:	Qt6Keychain-devel
BuildRequires:	Qt6Network-devel >= %{qt6ver}
BuildRequires:	Qt6Qml-devel >= %{qt6ver}
BuildRequires:	Qt6Svg-devel >= %{qt6ver}
BuildRequires:	Qt6WaylandClient-devel >= %{qt6ver}
BuildRequires:	Qt6Widgets-devel >= %{qt6ver}
BuildRequires:	Qt6Xml-devel >= %{qt6ver}
BuildRequires:	qca-qt6-devel
BuildRequires:	qt6-linguist
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libxcb-devel
BuildRequires:	miniaudio-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	wayland-devel >= 1.15
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-proto-xproto-devel
Requires:	Qt6Core >= %{qt6ver}
Requires:	Qt6DBus >= %{qt6ver}
Requires:	Qt6Gui >= %{qt6ver}
Requires:	Qt6Network >= %{qt6ver}
Requires:	Qt6Qml >= %{qt6ver}
Requires:	Qt6Svg >= %{qt6ver}
Requires:	Qt6WaylandClient >= %{qt6ver}
Requires:	Qt6Widgets >= %{qt6ver}
Requires:	Qt6Xml >= %{qt6ver}
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
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

%package -n gnome-shell-extension-copyq
Summary:	GNOME Shell extension for CopyQ
Summary(pl.UTF-8):	Rozszerzenie powłoki GNOME (GNOME Shell) dla CopyQ
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-shell >= 3.36
BuildArch:	noarch

%description -n gnome-shell-extension-copyq
GNOME Shell extension for CopyQ.

%description -n gnome-shell-extension-copyq -l pl.UTF-8
Rozszerzenie powłoki GNOME (GNOME Shell) dla CopyQ.

%prep
%setup -q -n CopyQ-%{version}
%patch -P0 -p1

%build
%cmake -B build \
	-DWITH_NATIVE_NOTIFICATIONS:BOOL=OFF \
	-DDATA_INSTALL_PREFIX:PATH=%{_datadir} \
	-DMINIAUDIO_INCLUDE_DIR:PATH=/usr/include/miniaudio
%{__make} -C build

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
%{_datadir}/metainfo/com.github.hluk.copyq.metainfo.xml

%files -n bash-completion-copyq
%defattr(644,root,root,755)
%{bash_compdir}/copyq

%files -n gnome-shell-extension-copyq
%defattr(644,root,root,755)
%dir %{_datadir}/gnome-shell/extensions/copyq-clipboard@hluk.github.com
%{_datadir}/gnome-shell/extensions/copyq-clipboard@hluk.github.com/extension.js
%{_datadir}/gnome-shell/extensions/copyq-clipboard@hluk.github.com/metadata.json
