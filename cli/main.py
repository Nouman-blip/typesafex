from config.loader import load_config
from core.plugin_manager import PluginManager
from core.engine import mode_context,export_test_stub_context,report_context,ci_context,fail_on_warn_context
from typing import Optional
import typer

# main entry point for cli
app=typer.Typer(help="TypeSafeX CLI tool. Use 'typesafex --help' subcommands.")
 
# load the config 
CONFIG= load_config()

from decorators.ensure_types import ensure_types
from decorators.ensures import ensures
from decorators.requires import requires

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
            ),
        report: Optional[bool] = typer.Option(
            False,  # default value
            "--report",  # long form of the option
            "-r",  # optional short term
            help="Generate a json report of violations.",
        ),
        ci: Optional[bool] = typer.Option(
            False,  # default value
            "--ci",  # long form of the option
            "-c",  # optional short term
            help="Enable CI mode(failed on violation).",
        ),
        fail_on_warn: Optional[bool] = typer.Option(
            False,  # default value
            "--fail-on-warn",  # long form of the option
            "-f",  # optional short term
            help="Treat warning as build failure.",
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
    # Set the report context variable based on the command line option
    effective_report = report if report else CONFIG['reporting']['export_report']
    report_token = report_context.set(effective_report)
    # Set the CI context variable based on the command line option
    effective_ci = ci if ci else False
    ci_token = ci_context.set(effective_ci)
    # Set the fail_on_warn context variable based on the command line option
    effective_fail_on_warn = fail_on_warn if fail_on_warn else False
    fail_on_warn_token = fail_on_warn_context.set(effective_fail_on_warn)
    try:
        result = greet('nouman', a=9)
    finally:
        mode_context.reset(mode_token)
        export_test_stub_context.reset(export_test_token)
        report_context.reset(report_token)
        ci_context.reset(ci_token)
        fail_on_warn_context.reset(fail_on_warn_token)


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