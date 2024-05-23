{
  description = "Telegram bot to generate Anki Cards";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-24.05";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
        inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication defaultPoetryOverrides;
      in
        with pkgs; rec {
          # TODO Check why is compiling chromium
          # Development environment
          devShell = mkShell {
            name = "anki_wiktionary";
            buildInputs = [
              pkgs.python311
              pkgs.poetry
            ];
            shellHook = ''
              poetry env use ${pkgs.lib.getExe pkgs.python311}
              export VIRTUAL_ENV=$(poetry env info --path)
              export PATH=$VIRTUAL_ENV/bin/:$PATH
              export CHROMEDRIVER_PATH=${pkgs.lib.getExe pkgs.chromedriver}
              export BROWSER_PATH=${pkgs.lib.getExe pkgs.brave}
            '';
          };

          # Runtime package
          packages.app = mkPoetryApplication {
            projectDir = ./.;
            preferWheels = true;
          };

          # The default package when a specific package name isn't specified.
          defaultPackage = packages.app;
          formatter = pkgs.alejandra;
        }
    );
}
