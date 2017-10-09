registerTest("parse", function test(wasmInstance: WasmJSInstance) {
  var lib: LibZ3 = new LibZ3(wasmInstance)
  var config: Z3_config = lib.Z3_mk_config()
  console.log("config: ", config)
  var context: Z3_context = lib.Z3_mk_context(config)
  console.log("context: ", context)
  //var ast = lib.Z3_parse_smtlib2_string(context, "(declare-fun x () Int)", 0, 0, 0, 0, 0, 0)
  //var ast = lib.Z3_parse_smtlib2_string(context, "", 0, 0, 0, 0, 0, 0)
  var stack = wasmInstance.stackSave()
  var a1 = wasmInstance.stackAlloc(128);
  var a2 = wasmInstance.stackAlloc(128);
  var b1 = wasmInstance.stackAlloc(128);
  var b2 = wasmInstance.stackAlloc(128);
  var ast = lib.Z3_parse_smtlib2_string(context, "", 0, a1, a2, 0, b1, b2)
  wasmInstance.stackRestore(stack)
  console.log("ast: ", ast)
})
