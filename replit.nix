{pkgs}: {
  deps = [
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
    pkgs.libpq
    pkgs.zlib
  ];
  
  env = {
    LD_LIBRARY_PATH = "${pkgs.postgresql.lib}/lib";
  };
}