{
  description = "Telegram bot to generate Anki Cards";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in with pkgs; rec {
        # Development environment
        devShell = mkShell {
          name = "anki_wiktionary";
          buildInputs = [
            pkgs.python311
            pkgs.poetry
            pkgs.chromedriver
            pkgs.chromium
          ];
          shellHook = ''
            poetry env use ${pkgs.lib.getExe pkgs.python311}
            export VIRTUAL_ENV=$(poetry env info --path)
            export PATH=$VIRTUAL_ENV/bin/:$PATH
            export CHROMEDRIVER_PATH=${pkgs.lib.getExe pkgs.chromedriver}
            export BROWSER_PATH=${pkgs.lib.getExe pkgs.chromium}
          '';
        };

        # Runtime package
        packages.app = poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };

        # The default package when a specific package name isn't specified.
        defaultPackage = packages.app;
      }
    );
}