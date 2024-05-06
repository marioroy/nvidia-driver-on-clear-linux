Name:           nv-codec-headers
Version:        12.2.72.0
Release:        3
Summary:        FFmpeg version of Nvidia Codec SDK headers
License:        MIT
URL:            https://github.com/FFmpeg/nv-codec-headers
Source:         %url/archive/n%{version}/%{name}-n%{version}.tar.gz

#BuildRequires:  make

%description
FFmpeg version of headers required to interface with Nvidias codec APIs.

%prep
%setup -q -n %{name}-n%{version}
sed -i -e 's@/include@/include/ffnvcodec@g' ffnvcodec.pc.in

# Extract license
sed -n '4,25p' include/ffnvcodec/nvEncodeAPI.h > LICENSE
sed -i '1,22s/^.\{,3\}//' LICENSE

%build
%make_build PREFIX=/usr/local-cuda LIBDIR=lib64

%install
%make_install PREFIX=/usr/local-cuda LIBDIR=lib64
mv %{buildroot}/usr/local-cuda %{buildroot}/usr/local
sed -i -e 's/local-cuda/local/' %{buildroot}/usr/local/lib64/pkgconfig/ffnvcodec.pc

%files
%doc README
%license LICENSE
/usr/local/include/ffnvcodec/
/usr/local/lib64/pkgconfig/ffnvcodec.pc

%changelog
# based on https://koji.fedoraproject.org/koji/packageinfo?packageID=26434

