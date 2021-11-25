MATCH (branch:Branch{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH branch
MATCH(course:Course)-[:COURSE_DESCRIBE]->(courseConcept:GraphConcept{name: split(branch.deltaGraphId,'.')[0]})
WITH branch, course
CALL{
    WITH branch, course
    MATCH (course)<-[wasExposed:BRANCH_DESCRIBE{userId: $userId}]-(:Branch)
    DELETE wasExposed
    RETURN null
UNION
    RETURN null
}
MERGE (course)<-[:BRANCH_DESCRIBE{userId: $userId}]-(branch)
RETURN branch