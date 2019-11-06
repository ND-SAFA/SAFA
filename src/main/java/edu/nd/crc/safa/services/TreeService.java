package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.neo4j.driver.internal.value.ListValue;
import org.neo4j.driver.internal.value.NodeValue;
import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Record;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;
import org.neo4j.driver.v1.Value;
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
        "WITH filter(c in collect(removed) WHERE c[0].type<>\"ADD\") as cRes\n" +
        "WITH extract(c in cRes | c[1]) as excluded\n" +
        // Find parent hazard
        String.format("MATCH path=(child)-[*0..]->(parent:Hazard {id: '%s'})\n", root) +
        "WITH excluded, path ORDER BY length(path) LIMIT 1\n" +
        // Get parent hazard
        "MATCH p=(root:Hazard {id: nodes(path)[0].id})<-[rel*0..]-(artifact)\n" +
        // Remove nodes
        "WHERE NOT any(e in excluded WHERE e IN nodes(p))\n" +
        "RETURN root, rel, artifact";
      // String query = String.format("MATCH path=(child)-[*0..]->(parent:Hazard {id: '%s'})\n", root) +
      //                "WITH path ORDER BY length(path) LIMIT 1\n" +
      //                "MATCH p=(root:Hazard {id: nodes(path)[0].id})<-[*0..]-(artifact) WITH *, relationships(p) as rel\n" +
      //                "RETURN root,rel,artifact\n";
      // String query = String.format("MATCH path=(child)-[*0..]->(parent:Hazard {id: '%s'})\n", root) +
      //                "WITH path ORDER BY length(path) LIMIT 1\n" +
      //                "MATCH (root:Hazard {id: nodes(path)[0].id})<-[rel*0..]-(artifact)\n"+
      //                "RETURN root,rel,artifact";
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

    List<Record> records = result.list();
    for(int i = 0; i < records.size(); i++) {
      Record rec = records.get(i);

      addNode(rec.get("artifact"), values, ids);

      {
        ListValue rels = (ListValue)rec.get("rel");
        rels.asObject().forEach(o -> {
          Relationship rel = (Relationship)o;
          Long relId = rel.id();
          if (!edges.containsKey(relId)) {
            edges.put(relId, true);
            System.out.println("[EDGE " + relId + ": " + rel.type() + "] from: " + ids.get(rel.startNodeId()) + ", to: " + ids.get(rel.endNodeId()));
            Map<String, Object> mapping = new HashMap<String, Object>(); 
            mapping.put("classes", "edge");
            mapping.put("id", relId);
            mapping.put("type", rel.type());
            mapping.put("source", ids.get(rel.startNodeId()));
            mapping.put("target", ids.get(rel.endNodeId()));
            values.add(mapping);
          }
        });
      } 
    }
    return values;
  } 

  private void addNode(Value rec, List<Map<String, Object>> values, Map<Long, String> ids) {
    Node node = (Node)rec.asObject();
    String label = ((List<String>)node.labels()).get(0).toString();
    Map<String, Object> mapping = new HashMap<String, Object>(node.asMap());
    System.out.println("[NODE " + node.id() + ":" + label + "] " + mapping);
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
  
  // private static <T> Collection<T>  
  //                 getCollectionFromIterable(Iterable<T> itr) 
  // { 
  //     // Create an empty Collection to hold the result 
  //     Collection<T> cltn = new ArrayList<T>(); 

  //     // Iterate through the iterable to 
  //     // add each element into the collection 
  //     for (T t : itr) 
  //         cltn.add(t); 

  //     // Return the converted collection 
  //     return cltn; 
  // } 
}