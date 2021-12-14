from neo4j.time import DateTime
from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class repositoryResources:
    def __init__(self, driver):
        self.driver = driver

    def list_course_repository(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "id": record["edges"].id,
                        "type": record["edges"].type,
                        "start": record["edges"].start_node.id,
                        "end": record["edges"].end_node.id,
                        "property": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["edges"].items()
                        },
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)