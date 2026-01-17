let pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = with pkgs; [
    gcc-arm-embedded
    openocd
    uv
  ];
  shellHook = ''
  source .venv/bin/activate
  jupyter lab3
  '';
}