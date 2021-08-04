package edu.nd.crc.safa.controllers;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import javax.servlet.http.HttpServletRequest;

import edu.nd.crc.safa.dao.Links;
import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.ProjectRepository;
import edu.nd.crc.safa.database.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.output.error.ResponseCodes;
import edu.nd.crc.safa.output.error.ServerError;
import edu.nd.crc.safa.output.responses.FlatFileResponse;
import edu.nd.crc.safa.output.responses.ProjectCreationResponse;
import edu.nd.crc.safa.output.responses.ServerResponse;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;
import edu.nd.crc.safa.services.TraceLinkService;

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
    private ArtifactRepository artifactRepository;
    private TraceLinkService traceLinkService;
    private ProjectRepository projectRepository;
    private ProjectVersionRepository projectVersionRepository;

    @Autowired
    public ProjectController(ProjectService projectService,
                             FlatFileService flatFileService,
                             ArtifactRepository artifactRepository,
                             TraceLinkService traceLinkService,
                             ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository) {
        this.projectService = projectService;
        this.flatFileService = flatFileService;
        this.artifactRepository = artifactRepository;
        this.traceLinkService = traceLinkService;
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
    }


    @PostMapping("projects/flat-files")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse uploadFile(@RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }
        Project project = new Project(); // TODO: extract name from TIM file
        this.projectRepository.save(project);
        FlatFileResponse flatFileResponse = this.flatFileService.parseFlatFiles(project, files);
        ProjectCreationResponse response = new ProjectCreationResponse(project, flatFileResponse);
        response.setFlatFileResponse(flatFileResponse);
        return new ServerResponse(project);
    }

    @GetMapping("projects/{projectId}/flat-files/")
    public ServerResponse getUploadedFile(@PathVariable String projectId,
                                          @RequestParam String filename) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(flatFileService.getUploadedFile(project, filename));
    }

    @GetMapping("projects/{projectId}/clear/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void clearUploadedFlatFiles(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        flatFileService.clearUploadedFiles(project);
    }

    @GetMapping("projects/{projectId}/uploaderrorlog/")
    public ServerResponse getUploadFilesErrorLog(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(flatFileService.getUploadErrorLog(project));
    }

    @GetMapping("projects/{projectId}/linkerrorlog/")
    public ServerResponse getLinkErrorLog(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(flatFileService.getLinkErrorLog(project));
    }

    @GetMapping("projects/{projectId}/generate/")
    public void generateLinks(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion projectVersion = getCurrentVersion(project);
        flatFileService.generateLinks(project, projectVersion); //TODO: return any error logs
    }

    @GetMapping("projects/{projectId}/linktypes/")
    public ServerResponse getLinkTypes(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(traceLinkService.getLinkTypes(project));
    }

    @GetMapping("projects/{projectId}/remove/")
    public void removeGeneratedFlatFiles(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        flatFileService.clearGeneratedFiles(project);
    }

    /**
     * Versioning, deltas, nodes
     */
    @GetMapping("projects/{projectId}/parents/{node}")
    public ServerResponse parents(@PathVariable String projectId,
                                  @PathVariable String node,
                                  @RequestParam String rootType) throws ServerError {
        return new ServerResponse(projectService.parents(projectId, node, rootType));
    }

    @GetMapping("projects/{projectId}/nodes/")
    public ServerResponse nodes(@PathVariable String projectId,
                                @RequestParam String nodeType) throws ServerError {
        return new ServerResponse(projectService.nodes(projectId, nodeType));
    }

    @GetMapping("projects/{projectId}/nodes/warnings")
    public ServerResponse nodeWarnings(@PathVariable String projectId) {
        return new ServerResponse(projectService.nodeWarnings(projectId));
    }

    @GetMapping("projects/{projectId}/trees/")
    public ServerResponse trees(@PathVariable String projectId,
                                @RequestParam String rootType) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(projectService.trees(project, rootType));
    }

    @GetMapping("projects/{projectId}/trees/{treeId}/")
    public ServerResponse tree(@PathVariable String projectId,
                               @PathVariable String treeId,
                               @RequestParam String rootType) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(projectService.tree(project, treeId, rootType));
    }

    @GetMapping("projects/{projectId}/versions/")
    public ServerResponse versions(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(projectService.versions(project));
    }

    @GetMapping("projects/{projectId}/trees/{treeId}/versions/{version}")
    public ServerResponse versions(@PathVariable String projectId,
                                   @PathVariable String treeId,
                                   @PathVariable int version,
                                   @RequestParam String rootType) throws ServerError {
        Project project = getProject(projectId);
        return new ServerResponse(projectService.versions(project, treeId, version, rootType));
    }

    @PostMapping("projects/{projectId}/versions/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse versionsTag(@PathVariable String projectId) {
        return new ServerResponse(projectService.versionsTag(projectId));
    }

    @GetMapping("projects/{projectId}/pull/")
    public ServerResponse projectPull(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion projectVersion = getCurrentVersion(project);
        return new ServerResponse(projectService.projectPull(project, projectVersion));
    }

    @PostMapping("projects/{projectId}/trees/{treeId}/layout/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse postTreeLayout(@PathVariable String projectId,
                                         @PathVariable String treeId,
                                         @RequestBody String b64EncodedLayout) throws Exception {
        Project project = getProject(projectId);
        projectService.postTreeLayout(project, treeId, b64EncodedLayout);
        return new ServerResponse("Layout");
    }

    @GetMapping(value = "projects/{projectId}/trees/{treeId}/layout/")
    public String getTreeLayout(@PathVariable String projectId, @PathVariable String treeId) throws ServerError {
        Project project = getProject(projectId);
        return projectService.getTreeLayout(project, treeId);
    }

    // Warnings
    @GetMapping("projects/{projectId}/warnings/")
    public Map<String, String> getWarnings(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        return projectService.getWarnings(project);
    }

    @PostMapping("projects/{projectId}/warnings/")
    @ResponseStatus(HttpStatus.CREATED)
    public void newWarning(@PathVariable String projectId,
                           @RequestParam("short") String nShort,
                           @RequestParam("long") String nLong,
                           @RequestParam("rule") String rule) throws ServerError {
        Project project = getProject(projectId);
        projectService.newWarning(project, nShort, nLong, rule);
    }

    // Links
    @GetMapping("projects/{projectId}/link/")
    public ServerResponse getLink(@PathVariable String projectId,
                                  @RequestParam("source") String source,
                                  @RequestParam("target") String target) {
        return new ServerResponse(projectService.getLink(projectId, source, target));
    }

    @PostMapping("projects/{projectId}/link/")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ServerResponse updateLink(@PathVariable String projectId, @RequestBody Links links) {
        return new ServerResponse(projectService.updateLink(projectId, links));
    }

    // Artifacts
    @GetMapping("projects/{projectId}/artifact/")
    public ServerResponse getArtifacts(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        List<Artifact> artifact = artifactRepository.findByProject(project);
        return new ServerResponse(artifact);
    }

    @GetMapping("projects/{projectId}/artifact/{source}/links")
    public ServerResponse getArtifactLinks(@PathVariable String projectId,
                                           @PathVariable String source,
                                           @RequestParam("target") String target,
                                           @RequestParam(name = "minScore", defaultValue = "0.0")
                                               Double minScore) {
        return new ServerResponse(projectService.getArtifactLinks(projectId, source, target, minScore));
    }

    @ExceptionHandler(ServerError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleServerError(HttpServletRequest req,
                                            ServerError exception) {
        exception.getError().printStackTrace();
        return new ServerResponse(exception, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleGenericError(HttpServletRequest req,
                                             Exception ex) {
        ex.printStackTrace();
        ServerError wrapper = new ServerError("unknown activity", ex);
        return new ServerResponse(wrapper, ResponseCodes.FAILURE);
    }

    private Project getProject(String projectId) throws ServerError {
        Optional<Project> queriedProject = this.projectRepository.findById(UUID.fromString(projectId));
        if (!queriedProject.isPresent()) {
            throw new ServerError("Could not find project with id:" + projectId);
        }
        return queriedProject.get();
    }

    private ProjectVersion getCurrentVersion(Project project) {
        return this.projectVersionRepository.findTopByProjectOrderByVersionIdDesc(project);
    }
}
