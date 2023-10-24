{
  description = "Tools for querying medical records with natural language";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.05";
    poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
  };
  nixConfig = {
    bash-prompt = ''\[\033[1;32m\][\[\e]0;\u@\h: \w\a\]dev-shell:\w]\$\[\033[0m\] '';
  };

  outputs = { self, poetry2nix, nixpkgs }: 
  let system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        overlay = [ poetry2nix.overlay ];
      };

      backend-app-env = (pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ./.;
        src = ./src;
        python = pkgs.python311;
        preferWheels = true;
      });

      query-app = pkgs.symlinkJoin {
        name = "query-app";

        paths = with pkgs; [
          (writeShellScriptBin "query-app" ''
            hypercorn ${./src}/app:asgi -b 127.0.0.1:$PORT
          '')
          backend-app-env
          stdenv.cc
        ];
        buildInputs = [ pkgs.makeWrapper ];
        postBuild = ''
          wrapProgram $out/bin/query-app --prefix PATH : $out/bin \
            --prefix LD_LIBRARY_PATH : $out/lib
        '';
      };

      site-dist = pkgs.callPackage ./bill-site/site-dist.nix {};
  in with pkgs; {
    packages.x86_64-linux = {
      site = site-dist;
    };
    nixosModules.backend = args: import ./vm/site-service.nix ({
      query-site = site-dist;
      inherit query-app;
    } // args);
    devShells.x86_64-linux.default = mkShell {
      buildInputs = [
        # `virtualenv` is a more capable version of the `venv` module.
        python311Packages.virtualenv
        python311
        nodejs_20
        nodePackages.pnpm
        prefetch-npm-deps
        poetry
        neo4j
        neo4j-desktop
        docker
      ];
       src = [
         ./flake.nix
         ./flake.lock
        ];

      shellHook = ''
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
