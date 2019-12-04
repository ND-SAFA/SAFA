package edu.nd.crc.safa.controller.projects;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import edu.nd.crc.safa.services.TreeService;

@RestController
public class TreesController {

  private final TreeService treeService;

  public TreesController(TreeService treeService) {
    this.treeService = treeService;
  }

  @GetMapping("/projects/{projId}/parents/{node}")
  public List<String> hazards(@PathVariable String projId, @PathVariable String node) {
    return treeService.parents(projId, node);
  }

  @GetMapping("/projects/{projId}/hazards/")
  public List<Map<String, Object>> hazards(@PathVariable String projId) {
    return treeService.hazards(projId);
  }

  @GetMapping("/projects/{projId}/trees/")
  public List<Map<String, Object>> trees(@PathVariable String projId) {
    return treeService.trees(projId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/")
  public List<Map<String, Object>> trees(@PathVariable String projId, @PathVariable String treeId) {
    return treeService.trees(projId, treeId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/versions/")
  public Map<String, Object> versions(@PathVariable String projId, @PathVariable String treeId) {
    return treeService.versions(projId, treeId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/versions/{version}")
  public List<Map<String, Object>> versions(@PathVariable String projId, @PathVariable String treeId, @PathVariable int version) {
    return treeService.versions(projId, treeId, version);
  }
}