package edu.nd.crc.safa.controller.projects;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import edu.nd.crc.safa.services.TreeService;

@RestController
public class TreesController {

	private final TreeService treeService;
	
	public TreesController(TreeService treeService) {
		this.treeService = treeService;
	}

  @GetMapping("/projects/{id}/trees")
  public List<Map<String, Object>> trees(@PathVariable String id, @RequestParam(value = "root", required = false) String root) {
    String projectId = id;
    if (root != null) {
      return treeService.trees(projectId, root);
    } 
    return treeService.hazards(projectId);
  } 
}