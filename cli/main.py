from config.loader import load_config
from core.plugin_manager import PluginManager
from plugins.test_collector import export_test_stub_context
from typing import Optional
import typer

# main entry point for cli
app=typer.Typer(help="TypeSafeX CLI tool. Use 'typesafex --help' subcommands.")
 
# load the config 
CONFIG= load_config()

from decorators.ensure_types import ensure_types, mode_context
from decorators.ensures import ensures, mode_context
from decorators.requires import requires, mode_context

@requires({'name':[('len(name)>8',lambda name: len(name)>8 ),("name=='Nouman'",lambda name: name=='Nouman' )],'a':[("isinstance(a,str)",lambda a: isinstance(a,str) )]})
def greet(name: str,a:str) -> str:
    return f"{name},bhai"


@app.command(help="Check contracts in your code.")
def check(
         mode_override: Optional[str] = typer.Option(
            None,  #defualt value
            "--mode",  # long form of the option
            "-m",  #optional short term
            help=f"Override enforecement mode for this check.  ",
         ),
         export_test: Optional[bool] = typer.Option(
                False,  # default value
                "--export-test",  # long form of the option
                "-e",  # optional short term
                help="Export test stubs to a file.",
            )
        )->None:
    """
    Scans,activate, and optionally enforce runtime contracts on decoratored 
     Python code

     like e.g typesefaex check file
       or typesafex check file --mode warn
    
    """
    effective_mode = mode_override if mode_override is not None else CONFIG['mode']
    mode_token = mode_context.set(effective_mode)
    # Set the export_test context variable based on the command line option
    effective_export_test= export_test if export_test else CONFIG['test_generation']['export_test_stub'] 
    export_test_token = export_test_stub_context.set(effective_export_test)
    try:
        result = greet('nouman', 9)
    finally:
        mode_context.reset(mode_token)
        export_test_stub_context.reset(export_test_token)


@app.command(help="List all loaded plugins.")
def plugins():
    try:
        # Initialize the PluginManager with the loaded config
        plugin_manager = PluginManager(CONFIG)
        for plugin in plugin_manager.plugins:
            typer.echo(f"{plugin.__class__.__name__}")
    except Exception as e:
        typer.echo(f"Error listing plugins: {e}", err=True)

@app.command(help="List all configuration settings.")
def config():
    """
    List all configuration settings.
    """
    typer.echo("Current configuration settings:")
    for key, value in CONFIG.items():
        typer.echo(f"{key}: {value}")

@app.command(help="Run the TypeSafeX CLI version command.")
def version():
    """
    Get the TypeSafeX CLI version.
    """
    typer.echo(f"TypeSafeX CLI version is '0.1.0' .")

if __name__ == "__main__":
    app()