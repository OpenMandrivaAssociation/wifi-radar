Summary:	Utility for managing WiFi profiles
Name:		wifi-radar
Version:	2.0.s09
Release:	1
Source0:	https://wifi-radar.tuxfamily.org/pub/%{name}-%{version}.tar.bz2
Source1:	16x%{name}.png
Source2:	32x%{name}.png
Source3:	48x%{name}.png
License:	GPL
Group:		Networking/Other
Url:		http://wifi-radar.systemimager.org/

Requires:	pygtk2.0
Requires:	dhcpcd
Requires:	usermode-consoleonly
BuildArch:	noarch

%description
WiFi Radar is a Python/PyGTK2  utility for managing WiFi profiles.
It enables you to scan for available networks and create profiles for
your preferred networks. At boot time, running WiFi Radar will
automatically scan for an available preferred network and connect to
it. You can drag and drop your preferred networks to arrange the
profile priority.

%prep
%setup -q
perl -pi -e 's!^CONF_FILE\s*=.*!CONF_FILE = "%{_sysconfdir}/%{name}.conf"!' %{name}

%build

%install
rm -rf %buildroot

install -D -m 755 %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}/
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 600 %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 %{name}.1 $RPM_BUILD_ROOT/%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
install -m 644 %{name}.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5

install -m 644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=WIFI radar
Comment=Simple wireless network manager
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/%{name} <<EOF
USER=root
PROGRAM=%{_sbindir}/%{name}
SESSION=true
EOF

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name} <<EOF
#%PAM-1.0
auth       sufficient   pam_rootok.so
auth       sufficient   pam_timestamp.so
auth       include      system-auth
session    required     pam_permit.so
session    optional     pam_xauth.so
session    optional     pam_timestamp.so
account    required     pam_permit.so
EOF

%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc CHANGE.LOG README README.WPA-Mini-HOWTO.txt TODO
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}.conf.5*



%changelog
* Sun Sep 20 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.9.9-2mdv2010.0
+ Revision: 445780
- rebuild

* Sun Mar 15 2009 Funda Wang <fundawang@mandriva.org> 1.9.9-1mdv2009.1
+ Revision: 355190
- New version 1.9.9

* Sun Aug 03 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.9.8-5mdv2009.0
+ Revision: 261983
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.9.8-4mdv2009.0
+ Revision: 255987
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 1.9.8-2mdv2008.1
+ Revision: 140932
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sat Aug 11 2007 Olivier Blin <oblin@mandriva.com> 1.9.8-2mdv2008.0
+ Revision: 61956
- do not use pam_stack anymore (#31659)

* Fri Apr 20 2007 Olivier Blin <oblin@mandriva.com> 1.9.8-1mdv2008.0
+ Revision: 16099
- XDG menu
- update url
- 1.9.8


* Mon Jul 25 2005 Olivier Blin <oblin@mandriva.com> 1.9.4-1mdk
- 1.9.4
- package man pages
- add menu and icons (from Nicolas Brouard)

* Wed May 04 2005 Olivier Blin <oblin@mandriva.com> 1.9.3-3mdk
- ship config file

* Wed May 04 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.9.3-2mdk
- packages is noarch
- mark conf files as %%config
- %%mkrel
- cosmetics

* Wed Apr 27 2005 Olivier Blin <oblin@mandriva.com> 1.9.3-1mdk
- initial release

