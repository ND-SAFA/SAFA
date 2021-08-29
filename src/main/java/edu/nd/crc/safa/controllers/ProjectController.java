package edu.nd.crc.safa.controllers;

import edu.nd.crc.safa.entities.application.ProjectApplicationEntity;
import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.ProjectVersion;
import edu.nd.crc.safa.repositories.ProjectRepository;
import edu.nd.crc.safa.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.responses.ProjectCreationResponse;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.responses.ServerResponse;
import edu.nd.crc.safa.services.FlatFileService;
import edu.nd.crc.safa.services.ProjectService;
import edu.nd.crc.safa.services.PullingService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@CrossOrigin
@RestController
public class ProjectController extends BaseController {

    private final ProjectService projectService;
    private final FlatFileService flatFileService;
    private final PullingService pullingService;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService,
                             FlatFileService flatFileService,
                             PullingService pullingService) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.flatFileService = flatFileService;
        this.pullingService = pullingService;
    }

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

    @PostMapping("projects/")
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@RequestBody ProjectApplicationEntity project) {
        ProjectCreationResponse response = this.projectService.createOrUpdateProject(project);
        return new ServerResponse(response);
    }

    @CrossOrigin
    @GetMapping("projects/")
    public ServerResponse getProjects() {
        return new ServerResponse(this.projectRepository.findAll());
    }

    @GetMapping("projects/{projectId}/pull/")
    public ServerResponse projectPull(@PathVariable String projectId) throws ServerError {
        Project project = getProject(projectId);
        ProjectVersion projectVersion = getCurrentVersion(project);
        return new ServerResponse(pullingService.projectPull(project, projectVersion));
    }
}
