package edu.nd.crc.safa.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.Neo4J;
import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.responses.ServerError;

import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.Session;
import org.neo4j.driver.Values;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class VersionService {

    Neo4J neo4J;
    TreeService treeService;
    Puller mPuller;

    @Autowired
    public VersionService(Neo4J neo4J, TreeService treeService, Puller mPuller) {
        this.neo4J = neo4J;
        this.treeService = treeService;
        this.mPuller = mPuller;
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> versions(Project project, String root, int version, String rootType)
        throws ServerError {
        Session session = neo4J.createSession();
        String query = "MATCH (p)-[r:UPDATES]->(c)\n"
            + "WHERE r.version <= $version\n"
            + "WITH p, c, r AS rs ORDER BY r.version DESC\n"
            + "WITH p, c, head(collect([p, rs, c])) AS removed\n"
            + "WITH [c in collect(removed) WHERE c[1].type='REMOVE' | [c[0],c[2]]] as excluded\n"
            // Find all removed relationships
            + "WITH [e in excluded | e[0]] AS eHead, [e in excluded | e[1]] AS eTail, apoc.coll.toSet(apoc.coll"
            + ".flatten([e in excluded WHERE e[0].id=e[1].id| e[0]])) AS eNo\n"
            + "OPTIONAL MATCH (a)-[eR]-(b)\n"
            + "WHERE a IN eHead AND b IN eTail\n"
            + "WITH eNo, apoc.coll.toSet(apoc.coll.flatten(collect(eR))) AS eRel\n"
            // Remove modification relations newer than requested version
            + "OPTIONAL MATCH (a)-[eR:UPDATES]-(b)\n"
            + "WHERE eR.version > $version AND eR.type='MODIFIED'\n"
            + "WITH eNo, apoc.coll.toSet(apoc.coll.flatten([eRel,collect(eR)])) AS eRelationships\n"
            // Find any nodes added after wanted version
            + "OPTIONAL MATCH (p)-[r:UPDATES]->(c)\n"
            + "WITH eRelationships, eNo, p, c, r AS rs ORDER BY r.version\n"
            + "WITH eRelationships, eNo, p, c, head(collect([p, rs, c])) AS removed\n"
            + "WITH eRelationships, eNo, apoc.coll.toSet([c in collect(removed) WHERE c[1].type<>'REMOVE' AND c[1]"
            + ".version > $version | c[2]]) as added\n"
            + "WITH eRelationships, apoc.coll.toSet(apoc.coll.flatten([eNo, added])) AS eNodes\n"
            // Get Paths
            + "MATCH (h:" + rootType + " {id: $root})\n"
            + "CALL apoc.path.expandConfig(h, {relationshipFilter:'>', uniqueness: 'RELATIONSHIP_GLOBAL'}) yield"
            + " path\n"
            // Prune unwanted nodes and relationships
            + "WHERE NOT ANY(e IN eRelationships WHERE e IN relationships(path)) AND NOT ANY(e IN eNodes WHERE e "
            + "IN nodes(path))\n"
            // Return a unique set of nodes and relationships
            + "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc"
            + ".coll.flatten(collect([r in relationships(path)]))) AS rel\n";

        Result result = session.run(query, Values.parameters("version",
            version, "root", root));

        final List<Map<String, Object>> retVal = treeService.parseArtifactTree(project, result);

        // Update warnings map
        treeService.addNodeWarning(root, false);
        for (Map<String, Object> v : retVal) {
            if (v.containsKey("warnings")) {
                treeService.addNodeWarning(root, true);
            }
        }

        return retVal;
    }

    @Transactional(readOnly = true)
    public Map<String, Object> versions(Project project) throws ServerError {
        int version = -1;
        Session session = neo4J.createSession();
        Result result = session.run("MATCH (v:VERSION) RETURN v.number");
        if (result.hasNext()) {
            Record record = result.next();
            version = record.get("v.number").asInt();
        }

        // If we have no version and but we have nodes then our current version is 0
        if (version == -1) {
            int count = 0;
            session = neo4J.createSession();
            result = session.run("MATCH (n) RETURN count(*)");
            if (result.hasNext()) {
                Record record = result.next();
                count = record.get("count(*)").asInt();
            }

            if (count > 0) {
                version = 0;
            }
        }

        Map<String, Object> ret = new HashMap<String, Object>();
        ret.put("latest", version);
        return ret;
    }

    public Map<String, Object> versionsTag(String projectId) {
        Map<String, Object> ret = new HashMap<String, Object>();
        try {
            ret.put("version", mPuller.mNeo4JService.tag());
        } catch (Exception e) {
            //
        }
        return ret;
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> tree(Project project, String root, String rootType) throws ServerError {
        int version = (Integer) versions(project).get("latest");
        return versions(project, root, version, rootType);
    }
}
