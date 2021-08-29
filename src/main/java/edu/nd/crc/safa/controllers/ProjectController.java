package edu.nd.crc.safa.controllers;

import java.util.List;

import edu.nd.crc.safa.entities.database.Artifact;
import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.ProjectVersion;
import edu.nd.crc.safa.repositories.ArtifactRepository;
import edu.nd.crc.safa.repositories.ProjectRepository;
import edu.nd.crc.safa.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.responses.ProjectCreationResponse;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.responses.ServerResponse;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ProjectController extends BaseController {

    private final ProjectService projectService;
    private final FlatFileService flatFileService;
    private final ArtifactRepository artifactRepository;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService,
                             FlatFileService flatFileService,
                             ArtifactRepository artifactRepository) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.flatFileService = flatFileService;
        this.artifactRepository = artifactRepository;
    }

    @CrossOrigin
    @PostMapping("projects/flat-files")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse uploadFile(@RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }
        Project project = new Project(); // TODO: extract name from TIM file
        this.projectRepository.save(project);
        ProjectCreationResponse response = this.flatFileService.createProjectFromFlatFiles(project, files);
        return new ServerResponse(response);
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

    @GetMapping("projects/{projectId}/remove/")
    public void removeGeneratedFlatFiles(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        flatFileService.clearGeneratedFiles(project);
    }

    @GetMapping("projects/{projectId}/pull/")
    public ServerResponse projectPull(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion projectVersion = getCurrentVersion(project);
        return new ServerResponse(projectService.projectPull(project, projectVersion));
    }

    @GetMapping("projects/{projectId}/artifact/")
    public ServerResponse getArtifacts(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        List<Artifact> artifact = artifactRepository.findByProject(project);
        return new ServerResponse(artifact);
    }
}
