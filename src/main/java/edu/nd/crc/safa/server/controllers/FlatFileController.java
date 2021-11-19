package edu.nd.crc.safa.server.controllers;

import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.importer.flatfiles.FlatFileService;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.FileUploadService;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;
import edu.nd.crc.safa.server.services.RevisionNotificationService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class FlatFileController extends BaseController {

    private final FileUploadService fileUploadService;
    private final RevisionNotificationService revisionNotificationService;
    private final FlatFileService flatFileService;
    private final ProjectRetrievalService projectRetrievalService;

    @Autowired
    public FlatFileController(ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              FileUploadService fileUploadService,
                              RevisionNotificationService revisionNotificationService,
                              FlatFileService flatFileParser,
                              ProjectRetrievalService projectRetrievalService) {
        super(projectRepository, projectVersionRepository);
        this.revisionNotificationService = revisionNotificationService;
        this.fileUploadService = fileUploadService;
        this.flatFileService = flatFileParser;
        this.projectRetrievalService = projectRetrievalService;
    }

    /**
     * Uploads and parses given flat files to the specified version.
     *
     * @param versionId - The id of the version that will be modified by given files.
     * @param files     - The flat files containing tim.json, artifact files, and trace link files.
     * @return ServerResponse whose body contains all entities in project created.
     * @throws ServerError - If no files are given.
     */
    @PostMapping(value = Routes.updateProjectVersionFromFlatFiles)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse updateProjectVersionFromFlatFiles(
        @PathVariable UUID versionId,
        @RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        Project project = projectVersion.getProject();
        ProjectEntities response = this.uploadAndCreateProjectFromFlatFiles(
            project,
            projectVersion,
            files);
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
        return new ServerResponse(response);
    }

    /**
     * Creates a new project using the given flat files to create the project arifacts, traces, and artifact types.
     *
     * @param files Files including artifact and traces files and requiring at minimum a Tim.json file.
     * @return ProjectCreationResponse containing project artifacts, traces, and warnings.
     * @throws ServerError Throws errors if tim.json file does not exist or an error occurred while parsing it.
     */
    @PostMapping(value = Routes.projectFlatFiles)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewProjectFromFlatFiles(@RequestParam MultipartFile[] files) throws ServerError {
        if (files.length == 0) {
            throw new ServerError("Could not create project because no files were received.");
        }

        Project project = createProjectIdentifier(null, null);
        ProjectVersion projectVersion = createProjectVersion(project);

        ProjectEntities response = this.uploadAndCreateProjectFromFlatFiles(project,
            projectVersion,
            files);
        this.revisionNotificationService.broadcastUpdateProject(projectVersion);
        return new ServerResponse(response);
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project        The project whose artifacts and trace links should be associated with
     * @param projectVersion The version that the artifacts and errors will be associated with.
     * @param files          the flat files defining the project
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws ServerError on any parsing error of tim.json, artifacts, or trace links
     */
    private ProjectEntities uploadAndCreateProjectFromFlatFiles(Project project,
                                                                ProjectVersion projectVersion,
                                                                MultipartFile[] files)
        throws ServerError {

        this.fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
        this.flatFileService.parseProjectFilesFromTIM(projectVersion);
        return this.projectRetrievalService.retrieveAndCreateProjectResponse(projectVersion);
    }
}
