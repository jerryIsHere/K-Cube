from neo4j import GraphDatabase

# https://stackoverflow.com/questions/6307761/how-to-decorate-all-functions-of-a-class-without-typing-it-over-and-over-for-eac
# example:
# @for_all_methods(sanitize_args_and_kwargs)
# class userResources:
def for_all_methods(decorator):
    def wrapper(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return wrapper


# the actual sanitize logic's implementation
def sanitize(value):

    return value


def sanitize_args_and_kwargs(function):
    def wrapper(*args, **kwargs):
        for each in args:
            each = sanitize(each)
        for key in kwargs:
            kwargs[key] = sanitize(kwargs[key])
        return function(*args, **kwargs)

    return wrapper


from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class APIDriver():
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        queries = """CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT draft_uid_constraint IF NOT EXISTS ON (n:Draft) ASSERT n.draftId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.displayName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;""".split(
            "\n"
        )
        queries.extend(
            [
                """MERGE (:Permission {
    role: "admin",
    canCreateGraphConcept: true,
    canCreateCourse: true,
    canCreateJob: true,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveRelationship: true,
    canOperateDraftForOthers: true,
    canUploadPhoto: true,
    canOwnDraft: true
});""",
                """MERGE (:Permission {
    role: "teacher",
    canCreateGraphConcept: true,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveRelationship: false,
    canOperateDraftForOthers: false,
    canUploadPhoto: false,
    canOwnDraft: true
});""",
                """MERGE (:Permission {
    role: "restricted",
    canCreateGraphConcept: false,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: false,
    canProposeRelationship: false,
    canApproveRelationship: false,
    canOperateDraftForOthers: false,
    canUploadPhoto: false,
    canOwnDraft: false
});""",
            ]
        )
        for query in queries:

            def _query(tx):

                result = tx.run(query)
                try:
                    return [record for record in result]
                except ServiceUnavailable as exception:
                    raise exception

            with self.driver.session() as session:
                session.write_transaction(_query)
            from .userResources import userResources
            self.user = userResources(driver=self.driver)
            from .courseResources import courseResources
            self.course = courseResources(driver=self.driver)

    def close(self):
        self.driver.close()
