package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.Collection;
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

// let trees;
//   if (delta.length) {
//     trees = [dataDelta.trees[rootId]];
//   } else {
//     trees = rootId ? [data.trees[rootId]] : Object.values(data.trees);
//   }
//   const elements = [];
//   // Iterate over root nodes
//   for (const tree of trees) {
//     tree['root-node'].__type = 'Hazard';
//     const stack = [tree['root-node']];
//     while (stack.length > 0) {
//       const current = stack.shift();
//       let classes = 'node';
//       // Add current node to elements
//       let label = `${current.__type}\n${current.id}\n${current.name}`;
//       if (current.__type === 'AcceptanceTest') {
//         label = `Acceptance test passed\n${current.id}\n${current.name}`;
//       } else if (current.__type === 'Package') {
//         // split ID along '\n' character to get ID and package name
//         const packageName = current.id.split('\\n');
//         label = `Package\n${packageName[0]}\n${packageName[1]}`;
//       } else if (current.__type === 'Code') {
//         // Parse file name from the end of current.name
//         const slashIndex = current.name.lastIndexOf('/');
//         const fileName = current.name.slice(slashIndex + 1);
//         label = `Code with\nPassed Tests\n${fileName}`;
//       }
//       if (current['is-delegated']) {
//         label = `Delegated to Adjacent System\n${current.id}\n${current.name}`;
//       }
//       if (current['is-modified']) {
//         classes = 'node_modified';
//       }
//       if (current['is-new']) {
//         classes = 'node_new';
//       }
//       if (current['is-deleted']) {
//         classes = 'node_deleted';
//       }
//       elements.push({
//         data: {
//           id: current.id,
//           label: label,
//           // TODO replace with valid link to issue tracker
//           href: 'https://notredamus.atlassian.net/browse/SAFA-14'
//         },
//         classes: classes
//       });
//       // Add an edge for each child
//       const children = Object.entries(current.children);
//       for (const [childType, childArray] of children) {
//         for (const child of childArray) {
//           elements.push({
//             data: {
//               source: current.id,
//               target: child.DATA.id
//             }
//           });
//           // Add child node to stack including node type
//           child.DATA.__type = childType;
//           stack.unshift(child.DATA);
//         }
//       }
//     }

  // private Map<String, Object> toCustomCytoscapeFormat(Collection<Tree> artifacts) {
  //   artifacts.forEach(a -> System.out.println(a.getData()));
  //   return new HashMap<String, Object>(2);
  //   for each artifact 
  // }

	// private Map<String, Object> toD3Format(Collection<Tree> artifacts) {
	// 	List<Map<String, Object>> nodes = new ArrayList<>();
	// 	List<Map<String, Object>> rels = new ArrayList<>();
  //   int i = 0;
	// 	Iterator<Tree> result = artifacts.iterator();
	// 	while (result.hasNext()) {
	// 		Tree artifact = result.next();
	// 		nodes.add(map("title", artifact.getTitle(), "label", "artifact"));
	// 		int target = i;
	// 		i++;
	// 		for (Role role : artifact.getRoles()) {
	// 			Map<String, Object> actor = map("title", role.getPerson().getName(), "label", "actor");
	// 			int source = nodes.indexOf(actor);
	// 			if (source == -1) {
	// 				nodes.add(actor);
	// 				source = i++;
	// 			}
	// 			rels.add(map("source", source, "target", target));
	// 		}
	// 	}
	// 	return map("nodes", nodes, "links", rels);
	// }

	// private Map<String, Object> map(String key1, Object value1, String key2, Object value2) {
	// 	Map<String, Object> result = new HashMap<String, Object>(2);
	// 	result.put(key1, value1);
	// 	result.put(key2, value2);
	// 	return result;
  // }

  
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
        Map<String, Object> mapping = new HashMap<String, Object>(node.asMap());
        mapping.put("classes", "node");
        values.add(mapping);
        LOG.debug("[NODE " + node.id() +"] " + mapping);
      }
      return values;
    }
  }

  private List<Map<String, Object>> convertToEdgesNodes(StatementResult result) {
    List<Map<String, Object>> values = new ArrayList<>();
    Map<Long, String> ids = new HashMap<>();
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
          LOG.debug("[EDGE " + rel.id() + ": " + rel.type() + "] from: " + ids.get(rel.startNodeId()) + ", to: " + ids.get(rel.endNodeId()));
          Map<String, Object> mapping = new HashMap<String, Object>(); 
          mapping.put("classes", "edge");
          mapping.put("id", rel.id());
          mapping.put("type", rel.type());
          mapping.put("source", ids.get(rel.startNodeId()));
          mapping.put("target", ids.get(rel.endNodeId()));
          values.add(mapping);
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
  
  private static <T> Collection<T>  
                  getCollectionFromIterable(Iterable<T> itr) 
  { 
      // Create an empty Collection to hold the result 
      Collection<T> cltn = new ArrayList<T>(); 

      // Iterate through the iterable to 
      // add each element into the collection 
      for (T t : itr) 
          cltn.add(t); 

      // Return the converted collection 
      return cltn; 
  } 
}