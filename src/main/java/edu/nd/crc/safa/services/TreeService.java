package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.config.Neo4J;
import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.responses.ServerError;
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

@Service
public class TreeService {

    private final Map<String, Boolean> mWarnings = new HashMap<String, Boolean>();
    Neo4J neo4j;
    WarningService warningService;

    @Autowired
    public TreeService(Neo4J neo4J, WarningService warningService) {
        this.neo4j = neo4J;
        this.warningService = warningService;
    }

    @Transactional(readOnly = true)
    public List<Map<String, Object>> trees(Project project, String rootType) throws ServerError {
        Session session = neo4j.createSession();
        String query = "MATCH path=(root:" + rootType + ")-[rel*]->(artifact:" + rootType + ")\n"
            + "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc"
            + ".coll.flatten(collect([r in relationships(path) WHERE TYPE(r)<>'UPDATES']))) AS rel";
        Result result = session.run(query);
        return parseArtifactTree(project, result);
    }

    public List<Map<String, Object>> parseArtifactTree(Project project, Result result) {
        List<Map<String, Object>> values = new ArrayList<>();
        Map<Long, String> ids = new HashMap<>();
        Map<Long, Boolean> edges = new HashMap<>();

        Record record = result.next();

        List<Node> nodes = record.get("artifact").asList(Values.ofNode());
        List<Relationship> rels = record.get("rel").asList(Values.ofRelationship());

        for (Node item : nodes) {
            addNodeToTreeMapping(values, ids, item);
        }

        // Find the highest version of the modification
        Map<String, Integer> maxModification = new HashMap<String, Integer>();
        for (final Relationship r : rels) {
            if (r.type().equals("UPDATES") && r.get("type").asString().equals("MODIFIED")) {
                final String root = ids.get(r.startNodeId());
                final int version = r.get("version").asInt();

                if (maxModification.getOrDefault(root, -1) < version) {
                    maxModification.put(root, version);
                }
            }
        }

        for (final Relationship r : rels) {
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

            for (Rule r : warningService.getProjectRules(project)) {
                verifier.addRule(r);
            }
        } catch (Exception e) {
            System.err.println(e);
        }
        Map<String, List<Rule.Name>> results = verifier.verify(nodes, ids, values);

        // Warnings
        for (final Node node : nodes) {
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

    private void addNodeToTreeMapping(List<Map<String, Object>> listOfNodeMaps,
                                      Map<Long, String> validIds,
                                      Node node) {
        if (!validIds.containsKey(node.id())) {
            String label = ((List<String>) node.labels()).get(0);
            Map<String, Object> mapping = new HashMap<String, Object>(node.asMap());
            if (node.get("id") == null || node.get("id").toString() == "NULL") {
                String nodeId = UUID.randomUUID().toString();
                mapping.put("id", nodeId);
                validIds.put(node.id(), nodeId);
            } else {
                if (label.equals("Package") || label.equals("Code")) {
                    validIds.put(node.id(), node.get("issue").asString() + "." + node.get("id").asString());
                    mapping.put("id", node.get("issue").asString() + "." + node.get("id").asString());
                } else {
                    validIds.put(node.id(), node.get("id").asString());
                }
            }
            mapping.put("classes", "node");
            mapping.put("label", label);
            listOfNodeMaps.add(mapping);
        }
    }

    private void addNodeToTreeMapping(Node node, List<Map<String, Object>> values) {
        addNodeToTreeMapping(values, new HashMap<>(), node);
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
            addNodeToTreeMapping(node, set);
        }
        return set;
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

    public Map<String, Boolean> getNodeWarnings() {
        return mWarnings;
    }

    public void addNodeWarning(String root, boolean flag) {
        this.mWarnings.put(root, flag);
    }
}
