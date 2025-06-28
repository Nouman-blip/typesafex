from config.loader import load_config
from typing import Optional
import typer

# main entry point for cli
app=typer.Typer(help="TypeSafeX CLI tool. Use 'typesafex --help' subcommands.")
 
# load the config 
config = load_config()

from decorators.ensure_types import ensure_types, mode_context
from decorators.ensures import ensures,mode_context

@ensures(('name must be str',lambda name: isinstance(name,str) ),("first letter be Capital",lambda name: len(name)>0 and name[0].isupper()))
def greet(name: str) -> str:
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
        result = greet('nouman')
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