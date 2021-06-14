function docker-restore-volume {
    VOL="$1"
    if [ -z "$VOL" ]; then
        echo "Usage: <volume> <filename.tar.gz>"
        return 1
    fi
    FILENAME="$2"
    if [ -z "$FILENAME" ]; then
        echo "Must supply filename."
        return 1
    fi
    docker inspect "$VOL"  >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Error: Volume '$VOL' already exists!"
    fi
    docker run --rm -v "$VOL:/vol" -v "$(dirname "$(realpath "$FILENAME")"):/pwd" busybox tar -xzvf "/pwd/$(basename "$FILENAME")"
}

docker-compose down

docker-restore-volume cs348_movielist_app_context context.tar.gz
docker-restore-volume cs348_movielist_database database.tar.gz
