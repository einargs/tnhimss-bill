{ lib, buildNpmPackage, ... }:

buildNpmPackage (rec {
  pname = "query-site";
  version = "0.0.1";
  # To regenerate do `prefetch-npm-deps ./notes-site/package-lock.json`
  npmDepsHash = "sha256-JywVvJ2wWyOuzvPc9rzZbK2uO4YXq6pZTEHmYne04hM=";
  npmPackFlags = [ "--ignore-scripts" ];
  NODE_OPTIONS = "--openssl-legacy-provider";
  # npmBuild = "vite build";
  src = ./.;

  # We just copy dist into the out folder
  installPhase = ''
    cp -r ./dist $out/
  '';
})
