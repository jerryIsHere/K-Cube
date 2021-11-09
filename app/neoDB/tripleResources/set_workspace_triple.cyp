MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH DISTINCT workspace
MATCH (approved_graph_relationship:GraphRelationship{name: $r_name})<-[:USER_APPROVE]-(:User)
WITH DISTINCT approved_graph_relationship, workspace
MERGE (h:GraphConcept{name: $h_name})
MERGE (t:GraphConcept{name: $t_name})
MERGE (h) -[r:DELTA_GRAPH_RELATIONSHIP{name: approved_graph_relationship.name, deltaGraphId: workspace.deltaGraphId}]-> (t)
SET
    workspace.lastModified = datetime.transaction(),
    r.creationDate = datetime.transaction(),
    r.value = $r_value
RETURN h.name, r.name, t.name, r.value;