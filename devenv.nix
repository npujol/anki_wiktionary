{ pkgs, ... }:

{
  # Match the project's previous flake development environment.
  packages = with pkgs; [
    python312
    poetry
    geckodriver
    firefox
    playwright-driver.browsers
    xvfb-run
    python312Packages.playwright
  ];

  languages.python = {
    enable = true;
    package = pkgs.python312;
    poetry = {
      enable = true;
      install = {
        enable = true;
        # Keep the environment aligned with the Poetry lockfile, including dev tools.
        groups = [ "main" "dev" ];
      };
    };
  };

  env = {
    BROWSERDRIVER_PATH = "${pkgs.geckodriver}/bin/geckodriver";
    BROWSER_PATH = "${pkgs.firefox}/bin/firefox";
    PLAYWRIGHT_BROWSERS_PATH = "${pkgs.playwright-driver.browsers}";
    PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS = "true";
    LD_PRELOAD = "${pkgs.stdenv.cc.cc.lib}/lib/libstdc++.so.6";
  };

  # Preserve the old shell's Poetry virtualenv activation behavior.
  enterShell = ''
    poetry env use ${pkgs.python312}/bin/python
    export VIRTUAL_ENV="$(poetry env info --path)"
    export PATH="$VIRTUAL_ENV/bin:$PATH"
  '';
}
