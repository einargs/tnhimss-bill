{
  description = "Tools for analyzing and disputing bills";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.05";
  };
  nixConfig = {
    bash-prompt = ''\[\033[1;32m\][\[\e]0;\u@\h: \w\a\]dev-shell:\w]\$\[\033[0m\] '';
  };

  outputs = { self, nixpkgs }: 
  let system = "x86_64-linux"; in
  with nixpkgs.legacyPackages.${system}; {
    devShells.x86_64-linux.default = mkShell {
      buildInputs = [
        # `virtualenv` is a more capable version of the `venv` module.
        python311Packages.virtualenv
        python311
        nodejs_20
        nodePackages.pnpm
      ];
       src = [
         ./flake.nix
         ./flake.lock
        ];

      shellHook = ''
        virtualenv .venv
        source .venv/bin/activate
      '';

      unpackPhase = ''
        for srcFile in $src; do
          cp $srcFile $(stripHash $srcFile)
        done
      ''; 
    };

  };
}
