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
          # Development shell including selenium dependencies
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

          # Runtime package with all dependencies using python version as default option.
          packages.app = mkPoetryApplication {
            projectDir = ./.;
            preferWheels = true;
          };

          defaultPackage = packages.app;
          formatter = pkgs.alejandra;
        }
    );
}
