MYHOST=`hostname -f`

MYSQL=`which mysql`

if [ "$1" == "-d" ]; then
        IS_DEBUG="true"
fi;

if [ "${MYHOST}" == "dbh24.mlan" ]; then
        SLAVE_HOST="dbh41.ulan"
else
        SLAVE_HOST="dbh24.mlan"
fi;

[[ -n "${IS_DEBUG}" ]] && echo -e "\nMaster host: ${MYHOST}\nSlave host: ${SLAVE_HOST}"

QUERY="SELECT UNIX_TIMESTAMP(ts) FROM MonitoringReplication.Replication WHERE hostname = '${MYHOST}';"

MASTER_TS=`${MYSQL} -s -h${MYHOST} -u${MYUSER} -p${MYPASSWD} -e "${QUERY}"`

SLAVE_TS=`${MYSQL} -s -h${SLAVE_HOST} -u${MYUSER} -p${MYPASSWD} -e "${QUERY}"`

DIFF=$((${MASTER_TS}-${SLAVE_TS}))

[[ -n "${IS_DEBUG}" ]] && echo -e "Query: ${QUERY}\n\nMaster TS: ${MASTER_TS} (`date -d@${MASTER_TS}`)\nSlave TS: ${SLAVE_TS} (`date -d@${SLAVE_TS}`)\n\nLag:"

echo $DIFF

