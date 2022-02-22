package edu.nd.crc.safa.server.controllers;

import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.importer.flatfiles.FlatFileService;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.FileUploadService;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;
import edu.nd.crc.safa.server.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/**
 * Provides endpoints for parsing a series of flat files into project entities.
 */
@RestController
public class FlatFileController extends BaseController {

    private final ProjectService projectService;
    private final FileUploadService fileUploadService;
    private final NotificationService notificationService;
    private final FlatFileService flatFileService;
    private final ProjectRetrievalService projectRetrievalService;

    @Autowired
    public FlatFileController(ProjectService projectService,
                              ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ResourceBuilder resourceBuilder,
                              FileUploadService fileUploadService,
                              NotificationService notificationService,
                              FlatFileService flatFileParser,
                              ProjectRetrievalService projectRetrievalService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.projectService = projectService;
        this.notificationService = notificationService;
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
     * @throws SafaError - If no files are given.
     */
    @PostMapping(value = AppRoutes.Projects.updateProjectVersionFromFlatFiles)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectEntities updateProjectVersionFromFlatFiles(
        @PathVariable UUID versionId,
        @RequestParam MultipartFile[] files) throws SafaError {
        if (files.length == 0) {
            throw new SafaError("Could not create project because no files were received.");
        }
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        Project project = projectVersion.getProject();
        ProjectEntities response = this.uploadAndCreateProjectFromFlatFiles(
            project,
            projectVersion,
            files);
        this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.VERSION);
        return response;
    }

    /**
     * Creates a new project using the given flat files to create the project arifacts, traces, and artifact types.
     *
     * @param files Files including artifact and traces files and requiring at minimum a Tim.json file.
     * @return ProjectCreationResponse containing project artifacts, traces, and warnings.
     * @throws SafaError Throws errors if tim.json file does not exist or an error occurred while parsing it.
     */
    @PostMapping(value = AppRoutes.Projects.projectFlatFiles)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectEntities createNewProjectFromFlatFiles(@RequestParam MultipartFile[] files) throws SafaError {
        if (files.length == 0) {
            throw new SafaError("Could not create project because no files were received.");
        }

        Project project = new Project("", "");
        this.projectRepository.save(project);
        this.projectService.setCurrentUserAsOwner(project);
        ProjectVersion projectVersion = projectService.createBaseProjectVersion(project);

        ProjectEntities response = this.uploadAndCreateProjectFromFlatFiles(project,
            projectVersion,
            files);
        this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.VERSION);
        return response;
    }

    /**
     * Responsible for creating a project from given flat files. This includes
     * parsing tim.json, creating artifacts, and their trace links.
     *
     * @param project        The project whose artifacts and trace links should be associated with
     * @param projectVersion The version that the artifacts and errors will be associated with.
     * @param files          the flat files defining the project
     * @return FlatFileResponse containing uploaded, parsed, and generated files.
     * @throws SafaError on any parsing error of tim.json, artifacts, or trace links
     */
    private ProjectEntities uploadAndCreateProjectFromFlatFiles(Project project,
                                                                ProjectVersion projectVersion,
                                                                MultipartFile[] files)
        throws SafaError {

        this.fileUploadService.uploadFilesToServer(project, Arrays.asList(files));
        this.flatFileService.parseProjectFilesFromTIM(projectVersion);
        return this.projectRetrievalService.retrieveAndCreateProjectResponse(projectVersion);
    }
}
