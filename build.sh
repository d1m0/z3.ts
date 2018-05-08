#! /usr/bin/env bash

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

check_has "tsc" "Please install typescript"
check_has "emconfigure" "Please install and activate Emscripten (run emsdk_env.sh)"
check_has "em++" "Please install and activate Emscripten (run emsdk_env.sh)"
check_has "emcc" "Please install and activate Emscripten (run emsdk_env.sh)"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
Z3_BUILD_OUT=$DIR/z3/build/
BUILD_OUT=$DIR/build/
TSC_BUILD_OUT=$DIR/build/ts/

if [ ! -d $Z3_BUILD_OUT ] ; then
  echo "Error: Z3 build directory $Z3_BUILD_OUT doesn't exist. Did you forget to run setup.sh?"
  exit -1
fi

if [ ! -d $TSC_BUILD_OUT ] ; then
  echo "Error: TypeScript build directory $TSC_BUILD_OUT doesn't exist. Did you forget to run setup.sh?"
  exit -1
fi


pushd $Z3_BUILD_OUT
echo "Building z3..."
make -j 8
popd

echo "Moving WASM libz3.so from $Z3_BUILD_OUT to $BUILD_OUT"
cp $Z3_BUILD_OUT/libz3.so.wasm $BUILD_OUT
cp $Z3_BUILD_OUT/libz3.so.js $BUILD_OUT

echo "Building typescript..."
tsc

echo "Fetching require.js..."
if [ ! -e $BUILD_OUT/require.js ] ; then
  wget http://requirejs.org/docs/release/2.3.5/comments/require.js -O $BUILD_OUT/require.js
fi

echo "Building test.html."
tests=`find $TSC_BUILD_OUT/tests -name '*.js'`
TAGS=""
TEST_PATH_MAPS=""
TEST_FILES=""
for file in $tests; do
  FILE_NAME=`basename $file .js`
  TEST_PATH="ts/tests/"`basename $file .js`
  TEST_PATH_MAPS+="\"$FILE_NAME\": \"$TEST_PATH\","
  TEST_FILES+="\"$FILE_NAME\","
done
cpp -P -DTEST_PATHS_MAP="$TEST_PATH_MAPS" -DTEST_FILES="$TEST_FILES" $DIR/templates/loader.js.template > $BUILD_OUT/loader.js
cpp -P -DTEST_PATHS_MAP="$TEST_PATH_MAPS" -DTEST_FILES="$TEST_FILES" $DIR/templates/test.html.template > $BUILD_OUT/test.html
