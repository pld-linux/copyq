Summary:	Advanced clipboard manager with editing and scripting features
Name:		copyq
Version:	3.13.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/hluk/CopyQ/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9597af33ac85be21c574e736382ed93a
Patch0:		%{name}-plugindir.patch
URL:		https://hluk.github.io/CopyQ/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Script-devel
BuildRequires:	Qt5Svg
BuildRequires:	Qt5Widgets-devel >= 5.5.0
BuildRequires:	Qt5Xml-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	qt5-linguist
Requires:	Qt5Widgets >= 5.5.0
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CopyQ monitors system clipboard and saves its content in customized
tabs. Saved clipboard can be later copied and pasted directly into any
application.

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
