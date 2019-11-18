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
import org.neo4j.driver.v1.Value;
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
  public List<Map<String, Object>> hazards(String projectId) {
    List<Map<String, Object>> set = new ArrayList<>();
    try ( Session session = driver.session() ) {
      String query = "MATCH (n:Hazard) WITH n ORDER BY n.id ASC RETURN n";
      StatementResult result = session.run(query);
      List<Record> records = result.list();
      for(int i = 0; i < records.size(); i++) {
        Node node = records.get(i).get("n").asNode();
        addNode(node, set);
      }
      return set;
    }
  }
  
  @Transactional(readOnly = true)
  public List<Map<String, Object>> trees(String projectId) {
    try ( Session session = driver.session() ) {
      String query = "MATCH path=(root:Hazard)<-[rel*]-(artifact:Hazard)\n" +
                     "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc.coll.flatten(collect([r in relationships(path) WHERE TYPE(r)<>'UPDATES']))) AS rel";
      StatementResult result = session.run(query);
      return parseArtifactTree(result);
    }
  }

  @Transactional(readOnly = true)
  public List<Map<String, Object>> trees(String projectId, String root) {
    int version = versions(projectId, root).get("latest");
    return versions(projectId, root, version);
  }

  @Transactional(readOnly = true)
  public Map<String, Integer> versions(String projectId, String root) {
    try ( Session session = driver.session() ) {
      String query = String.format("MATCH ({id:'%s'})<-[r*]-()\n", root) +
                    "UNWIND [re in r WHERE TYPE(re)='UPDATES' | re.version] AS ru\n" +
                    "WITH ru AS res ORDER BY res\n" +
                    "RETURN last(collect(distinct res)) as last";
      StatementResult result = session.run(query);
      Value last = result.single().get("last");
      int latestVersion = 0; 
      if (!last.isNull()) {
        latestVersion = last.asInt();
      }
      Map<String, Integer> ret = new HashMap<String, Integer>();
      ret.put("latest", latestVersion);
      return ret;
    }
  }

  @Transactional(readOnly = true)
  public List<Map<String, Object>> versions(String projectId, String root, int version) {
    try ( Session session = driver.session() ) {
      String query = "MATCH (p)<-[r:UPDATES]-(c)\n" +
        String.format("WHERE r.version <= %s\n", version) +
        "WITH p, c, r AS rs ORDER BY r.version DESC\n" +
        "WITH p, c, head(collect([p, rs, c])) AS removed\n" +
        "WITH [c in collect(removed) WHERE c[1].type<>'ADD' | c] as excluded\n" +
        "UNWIND excluded AS e\n" +
        "MATCH (a {id: e[0].id})<-[eR]-(b {id: e[2].id})\n" +
        "WITH eR, CASE WHEN e[0].id=e[2].id THEN e[0] ELSE [] END AS eN\n" +
        "WITH apoc.coll.toSet(apoc.coll.flatten(collect(eR))) AS eRelationships, apoc.coll.toSet(apoc.coll.flatten(collect(eN))) AS eNodes\n" +
        String.format("MATCH path=()-[*0..]->(:Hazard {id: '%s'})\n", root) +
        "WHERE NOT ANY(e IN eRelationships WHERE e IN relationships(path)) AND NOT ANY(e IN eNodes WHERE e IN nodes(path))\n" +
        "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc.coll.flatten(collect([r in relationships(path) WHERE TYPE(r)<>'UPDATES']))) AS rel";
        
      StatementResult result = session.run(query);
      return parseArtifactTree(result);
    }
  }

  private List<Map<String, Object>> parseArtifactTree(StatementResult result) {
    List<Map<String, Object>> values = new ArrayList<>();
    Map<Long, String> ids = new HashMap<>();
    Map<Long, Boolean> edges = new HashMap<>();

    Record record = result.next();

    List<Node> nodes = record.get("artifact").asList(Values.ofNode());
    List<Relationship> rels = record.get("rel").asList(Values.ofRelationship());

    for(int i = 0; i < nodes.size(); i++) {
      addNode(nodes.get(i), values, ids);
    }

    for(int i = 0; i < rels.size(); i++) {
      addEdge(rels.get(i), values, edges, ids);
    }

    return values;
  } 

  private void addNode(Node node, List<Map<String, Object>> values, Map<Long, String> ids) {
    if (!ids.containsKey(node.id())) {
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
  }

  private void addNode(Node node, List<Map<String, Object>> values) {
    addNode(node, values, new HashMap<Long, String>());
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