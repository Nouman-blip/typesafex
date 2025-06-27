from config.loader import load_config
from typing import Optional
import typer

# main entry point for cli
app=typer.Typer(help="TypeSafeX CLI tool. Use 'typesafex --help' subcommands.")
 
# load the config 
config = load_config()

from decorators.ensure_types import ensure_types 

@ensure_types
def greet(name: str) -> str:
    
    return f"Hello, {name}!"


@app.command()
def check(
         mode_override: Optional[str] = typer.Option(
            None,  #defualt value
            "--mode",  # long form of the option
            "-m",  #optional short term
            help=f"Override enforecement mode for this check.  "
         ) )->None:
    """
    Scans,activate, and optionally enforce runtime contracts on decoratored 
     Python code

     like e.g typesefaex check file
       or typesafex check file --mode warn
    
    """
    effective_mode = mode_override or config['mode']
    typer.echo(f" Running TypeSafeX check in {effective_mode.upper()} mode")

    result = greet('world')
    
    typer.echo(f"Decorated function return results {result}")

    

@app.command()
def mode(mode_type: str):
    """
    Enforcement mode strict,warn,off.
    """
    typer.echo(f"The user in {mode_type} mode.")

@app.command()
def version():
    """
    Get the TypeSafeX CLI version.
    """
    typer.echo(f"TypeSafeX CLI version is '0.1.0' .")

if __name__ == "__main__":
    app()