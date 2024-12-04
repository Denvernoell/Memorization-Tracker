import tomli

from pathlib import Path
from supabase import create_client,Client

# config_file = "secrets.toml"
config_file = "denver.toml"
if not Path(config_file).exists():
    config_file = r"I:\Project Resources\Coding\Credentials\denver.toml"

with open(config_file, "rb") as f:
    config = tomli.load(f)


supabase: Client = create_client(
        config["supabase"]["url"],
        config["supabase"]["key"],
    )
