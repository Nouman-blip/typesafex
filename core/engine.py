import logging

logger = logging.getLogger('typesafex')
logging.basicConfig(encoding='utf-8',
                     level=logging.DEBUG)

class Engine:
    """
    log the function it decides what should print and why
    """
    def __init__(self, mode:str) -> None:
        self._mode = mode
        
    def handle_type_violations(self, metadata: dict, args_violations: list, return_violations: str) -> None:
        """
        tracing the logs and showing the violation on the basis of mode.
        mode-> strict: then raised voilation -> warn: then raised warnings -> off: do nothing

        Args:
           metadata: dictionary of function name, args,kwargs and return value
           args_violation: list of argument violation excepted vs passed 
           return_violation: str of return violations excepted vs returned by type hint

        return:
           None: Nothing just log things
        """
        logger.info(f"[TRACE] called function {metadata['func_name']} with args={metadata['args']},return={metadata['return_value']}")
        match self._mode:
            case 'strict':
                if args_violations:
                    for violation in args_violations:
                        logger.warning(f"[Violation]: Argument {violation}")
                if return_violations:
                    logger.warning(f"[Violation]: Function {return_violations}")
                logger.info(f"[Mode: {self._mode}] TypeSafeX raised violation.")
            case 'warn':
                if args_violations:
                    logger.warning("there might be type error")
                else:
                    logger.info("no args violation")
                
                if return_violations:
                    logger.warning("there might be type error")
                else:
                    logger.info("no function violation")
                logger.info(f'[Mode: {self._mode}] TypeSafeX raised warning.')
            case 'off':
                logger.info(f'[Mode: {self._mode}] TypeSafeX doing nothing.')
            case _:
                logger.info(f"please choose from 'strict', 'warn', 'off")

    def handle_post_violation(self, function_name: str, violations: list) -> None:
        """
        handle post condtion violation of func
        Args:
          function_name: str of function name to check condition violation
          violations: list of condition's violation
        
        return:
            None: logs the violation
        """
        for violation in violations:
            if not violation:
                return
            match self._mode:
                case 'strict':
                    logger.error(str(violation))
                case 'warn':
                    logger.warning(f"[Warn] might be violation.")
                case 'off':
                    pass
                case _:
                    logger.info("Please choose from these strict,warn,off")