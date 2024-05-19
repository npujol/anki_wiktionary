{
  pkgs ?
    import (builtins.fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/b8697e57f10292a6165a20f03d2f42920dfaf973.tar.gz";
    }) {
      config.allowUnfree = true;
    },
}:
pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.poetry
  ];
  shellHook = ''
    poetry env use ${pkgs.lib.getExe pkgs.python311}
    export VIRTUAL_ENV=$(poetry env info --path)
    export PATH=$VIRTUAL_ENV/bin/:$PATH
  '';
}
