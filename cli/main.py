from config.loader import load_config
from typing import Optional
import typer

# main entry point for cli
app=typer.Typer(help="TypeSafeX CLI tool. Use 'typesafex --help' subcommands.")
 
# load the config 
config = load_config()

from decorators.ensure_types import ensure_types, mode_context
from decorators.ensures import ensures, mode_context
from decorators.requires import requires,mode_context

@requires(('name must be str',lambda name: isinstance(name,str) ),("must be integer",lambda a: isinstance(a,int) ))
def greet(name: str,a:int) -> str:
    return f"{name},bhai"


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
    token = mode_context.set(effective_mode)
    try:
        result = greet('nouman',9)
    finally:
        mode_context.reset(token)
    

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