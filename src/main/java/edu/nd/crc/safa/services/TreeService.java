package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.neo4j.driver.internal.value.ListValue;
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
    try ( Session session = driver.session() ) {
      String query = String.format("MATCH path=(child {id: '%s'})-[*]->(:Hazard)\n", root) +
                     "WITH path ORDER BY length(path) LIMIT 1\n" +
                     "MATCH (root:Hazard {id: nodes(path)[1].id})<-[rel*]-(artifact)\n"+
                     "RETURN root,rel,artifact";
      StatementResult result = session.run(query);
      return convertToEdgesNodes(result);
    }
  }

  @Transactional(readOnly = true)
  public List<Map<String, Object>> hazards(String projectId) {
    List<Map<String, Object>> values = new ArrayList<>();
    try ( Session session = driver.session() ) {
      String query = "Match (h:Hazard) return h;";
      StatementResult result = session.run(query);
      List<Record> records = result.list();
      for(int i = 0; i < records.size(); i++) {
        Record rec = records.get(i);
        Node node = (Node)rec.get("h").asObject();
        String label = node.labels().iterator().next();
        Map<String, Object> mapping = new HashMap<String, Object>(node.asMap());
        mapping.put("classes", "node");
        mapping.put("label", label);
        values.add(mapping);
        LOG.debug("[NODE " + node.id() +"] " + mapping);
      }
      return values;
    }
  }

  private List<Map<String, Object>> convertToEdgesNodes(StatementResult result) {
    List<Map<String, Object>> values = new ArrayList<>();
    Map<Long, String> ids = new HashMap<>();
    Map<Long, Boolean> edges = new HashMap<>();

    List<Record> records = result.list();
    for(int i = 0; i < records.size(); i++) {
      Record rec = records.get(i);
      if (values.isEmpty()) {
        addNode(rec.get("root"), values, ids);
      }

      addNode(rec.get("artifact"), values, ids);

      {
        ListValue rels = (ListValue)rec.get("rel");
        rels.asObject().forEach(o -> {
          Relationship rel = (Relationship)o;
          Long relId = rel.id();
          if (!edges.containsKey(relId)) {
            edges.put(relId, true);
            LOG.debug("[EDGE " + relId + ": " + rel.type() + "] from: " + ids.get(rel.startNodeId()) + ", to: " + ids.get(rel.endNodeId()));
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
    mapping.put("classes", "node");
    mapping.put("label", label);
    values.add(mapping);
    LOG.debug("[NODE " + node.id() + ":" + label + "] " + mapping);
    ids.put(node.id(), node.get("id").asString());
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