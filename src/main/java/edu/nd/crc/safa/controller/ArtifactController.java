package edu.nd.crc.safa.controller;

import java.util.Collection;
// import java.util.Map;

import edu.nd.crc.safa.domain.Artifact;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import edu.nd.crc.safa.services.ArtifactService;

/**
 * @author Mark Angrish
 * @author Michael J. Simons
 */
@RestController
@RequestMapping("/")
public class ArtifactController {

	private final ArtifactService artifactService;
	
	public ArtifactController(ArtifactService artifactService) {
		this.artifactService = artifactService;
	}

  @GetMapping("/tree")
  public Collection<Artifact> graph(@RequestParam(value = "root", required = true) String root, 
                                    @RequestParam(value = "limit", required = false) Integer limit) {
		return artifactService.tree(root, limit == null ? 100 : limit);
	}
}