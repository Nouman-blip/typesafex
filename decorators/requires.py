# @requires decorator logic

"""
you specify preconditions like @requires(state=open). if the condition not met
the function won't run, preventing invalid states.
"""
from functools import wraps
from contracts.violations import Violation
from core.engine import Engine
import contextvars
import inspect

mode_context=contextvars.ContextVar('mode',default=None)
def requires(*conditions):
    def requires_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mode_ = mode_context.get()
            engine=Engine(mode_)
            violations = []
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            arguments_ = bound.arguments
            #failed_conditions in conditions by dict comprehension
            failed_conditions = {arg_name:[(label, func_(arguments_[arg_name])) for label, func_ in cond_list if not func_(arguments_[arg_name])] for arg_name, cond_list in conditions[0].items() if arg_name in arguments_.keys()}
            keep_only_non_empty_list_value = {arg_name: result_list for arg_name, result_list in failed_conditions.items() if result_list}
            only_labels_list_value = {arg_name: [condition_label for condition_label, bool_val in violate_list] for arg_name, violate_list in keep_only_non_empty_list_value.items()}
            
            violations_results = {arg_name: [(arg_name,arguments_[arg_name], label) for label in condition_list] for arg_name, condition_list in only_labels_list_value.items()}
            #flatten into single list of tuples final -results 
            results_list=[violate_result for sublist in violations_results.values() for violate_result in sublist]
        
            if results_list:
                for result in results_list:
                    violations.update(Violation(
                        func=func.__name__,
                        arg_name=result[0]
                        arg_val=result[1],
                        condition=result[2]
                        reason=f"Pre-condition failed: {result[2]}",
                        args=bound.args,
                        kwargs=bound.kwargs,
                        location='precondition'
                    ))
            engine.handle_violation(func.__name__, violations)
            # block func call if violation occur means before function call
            if violations:
                return
            # call function call if no violations occur
            result=func(*args,**kwargs)
            return result
        return wrapper
    return requires_decorator