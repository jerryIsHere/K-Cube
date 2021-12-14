MATCH
    (branch:Branch),
    (user:User{userId: $userId}),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WITH 
    branch,
    user,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
    EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})) as isTeaching,
    EXISTS((branch)<-[:USER_OWN]-(user)) as isOwner,
    EXISTS((:GraphConcept{name: $courseCode})-[:COURSE_DESCRIBE]-()<-[:BRANCH_DESCRIBE]-(branch)) as isExposed
WHERE
    split(branch.deltaGraphId,'.')[0] = toString(id(course)) AND (
        (branch.visibility = 4) OR
        (branch.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (branch.visibility = 2 AND isInstructor) OR
        (branch.visibility = 1 AND isTeaching) OR
        isOwner
    )
RETURN DISTINCT branch AS nodes, isOwner, isExposed
