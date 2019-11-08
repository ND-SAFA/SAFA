package edu.nd.crc.safa.services;

import java.io.Console;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.neo4j.driver.internal.value.ListValue;
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
  public List<Map<String, Object>> trees(String projectId) {
    try ( Session session = driver.session() ) {
      String query = String.format("MATCH path=(child:Hazard)-[*0..]->(parent:Hazard)\n") +
                     "WITH path ORDER BY length(path)\n" +
                     "MATCH (root:Hazard {id: nodes(path)[0].id})<-[rel*0..]-(artifact:Hazard)\n"+
                    //  "UNWIND [rf IN r WHERE TYPE(rf)<>'UPDATES'] as rel\n" +
                     "RETURN artifact, rel, root";
      StatementResult result = session.run(query);
      return parseHazardTree(result);

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
                    "RETURN last(collect(distinct ru)) as last";
      StatementResult result = session.run(query);
      Value last = result.next().get("last");
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
      String query = "MATCH ()<-[r:UPDATES]-(o)\n" +
        String.format("WHERE r.version <= %s\n", version) +
        "WITH o, r AS rs ORDER BY r.version DESC\n" +
        "WITH o, head(collect([rs,o])) AS removed\n" +
        "WITH [c in collect(removed) WHERE c[0].type<>'ADD' | c[1]] as excluded\n" +
        String.format("MATCH pEx=(a:Hazard {id: '%s'})<-[r*0..]-(b)\n", root) +
        String.format("WITH excluded, apoc.coll.toSet(collect([r in relationships(pEx) WHERE r.version > %s | startNode(r)])) AS uEx\n", version) +

        String.format("MATCH path=(artifact)-[r*0..]->(root:Hazard {id: '%s'})\n", root) +
        "WHERE NOT ANY(e IN excluded WHERE e IN nodes(path)) AND NOT ANY(e IN uEx WHERE ANY (ez IN e WHERE ez IN nodes(path)))\n" +
        "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc.coll.flatten(collect([r in relationships(path) WHERE TYPE(r)<>'UPDATES']))) AS rel";
      StatementResult result = session.run(query);
      return parseArtifactTree(result);
    }
  }

  private List<Map<String, Object>> parseHazardTree(StatementResult result) {
    List<Map<String, Object>> values = new ArrayList<>();
    Map<Long, String> ids = new HashMap<>();
    Map<Long, Boolean> edges = new HashMap<>();

    List<Record> records = result.list();

    for(int i = 0; i < records.size(); i++) {
      Record record = records.get(i);
      Node node = (Node)record.get("artifact").asObject();
      addNode(node, values, ids);
      {
        ListValue rels = (ListValue)record.get("rel");
        rels.asObject().forEach(o -> {
          Relationship rel = (Relationship)o;
          addEdge(rel, values, edges, ids);
        });
      }
    }

    return values;
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