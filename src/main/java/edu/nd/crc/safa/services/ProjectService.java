package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import edu.nd.crc.safa.dao.Links;
import edu.nd.crc.safa.database.connection.Neo4J;
import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.importer.MySQL;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.warnings.Rule;
import edu.nd.crc.safa.warnings.TreeVerifier;

import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.Session;
import org.neo4j.driver.Values;
import org.neo4j.driver.types.Node;
import org.neo4j.driver.types.Relationship;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;


@Service
/* Responsible for all providing an API for peforming the
 * business logic involved in ProjectsController.
 * TODO: Unused ProjectID variables should be used to authenticate access to resources.
 */
public class ProjectService {

    Neo4J neo4j;
    Puller mPuller;
    MySQL sql;

    @Autowired
    public ProjectService(Neo4J neo4j,
                          Puller puller,
                          MySQL mysql) {
        this.neo4j = neo4j;
        this.mPuller = puller;
        this.sql = mysql;
    }

    private Map<String, Boolean> mWarnings = new HashMap<String, Boolean>();


    private void init() throws ServerError { //TODO: Run after Dependency injection once test connection has been
        // installed
        final List<Map<String, Object>> nodes = nodes("test", "Hazard");
        for (Map<String, Object> node : nodes) {
            final String id = (String) node.get("id");
            final int version = (Integer) versions("test").get("latest");
            final List<Map<String, Object>> data = versions("test", id, version, "Hazard");
            mWarnings.put(id, false);
            for (Map<String, Object> v : data) {
                if (v.containsKey("warnings")) {
                    mWarnings.put(id, true);
                }
            }
        }
        System.out.println(mWarnings);
    }

    public SseEmitter projectPull(String projId) {
        SseEmitter emitter = new SseEmitter(0L);
        ExecutorService sseMvcExecutor = Executors.newSingleThreadExecutor();
        sseMvcExecutor.execute(() -> {
            try {
                emitter.send(SseEmitter.event()
                    .data("{\"complete\": false}")
                    .id(String.valueOf(0))
                    .name("update"));

                String Mysql2NeoData = mPuller.mySQLNeo();
                emitter.send(SseEmitter.event()
                    .data(Mysql2NeoData)
                    .id(String.valueOf(3))
                    .name("update"));

                mPuller.execute();
                emitter.send(SseEmitter.event()
                    .data("{\"complete\": true}")
                    .id(String.valueOf(4))
                    .name("update"));

                emitter.complete();
            } catch (Exception ex) {
                emitter.completeWithError(ex);
            }
        });
        return emitter;
    }


    @Transactional(readOnly = true)
    public List<String> parents(String projectId, String node, String rootType) throws ServerError {
        Session session = neo4j.createSession();
        String query = "MATCH (a)\n"
            + "WHERE a.id =~ $node\n"
            + "CALL apoc.path.expandConfig(a, {relationshipFilter:'<', labelFilter:'/" + rootType + "', uniqueness"
            + ": 'RELATIONSHIP_GLOBAL'}) yield path \n"
            + "RETURN CASE WHEN LABELS(a)[0]='" + rootType + "' THEN [a] ELSE apoc.coll.toSet(apoc.coll.flatten"
            + "(collect(last(nodes(path))))) END AS nodes";
        Result result = session.run(query, Values.parameters("node", "(?i)"
            + node.replace(".", "\\\\.")));

        List<String> ret = new ArrayList<String>();
        while (result.hasNext()) {
            List<Node> nodes = result.next().get("nodes").asList(Values.ofNode());
            for (Node n : nodes) {
                ret.add(n.get("id").asString());
            }
        }
        return ret;
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> nodes(String projectId, String nodeType) throws ServerError {
        List<Map<String, Object>> set = new ArrayList<>();
        Session session = neo4j.createSession();
        String query = "MATCH (n:" + nodeType + ") WITH n ORDER BY n.id ASC RETURN n";
        Result result = session.run(query);
        List<Record> records = result.list();
        for (Record record : records) {
            Node node = record.get("n").asNode();
            addNode(node, set);
        }
        return set;
    }

    @Transactional(readOnly = true)
    public Map<String, Boolean> nodeWarnings(String projectId) {
        return mWarnings;
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> trees(String projectId, String rootType) throws ServerError {
        Session session = neo4j.createSession();
        String query = "MATCH path=(root:" + rootType + ")-[rel*]->(artifact:" + rootType + ")\n"
            + "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc"
            + ".coll.flatten(collect([r in relationships(path) WHERE TYPE(r)<>'UPDATES']))) AS rel";
        Result result = session.run(query);
        return parseArtifactTree(result, projectId);
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> tree(String projectId, String root, String rootType) throws ServerError {
        int version = (Integer) versions(projectId).get("latest");
        return versions(projectId, root, version, rootType);
    }

    @Transactional(readOnly = true)
    public Map<String, Object> versions(String projectId) throws ServerError {
        int version = -1;
        Session session = neo4j.createSession();
        Result result = session.run("MATCH (v:VERSION) RETURN v.number");
        if (result.hasNext()) {
            Record record = result.next();
            version = record.get("v.number").asInt();
        }

        // If we have no version and but we have nodes then our current version is 0
        if (version == -1) {
            int count = 0;
            session = neo4j.createSession();
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


    @Transactional(readOnly = true)
    public List<Map<String, Object>> versions(String projectId, String root, int version, String rootType)
        throws ServerError {
        Session session = neo4j.createSession();
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

        final List<Map<String, Object>> retVal = parseArtifactTree(result, projectId);

        // Update warnings map
        mWarnings.put(root, false);
        for (Map<String, Object> v : retVal) {
            if (v.containsKey("warnings")) {
                mWarnings.put(root, true);
            }
        }

        return retVal;
    }

    public Map<String, Object> versionsTag(String projectId) {
        Map<String, Object> ret = new HashMap<String, Object>();
        try {
            ret.put("version", mPuller.mDatabase.tag());
        } catch (Exception e) {
            //
        }
        return ret;
    }

    @Transactional(readOnly = true)
    public String getTreeLayout(String projId, String hash) throws ServerError {
        // TODO(Adam): Do something with the projId?
        String b64EncodedLayout = sql.fetchLayout(hash);
        return b64EncodedLayout;
    }

    public void postTreeLayout(String projId, String hash, String b64EncodedLayout) throws ServerError {
        sql.saveLayout(hash, b64EncodedLayout);
    }

    private List<Map<String, Object>> parseArtifactTree(Result result, String projectId) {
        List<Map<String, Object>> values = new ArrayList<>();
        Map<Long, String> ids = new HashMap<>();
        Map<Long, Boolean> edges = new HashMap<>();

        Record record = result.next();

        List<Node> nodes = record.get("artifact").asList(Values.ofNode());
        List<Relationship> rels = record.get("rel").asList(Values.ofRelationship());

        for (int i = 0; i < nodes.size(); i++) {
            addNode(nodes.get(i), values, ids);
        }

        // Find the highest version of the modification
        Map<String, Integer> maxModification = new HashMap<String, Integer>();
        for (int i = 0; i < rels.size(); i++) {
            final Relationship r = rels.get(i);
            if (r.type().equals("UPDATES") && r.get("type").asString().equals("MODIFIED")) {
                final String root = ids.get(r.startNodeId());
                final int version = r.get("version").asInt();

                if (maxModification.getOrDefault(root, -1) < version) {
                    maxModification.put(root, version);
                }
            }
        }

        for (int i = 0; i < rels.size(); i++) {
            final Relationship r = rels.get(i);
            if (!r.type().equals("UPDATES")) {
                addEdge(r, values, edges, ids);
            } else {
                // Handle modifications
                if (r.get("type").asString().equals("MODIFIED")) {
                    final String root = ids.get(r.startNodeId());

                    // Make sure we only apply the latest version
                    final int version = r.get("version").asInt();
                    if (maxModification.get(root) != version) {
                        continue;
                    }

                    // Handle updating nodes
                    for (Map<String, Object> value : values) {
                        if (value.get("id").equals(root)) {
                            if (!value.get("label").equals("Code") && !value.get("label").equals("Package")) {
                                if (!value.containsKey("original")) {
                                    value.put("original", value.get("DATA").toString());
                                }
                                value.put("DATA", r.get("data").asString());
                            }

                            if (value.get("label").equals("Code")) {
                                if (!value.containsKey("original")) {
                                    value.put("original", value.get("commit").toString());
                                }
                                value.put("commit", r.get("data").asString());
                            }

                            value.put("modified", true);
                        }
                    }
                }
            }
        }

        TreeVerifier verifier = new TreeVerifier();
        try {
            verifier.addRule("Missing child",
                "At least one requirement child for hazards",
                "at-least-one(Hazard, child, Requirement)");

            verifier.addRule("Missing child",
                "At least one requirement, design or process child for requirements",
                "at-least-one(Requirement, child, Requirement) || at-least-one(Requirement, child, Design) || "
                    + "at-least-one(Requirement, child, Process)");
            verifier.addRule("Missing child",
                "Requirements must not have package children",
                "exactly-n(0, Requirement, child, Package)");

            verifier.addRule("Missing child", "At least one package child for design definitions",
                "at-least-one(DesignDefinition, child, Package)");

            for (Rule r : sql.getWarnings(projectId)) {
                verifier.addRule(r);
            }
        } catch (Exception e) {
            System.out.println(e.toString());
        }
        Map<String, List<Rule.Name>> results = verifier.verify(nodes, ids, values);

        // Warnings
        for (int i = 0; i < nodes.size(); i++) {
            final Node node = nodes.get(i);
            final String id = ids.get(node.id());

            List<Rule.Name> warnings = results.get(id);

            if (warnings != null && !warnings.isEmpty()) {
                for (Map<String, Object> value : values) {
                    if (value.getOrDefault("id", "").equals(id)) {
                        value.put("warnings", warnings.toArray());
                    }
                }
            }
        }

        return values;
    }

    private void addNode(Node node, List<Map<String, Object>> values, Map<Long, String> ids) {
        if (!ids.containsKey(node.id())) {
            String label = ((List<String>) node.labels()).get(0).toString();
            Map<String, Object> mapping = new HashMap<String, Object>(node.asMap());
            // System.out.println("[NODE " + node.id() + ":" + label + "] " + mapping);
            if (node.get("id") == null || node.get("id").toString() == "NULL") {
                String nodeId = UUID.randomUUID().toString();
                mapping.put("id", nodeId);
                ids.put(node.id(), nodeId);
            } else {
                if (label.equals("Package") || label.equals("Code")) {
                    ids.put(node.id(), node.get("issue").asString() + "." + node.get("id").asString());
                    mapping.put("id", node.get("issue").asString() + "." + node.get("id").asString());
                } else {
                    ids.put(node.id(), node.get("id").asString());
                }
            }
            mapping.put("classes", "node");
            mapping.put("label", label);
            values.add(mapping);
        }
    }

    private void addNode(Node node, List<Map<String, Object>> values) {
        addNode(node, values, new HashMap<Long, String>());
    }

    private void addEdge(Relationship rel,
                         List<Map<String, Object>> values,
                         Map<Long, Boolean> edges,
                         Map<Long, String> ids) {
        Long relId = rel.id();
        if (!edges.containsKey(relId)) {
            edges.put(relId, true);
            Map<String, Object> mapping = new HashMap<String, Object>();
            mapping.put("classes", "edge");
            mapping.put("id", relId);
            mapping.put("type", rel.type());
            mapping.put("source", ids.get(rel.startNodeId()));
            mapping.put("target", ids.get(rel.endNodeId()));
            values.add(mapping);
        }
    }

    @Transactional(readOnly = true)
    public Map<String, String> getWarnings(String projectId) {
        Map<String, String> result = new HashMap<String, String>();
        try {
            for (Rule r : sql.getWarnings(projectId)) {
                result.put(r.toString(), r.unprocessedRule());
            }
        } catch (Exception e) {
            System.out.println(e.toString());
        }
        return result;
    }

    public void newWarning(String projectId, String nShort, String nLong, String rule) {
        try {
            sql.newWarning(projectId, nShort, nLong, rule);
        } catch (Exception e) {
            System.out.println(e.toString());
        }
    }

    // Links
    @Transactional(readOnly = true)
    public Map<String, String> getLink(String projectId, String source, String target) {
        Map<String, String> result = new HashMap<String, String>();
        try {
            result.put("approval", sql.getLinkApproval(projectId, source, target).toString());
        } catch (Exception e) {
            System.out.println(e.toString());
        }
        return result;
    }

    // public Map<String, String> updateLink(String projectId, String source, String target, Integer approval) {
    public Map<String, String> updateLink(String projectId, Links links) {
        Map<String, String> result = new HashMap<String, String>();
        try {
            result.put("success", String.format("%b", sql.updateLink(projectId, links)));
            // result.put("success", String.format("%b", sql.updateLink(projectId, source, target, approval)));
        } catch (Exception e) {
            result.put("success", "false");
            result.put("message", e.toString());
        }
        return result;
    }

    @Transactional(readOnly = true)
    public Map<String, Object> getArtifactLinks(String projectId, String source, String target, Double minScore) {
        Map<String, Object> result = new HashMap<String, Object>();
        try {
            result.put("links", sql.getArtifactLinks(projectId, source, target, minScore));
        } catch (Exception e) {
            result.put("success", "false");
            result.put("message", e.toString());
        }
        return result;
    }
}
