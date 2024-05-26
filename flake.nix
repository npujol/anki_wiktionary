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
        pkgs = import nixpkgs {
          inherit system;
        };
        inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication defaultPoetryOverrides;
      environment-variable = ''
        export BROWSERDRIVER_PATH=${pkgs.lib.getExe pkgs.geckodriver}
        export BROWSER_PATH=${pkgs.lib.getExe pkgs.firefox}
      '';
      in
        with pkgs; rec {
          # Development shell including selenium dependencies
          devShell = mkShell {
            name = "anki_wiktionary";
            buildInputs = [
              pkgs.python312
              pkgs.poetry
            ];
            shellHook = ''
              poetry env use ${pkgs.lib.getExe pkgs.python312}
              export VIRTUAL_ENV=$(poetry env info --path)
              export PATH=$VIRTUAL_ENV/bin/:$PATH
              ${environment-variable}
            '';
          };

          # Runtime package with all dependencies using python version as default option.
          packages.app = mkPoetryApplication {
            projectDir = ./.;
            preferWheels = true;
            python = pkgs.python312;
            checkGroups = [];
          };

          # Use xvfb-run to run the bot in headless mode
          packages.bot = pkgs.writeShellScriptBin "bot" ''
            ${environment-variable}
            ${pkgs.lib.getExe pkgs.xvfb-run} ${packages.app}/bin/bot
          '';

          defaultPackage = packages.bot;
          formatter = pkgs.alejandra;
        }
    );
}
