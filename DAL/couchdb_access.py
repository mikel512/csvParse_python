from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator


class CouchDbAccess:
    def __init__(self):
        # using a local server
        self.cluster = Cluster('couchbase://localhost:8091', ClusterOptions(
            PasswordAuthenticator('Administrator', 'password1234')
        ))

    def upsert_doc(self, doc, doc_id, bucket_name):
        print("Upsert document: ")
        cb = self.cluster.bucket(bucket_name)
        coll = cb.default_collection()
        try:
            result = coll.insert(doc_id, doc)
            print(result.cas)
        except Exception as e:
            print(e)