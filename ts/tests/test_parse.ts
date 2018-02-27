registerTest("parse", function test(wasmInstance: WasmJSInstance) {
  var lib: LibZ3 = new LibZ3(wasmInstance)
  var config: Z3_config = lib.Z3_mk_config()
  console.log("config: ", config)
  var context: Z3_context = lib.Z3_mk_context(config)
  console.log("context: ", context)
  var ast = lib.Z3_parse_smtlib2_string(context, "(declare-fun x () Int)", 0, 0, 0, 0, 0, 0)
  console.log("ast: ", ast)
})
