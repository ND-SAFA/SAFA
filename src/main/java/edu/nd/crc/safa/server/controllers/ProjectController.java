package edu.nd.crc.safa.server.controllers;

import edu.nd.crc.safa.db.entities.application.ProjectApplicationEntity;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.repositories.sql.ProjectRepository;
import edu.nd.crc.safa.db.repositories.sql.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ProjectCreationResponse;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;
import edu.nd.crc.safa.server.services.FlatFileService;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.SynchronizeService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
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
    private final SynchronizeService synchronizeService;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ProjectService projectService,
                             FlatFileService flatFileService,
                             SynchronizeService synchronizeService) {
        super(projectRepository, projectVersionRepository);
        this.projectService = projectService;
        this.flatFileService = flatFileService;
        this.synchronizeService = synchronizeService;
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
}
