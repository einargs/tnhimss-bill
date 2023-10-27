{ config, pkgs, lib, query-app, ... }:

let cfg = config.services.query-backend; in
with lib;

{
  options = {
    services.query-backend = {
      enable = mkEnableOption "query-backend";

      port = mkOption {
        type = with types; nullOr port;
        default = 80;
        example = 8000;
        description = "The port to bind the server to.";
      };
    };
  };

  config = mkIf cfg.enable {
    systemd.services.query-backend = {
      # TODO: figure out how to setup the proper user.
      description = "socket.io backend for the site";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];
      environment = {
        FHIR_PATH = "${./data/fhir}";
        ENV_FILE = "/var/lib/query-backend/env-file";
        PORT = builtins.toString cfg.port;
      };
      serviceConfig = {
        StateDirectory = "query-backend";
        ExecStart = "${query-app}/bin/query-app";
      };
    };
  };
}
