#! /usr/bin/env bash

# 1. make sure we have the required tools
function check_has {
  NAME=$1
  MSG=$2
  P=$(command -v $NAME)
  if [ $? -ne 0 ] ; then
    echo "Cannot find executable $NAME. $MSG";
    exit -1;
  fi

  if [ ! -x $P ] ; then
    echo "Cannot find executable $NAME. $MSG";
    exit -1;
  fi
}

check_has "node" "Please install nodejs"
check_has "tsc" "Please install typescript"
check_has "emconfigure" "Please install and activate Emscripten (run emsdk_env.sh)"
check_has "em++" "Please install and activate Emscripten (run emsdk_env.sh)"
check_has "emcc" "Please install and activate Emscripten (run emsdk_env.sh)"

# 2. Some global variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
Z3_BUILD_OUT=$DIR/z3/build/
TSC_BUILD_OUT=$DIR/build/ts/
source "$DIR/api_entries.sh"
WASM_MEM=33554432  # 32MB

MY_CFLAGS='-s WASM=1 -s DISABLE_EXCEPTION_CATCHING=0 -s NO_EXIT_RUNTIME=1 -s ALLOW_MEMORY_GROWTH=1 -O2 -g4 -s DEMANGLE_SUPPORT=1'

# 3. Configure z3 build
pushd $DIR/z3

function get_emconfig_var {
  VAR=$1
  raw=`emconfigure env 2>/dev/null | grep "^ *$VAR="`
  VAL=`echo $raw | sed "s/^ *$VAR=//"`
  echo $VAL
}

# emconfigure recently changed their CC,CXX,AR.. variables from something like
# '<emsdk_root>/emcc' to 'python <emsdk_root>/emcc.py'.  Unfortunately this
# break z3's mk_make.py, which looks for AR using 'which' instead of running
# it. Obviously 'which python ..../emar.py' throws an error. To hack around this,
# we are setting all our own variables here instead of using emconfigure
export CC=`which emcc`
export CXX=`which em++`
export AR=`which emar`
export LD=`which emcc`
export NM=`get_emconfig_var NM`
export LDSHARED=`which emcc`
export RANLIB=`get_emconfig_var RANLIB`
export EMMAKEN_COMPILER=`get_emconfig_var EMMAKEN_COMPILER`
export EMSCRIPTEN_TOOLS=`get_emconfig_var EMSCRIPTEN_TOOLS`
export CFLAGS=`get_emconfig_var CFLAGS`
export HOST_CC=`get_emconfig_var HOST_CC`
export HOST_CXX=`get_emconfig_var HOST_CXX`
export HOST_CFLAGS=`get_emconfig_var HOST_CFLAGS`
export HOST_CXXFLAGS=`get_emconfig_var HOST_CXXFLAGS`
export PKG_CONFIG_LIBDIR=`get_emconfig_var PKG_CONFIG_LIBDIR`
export PKG_CONFIG_PATH=`get_emconfig_var PKG_CONFIG_PATH`
export EMSCRIPTEN=`get_emconfig_var EMSCRIPTEN`
export PATHS=`get_emconfig_var PATHS`
export CROSS_COMPILES=`get_emconfig_var CROSS_COMPILES`

export CFLAGS+=$MY_CFLAGS
export CXXFLAGS+=$MY_CFLAGS
export LDFLAGS+=$MY_CFLAGS
python ./scripts/mk_make.py --build=build/ -d --x86
rm -f a.out.js a.out.wasm
popd

EXTRA_FUNCS="'["
EXTRA_FUNCS+="\"ccall\","
EXTRA_FUNCS+="\"cwrap\""
EXTRA_FUNCS+="]'"

# 4. Final tweaks in z3's config.mk - add EXPORTED_FUNCTIONS to SLINK_FLAGS,
# change .SO extension, etc.
pushd $Z3_BUILD_OUT
sed -i "1 i\EXTRA_FUNCS=$EXTRA_FUNCS" config.mk
sed -i "1 i\Z3_API_FUNCS=$Z3_API_FUNCS" config.mk
sed -i "s/SO_EXT=.so/SO_EXT=.so.js/" config.mk
sed -i "s/EXE_EXT=/EXE_EXT=.js/" config.mk
sed -i "s/LINK_FLAGS=.*/LINK_FLAGS=-s WASM=1 -O0 --emrun /" config.mk
sed -i "s/SLINK_FLAGS=.*/SLINK_FLAGS=-shared -s EXPORTED_FUNCTIONS=\$(Z3_API_FUNCS) -s EXTRA_EXPORTED_RUNTIME_METHODS=\$(EXTRA_FUNCS) --emrun $MY_CFLAGS/" config.mk
#sed -i "s/LINK_FLAGS=.*/LINK_FLAGS=-s WASM=1 -O2 --emrun/" config.mk
#sed -i "s/SLINK_FLAGS=.*/SLINK_FLAGS=-shared -s WASM=1 -s EXPORTED_FUNCTIONS=\$(Z3_API_FUNCS) -O2 -s DISABLE_EXCEPTION_CATCHING=0 --emrun/" config.mk
popd

mkdir -p $TSC_BUILD_OUT

# 5. Install any nodejs dependencies (e.g. webassembly @typings)
npm install
