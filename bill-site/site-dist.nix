{ lib, buildNpmPackage, ... }:

buildNpmPackage (rec {
  pname = "query-site";
  version = "0.0.1";
  # To regenerate do `prefetch-npm-deps ./notes-site/package-lock.json`
  npmDepsHash = "sha256-O8nPJYytM5DSMTf5bsR3SDfOpkFxdtLOw9WQm66puJ4=";
  npmPackFlags = [ "--ignore-scripts" ];
  NODE_OPTIONS = "--openssl-legacy-provider";
  # npmBuild = "vite build";
  src = ./.;

  # We just copy dist into the out folder
  installPhase = ''
    cp -r ./dist $out/
  '';
})
