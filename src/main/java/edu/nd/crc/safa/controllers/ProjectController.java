package edu.nd.crc.safa.controllers;

import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import edu.nd.crc.safa.dao.Links;
import edu.nd.crc.safa.error.ResponseCodes;
import edu.nd.crc.safa.error.ServerError;
import edu.nd.crc.safa.responses.ProjectCreationResponse;
import edu.nd.crc.safa.responses.ServerResponse;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;


@RestController
public class ProjectController {

    private ProjectService projectService;
    private FlatFileService flatFileService;

    @Autowired
    public ProjectController(ProjectService projectService, FlatFileService flatFileService) {
        this.projectService = projectService;
        this.flatFileService = flatFileService;
    }

    /* Flat File Routes
     * Includes the ability to upload, download, and remove flat files
     */
    @PostMapping(value = "/projects/flat-files")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse uploadProjectFiles(@RequestParam("files") MultipartFile[] files) {
        ProjectCreationResponse response = new ProjectCreationResponse();
        response.setFilesReceived(files);
        return new ServerResponse(response);
    }

    @PostMapping("projects/{projId}/upload/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse uploadFile(@PathVariable String projId,
                                     @RequestBody String encodedStr) throws ServerError {
        return new ServerResponse(flatFileService.uploadAndParseFile(projId, encodedStr));
    }

    @GetMapping("projects/{projId}/upload/")
    public ServerResponse getUploadedFile(@PathVariable String projId,
                                          @RequestParam String filename) throws ServerError {
        return new ServerResponse(flatFileService.getUploadedFile(projId, filename));
    }

    @GetMapping("projects/{projId}/clear/")
    public ServerResponse clearUploadedFlatfiles(@PathVariable String projId) throws ServerError {
        return new ServerResponse(flatFileService.clearUploadedFlatFiles(projId));
    }

    @GetMapping("projects/{projId}/uploaderrorlog/")
    public ServerResponse getUploadFilesErrorLog(@PathVariable String projId) throws ServerError {
        System.out.println("/projects/{projId}/uploaderrorlog/");
        return new ServerResponse(flatFileService.getUploadFilesErrorLog(projId));
    }

    @GetMapping("projects/{projId}/linkerrorlog/")
    public ServerResponse getLinkErrorLog(@PathVariable String projId) throws ServerError {
        System.out.println("/projects/{projId}/errorlog/");
        return new ServerResponse(flatFileService.getLinkErrorLog(projId));
    }

    @GetMapping("projects/{projId}/generate/")
    public ServerResponse generateLinks(@PathVariable String projId) throws ServerError {
        return new ServerResponse(flatFileService.generateLinks(projId));
    }

    @GetMapping("projects/{projId}/linktypes/")
    public ServerResponse getLinkTypes(@PathVariable String projId) throws ServerError {
        return new ServerResponse(flatFileService.getLinkTypes(projId));
    }

    @GetMapping("projects/{projId}/remove/")
    public ServerResponse removeGeneratedFlatFiles(@PathVariable String projId) throws ServerError {
        return new ServerResponse(flatFileService.clearGeneratedFlatFiles(projId));
    }

    /* Versioning, deltas, nodes
     *
     */
    @GetMapping("projects/{projId}/parents/{node}")
    public ServerResponse parents(@PathVariable String projId,
                                  @PathVariable String node,
                                  @RequestParam String rootType) throws ServerError {
        return new ServerResponse(projectService.parents(projId, node, rootType));
    }

    @GetMapping("projects/{projId}/nodes/")
    public ServerResponse nodes(@PathVariable String projId,
                                @RequestParam String nodeType) throws ServerError {
        return new ServerResponse(projectService.nodes(projId, nodeType));
    }

    @GetMapping("projects/{projId}/nodes/warnings")
    public ServerResponse nodeWarnings(@PathVariable String projId) {
        return new ServerResponse(projectService.nodeWarnings(projId));
    }

    @GetMapping("projects/{projId}/trees/")
    public ServerResponse trees(@PathVariable String projId,
                                @RequestParam String rootType) throws ServerError {
        return new ServerResponse(projectService.trees(projId, rootType));
    }

    @GetMapping("projects/{projId}/trees/{treeId}/")
    public ServerResponse tree(@PathVariable String projId,
                               @PathVariable String treeId,
                               @RequestParam String rootType) throws ServerError {
        return new ServerResponse(projectService.tree(projId, treeId, rootType));
    }

    @GetMapping("projects/{projId}/versions/")
    public ServerResponse versions(@PathVariable String projId) throws ServerError {
        return new ServerResponse(projectService.versions(projId));
    }

    @GetMapping("projects/{projId}/trees/{treeId}/versions/{version}")
    public ServerResponse versions(@PathVariable String projId,
                                   @PathVariable String treeId,
                                   @PathVariable int version,
                                   @RequestParam String rootType) throws ServerError {
        return new ServerResponse(projectService.versions(projId, treeId, version, rootType));
    }

    @PostMapping("projects/{projId}/versions/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse versionsTag(@PathVariable String projId) {
        return new ServerResponse(projectService.versionsTag(projId));
    }

    @GetMapping("projects/{projId}/pull/")
    public ServerResponse projectPull(@PathVariable String projId) {
        return new ServerResponse(projectService.projectPull(projId));
    }

    @PostMapping("projects/{projId}/trees/{treeId}/layout/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse postTreeLayout(@PathVariable String projId,
                                         @PathVariable String treeId,
                                         @RequestBody String b64EncodedLayout) throws Exception {
        projectService.postTreeLayout(projId, treeId, b64EncodedLayout);
        return new ServerResponse("Layout");
    }

    @GetMapping(value = "projects/{projId}/trees/{treeId}/layout/")
    public String getTreeLayout(@PathVariable String projId, @PathVariable String treeId) throws ServerError {
        return projectService.getTreeLayout(projId, treeId);
    }

    // Warnings
    @GetMapping("projects/{projId}/warnings/")
    public Map<String, String> getWarnings(@PathVariable String projId) {
        return projectService.getWarnings(projId);
    }

    @PostMapping("projects/{projId}/warnings/")
    @ResponseStatus(HttpStatus.CREATED)
    public void newWarning(@PathVariable String projId,
                           @RequestParam("short") String nShort,
                           @RequestParam("long") String nLong,
                           @RequestParam("rule") String rule) {
        projectService.newWarning(projId, nShort, nLong, rule);
    }

    // Links
    @GetMapping("projects/{projId}/link/")
    public ServerResponse getLink(@PathVariable String projId,
                                  @RequestParam("source") String source,
                                  @RequestParam("target") String target) {
        return new ServerResponse(projectService.getLink(projId, source, target));
    }

    @PostMapping("projects/{projId}/link/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse updateLink(@PathVariable String projId, @RequestBody Links links) {
        return new ServerResponse(projectService.updateLink(projId, links));
    }

    // Artifacts
    @GetMapping("projects/{projId}/artifact/")
    public ServerResponse getArtifacts(@PathVariable String projId) {
        return new ServerResponse(projectService.getArtifacts(projId));
    }

    @GetMapping("projects/{projId}/artifact/{source}/links")
    public ServerResponse getArtifactLinks(@PathVariable String projId,
                                           @PathVariable String source,
                                           @RequestParam("target") String target,
                                           @RequestParam(name = "minScore", defaultValue = "0.0")
                                               Double minScore) {
        return new ServerResponse(projectService.getArtifactLinks(projId, source, target, minScore));
    }

    @ExceptionHandler(ServerError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleServerError(HttpServletRequest req,
                                            ServerError exception) {
        return new ServerResponse(exception, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleGenericError(HttpServletRequest req,
                                             Exception ex) {
        ServerError wrapper = new ServerError("unknown activity", ex);
        return new ServerResponse(wrapper, ResponseCodes.FAILURE);
    }
}
