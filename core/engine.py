from config.loader import load_config
from reporting.test_generator import TestGenerator
from reporting.json_format_violations import ViolationJson
from core.plugin_manager import PluginManager
from typing import List, Dict, Any
from sys import exit
import contextvars
import logging
import time
import re

logger = logging.getLogger('typesafex')
logging.basicConfig(encoding='utf-8',
                     level=logging.DEBUG)

# load config from config.loader

CONFIG = load_config()
report_context = contextvars.ContextVar("report", default=False)
mode_context = contextvars.ContextVar("mode", default=None)
export_test_stub_context = contextvars.ContextVar("export_test_stub", default=False)
ci_context = contextvars.ContextVar("ci", default=False)
fail_on_warn_context= contextvars.ContextVar("fail_on_warn", default=False)

class Engine:
    """
    log the function it decides what should print and why
    """
    def __init__(self) -> None:
        self._mode: bool = mode_context.get()
        self._plugin_manager = None
        self._report: bool = report_context.get() 
        self._violations: List[Dict[str, Any]] = []
        self._export_test_stub: bool = export_test_stub_context.get()
        self._ci: bool = ci_context.get()
        self._fail_on_warn: bool = fail_on_warn_context.get()


    @property
    def plugin_manager(self):
        """
        Lazy initialization of plugin manager
        """
        if self._plugin_manager is None:
            self._plugin_manager = PluginManager(CONFIG)
        return self._plugin_manager

    def handle_violations(self, function_name: str, violations: list) -> None:
        """
        Handle function contract type violations based on the current mode. 
        Args:
          function_name: str of function name to check condition violation
          violations: list of condition's violation
        
        return:
            None: logs the violation
        """
        
        for violation in violations:
            if not violation:
                return
            #append violation to the list of dicts
            self._violations.append({
                "func_name": violation.func,
                "reason": violation.reason,
                "args": violation.args,
                "kwargs": violation.kwargs,
                "contract_type": violation.location,
                "mode": self._mode,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            })
            # generate test stub 
            test_stub = TestGenerator(
                func_name=violation.func,
                arg_name=violation.arg_name,
                arg_val=violation.arg_val,
                location=violation.location,
                condition=violation.condition
            )
            match self._mode:
                case 'strict':
                    # logging violation
                    logger.error(str(violation))
                    #  pass to the plugin manager to handle violation
                    self.plugin_manager.dispatch('on_violation', violation)
                    #logging test suggestion
                    self.plugin_manager.dispatch("on_test_generated",violation.func,violation.location,self._export_test_stub,str(test_stub))
                    # logger.info(str(test_stub_generated))
                case 'warn':
                    logger.warning(f"[Warn] Continuing despite violation.")
                case 'off':
                    pass
                case _:
                    logger.info("Please choose from these strict,warn,off")
        # if _report_true then send the path and violation data to the ViolationJson class method save to file
        if self._report:
            file_path = CONFIG.get('reporting', {}).get('json_file_path', None)
            ViolationJson.save_to_file(file_path, self._violations)
            logger.info(f"Violation data saved to {file_path}")
        else:
            logger.info("Reporting is disabled, no violation data saved.")
        #handle ci make TypesafeX return the correct exit code on the base on violation found and ta
        if self._ci:
            if self._mode == "strict" and violations:
                logger.error(f"[TYPESAFEX] ❌ {len(violations)} violation(s) found -- build failed.")
                exit(1)
            elif self._mode == "warn" and self._fail_on_warn and violations:
                logger.error(f"[TYPESAFEX] ❌ {len(violations)} warning(s) found -- build failed (--fail_on_warn).")
                exit(1)
            else:
                logger.info(f"[TYPESAFEX] ✅ CI mode passed with mode == {self._mode}")
                exit(0)
                
