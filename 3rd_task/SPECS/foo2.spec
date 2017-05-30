Name:           foo2
Version:        0.1
Release:        1%{?dist}
Summary:        Test package

License:        MIT

%description
Test package

%pre
echo preinstall $1

%post
echo postinstall $1

%preun
echo preuninstall $1

%postun
echo postuninstall $1

%files
