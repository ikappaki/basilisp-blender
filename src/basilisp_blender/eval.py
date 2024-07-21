"""Functions for evaluating Basilisp code."""

from basilisp import cli
from basilisp import main as basilisp
from basilisp.lang import compiler, runtime

from basilisp_blender import COMPILER_OPTS

# the namesapce where the command will be evaluated at
EVALUATION_NS_ = "blender-user"

CTX_ = compiler.CompilerContext(filename="blender", opts=COMPILER_OPTS)
NS_VAR_ = runtime.set_current_ns(EVALUATION_NS_)
EOF_ = object()


def eval_str(code):
    """Evaluate the given `code` string in Basilisp and return the
    result.

    """
    return cli.eval_str(code, CTX_, NS_VAR_.value, EOF_)


def eval_file(filepath):
    """Evaluate the Basilisp code from the file specified by
    `filepath`.

    """
    return cli.eval_file(filepath, CTX_, NS_VAR_.value)


# Set up the Basilisp namespace for command evaluation
eval_str(f"(ns {EVALUATION_NS_} (:require clojure.core))")

try:
    import bpy

    def eval_editor(text_block):
        """Evaluate the Basilisp code contained in the specified
        Blender Text Editor `text_block` and return the result.

        """
        code = bpy.data.texts[text_block].as_string()
        return eval_str(code)

except ImportError:
    pass
