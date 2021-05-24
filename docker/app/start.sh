# Wait for DB boot
while ! mysqladmin ping -h"$DATABASE_HOST" --silent; do
    sleep 1
done

FIRST_RUN_FILE="/context/first_run"

pushd /app || exit 1
if [ ! -f "$FIRST_RUN_FILE" ]; then
    echo "[FIRST RUN] Creating users..."
    cp ./create_user.txt /tmp/
    sed -i "s/@'localhost'//g" /tmp/create_user.txt
    echo "flush privileges;" | cat - /tmp/create_user.txt | mysql -h "$DATABASE_HOST" -u root -pyolo || exit 1
fi
pushd pyflask || exit 1
if [ ! -f "$FIRST_RUN_FILE" ]; then
    echo "[FIRST RUN] Initing DB..."
    python3 init.py || exit 1
    touch "$FIRST_RUN_FILE"
fi
flask run --host=0.0.0.0

