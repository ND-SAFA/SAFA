package edu.nd.crc.safa.controller.projects;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import edu.nd.crc.safa.services.ProjectService;

@RestController
public class ProjectsController {

  private final ProjectService projectService;

  public ProjectsController(ProjectService projectService) {
    this.projectService = projectService;
  }

  @GetMapping("/projects/{projId}/parents/{node}")
  public List<String> parents(@PathVariable String projId, @PathVariable String node, @RequestParam String rootType) {
    return projectService.parents(projId, node, rootType);
  }

  @GetMapping("/projects/{projId}/nodes/")
  public List<Map<String, Object>> nodes(@PathVariable String projId, @RequestParam String nodeType) {
    return projectService.nodes(projId, nodeType);
  }

  @GetMapping("/projects/{projId}/nodes/warnings")
  public Map<String, Boolean> nodeWarnings(@PathVariable String projId) {
    return projectService.nodeWarnings(projId);
  }

  @GetMapping("/projects/{projId}/trees/")
  public List<Map<String, Object>> trees(@PathVariable String projId, @RequestParam String rootType) {
    return projectService.trees(projId, rootType);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/")
  public List<Map<String, Object>> tree(@PathVariable String projId, @PathVariable String treeId, @RequestParam String rootType) {
    return projectService.tree(projId, treeId, rootType);
  }

  @GetMapping("/projects/{projId}/versions/")
  public Map<String, Object> versions(@PathVariable String projId) {
    return projectService.versions(projId);
  }

  @PostMapping("/projects/{projId}/versions/")
  public Map<String, Object> versionsTag(@PathVariable String projId) {
    return projectService.versionsTag(projId);
  }

  @GetMapping("/projects/{projId}/clear/")
  public String clearUploadedFlatfiles(@PathVariable String projId){
    return projectService.clearUploadedFlatfiles(projId);
  }

  @PostMapping("/projects/{projId}/upload/")
  public String uploadFile(@PathVariable String projId, @RequestBody String encodedStr) {
    System.out.println("/projects/{projId}/upload/");
    return projectService.uploadFile(projId, encodedStr);
  }

  @GetMapping("/projects/{projId}/errorlog/")
  public String getUploadFilesErrorLog(@PathVariable String projId) {
    System.out.println("/projects/{projId}/errorlog/");
    return projectService.getUploadFilesErrorLog(projId);
  }

  // @GetMapping("/projects/{projId}/generate/")
  // public String generateLinks(@PathVariable String projId) {
  //   System.out.println("/projects/{projId}/generate/");
  //   return projectService.generateLinks(projId);
  // }

  // @GetMapping("/projects/{projId}/linkserrorlog/")
  // public String getGenerateLinksErrorLog(@PathVariable String projId) {
  //   System.out.println("/projects/{projId}/generate/");
  //   return projectService.getGenerateLinksErrorLog(projId);
  // }

  // @GetMapping("/projects/{projId}/linktypes/")
  // public String getLinkTypes(@PathVariable String projId) {
  //   System.out.println("/projects/{projId}/linktypes/");
  //   return projectService.getLinkTypes(projId);
  // }

  @GetMapping("/projects/{projId}/remove/")
  public String clearGeneratedFlatfiles(@PathVariable String projId) {
    System.out.println("/projects/{projId}/generate/");
    return projectService.clearGeneratedFlatfiles(projId);
  }

  @GetMapping("/projects/{projId}/trees/{treeId}/versions/{version}")
  public List<Map<String, Object>> versions(@PathVariable String projId, @PathVariable String treeId, @PathVariable int version, @RequestParam String rootType) {
    return projectService.versions(projId, treeId, version, rootType);
  }

  @GetMapping("/projects/{projId}/pull/")
  public SseEmitter projectPull(@PathVariable String projId) {
    return projectService.projectPull(projId);
  }
}