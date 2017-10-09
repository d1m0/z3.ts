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

MY_CFLAGS='-s WASM=1 -s ASSERTIONS=1 -s DISABLE_EXCEPTION_CATCHING=0 -s NO_EXIT_RUNTIME=1 -s ALLOW_MEMORY_GROWTH=1 -O2'

# 3. Configure z3 build
pushd $DIR/z3

export CFLAGS+=$MY_CFLAGS
export CXXFLAGS+=$MY_CFLAGS
export LDFLAGS+=$MY_CFLAGS
emconfigure ./configure  --build=build/
rm -f a.out.js a.out.wasm
popd

# 4. Final tweaks in z3's config.mk - add EXPORTED_FUNCTIONS to SLINK_FLAGS,
# change .SO extension, etc.
pushd $Z3_BUILD_OUT
sed -i "1 i\Z3_API_FUNCS=$Z3_API_FUNCS" config.mk
sed -i "s/SO_EXT=.so/SO_EXT=.so.js/" config.mk
sed -i "s/EXE_EXT=/EXE_EXT=.js/" config.mk
sed -i "s/LINK_FLAGS=.*/LINK_FLAGS=-s WASM=1 -O3/" config.mk
sed -i "s/SLINK_FLAGS=.*/SLINK_FLAGS=-shared -s WASM=1 -s EXPORTED_FUNCTIONS=\$(Z3_API_FUNCS) -O2 -s ASSERTIONS=1 -s DISABLE_EXCEPTION_CATCHING=0/" config.mk
popd

mkdir -p $TSC_BUILD_OUT

# 5. Install any nodejs dependencies (e.g. webassembly @typings)
npm install
