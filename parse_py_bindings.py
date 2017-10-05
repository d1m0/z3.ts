#import sys
#import os

#DIR = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, DIR + "/z3/build/python/")

import z3.z3core as z3c
from z3.z3core import lib
import z3.z3types as z3t
import ctypes

t = [getattr(z3t, x) for x in dir(z3t)]

t1 = [x for x in t if hasattr(x, '_type_')]

mapping = {
    z3t.ApplyResultObj: ("Z3_apply_result", "voidp"),
    z3t.Ast: ("Z3_ast", "voidp"),
    z3t.AstMapObj: ("Z3_ast_map", "voidp"),
    z3t.AstVectorObj: ("Z3_ast_vector", "voidp"),
    z3t.Config: ("Z3_config", "voidp"),
    z3t.Constructor: ("Z3_constructor", "voidp"),
    z3t.ConstructorList: ("Z3_constructorList", "voidp"),
    z3t.ContextObj: ("Z3_context", "voidp"),
    z3t.FixedpointObj: ("Z3_fixedpoint", "voidp"),
    z3t.FuncDecl: ("Z3_func_decl", "voidp"),
    z3t.FuncEntryObj: ("Z3_func_entry", "voidp"),
    z3t.FuncInterpObj: ("Z3_func_interp", "voidp"),
    z3t.GoalObj: ("Z3_goal", "voidp"),
#    z3t.Literals: None,
    z3t.Model: ("Z3_model", "voidp"),
#    z3t.ModelObj: None,
    z3t.OptimizeObj: ("Z3_optimize", "voidp"),
    z3t.ParamDescrs: ("Z3_param_descrs", "voidp"),
    z3t.Params: ("Z3_param", "voidp"),
    z3t.Pattern: ("Z3_pattern", "voidp"),
    z3t.ProbeObj: ("Z3_probe", "voidp"),
    z3t.RCFNumObj: ("Z3_rcf_num", "voidp"),
    z3t.SolverObj: ("Z3_solver", "voidp"),
    z3t.Sort: ("Z3_sort", "voidp"),
    z3t.StatsObj: ("Z3_stats", "voidp"),
    z3t.Symbol: ("Z3_symbol", "voidp"),
    z3t.TacticObj: ("Z3_tactic", "voidp"),
    ctypes.c_int: ("c_int", "number"),
    ctypes.c_long: ("c_long", "number"),
    ctypes.c_uint: ("c_uint", "number"),
    ctypes.c_ulong: ("c_ulong", "number"),
    ctypes.c_double: ("c_double", "number"),
    ctypes.c_float: ("c_float", "number"),
    ctypes.c_char_p: ("c_char_p", "string"),
    ctypes.c_bool: ("c_bool", "number"),
    ctypes.POINTER(z3t.Ast): ("Z3_ast_arr", "voidp_arr"),
    ctypes.POINTER(ctypes.c_char_p): ("string_arr", "voidp_arr"),
    ctypes.POINTER(ctypes.c_int): ("c_int_arr", "uint_arr"),
    ctypes.POINTER(ctypes.c_long): ("c_long_arr", "uint_arr"),
    ctypes.POINTER(ctypes.c_uint): ("c_uint_arr", "uint_arr"),
    ctypes.POINTER(ctypes.c_ulong): ("c_ulong_arr", "uint_arr"),
    ctypes.POINTER(z3t.Symbol): ("Z3_symbol_arr", "voidp_arr"),
    ctypes.POINTER(z3t.Sort): ("Z3_sort_arr", "voidp_arr"),
    ctypes.POINTER(z3t.Constructor): ("Z3_constructor_arr", "voidp_arr"),
    ctypes.POINTER(z3t.ConstructorList): ("Z3_constructor_list_arr",
                                          "voidp_arr"),
    ctypes.POINTER(z3t.FuncDecl): ("Z3_func_decl_arr", "voidp_arr"),
    ctypes.POINTER(z3t.AstVectorObj): ("Z3_ast_vector_arr", "voidp_arr"),
    ctypes.POINTER(z3t.Model): ("Z3_model_arr", "voidp_arr"),
    ctypes.POINTER(z3t.Pattern): ("Z3_pattern_arr", "voidp_arr"),
    ctypes.POINTER(z3t.RCFNumObj): ("Z3_rcf_num_arr", "voidp_arr"),
    ctypes.POINTER(z3t.TacticObj): ("Z3_tactic_arr", "voidp_arr"),
}

wasm_mapping  = {
    "number":   "number",
    "voidp":    "number",
    "string":   "string",
    "voidp_arr":    "number",
    "uint_arr":    "number",
}

l = lib()

# Types
print "type Z3_lbool = number;"
for t, (ts_name, ts_type) in mapping.items():
    print "type {} = {};".format(ts_name, ts_type)

print \
"""
interface WasmJSInstance extends WebAssembly.Instance {
  ccall(fname: string, returnType: string, argTypes: string[], args: any[]): any;
}
"""

print \
"""
class LibZ3 {
  constructor(private wasmInstance: WasmJSInstance) { }

"""


for x in dir(l):
    t = getattr(l, x)

    if not isinstance(t, l._FuncPtr):
        continue

    resT = t.restype
    argsT = t.argtypes

    if argsT is None:
        print x, resT, argsT
        continue

    assert resT in mapping,\
        "Missing result type {} for {}".format(resT, x)

    tsResT = mapping[resT][0]
    wasmResT = wasm_mapping[mapping[resT][1]]

    tsArgTs = []
    wasmArgTs = []

    for i, t in enumerate(argsT):
        assert t in mapping,\
            "Missing {}-th argument type {} for {}".format(i, t, x)
        tsArgTs.append(mapping[t][0])
        wasmArgTs.append(wasm_mapping[mapping[t][1]])

    funcArgs = ", ".join(["arg{}: {}".format(i, t) for (i, t) in enumerate(tsArgTs)])
    func = "    {}({}): {} {{\n".format(x, funcArgs, tsResT)

    wasmArgsTsStr = "[" + ", ".join("'{}'".format(x) for x in wasmArgTs) + "]"
    wasmArgs = "[" + ", ".join(["arg{}".format(i) for i in range(len(wasmArgTs))]) + "]"

    if wasmResT != "null":
        wasmResT = "'{}'".format(wasmResT)

    func += "        return this.wasmInstance.ccall('{}', {}, {}, {})\n".format(x, wasmResT, wasmArgsTsStr, wasmArgs)
    func += "    }\n"

    print func

print "}"