from neo4j import GraphDatabase as gd

def connect(URL:str, auth:tuple):
    gdb = gd.driver(URL, auth=auth)
    gdb.verify_connectivity()

def query_neo4j(gdb:gd.driver, query:str)->str:
    if not gdb: gdb = connect()

    try:
        records, summary, keys = gdb.execute_query(query)
        return repr(records)
    except Exception as e:
        return repr(e)