%global gitdate 20211012
%global commit 509d3b21a1084b4f492b50cced8835f4cd591c4a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           vdpau-va-driver-vp9
Version:        0.7.4
Release:        1.%{shortcommit}
Summary:        A VA-API implementation that uses VDPAU as a backend

License:        MIT
URL:            https://github.com/xuanruiqi/vdpau-va-driver-vp9
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

#BuildRequires:  gcc
#BuildRequires:  make
#BuildRequires:  libva-dev
#BuildRequires:  libvdpau-dev
#BuildRequires:  libX11-dev
#BuildRequires:  mesa-dev
#BuildRequires:  xorgproto-dev
#BuildRequires:  pkg-config
#BuildRequires:  pkgconfig(gl)

Provides: %{name} = %{version}-%{release}

%description
This is a VA-API implementation that uses VDPAU as a backend.

%prep
%setup -n %{name}-%{commit}

# Rename the target inside src/Makefile.am so not to create
# the symbolic link automatically, during installation.
# This allows the NVDEC and VDPAU VA-API drivers to co-exist.
pushd %{_builddir}/%{name}-%{commit}
mv src/Makefile.am src/Makefile.am.orig
awk '
    /^install-data-hook:/ {
        print "install-data-hook-not-used:"
        next
    }
    {
        print
    }
' src/Makefile.am.orig >src/Makefile.am
popd


%build
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export FCFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export FFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export CXXFLAGS="$CXXFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "

./autogen.sh --prefix=/usr --enable-glx

make %{?_smp_mflags}


%install
DESTDIR=%{buildroot} make install
rm -f %{buildroot}%{_libdir}/dri/vdpau_drv_video.la


%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/dri/vdpau_drv_video.so


%changelog
# based on https://github.com/clearfraction/gstreamer-libav

