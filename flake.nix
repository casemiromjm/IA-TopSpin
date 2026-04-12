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
        zlib
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
          python313
          python313Packages.matplotlib

          python313Packages.uv
          python313Packages.ruff

          just
          typst
        ];

        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibs;
        SDL_VIDEODRIVER = "wayland,x11";
        UV_PYTHON = "python3.13";

        shellHook = ''
          if [ ! -d ".venv" ]; then
            uv venv -- pyhton
          fi

          source .venv/bin/activate
          uv sync
        '';
      };
    });
}
