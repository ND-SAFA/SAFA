package edu.nd.crc.safa.features.flatfiles.controllers;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.controllers.entities.ArtifactNameCheck;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IFileParser;
import edu.nd.crc.safa.features.flatfiles.services.CheckArtifactNameService;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/**
 * Provides endpoints for parsing artifact and trace files. This also includes endpoints
 * for validating a particular entity.
 */
@RestController
public class ParseDataFileController extends BaseController {

    private final CheckArtifactNameService checkArtifactNameService;

    @Autowired
    public ParseDataFileController(ResourceBuilder resourceBuilder,
                                   ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.checkArtifactNameService = serviceProvider.getCheckArtifactNameService();
    }

    /**
     * Parses an artifact data file defining artifact id, summary, and content into artifact entities.
     *
     * @param artifactType The name of the artifact type associated with artifacts.
     * @param file         The file defining a list of artifacts containing columns id, summary, and content.
     * @return ParseArtifactResponse containing artifacts and error messages occurring during parsing.
     */
    @PostMapping(value = AppRoutes.FlatFiles.PARSE_ARTIFACT_FILE)
    @ResponseStatus(HttpStatus.OK)
    public EntityParsingResult<ArtifactAppEntity, String> parseArtifactFile(@PathVariable String artifactType,
                                                                            @RequestParam MultipartFile file) {
        EntityParsingResult<ArtifactAppEntity, String> response = new EntityParsingResult<>();
        tryParseFile(response, () -> {
            AbstractArtifactFile<?> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType, file);
            response.setEntities(artifactFile.getEntities());
            response.setErrors(artifactFile.getErrors());
        });
        return response;
    }

    /**
     * Parses an trace link data file containing list of source and target artifact pairs into trace links entities.
     *
     * @param file The file defining a list of trace links containing columns source and target.
     * @return ParseArtifactResponse containing trace links and error messages occurring during parsing.
     */
    @PostMapping(value = AppRoutes.FlatFiles.PARSE_TRACE_FILE)
    @ResponseStatus(HttpStatus.OK)
    public EntityParsingResult<TraceAppEntity, String> parseTraceFile(@RequestParam MultipartFile file) {
        EntityParsingResult<TraceAppEntity, String> response = new EntityParsingResult<>();
        tryParseFile(response, () -> {
            AbstractTraceFile<?> traceFile = DataFileBuilder.createTraceFileParser(file);
            response.setEntities(traceFile.getEntities());
            response.setErrors(traceFile.getErrors());
        });
        return response;
    }

    /**
     * Returns flag `artifactExists` indicating whether artifact exists in the project.
     *
     * @param versionId         The version id to check if the given artifact name is already in it.
     * @param artifactNameCheck Object containing artifact name to check.
     * @return `artifactExists` flag indicating presence of artifact in project.
     */
    @PostMapping(AppRoutes.Projects.Entities.CHECK_IF_ARTIFACT_EXISTS)
    public Map<String, Boolean> checkIfNameExists(@PathVariable UUID versionId,
                                                  @RequestBody ArtifactNameCheck artifactNameCheck) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
            .withPermission(ProjectPermission.VIEW, user).get();
        boolean artifactExists = checkArtifactNameService.doesArtifactExist(projectVersion, artifactNameCheck);
        Map<String, Boolean> response = new HashMap<>();
        response.put(ProjectVariables.ARTIFACT_EXISTS, artifactExists);
        return response;
    }

    private <T> void tryParseFile(EntityParsingResult<T, String> response, IFileParser fileParser) {
        try {
            fileParser.parseFile();
        } catch (Exception e) {
            response.setErrors(List.of(e.getMessage()));
        }
    }
}
