import json
from prefect import flow
from neo4j import GraphDatabase
from prefect_aws.secrets_manager import AwsSecret


@flow(name="try-put", log_prints=True)
def try_put(
        commit: str = 'test',
) -> None:

    mdb_creds  = AwsSecret.load("mdb-cloud-one-neo4j-creds")
    mdb_creds = json.loads(mdb_creds.read_secret())
    
    drv = GraphDatabase.driver(mdb_creds['neo4j_bolt_uri'],
                               auth=(mdb_creds['neo4j_user'],
                                     mdb_creds['neo4j_pass']))
    drv.verify_connectivity()
    drv.execute_query(
        'CREATE (n:TEST {_commit: $commit}) RETURN n',
        database_='neo4j',
        commit=commit
    )
