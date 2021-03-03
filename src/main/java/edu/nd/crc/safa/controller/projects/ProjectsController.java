package edu.nd.crc.safa.controller.projects;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
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
  public List<Map<String, Object>> versions(@PathVariable String projId, @PathVariable String treeId, @PathVariable int version) {
    return projectService.versions(projId, treeId, version);
  }

  @GetMapping("/projects/{projId}/pull/")
  public SseEmitter projectPull(@PathVariable String projId) {
    return projectService.projectPull(projId);
  }
}