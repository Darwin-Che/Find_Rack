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

if [ ! -f "$FIRST_RUN_FILE" ]; then
    echo "[FIRST RUN] Preparing to load dataset..."
    rm -rf /context/test
    cp -rv /app/test /context/

    if [ "$USE_REAL_DATA" == "true" ]; then
        echo "[FIRST RUN] Fetching dataset..."
        pushd /context/test/datapath || exit 1
        wget "https://datasets.imdbws.com/name.basics.tsv.gz" || exit 1
        wget "https://datasets.imdbws.com/title.basics.tsv.gz" || exit 1
        wget "https://datasets.imdbws.com/title.crew.tsv.gz" || exit 1
        wget "https://datasets.imdbws.com/title.principals.tsv.gz" || exit 1
        echo "[FIRST RUN] Extracting dataset..."
        gunzip *.tsv.gz
        echo "[FIRST RUN] Transforming dataset..."
        echo "[FIRST RUN]   Transforming cast information..."
        python3 /app/transformation_scripts/cast_table.py || exit 1
        echo "[FIRST RUN]   Transforming movie information..."
        python3 /app/transformation_scripts/movie_tables.py || exit 1
        mv cast.scsv cast_movie.scsv || exit 1
        mv name.scsv casts.scsv || exit 1
        mv movie_genre.scsv genre_movie.scsv || exit 1
        rm *.tsv
        popd
    else
        echo "[FIRST RUN] Currently configured to use test data, set USE_REAL_DATA=true to load real IMDB data (very slow)..."
    fi

    echo "[FIRST RUN] Creating DB users..."
    USER_CREATION_SCRIPT="$(sed "s/@'localhost'//g" /app/create_user.txt)"
    echo "flush privileges;$USER_CREATION_SCRIPT" | exec_sql || exit 1

    echo "[FIRST RUN] Initing DB..."
    pushd /context || exit 1
    python3 /app/pyflask/init.py || exit 1
    popd
    rm -rf /context/test/datapath
    touch "$FIRST_RUN_FILE"
fi
pushd /app/pyflask || exit 1
flask run --host=0.0.0.0

