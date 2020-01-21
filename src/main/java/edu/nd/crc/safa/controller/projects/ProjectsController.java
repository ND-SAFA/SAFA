package edu.nd.crc.safa.controller.projects;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import edu.nd.crc.safa.services.ProjectService;

@RestController
public class ProjectsController {

  private final ProjectService projectService;

  public ProjectsController(ProjectService projectService) {
    this.projectService = projectService;
  }

  @GetMapping("/projects/{projId}/parents/{node}")
  public List<String> hazards(@PathVariable String projId, @PathVariable String node) {
    return projectService.parents(projId, node);
  }

  @GetMapping("/projects/{projId}/hazards/")
  public List<Map<String, Object>> hazards(@PathVariable String projId) {
    return projectService.hazards(projId);
  }

  @GetMapping("/projects/{projId}/hazards/warnings")
  public Map<String, Boolean> hazardWarnings(@PathVariable String projId) {
    return projectService.hazardWarnings(projId);
  }

  @GetMapping("/projects/{projId}/trees/")
  public List<Map<String, Object>> trees(@PathVariable String projId) {
    return projectService.trees(projId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/")
  public List<Map<String, Object>> trees(@PathVariable String projId, @PathVariable String treeId) {
    return projectService.trees(projId, treeId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/versions/")
  public Map<String, Object> versions(@PathVariable String projId, @PathVariable String treeId) {
    return projectService.versions(projId, treeId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/versions/{version}")
  public List<Map<String, Object>> versions(@PathVariable String projId, @PathVariable String treeId, @PathVariable int version) {
    return projectService.versions(projId, treeId, version);
  }

  @GetMapping("/projects/{projId}/pull/")
  public boolean projectPull(@PathVariable String projId) {
    return projectService.projectPull(projId);
  }
}