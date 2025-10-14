package edu.nd.crc.safa.features.flatfiles.controllers;

import java.io.File;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileProjectBuilder;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.JobUtil;

import jakarta.servlet.http.HttpServletResponse;
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

    @Autowired
    public FlatFileController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Uploads and parses given flat files to the specified version.
     *
     * @param versionId     The id of the version that will be modified by given files.
     * @param files         The flat files containing tim.json, artifact files, and trace link files.
     * @param asCompleteSet Whether entities in flat files are complete set of entities in version.
     * @param summarizeArtifacts Whether to run a summarization job in addition to doing the import
     * @return ServerResponse whose body contains all entities in project created.
     * @throws SafaError Throws errors if no files are given.
     */
    @PostMapping(value = AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectAppEntity updateProjectVersionFromFlatFiles(
        @PathVariable UUID versionId,
        @RequestParam("files") Optional<List<MultipartFile>> files,
        @RequestParam(required = false, defaultValue = "false") boolean asCompleteSet,
        @RequestParam(required = false, defaultValue = "false") boolean summarizeArtifacts)
        throws SafaError {

        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
            .withPermission(ProjectPermission.EDIT, user).get();

        if (files.isEmpty()) {
            throw new SafaError("Could not create project because no files were received.");
        }

        FlatFileBuilderStore args = new FlatFileBuilderStore(
            user,
            files.orElseGet(JobUtil::defaultFileListSupplier),
            projectVersion,
            asCompleteSet,
            summarizeArtifacts,
            true);
        FlatFileProjectBuilder.build(args, getServiceProvider());

        if (summarizeArtifacts) {
            getServiceProvider().getEmailService().sendGenerationCompleted(user.getEmail(), projectVersion, null);
        }

        return getServiceProvider().getProjectRetrievalService().getProjectAppEntity(projectVersion);
    }

    @GetMapping(AppRoutes.FlatFiles.DOWNLOAD_FLAT_FILES)
    public void downloadFlatFiles(@PathVariable UUID versionId,
                                  @PathVariable String fileType,
                                  HttpServletResponse response) throws Exception {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
            .withPermission(ProjectPermission.VIEW, user).get();
        String projectName = projectVersion.getProject().getName();
        String versionName = projectVersion.toString();
        String fileName = String.format("%s-%s.zip", projectName, versionName);

        List<File> projectFiles = getServiceProvider()
            .getFileDownloadService()
            .downloadProjectFiles(projectVersion,
                fileType.toLowerCase());
        getServiceProvider().getZipFileService().sendFilesAsZipResponse(response, fileName, projectFiles);
    }
}
