package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.Base64;
import java.io.File;
import java.io.FileNotFoundException; 
import java.nio.file.Files;
import javax.annotation.PostConstruct;

import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Record;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;
import org.neo4j.driver.v1.Transaction;
import org.neo4j.driver.v1.Values;
import org.neo4j.driver.v1.types.Node;
import org.neo4j.driver.v1.types.Relationship;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import edu.nd.crc.safa.importer.Database;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.importer.UploadFlatfile;
import edu.nd.crc.safa.importer.GenerateFlatfile;
import edu.nd.crc.safa.importer.Flatfile.MissingFileException;


@Service
public class ProjectService {

  @Autowired
  Driver driver;

  @Autowired
  Puller mPuller;

  @Autowired
  UploadFlatfile uploadFlatfile;

  @Autowired
  GenerateFlatfile generateFlatfile;

  private Map<String, Boolean> mWarnings = new HashMap<String, Boolean>();

  public ProjectService() {
  }
  
  public ProjectService(Driver driver) {
    this.driver = driver;
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

          // mPuller.ParseJIRAIssues();
          // emitter.send(SseEmitter.event()
          //   .data("{\"complete\": false}")
          //   .id(String.valueOf(1))
          //   .name("update"));

          // mPuller.ParseSourceLinks();
          // emitter.send(SseEmitter.event()
          //   .data("{\"complete\": false}")
          //   .id(String.valueOf(2))
          //   .name("update"));
          
          String data = "{\"complete\": false}";     
          try {
            mPuller.parseFlatfiles();
            System.out.println("Completed ParseFlatfiles without exceptions");
          } catch (MissingFileException e) {
            System.out.println("MissingFileException");
            data = String.format("{\"complete\": true, \"file\": %s}", e.getMessage());
          } catch (Exception e) {
            System.out.println("Regular Exception");
            data = String.format("{\"complete\": true, \"message\": \"%s\"}", e.getMessage());
          }
          emitter.send(SseEmitter.event()
              .data(data)
              .id(String.valueOf(3))
              .name("update"));

          mPuller.Execute();
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

  public String generateLinks(String projId){
    try {
      return generateFlatfile.generateFiles();
    } 
    catch (Exception e) {
      return String.format("{ \"success\": false, \"message\": \"%s\"}", e.toString());
    }
  }

  public String clearGeneratedFilesDir(String projId) {
    try {
      String dir = "/generatedFilesDir";
      return uploadFlatfile.deleteDirectory(dir, "Generated Links");
    }
    catch(Exception e) {
      return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
    }
  }

  public String uploadFile(String projId, String encodedStr) {
    try {
      uploadFlatfile.uploadFile(projId, encodedStr);

      try {
        return uploadFlatfile.getMissingFiles(projId);
      }
      catch(Exception e){
        if (e.getClass().getName().equals("com.jsoniter.spi.JsonException")) {
          return "{ \"success\": false, \"message\": \"Error parsing tim.json file: File does not match expected tim.json structure\"}";
        }
        else if (e.getMessage().equals("Please upload a tim.json file")) {
          return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
        }
        else {
          return String.format("{ \"success\": false, \"message\": \"Error checking for missing files: %s\"}", e.toString());
        }
      }
    }
    catch(Exception e){
      if (e.getClass().getName().equals("com.jsoniter.spi.JsonException")) {
        return "{ \"success\": false, \"message\": \"Error uploading Flatfiles: Could not parse API JSON body.\"}";
      }
      else {
        System.out.println("Error uploading Flatfiles: OTHER");
        return String.format("{ \"success\": false, \"message\": \"Error uploading Flatfiles: %s\"}", e.toString());
      }
    }
  }

  public String getUploadFilesErrorLog(String projId) {
    try {
      File myObj = new File("/flatfilesDir/ErrorReport.txt");
      byte[] fileContent = Files.readAllBytes(myObj.toPath());
      String returnStr = Base64.getEncoder().encodeToString(fileContent);
      return String.format("{ \"success\": true, \"data\": \"%s\"}", returnStr);
    } catch (Exception e) {
      return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
    }
  }

  public String getGenerateLinksErrorLog(String projId) {
    try {
      File myObj = new File("/generatedFilesDir/ErrorText.csv"); 
      byte[] fileContent = Files.readAllBytes(myObj.toPath());
      String returnStr = Base64.getEncoder().encodeToString(fileContent);
      return String.format("{ \"success\": true, \"data\": \"%s\"}", returnStr);
    } catch (Exception e) {
      return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
    }
  }

  public String clearFlatfileDir() {
    try {
      String dir = "/flatfilesDir";
      return uploadFlatfile.deleteDirectory(dir, "Flatfile Uploads");
    }
    catch(Exception e) {
      return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
    }
  }

  @PostConstruct
  private void init() {
    final List<Map<String, Object>> hazards = hazards("test");
    for( Map<String, Object> node : hazards ){
      final String id = (String)node.get("id");
      final int version = (Integer)versions("test").get("latest"); 
      final List<Map<String, Object>> data = versions("test", id, version);
      mWarnings.put(id, false);
      for( Map<String, Object> v: data) {
        if( v.containsKey("warnings") ){
          mWarnings.put(id, true);
        }
      }
    }
    System.out.println(mWarnings);
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
  public Map<String, Boolean> hazardWarnings(String projectId) {
    return mWarnings;
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
    int version = (Integer)versions(projectId).get("latest");
    return versions(projectId, root, version);
  }

  @Transactional(readOnly = true)
  public Map<String, Object> versions(String projectId) {
    int version = -1;
    try ( Session session = driver.session() ) {
      StatementResult result = session.run("MATCH (v:VERSION) RETURN v.number");
      if (result.hasNext()) {
          Record record = result.next();
          version = record.get("v.number").asInt();
      }
    }

    // If we have no version and but we have nodes then our current version is 0
    if( version == -1 ){
        int count = 0;
        try (Session session = driver.session()) {
            StatementResult result = session.run("MATCH (n) RETURN count(*)");
            if (result.hasNext()) {
                Record record = result.next();
                count = record.get("count(*)").asInt();
            }
        }
        if( count > 0 ) {
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
        ret.put("version", mPuller.mDatabase.Tag());
      } catch (Exception e) {
        //
      }
      return ret;
  }

  // MARKED AS DEPRECATED
  //
  // @Transactional(readOnly = true)
  // public Map<String, Object> versions(String projectId, String root) {
  //   try ( Session session = driver.session() ) {
  //     String query = "MATCH (a {id: $root})" +
  //     "CALL apoc.path.expandConfig(a, {relationshipFilter:'>', uniqueness: 'RELATIONSHIP_GLOBAL'}) yield path \n" + 
  //     "WITH apoc.coll.toSet(apoc.coll.flatten(collect([r in relationships(path) WHERE TYPE(r)='UPDATES' | r.version]))) AS rel\n" + 
  //     "UNWIND rel as ru\n" + 
  //     "WITH ru AS res ORDER BY res\n" + 
  //     "RETURN collect(distinct res) as last";
        
  //     StatementResult result = session.run(query, Values.parameters("root", root));
  //     List<Integer> last = result.single().get("last").asList(Values.ofInteger());

  //     Map<String, Object> ret = new HashMap<String, Object>();
  //     if( last.size() == 0 ) return ret;

  //     ret.put("latest", last.get(last.size()-1));
  //     ret.put("available", last);
  //     return ret;
  //   }
  // }
  //
  // END MARKED AS DEPRECATED

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

      final List<Map<String, Object>> retVal = parseArtifactTree(result);

      // Update warnings map
      mWarnings.put(root, false);
      for( Map<String, Object> v: retVal) {
        if( v.containsKey("warnings") ){
          mWarnings.put(root, true);
        }
      }
      
      return retVal;
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

        if( maxModification.getOrDefault(root, -1) < version ){
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
        if( !containsChildOfType("Package", node, nodes, ids, values) ){
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
        if( label.equals("Package") || label.equals("Code") ){
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