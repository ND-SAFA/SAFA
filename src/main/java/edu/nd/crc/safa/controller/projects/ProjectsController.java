package edu.nd.crc.safa.controller.projects;

import java.util.List;
import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

import edu.nd.crc.safa.services.ProjectService;
import edu.nd.crc.safa.dao.Layout;

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

  @GetMapping("/projects/{projId}/uploaderrorlog/")
  public String getUploadFilesErrorLog(@PathVariable String projId) {
    System.out.println("/projects/{projId}/uploaderrorlog/");
    return projectService.getUploadFilesErrorLog(projId);
  }

  @GetMapping("/projects/{projId}/linkerrorlog/")
  public String getLinkErrorLog(@PathVariable String projId) {
    System.out.println("/projects/{projId}/errorlog/");
    return projectService.getLinkErrorLog(projId);
  }

  @GetMapping("/projects/{projId}/generate/")
  public String generateLinks(@PathVariable String projId) {
    System.out.println("/projects/{projId}/generate/");
    return projectService.generateLinks(projId);
  }

  // @GetMapping("/projects/{projId}/linkserrorlog/")
  // public String getGenerateLinksErrorLog(@PathVariable String projId) {
  //   System.out.println("/projects/{projId}/generate/");
  //   return projectService.getGenerateLinksErrorLog(projId);
  // }

  @GetMapping("/projects/{projId}/linktypes/")
  public String getLinkTypes(@PathVariable String projId) {
    System.out.println("/projects/{projId}/linktypes/");
    return projectService.getLinkTypes(projId);
  }

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

  @PostMapping("/projects/{projId}/trees/{treeId}/layout/")
  public String postTreeLayout(@PathVariable String projId, @PathVariable String treeId, @RequestBody String b64EncodedLayout) {
    try {
      return projectService.postTreeLayout(projId, treeId, b64EncodedLayout);
    } catch (Exception e) {
      throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage());
    }
  }
  
  @GetMapping(value = "/projects/{projId}/trees/{treeId}/layout/")
  public String getTreeLayout(@PathVariable String projId, @PathVariable String treeId) {
    try {
      return projectService.getTreeLayout(projId, treeId);
    } catch (Exception e) {
      throw new ResponseStatusException(HttpStatus.NOT_FOUND);
    }
  }
  
  // Warnings
  @GetMapping("/projects/{projId}/warnings/")
  public Map<String,String> getWarnings(@PathVariable String projId) {
    return projectService.getWarnings(projId);
  }

  @PostMapping("/projects/{projId}/warnings/")
  public void newWarning(@PathVariable String projId, @RequestParam("name") String name, @RequestParam("rule") String rule) {
    projectService.newWarning(projId, name, rule);
  }

  // Links
  @GetMapping("/projects/{projId}/link/")
  public Map<String, String> getLink(@PathVariable String projId, @RequestParam("source") String source, @RequestParam("target") String target) {
    return projectService.getLink(projId, source, target);
  }

  @PostMapping("/projects/{projId}/link/")
  public Map<String, String> updateLink(@PathVariable String projId, @RequestParam("source") String source, @RequestParam("target") String target, @RequestParam("approval") Integer approval) {
    return projectService.updateLink(projId, source, target, approval);
  }

  // Artifacts
  @GetMapping("/projects/{projId}/artifact/")
  public Map<String, Object> getArtifacts(@PathVariable String projId) {
    return projectService.getArtifacts(projId);
  }

  @GetMapping("/projects/{projId}/artifact/{source}/links")
  public Map<String, Object> getArtifactLinks(@PathVariable String projId, @PathVariable String source, @RequestParam("target") String target) {
    return projectService.getArtifactLinks(projId, source, target);
  }
}