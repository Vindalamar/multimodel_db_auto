
from datetime import timedelta

# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

# Update this to your cluster
username = "-"
password = "-"
bucket_name = "-"
# User Input ends here.

# Connect options - authentication
auth = PasswordAuthenticator(
    username,
    password,
)

# Get a reference to our cluster
# NOTE: For TLS/SSL connection use 'couchbases://<your-ip-address>' instead
cluster = Cluster('couchbase://localhost', ClusterOptions(auth))

# Wait until the cluster is ready for use.
cluster.wait_until_ready(timedelta(seconds=5))

# get a reference to our bucket
cb = cluster.bucket(bucket_name)

cb_chime = cb.scope("chime").collection("ch")
cb_auto = cb.scope("autos").collection("a_1")

# Get a reference to the default collection, required for older Couchbase server versions
cb_coll_default = cb.default_collection()


def upsert_document(doc, coll):
    print("\nUpsert CAS: ")
    try:
        # key will equal: "airline_8091"
        key = doc["company"] + '_' + doc["name"]
        result = coll.upsert(key, doc)
        return result.cas
    except Exception as e:
        return e

# get document function


def get_airline_by_key(key, coll):
    print("\nGet Result: ")
    try:
        result = coll.get(key)
        return result.content_as[str]
    except Exception as e:
        return e


def remove_doc(key, coll):
    print("\nremove Result: ")
    try:
        result = coll.remove(key)
        return result.cas
    except Exception as e:
        return e

# query for new document by callsign

# def lookup_by_callsign(cs):
#     print("\nLookup Result: ")
#     try:
#         inventory_scope = cb.scope('inventory')
#         sql_query = 'SELECT VALUE name FROM airline WHERE callsign = $1'
#         row_iter = inventory_scope.query(
#             sql_query,
#             QueryOptions(positional_parameters=[cs]))
#         for row in row_iter:
#             print(row)
#     except Exception as e:
#         print(e)


auto = {
    "id": 1,
    "name": "",
    "company": "",
    "description": ""
    }

# upsert_document(auto)

# get_airline_by_key("airline_8093")
#
# lookup_by_callsign("CBsS")
