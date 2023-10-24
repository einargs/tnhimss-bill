{ lib, buildNpmPackage, ... }:

buildNpmPackage (rec {
  pname = "query-site";
  version = "0.0.1";
  # To regenerate do `prefetch-npm-deps ./notes-site/package-lock.json`
  npmDepsHash = "sha256-mwU1i/N5h/GzCJfGm3m9kNzxwz3wPT2z9bUTz4yjIzU=";
  src = ./.;

  # We just copy dist into the out folder
  installPhase = ''
    cp -r ./dist $out/
  '';
})
