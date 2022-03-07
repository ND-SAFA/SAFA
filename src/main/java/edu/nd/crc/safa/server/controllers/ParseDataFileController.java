package edu.nd.crc.safa.server.controllers;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.server.entities.api.FileParser;
import edu.nd.crc.safa.server.entities.api.ParseArtifactFileResponse;
import edu.nd.crc.safa.server.entities.api.ParseFileResponse;
import edu.nd.crc.safa.server.entities.api.ParseTraceFileResponse;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectVersionRepository;

import org.apache.commons.csv.CSVParser;
import org.javatuples.Pair;
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

    private final ArtifactFileParser artifactFileParser;
    private final TraceFileParser traceFileParser;

    private final ArtifactRepository artifactRepository;
    private final ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    public ParseDataFileController(ProjectRepository projectRepository,
                                   ProjectVersionRepository projectVersionRepository,
                                   ResourceBuilder resourceBuilder,
                                   ArtifactRepository artifactRepository,
                                   ArtifactVersionRepository artifactVersionRepository,
                                   ArtifactFileParser artifactFileParser,
                                   TraceFileParser traceFileParser) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.artifactFileParser = artifactFileParser;
        this.artifactRepository = artifactRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.traceFileParser = traceFileParser;
    }

    /**
     * Parses an artifact data file defining artifact id, summary, and content into artifact entities.
     *
     * @param artifactType The name of the artifact type associated with artifacts.
     * @param file         The file defining a list of artifacts containing columns id, summary, and content.
     * @return ParseArtifactResponse containing artifacts and error messages occurring during parsing.
     * @throws IOException Throws error if file was unable to be read otherwise errors are returned as parsing errors.
     */
    @PostMapping(value = AppRoutes.Projects.parseArtifactFile)
    @ResponseStatus(HttpStatus.OK)
    public ParseArtifactFileResponse parseArtifactFile(@PathVariable String artifactType,
                                                       @RequestParam MultipartFile file) {
        ParseArtifactFileResponse response = new ParseArtifactFileResponse();
        tryParseFile(response, () -> {
            CSVParser fileCSV = artifactFileParser.readArtifactFile(file);
            List<ArtifactAppEntity> artifacts =
                artifactFileParser.parseArtifactFileIntoApplicationEntities(
                    file.getOriginalFilename(),
                    artifactType,
                    fileCSV);
            response.setArtifacts(artifacts);
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
    @GetMapping(AppRoutes.Projects.checkIfArtifactExists)
    public Map<String, Boolean> checkIfNameExists(@PathVariable UUID versionId,
                                                  @PathVariable String artifactName) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        Optional<Artifact> artifactQuery =
            this.artifactRepository.findByProjectAndName(projectVersion.getProject(), artifactName);
        boolean artifactExists = false;
        if (artifactQuery.isPresent()) {
            String artifactId = artifactQuery.get().getArtifactId().toString();
            Optional<ArtifactVersion> artifactVersionQuery =
                this.artifactVersionRepository.getEntityVersionsByProjectVersionAndBaseEntityId(
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

    /**
     * Parses an trace link data file containing list of source and target artifact pairs into trace links entities.
     *
     * @param file The file defining a list of trace links containing columns source and target.
     * @return ParseArtifactResponse containing trace links and error messages occurring during parsing.
     */
    @PostMapping(value = AppRoutes.Projects.parseTraceFile)
    @ResponseStatus(HttpStatus.OK)
    public ParseTraceFileResponse parseTraceFile(@RequestParam MultipartFile file) {
        ParseTraceFileResponse response = new ParseTraceFileResponse();
        tryParseFile(response, () -> {
            CSVParser fileCSV = traceFileParser.readTraceFile(file);
            Pair<List<TraceAppEntity>, List<Pair<String, Long>>> parseResponse =
                traceFileParser.readTraceFile(fileCSV);
            List<String> errors = parseResponse.getValue1().stream().map(Pair::getValue0).collect(Collectors.toList());

            response.setTraces(parseResponse.getValue0());
            response.setErrors(errors);
        });
        return response;
    }

    private void tryParseFile(ParseFileResponse response, FileParser fileParser) {
        try {
            fileParser.parseFile();
        } catch (Exception e) {
            response.setErrors(List.of(e.getMessage()));
        }
    }
}
