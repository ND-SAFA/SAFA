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
  public String clearFlatfileDir(){
    try {
      return projectService.clearFlatfileDir();  // only keep for testing if you want directory to clear before re-uploading. 
    }
    catch(Exception e){
      return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
    }
  }

  @PostMapping("/projects/{projId}/upload/")
  public String uploadFile(@PathVariable String projId, @RequestBody String encodedStr) {
    System.out.println("/projects/{projId}/upload/");
    try {
      projectService.uploadFile(projId, encodedStr);
      try {
        return projectService.missingFiles(projId);
      } 
      catch(Exception e){
        System.out.println("Missing Files Error");
        if (e.getClass().getName().equals("com.jsoniter.spi.JsonException")) {
          System.out.println("com.jsoniter.spi.JsonException");
          return "{ \"success\": false, \"message\": \"Error parsing tim.json file: File does not match expected tim.json structure\"}";
        }
        else if (e.getMessage().equals("Please upload a tim.json file")){
          return String.format("{ \"success\": false, \"message\": \"%s\"}", e.getMessage());
        }
        else {
          return String.format("{ \"success\": false, \"message\": \"Error checking for missing files: %s\"}", e.toString());
        }
      }

    } 
    catch(Exception e){
      System.out.println("uploadFile Error");
      if (e.getClass().getName().equals("com.jsoniter.spi.JsonException")) {
        System.out.println("com.jsoniter.spi.JsonException");
        return "{ \"success\": false, \"message\": \"Error uploading Flatfiles: Could not parse API JSON body.\"}";
      }
      else {
        System.out.println("Error uploading Flatfiles: OTHER");
        return String.format("{ \"success\": false, \"message\": \"Error uploading Flatfiles: %s\"}", e.toString());
      }
    }
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