{pkgs}: {
  deps = [
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.tk
    pkgs.tcl
    pkgs.qhull
    pkgs.gtk3
    pkgs.gobject-introspection
    pkgs.ghostscript
    pkgs.freetype
    pkgs.ffmpeg-full
    pkgs.cairo
    pkgs.bash
    pkgs.libxcrypt
    pkgs.glibcLocales
    # Python base
    pkgs.python39
    pkgs.poetry
    
    # Node.js
    pkgs.nodejs-18_x
    pkgs.yarn
    
    # PostgreSQL
    pkgs.postgresql
    
    # Development tools
    pkgs.nodePackages.typescript-language-server
    
    # Build dependencies
    pkgs.gcc
    pkgs.cmake
    pkgs.pkg-config
    
    # PDF processing
    pkgs.poppler_utils
    
    # System libraries
    pkgs.openssl
    pkgs.zlib
  ];
  
  env = {
    LD_LIBRARY_PATH = "${pkgs.postgresql.lib}/lib";
  };
}