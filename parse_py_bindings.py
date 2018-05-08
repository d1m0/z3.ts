from z3.z3core import lib
import z3.z3types as z3t
import ctypes

t = [getattr(z3t, x) for x in dir(z3t)]

t1 = [x for x in t if hasattr(x, '_type_')]

mapping = {
    z3t.ApplyResultObj: ("Z3_apply_result", "Ptr"),
    z3t.Ast: ("Z3_ast", "Ptr"),
    z3t.AstMapObj: ("Z3_ast_map", "Ptr"),
    z3t.AstVectorObj: ("Z3_ast_vector", "Ptr"),
    z3t.Config: ("Z3_config", "Ptr"),
    z3t.Constructor: ("Z3_constructor", "Ptr"),
    z3t.ConstructorList: ("Z3_constructorList", "Ptr"),
    z3t.ContextObj: ("Z3_context", "Ptr"),
    z3t.FixedpointObj: ("Z3_fixedpoint", "Ptr"),
    z3t.FuncDecl: ("Z3_func_decl", "Ptr"),
    z3t.FuncEntryObj: ("Z3_func_entry", "Ptr"),
    z3t.FuncInterpObj: ("Z3_func_interp", "Ptr"),
    z3t.GoalObj: ("Z3_goal", "Ptr"),
#    z3t.Literals: None,
    z3t.Model: ("Z3_model", "Ptr"),
#    z3t.ModelObj: None,
    z3t.OptimizeObj: ("Z3_optimize", "Ptr"),
    z3t.ParamDescrs: ("Z3_param_descrs", "Ptr"),
    z3t.Params: ("Z3_param", "Ptr"),
    z3t.Pattern: ("Z3_pattern", "Ptr"),
    z3t.ProbeObj: ("Z3_probe", "Ptr"),
    z3t.RCFNumObj: ("Z3_rcf_num", "Ptr"),
    z3t.SolverObj: ("Z3_solver", "Ptr"),
    z3t.Sort: ("Z3_sort", "Ptr"),
    z3t.StatsObj: ("Z3_stats", "Ptr"),
    z3t.Symbol: ("Z3_symbol", "Ptr"),
    z3t.TacticObj: ("Z3_tactic", "Ptr"),
    ctypes.c_int: ("Sint32", "Sint32"),
    ctypes.c_long: ("Sint64", "Sint64"),
    ctypes.c_uint: ("Uint32", "Uint32"),
    ctypes.c_ulong: ("Uint64", "Uint64"),
    ctypes.c_double: ("Double", "Double"),
    ctypes.c_float: ("Float", "Float"),
    ctypes.c_char_p: ("string", "string"),
    ctypes.c_bool: ("Bool", "Uint8"),
    ctypes.POINTER(z3t.Ast): ("Z3_ast_arr", "Ptr"),
    ctypes.POINTER(ctypes.c_char_p): ("string_arr", "Ptr"),
    ctypes.POINTER(ctypes.c_int): ("Sint32Arr", "Ptr"),
    ctypes.POINTER(ctypes.c_long): ("Sint64Arr", "Ptr"),
    ctypes.POINTER(ctypes.c_uint): ("Uint32Arr", "Ptr"),
    ctypes.POINTER(ctypes.c_ulong): ("Uint64Arr", "Ptr"),
    ctypes.POINTER(z3t.Symbol): ("Z3_symbol_arr", "Ptr"),
    ctypes.POINTER(z3t.Sort): ("Z3_sort_arr", "Ptr"),
    ctypes.POINTER(z3t.Constructor): ("Z3_constructor_arr", "Ptr"),
    ctypes.POINTER(z3t.ConstructorList): ("Z3_constructor_list_arr",
                                          "Ptr"),
    ctypes.POINTER(z3t.FuncDecl): ("Z3_func_decl_arr", "Ptr"),
    ctypes.POINTER(z3t.AstVectorObj): ("Z3_ast_vector_arr", "Ptr"),
    ctypes.POINTER(z3t.Model): ("Z3_model_arr", "Ptr"),
    ctypes.POINTER(z3t.Pattern): ("Z3_pattern_arr", "Ptr"),
    ctypes.POINTER(z3t.RCFNumObj): ("Z3_rcf_num_arr", "Ptr"),
    ctypes.POINTER(z3t.TacticObj): ("Z3_tactic_arr", "Ptr"),
}

primitive = ["string"]
wasmMap = {
    "Ptr": "number",
    "CString": "string",
    "Sint8": "number",
    "Uint8": "number",
    "Sint16": "number",
    "Uint16": "number",
    "Sint32": "number",
    "Uint32": "number",
    "Sint64": "number",
    "Uint64": "number",
    "Double": "number",
    "Float": "number",
    "string": "string",
}

voidReturn = [
  "Z3_global_param_set",
  "Z3_global_param_reset_all",
  "Z3_del_config",
  "Z3_set_param_value",
  "Z3_del_context",
  "Z3_inc_ref",
  "Z3_dec_ref",
  "Z3_update_param_value",
  "Z3_interrupt",
  "Z3_params_inc_ref",
  "Z3_params_dec_ref",
  "Z3_params_set_bool",
  "Z3_params_set_uint",
  "Z3_params_set_double",
  "Z3_params_set_symbol",
  "Z3_params_validate",
  "Z3_param_descrs_inc_ref",
  "Z3_param_descrs_dec_ref",
  "Z3_del_constructor",
  "Z3_del_constructor_list",
  "Z3_mk_datatypes",
  "Z3_query_constructor",
  "Z3_model_inc_ref",
  "Z3_model_dec_ref",
  "Z3_func_interp_inc_ref",
  "Z3_func_interp_dec_ref",
  "Z3_func_entry_inc_ref",
  "Z3_func_entry_dec_ref",
  "Z3_append_log",
  "Z3_close_log",
  "Z3_toggle_warning_messages",
  "Z3_set_ast_print_mode",
  "Z3_parse_smtlib_string",
  "Z3_parse_smtlib_file",
  "Z3_set_error",
  "Z3_get_version",
  "Z3_enable_trace",
  "Z3_disable_trace",
  "Z3_reset_memory",
  "Z3_finalize_memory",
  "Z3_goal_inc_ref",
  "Z3_goal_dec_ref",
  "Z3_goal_assert",
  "Z3_goal_reset",
  "Z3_tactic_inc_ref",
  "Z3_tactic_dec_ref",
  "Z3_probe_inc_ref",
  "Z3_probe_dec_ref",
  "Z3_apply_result_inc_ref",
  "Z3_apply_result_dec_ref",
  "Z3_solver_set_params",
  "Z3_solver_inc_ref",
  "Z3_solver_dec_ref",
  "Z3_solver_push",
  "Z3_solver_pop",
  "Z3_solver_reset",
  "Z3_solver_assert",
  "Z3_solver_assert_and_track",
  "Z3_stats_inc_ref",
  "Z3_stats_dec_ref",
  "Z3_ast_vector_inc_ref",
  "Z3_ast_vector_dec_ref",
  "Z3_ast_vector_set",
  "Z3_ast_vector_resize",
  "Z3_ast_vector_push",
  "Z3_ast_map_inc_ref",
  "Z3_ast_map_dec_ref",
  "Z3_ast_map_insert",
  "Z3_ast_map_erase",
  "Z3_ast_map_reset",
  "Z3_rcf_del",
  "Z3_rcf_get_numerator_denominator",
  "Z3_fixedpoint_inc_ref",
  "Z3_fixedpoint_dec_ref",
  "Z3_fixedpoint_add_rule",
  "Z3_fixedpoint_add_fact",
  "Z3_fixedpoint_assert",
  "Z3_fixedpoint_update_rule",
  "Z3_fixedpoint_add_cover",
  "Z3_fixedpoint_register_relation",
  "Z3_fixedpoint_set_predicate_representation",
  "Z3_fixedpoint_set_params",
  "Z3_fixedpoint_push",
  "Z3_fixedpoint_pop",
  "Z3_optimize_inc_ref",
  "Z3_optimize_dec_ref",
  "Z3_optimize_assert",
  "Z3_optimize_push",
  "Z3_optimize_pop",
  "Z3_optimize_set_params",
  "Z3_optimize_from_string",
  "Z3_optimize_from_file",
  "Z3_write_interpolation_problem",
]

l = lib()
# Imports
print \
"""
import {Uint8, Ptr, Void, Uint32, Sint32, Float, Double, Uint64, Sint64} from './ctypes'
import {WasmJSInstance} from "wasmInstance"
"""

# Types
print "export class Z3_lbool extends Uint8 {};"
for t, (ts_name, ts_type) in mapping.items():
    if (ts_name == ts_type):
        continue;
    print "export class {} extends {} {{ }};".format(ts_name, ts_type)

print \
"""
export class LibZ3 {
  constructor(private wasmInstance: WasmJSInstance) { }

"""


for funcName in dir(l):
    t = getattr(l, funcName)

    if not isinstance(t, l._FuncPtr):
        continue

    resT = t.restype
    argsT = t.argtypes

    if argsT is None:
        print funcName, resT, argsT
        continue

    assert resT in mapping,\
        "Missing result type {} for {}".format(resT, funcName)

    if funcName not in voidReturn:
        tsResT = mapping[resT][0]
        wasmResT = wasmMap[mapping[resT][1]]
    else:
        tsResT = "void"
        wasmResT = "number"

    wasmArgsT = []
    tsArgsT = []
    tsArgUse = []

    for i, t in enumerate(argsT):
        assert t in mapping,\
            "Missing {}-th argument type {} for {}".format(i, t, funcName)
        argT = mapping[t][0]
        tsArgsT.append(argT)
        wasmArgsT.append(wasmMap[mapping[t][1]])
        tsArgUse.append("arg{}".format(i) if argT in primitive else "arg{}.val()".format(i))

    funcArgs = ", ".join(["arg{}: {}".format(i, t)
                          for (i, t) in enumerate(tsArgsT)])
    funcSignature = "    {}({}): {} {{\n".format(funcName, funcArgs, tsResT)

    innerCall = "this.wasmInstance.ccall('{}', '{}', {}, {})".format(
            funcName,
            wasmResT,
            "[" + ", ".join("'" + argT + "'" for argT in wasmArgsT) + "]",
            "[" + ", ".join(tsArgUse) + "]"
    )

    if (tsResT not in primitive and tsResT != "void"):
        innerCall = "new {}({})".format(tsResT, innerCall)

    if (tsResT != "void"):
        funcBody = "        return {}\n".format(innerCall) + "    }\n"
    else:
        funcBody = "        {}\n".format(innerCall) + "    }\n"

    print funcSignature + funcBody

print "}"
