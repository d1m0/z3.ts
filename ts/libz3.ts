type voidp = number;
type Z3_config = voidp;
type Z3_context = voidp;
type Z3_solver = voidp;
type Z3_sort = voidp;
type Z3_ast = voidp;
type Z3_symbol = voidp;
type Z3_lbool = number;

interface WasmJSInstance extends WebAssembly.Instance {
  ccall(fname: string, returnType: string, argTypes: string[], args: any[]): any;
}

class LibZ3 {
  constructor(private wasmInstance: WasmJSInstance) { }

  Z3_mk_config(): Z3_config {
    return this.wasmInstance.ccall('Z3_mk_config', 'number', [], [])
  }

  Z3_mk_context(config: Z3_config): Z3_context {
    return this.wasmInstance.ccall('Z3_mk_context', 'number', ['number'], [config])
  }

  Z3_mk_solver(context: Z3_context): Z3_solver {
    return this.wasmInstance.ccall('Z3_mk_solver', 'number', ['number'], [context])
  }

  Z3_mk_int_sort(context: Z3_context): Z3_sort {
    return this.wasmInstance.ccall('Z3_mk_int_sort', 'number', ['number'], [context])
  }

  Z3_mk_int_symbol(context: Z3_context, idx: number): Z3_symbol {
    return this.wasmInstance.ccall('Z3_mk_int_symbol', 'number', ['number', 'number'], [context, idx])
  }

  Z3_mk_const(context: Z3_context, symbol: Z3_symbol, sort: Z3_sort): Z3_symbol {
    return this.wasmInstance.ccall('Z3_mk_const', 'number', ['number', 'number', 'number'],
                                   [context, symbol, sort])
  }


  Z3_mk_eq(context: Z3_context, lhs: Z3_ast, rhs: Z3_ast): Z3_ast {
    return this.wasmInstance.ccall('Z3_mk_eq', 'number', ['number', 'number', 'number'],
                                   [context, lhs, rhs])
  }

  Z3_mk_not(context: Z3_context, exp: Z3_ast): Z3_ast {
    return this.wasmInstance.ccall('Z3_mk_not', 'number', ['number', 'number'],
                                   [context, exp])
  }

  Z3_solver_assert(context: Z3_context, solver: Z3_solver, predicate: Z3_ast): void {
    return this.wasmInstance.ccall('Z3_solver_assert', null, ['number', 'number', 'number'],
                                   [context, solver, predicate])
  }

  Z3_solver_check(context: Z3_context, solver: Z3_solver): Z3_lbool {
    return this.wasmInstance.ccall('Z3_solver_check', 'number', ['number', 'number'],
                                   [context, solver])
  }
}
