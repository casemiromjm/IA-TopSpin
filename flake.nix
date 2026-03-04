{
  description = "Python development environment with uv on Wayland.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};

      runtimeLibs = with pkgs; [
        libGL
        libxkbcommon
        wayland
        libX11
        libXcursor
        libXinerama
        libXext
        libXrandr
        libpulseaudio
      ];
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python312
          uv
          just
        ];

        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibs;
        SDL_VIDEODRIVER = "wayland,x11";

        shellHook = ''
          if [ ! -d ".venv" ]; then
            uv venv
          fi

          source .venv/bin/activate
          uv sync
        '';
      };
    });
}
