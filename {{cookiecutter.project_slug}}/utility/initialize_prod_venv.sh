
UTIL_DIR=$(dirname "$(realpath "$0")")
ROOT_DIR=$(dirname "$(dirname "$(realpath "$0")")")
VENV=$ROOT_DIR/.prod_venv
virtualenv $VENV
echo "Created virtual env at path ${VENV}"
cp $UTIL_DIR/activate $VENV/bin/.
cp $UTIL_DIR/postactivate $VENV/bin/.
cp $UTIL_DIR/predeactivate $VENV/bin/.

sed -i 's/local/production/g' $VENV/bin/postactivate
sed -i 's/local/production/g' $VENV/bin/predeactivate