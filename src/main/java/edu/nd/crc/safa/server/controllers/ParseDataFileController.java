package edu.nd.crc.safa.server.controllers;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.flatfiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.server.entities.api.FileParser;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ProjectRetriever;

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
 * Provides endpoints for parsing artifact and trace files. This also includes endpoints
 * for validating a particular entity.
 */
@RestController
public class ParseDataFileController extends BaseController {

    private final ProjectRetriever artifactRepository;
    private final ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    public ParseDataFileController(ResourceBuilder resourceBuilder,
                                   ProjectRetriever artifactRepository,
                                   ArtifactVersionRepository artifactVersionRepository) {
        super(resourceBuilder);
        this.artifactRepository = artifactRepository;
        this.artifactVersionRepository = artifactVersionRepository;
    }

    /**
     * Parses an artifact data file defining artifact id, summary, and content into artifact entities.
     *
     * @param artifactType The name of the artifact type associated with artifacts.
     * @param file         The file defining a list of artifacts containing columns id, summary, and content.
     * @return ParseArtifactResponse containing artifacts and error messages occurring during parsing.
     * @throws IOException Throws error if file was unable to be read otherwise errors are returned as parsing errors.
     */
    @PostMapping(value = AppRoutes.Projects.FlatFiles.parseArtifactFile)
    @ResponseStatus(HttpStatus.OK)
    public EntityParsingResult<ArtifactAppEntity, String> parseArtifactFile(@PathVariable String artifactType,
                                                                            @RequestParam MultipartFile file) {
        EntityParsingResult<ArtifactAppEntity, String> response = new EntityParsingResult<>();
        tryParseFile(response, () -> {
            AbstractArtifactFile<? extends Object> artifactFile =
                DataFileBuilder.createArtifactFileParser(artifactType,
                    DocumentType.ARTIFACT_TREE,
                    file);
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
    @PostMapping(value = AppRoutes.Projects.FlatFiles.parseTraceFile)
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
     * @param versionId    The version id to check if the given artifact name is already in it.
     * @param artifactName The name / identifier of the artifact.
     * @return `artifactExists` flag indicating presence of artifact in project.
     */
    @GetMapping(AppRoutes.Projects.Entities.checkIfArtifactExists)
    public Map<String, Boolean> checkIfNameExists(@PathVariable UUID versionId,
                                                  @PathVariable String artifactName) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        Optional<Artifact> artifactQuery =
            this.artifactRepository.findByProjectAndName(projectVersion.getProject(), artifactName);
        boolean artifactExists = false;
        if (artifactQuery.isPresent()) {
            String artifactId = artifactQuery.get().getArtifactId().toString();
            Optional<ArtifactVersion> artifactVersionQuery =
                this.artifactVersionRepository.findVersionEntityByProjectVersionAndBaseEntityId(
                    projectVersion,
                    artifactId);
            if (artifactVersionQuery.isPresent()) {
                artifactExists = !artifactVersionQuery.get().getModificationType().equals(ModificationType.REMOVED);
            }
        }
        Map<String, Boolean> response = new HashMap<>();
        response.put("artifactExists", artifactExists);
        return response;
    }

    private <T> void tryParseFile(EntityParsingResult<T, String> response, FileParser fileParser) {
        try {
            fileParser.parseFile();
        } catch (Exception e) {
            response.setErrors(List.of(e.getMessage()));
        }
    }
}
