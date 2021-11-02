MATCH
(permission:Permission{role: $role}),
(user:User{userId: $userId})
MERGE (permission)<-[permission_grant:PRIVILEGED_OF]-(user)
ON CREATE
SET
permission_grant.creationDate = datetime.transaction()
RETURN user, permission_grant, permission;