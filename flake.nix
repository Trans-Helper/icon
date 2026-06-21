{
  description = "Trans-Helper Icon Generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            cairo
            uv
            python3
          ];

          shellHook = ''
            export LD_LIBRARY_PATH="${pkgs.cairo.out}/lib:$LD_LIBRARY_PATH"
          '';
        };
      }
    );
}
