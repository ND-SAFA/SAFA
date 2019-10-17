package edu.nd.crc.safa.services;

// import java.util.ArrayList;
import java.util.Collection;
// import java.util.HashMap;
// import java.util.Iterator;
// import java.util.List;
// import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import edu.nd.crc.safa.domain.Artifact;
// import edu.nd.crc.safa.domain.ArtifactConstraint;
import edu.nd.crc.safa.repositories.ArtifactRepository;

@Service
public class ArtifactService {

  private final static Logger LOG = LoggerFactory.getLogger(ArtifactService.class);

	private final ArtifactRepository artifactRepository;
	public ArtifactService(ArtifactRepository artifactRepository) {
		this.artifactRepository = artifactRepository;
	}

	// private Map<String, Object> toD3Format(Collection<Artifact> artifacts) {
	// 	List<Map<String, Object>> nodes = new ArrayList<>();
	// 	List<Map<String, Object>> rels = new ArrayList<>();
	// 	int i = 0;
	// 	Iterator<Artifact> result = artifacts.iterator();
	// 	while (result.hasNext()) {
	// 		Artifact artifact = result.next();
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
  public Artifact findByName(String name) {
    Artifact result = artifactRepository.findByName(name);
    return result;
  }

	@Transactional(readOnly = true)
	public Collection<Artifact> tree(String root, int limit) {
    LOG.info(root);
		Collection<Artifact> result = artifactRepository.tree(root, limit);
    return result;
	}
}