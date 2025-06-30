from reporting.test_generator import TestGenerator
from typing import List,Any
import logging
import re

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

    def handle_violation(self, function_name: str, violations: list) -> None:
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
            violation_list = self.extract_values(str(violation))
            match self._mode:
                case 'strict':
                    logger.error(str(violation))
                    x = TestGenerator(
                        func_name=violation_list[0],
                        arg_val=violation_list[1],
                        location=violation_list[2],
                        reason=violation_list[3]
                       )
                    logger.info(str(x))
                case 'warn':
                    logger.warning(f"[Warn] Continuing despite violation.")
                case 'off':
                    pass
                case _:
                    logger.info("Please choose from these strict,warn,off")
    @staticmethod                
    def extract_values(violate_str: str) -> List[Any]:
        """
        --violate str of to capture list of var from thi string
        Args:
          violate_str: violation str
        
        return:
            List[str]: [func_name,arg_val,location,reason]
        """
        pattern = (
            r"in func_name:(?P<func_name>\w+)\s+at\s+location:(?P<location>\w+):"
            r"Pre-condition failed:\s+arg_name:(?P<arg_name>\w+)=\s*arg_val:(?P<arg_val>[^->]+)->reason:(?P<reason>.+)"
        )
       
        match = re.search(pattern, violate_str)
        violate_list=[]
        if match:
            func_name = match.group('func_name')
            violate_list.append(func_name)
            arg_name = match.group('arg_name')
            arg_val = match.group('arg_val').strip()
            final_arg_val = __class__.str_other_type(arg_val)
            violate_list.append(final_arg_val)
            location = match.group('location')
            violate_list.append(location)
            reason = match.group('reason')
            reason = re.sub(rf"\b{re.escape(arg_name)}\b", str(final_arg_val), reason)
            violate_list.append(reason)
        return violate_list

    @staticmethod
    def str_other_type(arg_val: Any) -> Any:
        """
        To check if value is str or other type to repr it. if it is string then repr other wise not
        Args:
           arg_val:Any type
        return:
            Any:Any type means if str then repr on the str
        """
        try:
            #first try int
            arg_val_converted=int(arg_val)
        except ValueError:
            try:
                # then convert to float
                arg_val_converted=float(arg_val)
            except ValueError:
                #keep string if not number
                arg_val_converted = arg_val
        # now decide whether repr or not
        if not isinstance(arg_val_converted, str):
            final_arg_val = arg_val_converted
        else:
            final_arg_val = repr(arg_val_converted)
        return final_arg_val