package edu.nd.crc.safa.features.flatfiles.controllers;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.UUID;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.flatfiles.services.FileDownloadService;
import edu.nd.crc.safa.features.flatfiles.services.FlatFileService;
import edu.nd.crc.safa.features.flatfiles.services.ZipFileService;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
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
    private final NotificationService notificationService;
    private final FlatFileService flatFileService;
    private final ZipFileService zipFileService;
    private final FileDownloadService fileDownloadService;

    @Autowired
    public FlatFileController(ResourceBuilder resourceBuilder,
                              ProjectService projectService,
                              NotificationService notificationService,
                              FlatFileService flatFileService,
                              ZipFileService zipFileService,
                              FileDownloadService fileDownloadService) {
        super(resourceBuilder);
        this.projectService = projectService;
        this.notificationService = notificationService;
        this.flatFileService = flatFileService;
        this.zipFileService = zipFileService;
        this.fileDownloadService = fileDownloadService;
    }


    /**
     * Uploads and parses given flat files to the specified version.
     *
     * @param versionId - The id of the version that will be modified by given files.
     * @param files     - The flat files containing tim.json, artifact files, and trace link files.
     * @return ServerResponse whose body contains all entities in project created.
     * @throws SafaError - If no files are given.
     */
    @PostMapping(value = AppRoutes.Projects.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectAppEntity updateProjectVersionFromFlatFiles(
        @PathVariable UUID versionId,
        @RequestParam MultipartFile[] files) throws SafaError, IOException {
        if (files.length == 0) {
            throw new SafaError("Could not create project because no files were received.");
        }
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        Project project = projectVersion.getProject();
        ProjectAppEntity projectCreated = this.flatFileService.createProjectFromFlatFiles(
            project,
            projectVersion,
            files);
        this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.VERSION);
        return projectCreated;
    }

    /**
     * Creates a new project using the given flat files to create the project arifacts, traces, and artifact types.
     *
     * @param files Files including artifact and traces files and requiring at minimum a Tim.json file.
     * @return ProjectCreationResponse containing project artifacts, traces, and warnings.
     * @throws SafaError Throws errors if tim.json file does not exist or an error occurred while parsing it.
     */
    @PostMapping(value = AppRoutes.Projects.FlatFiles.CREATE_PROJECT_FROM_FLAT_FILES)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectAppEntity createNewProjectFromFlatFiles(@RequestParam MultipartFile[] files)
        throws SafaError, IOException {
        if (files.length == 0) {
            throw new SafaError("Could not create project because no files were received.");
        }
        Project project = new Project("", "");
        this.projectService.saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = projectService.createInitialProjectVersion(project);
        ProjectAppEntity projectAppEntity = this.flatFileService.createProjectFromFlatFiles(project,
            projectVersion,
            files);
        this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.VERSION);
        return projectAppEntity;
    }

    @GetMapping(AppRoutes.Projects.FlatFiles.DOWNLOAD_FLAT_FILES)
    public void downloadFlatFiles(@PathVariable UUID versionId,
                                  @PathVariable String fileType,
                                  HttpServletResponse response) throws Exception {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withViewVersion();
        String projectName = projectVersion.getProject().getName();
        String versionName = projectVersion.toString();
        String fileName = String.format("%s-%s.zip", projectName, versionName);

        List<File> projectFiles = fileDownloadService.downloadProjectFiles(projectVersion, fileType);
        zipFileService.sendFilesAsZipResponse(response, fileName, projectFiles);
    }
}
