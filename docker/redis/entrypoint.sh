#!/bin/bash
set -e

CONFIG_FILE="${REDIS_CONFIG_FILE:-/etc/redis/redis.conf}"
CONFIG_DIR="$(dirname ${CONFIG_FILE})"
[[ ! -d "${CONFIG_DIR}" ]] && mkdir -p "${CONFIG_DIR}"

# if the config file exists and a password is set, remove auth-related commands
if [[ -f "${CONFIG_FILE}" && -n "${REDIS_PASSWORD}" ]]; then
    chmod 0600 "${CONFIG_FILE}"
    sed -e '/^\s\?user\W/d' -e '/^\s\?requirepass\W/d' -i "${CONFIG_FILE}"
fi

# if credentials have been supplied, add them to the redis config
if [[ -n "${REDIS_USER}" && -n "${REDIS_PASSWORD}" ]]; then
    echo "Running with username and password"
    echo "user default off" >> ${CONFIG_FILE}
    echo "user ${REDIS_USER} on allcommands allkeys >${REDIS_PASSWORD}" >> "${CONFIG_FILE}"

elif [[ -n "${REDIS_PASSWORD}" ]]; then
    echo "Running with password only"
    echo "requirepass ${REDIS_PASSWORD}" >> "${CONFIG_FILE}"

else
    echo "Running without credentials"
fi

# start the redis server with the config file if it exists
if [[ -f ${CONFIG_FILE} ]]; then
    chmod 0400 "${CONFIG_FILE}"
    redis-server "${CONFIG_FILE}" $@
else
    redis-server $@
fi
