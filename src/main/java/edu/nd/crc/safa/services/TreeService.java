package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Record;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;
import org.neo4j.driver.v1.Values;
import org.neo4j.driver.v1.types.Node;
import org.neo4j.driver.v1.types.Relationship;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@Service
public class TreeService {

  @Autowired
  Driver driver;

  private final static Logger LOG = LoggerFactory.getLogger(TreeService.class);

  public TreeService() {
  }
  
  public TreeService(Driver driver) {
    this.driver = driver;
  }
  
  @Transactional(readOnly = true)
  public List<Map<String, Object>> trees(String projectId, String root) {
    int version = 1;
    try ( Session session = driver.session() ) {
      String query = "MATCH ()<-[r:UPDATE]-(o)\n" +
        String.format("WHERE r.version <= %s\n", version) +
        "WITH o, r AS rs ORDER BY r.version DESC\n" +
        "WITH o, head(collect([rs,o])) AS removed\n" +
        "WITH [c in collect(removed) WHERE c[0].type<>'ADD' | c[1]] as excluded\n" +
        String.format("MATCH path=(artifact)-[r*0..]->(root:Hazard {id: '%s'})\n", root) +
        String.format("WHERE NOT ANY(e IN excluded WHERE e IN nodes(path)) AND NOT ANY(r IN relationships(path) WHERE EXISTS(r.version) AND r.version > %s)\n", version) +
        "UNWIND [rf IN r WHERE TYPE(rf)<>'UPDATES'] as rel\n" +
        "RETURN collect(distinct artifact), collect(distinct rel), root";
      StatementResult result = session.run(query);
      return convertToEdgesNodes(result);
    }
  }

  @Transactional(readOnly = true)
  public List<Map<String, Object>> hazards(String projectId) {
    try ( Session session = driver.session() ) {
      String query = String.format("MATCH path=(child:Hazard)-[*0..]->(parent:Hazard)\n") +
                     "WITH path ORDER BY length(path)\n" +
                     "MATCH (root:Hazard {id: nodes(path)[0].id})<-[rel*0..]-(artifact:Hazard)\n"+
                     "RETURN root,rel,artifact";
      StatementResult result = session.run(query);
      return convertToEdgesNodes(result);
    }
  }

  private List<Map<String, Object>> convertToEdgesNodes(StatementResult result) {
    List<Map<String, Object>> values = new ArrayList<>();
    Map<Long, String> ids = new HashMap<>();
    Map<Long, Boolean> edges = new HashMap<>();

    Record record = result.single();

    List<Node> nodes = record.get("collect(distinct artifact)").asList(Values.ofNode());
    List<Relationship> rels = record.get("collect(distinct rel)").asList(Values.ofRelationship());
    Node root = record.get("root").asNode();

    addNode(root, values, ids);

    for(int i = 0; i < nodes.size(); i++) {
      addNode(nodes.get(i), values, ids);
    }

    for(int i = 0; i < rels.size(); i++) {
      addEdge(rels.get(i), values, edges, ids);
    }

    return values;
  } 

  private void addNode(Node node, List<Map<String, Object>> values, Map<Long, String> ids) {
    String label = ((List<String>)node.labels()).get(0).toString();
    Map<String, Object> mapping = new HashMap<String, Object>(node.asMap());
    // System.out.println("[NODE " + node.id() + ":" + label + "] " + mapping);
    if (node.get("id") == null || node.get("id").toString() == "NULL") {
      String nodeId = UUID.randomUUID().toString();
      mapping.put("id", nodeId);
      ids.put(node.id(), nodeId);
    } else {
      ids.put(node.id(), node.get("id").asString());
    }
    mapping.put("classes", "node");
    mapping.put("label", label);
    values.add(mapping);
  }

  private void addEdge(Relationship rel, List<Map<String, Object>> values,  Map<Long, Boolean> edges, Map<Long, String> ids) {
    Long relId = rel.id();
    if (!edges.containsKey(relId)) {
      edges.put(relId, true);
      // System.out.println("[EDGE " + relId + ": " + rel.type() + "] from: " + ids.get(rel.startNodeId()) + ", to: " + ids.get(rel.endNodeId()));
      Map<String, Object> mapping = new HashMap<String, Object>(); 
      mapping.put("classes", "edge");
      mapping.put("id", relId);
      mapping.put("type", rel.type());
      mapping.put("source", ids.get(rel.startNodeId()));
      mapping.put("target", ids.get(rel.endNodeId()));
      values.add(mapping);
    }
  }
}