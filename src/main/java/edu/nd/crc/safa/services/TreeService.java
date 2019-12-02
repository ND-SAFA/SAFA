package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
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
  public List<String> parents(String projectId, String node) {
    try ( Session session = driver.session() ) {
      String query = "MATCH (a)\n" +
        "WHERE a.id =~ $node\n" +
        "CALL apoc.path.expandConfig(a, {relationshipFilter:'<', labelFilter:'/Hazard', uniqueness: 'RELATIONSHIP_GLOBAL'}) yield path \n" + 
        "RETURN CASE WHEN LABELS(a)[0]='Hazard' THEN [a] ELSE apoc.coll.toSet(apoc.coll.flatten(collect(last(nodes(path))))) END AS nodes";
      StatementResult result = session.run(query, Values.parameters("node", "(?i)"+node.replace(".", "\\\\.")));

      List<String> ret = new ArrayList<String>();
      while( result.hasNext() ){
        List<Node> nodes = result.next().get("nodes").asList(Values.ofNode());
        for( Node n : nodes ){
          ret.add(n.get("id").asString());
        }
      }
      return ret;
    }
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
      String query = "MATCH path=(root:Hazard)-[rel*]->(artifact:Hazard)\n" +
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
      String query = "MATCH (a {id: $root})" +
      "CALL apoc.path.expandConfig(a, {relationshipFilter:'>', uniqueness: 'RELATIONSHIP_GLOBAL'}) yield path \n" + 
      "WITH apoc.coll.toSet(apoc.coll.flatten(collect([r in relationships(path) WHERE TYPE(r)='UPDATES' | r.version]))) AS rel\n" + 
      "UNWIND rel as ru\n" + 
      "WITH ru AS res ORDER BY res\n" + 
      "RETURN last(collect(distinct res)) as last";
        
      StatementResult result = session.run(query, Values.parameters("root", root));
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
      String query ="MATCH (p)-[r:UPDATES]->(c)\n" +
        "WHERE r.version <= $version\n" +
        "WITH p, c, r AS rs ORDER BY r.version DESC\n" +
        "WITH p, c, head(collect([p, rs, c])) AS removed\n" +
        "WITH [c in collect(removed) WHERE c[1].type='REMOVE' | [c[0],c[2]]] as excluded\n" +
        "WITH [e in excluded | e[0]] AS eHead, [e in excluded | e[1]] AS eTail, apoc.coll.toSet(apoc.coll.flatten([e in excluded WHERE e[0].id=e[1].id| e[0]])) AS eNo\n" +
        // Find all removed relationships
        "OPTIONAL MATCH (a)-[eR]-(b)\n" +
        "WHERE a IN eHead AND b IN eTail\n" +
        "WITH eNo, apoc.coll.toSet(apoc.coll.flatten(collect(eR))) AS eRel\n" +
        // Remove modification relations newer than requested version
        "OPTIONAL MATCH (a)-[eR:UPDATES]-(b)\n" +
        "WHERE eR.version > $version AND eR.type='MODIFIED'\n" +
        "WITH eNo, apoc.coll.toSet(apoc.coll.flatten([eRel,collect(eR)])) AS eRelationships\n" +
        // Find any nodes added after wanted version
        "OPTIONAL MATCH (p)-[r:UPDATES]->(c)\n" +
        "WITH eRelationships, eNo, p, c, r AS rs ORDER BY r.version\n" +
        "WITH eRelationships, eNo, p, c, head(collect([p, rs, c])) AS removed\n" +
        "WITH eRelationships, eNo, apoc.coll.toSet([c in collect(removed) WHERE c[1].type<>'REMOVE' AND c[1].version > $version | c[2]]) as added\n" +
        "WITH eRelationships, apoc.coll.toSet(apoc.coll.flatten([eNo, added])) AS eNodes\n" +
        // Get Paths
        "MATCH (h:Hazard {id: $root})\n" +
        "CALL apoc.path.expandConfig(h, {relationshipFilter:'>', uniqueness: 'RELATIONSHIP_GLOBAL'}) yield path\n" +
        // Prune unwanted nodes and relationships
        "WHERE NOT ANY(e IN eRelationships WHERE e IN relationships(path)) AND NOT ANY(e IN eNodes WHERE e IN nodes(path))\n" +
        // Return a unique set of nodes and relationships
        "RETURN apoc.coll.toSet(apoc.coll.flatten(collect(nodes(path)))) AS artifact, apoc.coll.toSet(apoc.coll.flatten(collect([r in relationships(path)]))) AS rel\n";
      StatementResult result = session.run(query, Values.parameters("version", version, "root", root));
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

    // Find the highest version of the modification
    Map<String, Integer> maxModification = new HashMap<String, Integer>();
    for( int i = 0; i < rels.size(); i++ ){
      final Relationship r = rels.get(i);
      if( r.type().equals("UPDATES") && r.get("type").asString().equals("MODIFIED") ){
        final String root = ids.get(r.startNodeId());
        final int version = r.get("version").asInt();

        if( maxModification.getOrDefault(root, 0) < version ){
          maxModification.put(root, version);
        }
      }
    }

    for(int i = 0; i < rels.size(); i++) {
      final Relationship r = rels.get(i);
      if( !r.type().equals("UPDATES") ){
        addEdge(r, values, edges, ids);
      }else{
        // Handle modifications
        if( r.get("type").asString().equals("MODIFIED") ) {
          final String root = ids.get(r.startNodeId());

          // Make sure we only apply the latest version
          final int version = r.get("version").asInt();
          if( maxModification.get(root) != version ){
            continue;
          }

          // Handle updating nodes
          for( Map<String,Object> value : values ){
            if( value.get("id").equals(root) ){
              if( !value.get("label").equals("Code") && !value.get("label").equals("Package") ){
                if( !value.containsKey("original") ){
                  value.put("original", value.get("DATA").toString());
                }
                value.put("DATA", r.get("data").asString());
              }

              if( value.get("label").equals("Code") ){
                if( !value.containsKey("original") ){
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

    // Warnings
    for(int i = 0; i < nodes.size(); i++) {
      final Node node = nodes.get(i);
      final String id = ids.get(node.id());
      final String label = ((List<String>)node.labels()).get(0).toString();

      List<String> warnings = new ArrayList<String>();

      // Handle design definitions with no child nodes
      if( label.equals("DesignDefinition") ){
        if( !containsChildOfType("Code", node, nodes, ids, values) ){
          warnings.add("Missing Code");
        }
      }

      // Handle requirements with no design definitions
      if( label.equals("Requirement") ){
        if( !containsChildOfType("DesignDefinition", node, nodes, ids, values) ){
          warnings.add("Missing Design Definition");
        }
      }

      if( !warnings.isEmpty() ) {
        // Find this node's values
        for( Map<String,Object> value : values ){
          if( value.getOrDefault("id", "").equals(id) ){
            value.put("warnings", warnings.toArray());
          }
        }
      }
    }

    return values;
  } 

  private boolean containsChildOfType(final String type, final Node node, final List<Node> nodes, final Map<Long, String> ids, final List<Map<String, Object>> values) {
    final String id = ids.get(node.id());

    List<String> nChildren = new ArrayList<String>();
    for( Map<String,Object> value : values ){
      if( value.getOrDefault("source", "").equals(id) && !value.getOrDefault("type", "").equals("UPDATES") ){
        String target = (String)value.getOrDefault("target", "");
        if (!target.isEmpty()){
          nChildren.add(target);
        }
      }
    }

    for( String child: nChildren) {
      for( Node n: nodes ){
        if( ids.get(n.id()).equals(child) && ((List<String>)n.labels()).get(0).toString().equals(type)){
          return true;
        }
      }
    }

    return false;
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
        if( label.equals("Package") ){
          ids.put(node.id(), node.get("issue").asString() + "." + node.get("id").asString());
          mapping.put("id", node.get("issue").asString() + "." + node.get("id").asString());
        }else{
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