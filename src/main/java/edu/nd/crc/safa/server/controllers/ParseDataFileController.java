package edu.nd.crc.safa.server.controllers;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.server.entities.api.FileParser;
import edu.nd.crc.safa.server.entities.api.ParseArtifactFileResponse;
import edu.nd.crc.safa.server.entities.api.ParseFileResponse;
import edu.nd.crc.safa.server.entities.api.ParseTraceFileResponse;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceApplicationEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.apache.commons.csv.CSVParser;
import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/**
 * Provides API for parsing ArtifactFiles and TraceFile.
 */
@CrossOrigin
@RestController
public class ParseDataFileController extends BaseController {

    private final ArtifactFileParser artifactFileParser;
    private final TraceFileParser traceFileParser;

    @Autowired
    public ParseDataFileController(ProjectRepository projectRepository,
                                   ProjectVersionRepository projectVersionRepository,
                                   ArtifactFileParser artifactFileParser,
                                   TraceFileParser traceFileParser) {
        super(projectRepository, projectVersionRepository);
        this.artifactFileParser = artifactFileParser;
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
    @PostMapping(value = Routes.parseArtifactFile)
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse parseArtifactFile(@PathVariable String artifactType,
                                            @RequestParam MultipartFile file) {
        ParseArtifactFileResponse response = new ParseArtifactFileResponse();
        tryParseFile(response, () -> {
            CSVParser fileCSV = artifactFileParser.readArtifactFile(file);
            Pair<List<ArtifactAppEntity>, List<String>> parseResponse =
                artifactFileParser.parseArtifactFileIntoApplicationEntities(
                    file.getOriginalFilename(),
                    artifactType,
                    fileCSV);
            response.setArtifacts(parseResponse.getValue0());
            response.setErrors(parseResponse.getValue1());
        });
        return new ServerResponse(response);
    }

    /**
     * Parses an trace link data file containing list of source and target artifact pairs into trace links entities.
     *
     * @param file The file defining a list of trace links containing columns source and target.
     * @return ParseArtifactResponse containing trace links and error messages occurring during parsing.
     */
    @PostMapping(value = Routes.parseTraceFile)
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse parseTraceFile(@RequestParam MultipartFile file) {
        ParseTraceFileResponse response = new ParseTraceFileResponse();
        tryParseFile(response, () -> {
            CSVParser fileCSV = traceFileParser.readTraceFile(file);
            Pair<List<TraceApplicationEntity>, List<Pair<String, Long>>> parseResponse =
                traceFileParser.readTraceFile(
                    (a) -> Optional.of(new Artifact()), //TODO: Replace with artifacts from json
                    (s, t) -> Optional.empty(), // TODO: Replace with traces from json
                    fileCSV);
            List<String> errors = parseResponse.getValue1().stream().map(Pair::getValue0).collect(Collectors.toList());

            response.setTraces(parseResponse.getValue0());
            response.setErrors(errors);
        });
        return new ServerResponse(response);
    }

    private void tryParseFile(ParseFileResponse response, FileParser fileParser) {
        try {
            fileParser.parseFile();
        } catch (Exception e) {
            response.setErrors(List.of(e.getMessage()));
        }
    }
}
