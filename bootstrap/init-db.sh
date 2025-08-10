#!/bin/bash
set -e

create_db_if_not_exists() {
    local db_name=$1
    if ! psql -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        createdb "$db_name"
    fi
}

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    $(create_db_if_not_exists "$POSTGRES_DB")
    $(create_db_if_not_exists "$POSTGRES_DB_TEST")
EOSQL
