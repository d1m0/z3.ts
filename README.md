# README #

### What is this repository for? ###

TypeScript bindings around a WebAssembly-compiled Z3, mimicking the [Z3 C Api](https://z3prover.github.io/api/html/group__capi.html).

### How do I get set up? ###

* Prerequisites:	[emscripten](https://github.com/kripken/emscripten), [nodejs](https://nodejs.org/en/), [TypeScript](https://www.typescriptlang.org/)
* Clone Repo. Don't forget to add --recursive to get z3 as a submodule.
```
git clone --recursive git@bitbucket.org:dbounov/z3.ts.git
```
* Assuming the repo root directory is $REPO, run `$REPO/setup.sh`. This script will
    * Configure the z3 build to use Emscripten
    * Install any nodejs dependencies (e.g. WebAssembly TS typings)
* Run `$REPO/build.sh`. The build script:
    * Builds libz3.so.js, libz3.so.wasm
    * Moves the libz3.so.* files under $REPO/build/
    * Build typescript files
    * Build a $REPO/build/test.html that includes all the compiled tests from ts/tests/*.ts
* How to run tests
    * Start a simple webserver under build/. E.g. `cd $REPO/build; emrun --no_browser --port 8080 .`
    * Open the tests.html in the browser - `http://localhost:8080/tests.html` and look for output in the console.