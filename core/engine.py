import logging

logger = logging.getLogger('typesafex')
logging.basicConfig(encoding='utf-8',
                     level=logging.DEBUG)

class Engine:
    """
    log the function it decides what should print and why
    """
    @staticmethod
    def logger_info(metadata):
        logger.info(f"[TRACE] called function {metadata['func_name']} with args={metadata['args']},return={metadata['return_value']}")