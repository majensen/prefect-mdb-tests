import json
import os
from prefect import flow
from neo4j import GraphDatabase
from prefect_aws.secrets_manager import AwsSecret


@flow(name="try-put", log_prints=True)
def try_put(
        commit: str = 'test',
) -> None:

    print(os.getcwd())
    
    mdb_creds  = AwsSecret.load("mdb-cloud-one-neo4j-creds")
    mdb_creds = json.loads(mdb_creds.read_secret())
    
    drv = GraphDatabase.driver(mdb_creds['neo4j_bolt_uri'],
                               auth=(mdb_creds['neo4j_user'],
                                     mdb_creds['neo4j_pass']))
    drv.verify_connectivity()
    recs, summ, keys = drv.execute_query(
        'CREATE (n:TEST {_commit: $commit}) RETURN n',
        database_='neo4j',
        commit=commit
    )
    print([x for x in recs], summ, [x for x in keys])

@flow(name="try-get", log_prints=True)
def try_get() -> None:

    print(os.getcwd())
    
    mdb_creds  = AwsSecret.load("mdb-cloud-one-neo4j-creds")
    mdb_creds = json.loads(mdb_creds.read_secret())
    
    drv = GraphDatabase.driver(mdb_creds['neo4j_bolt_uri'],
                               auth=(mdb_creds['neo4j_user'],
                                     mdb_creds['neo4j_pass']))
    drv.verify_connectivity()
    result = drv.execute_query(
        'MATCH (n:TEST) RETURN n',
        database_='neo4j',
    )
    print( [x for x in result] )
