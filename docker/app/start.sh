# Wait for DB boot
while ! mysqladmin ping -h"$DATABASE_HOST" --silent; do
    sleep 1
done

FIRST_RUN_FILE="/context/first_run"

INITIAL_MYSQL_PASSWORD="yolo"
MYSQL_DATABASE="MovieList"

exec_sql() {
    mysql -h "$DATABASE_HOST" -u root "-p$INITIAL_MYSQL_PASSWORD"
}

exec_sql_in_db() {
    mysql -h "$DATABASE_HOST" -u root "-p$INITIAL_MYSQL_PASSWORD" "$MYSQL_DATABASE"
}

pushd /app || exit 1
if [ ! -f "$FIRST_RUN_FILE" ]; then
    echo "[FIRST RUN] Creating users..."
    USER_CREATION_SCRIPT="$(sed "s/@'localhost'//g" create_user.txt)"
    echo "flush privileges;$USER_CREATION_SCRIPT" | exec_sql || exit 1
fi
pushd pyflask || exit 1
if [ ! -f "$FIRST_RUN_FILE" ]; then
    echo "[FIRST RUN] Initing DB..."
    python3 init.py || exit 1
    touch "$FIRST_RUN_FILE"
fi
flask run --host=0.0.0.0

