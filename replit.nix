{pkgs}: {
  deps = [
    # Python
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
    
    # Additional system libraries
    pkgs.openssl
    pkgs.libpq
    pkgs.zlib
  ];
}