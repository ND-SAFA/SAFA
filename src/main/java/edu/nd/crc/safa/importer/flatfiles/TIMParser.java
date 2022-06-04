package edu.nd.crc.safa.importer.flatfiles;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.ProjectVariables;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.javatuples.Pair;
import org.json.JSONObject;

/**
 * Responsible for parsing a project from a TIM definition.
 */
public class TIMParser {

    public static final String FILE_PARAM = "file";
    private final List<TraceFileParser> traceFileParsers;
    private final List<ArtifactFile> artifactTypeDefinitions;
    private boolean parsed;
    private JSONObject timFileJson;

    public TIMParser() {
        this.artifactTypeDefinitions = new ArrayList<>();
        this.traceFileParsers = new ArrayList<>();
        this.parsed = false;
    }

    public TIMParser(JSONObject timFileJson) {
        this();
        this.timFileJson = FileUtilities.toLowerCase(timFileJson);
    }

    public List<TraceFileParser> getTraceMatrixDefinitions() {
        return traceFileParsers;
    }

    public void parse() throws SafaError {
        JSONObject dataFiles = this.getDataFiles();
        List<String> artifactTypes = this.getArtifactTypes();

        for (String artifactType : artifactTypes) {
            JSONObject artifactDefinition = dataFiles.getJSONObject(artifactType);
            FileUtilities.assertHasKeys(artifactDefinition, ArtifactFile.REQUIRED_KEYS);
            ArtifactFile artifactTypeDefinition = new ArtifactFile(artifactType,
                artifactDefinition.getString(FILE_PARAM));
            this.artifactTypeDefinitions.add(artifactTypeDefinition);
        }

        for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next();

            if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                continue;
            }
            JSONObject traceMatrix = timFileJson.getJSONObject(traceMatrixKey);
            TraceFileParser traceFileParser = TraceFileParser.fromJson(traceMatrix, traceMatrixKey,
                artifactTypes);
            this.traceFileParsers.add(traceFileParser);
        }
        this.parsed = true;
    }

    public Pair<List<TraceAppEntity>, List<TraceGenerationRequest>> parseTraces(
        ProjectVersion projectVersion) throws SafaError {
        List<TraceAppEntity> traces = new ArrayList<>();
        List<TraceGenerationRequest> traceGenerationRequests = new ArrayList<>();

        for (TraceFileParser traceFileParser : this.getTraceMatrixDefinitions()) {
            List<TraceAppEntity> traceAppEntities =
                traceFileParser.readAndParseTraceFile(projectVersion.getProject());
            traces.addAll(traceAppEntities);

            if (traceFileParser.isGenerated()) {
                TraceGenerationRequest traceGenerationRequest = new TraceGenerationRequest(
                    traceFileParser.getSource(),
                    traceFileParser.getTarget());
                traceGenerationRequests.add(traceGenerationRequest);
            }
        }
        return new Pair<>(traces, traceGenerationRequests);
    }

    public JSONObject getDataFiles() {
        return this.timFileJson.getJSONObject(ProjectVariables.DATAFILES_PARAM);
    }

    public List<String> getArtifactTypes() {
        return Arrays.stream(this.getDataFiles()
                .keySet()
                .toArray())
            .map(Object::toString)
            .collect(Collectors.toList());
    }

    public List<ArtifactFile> getArtifactTypeDefinitions() {
        assertParsed();
        return this.artifactTypeDefinitions;
    }

    private void assertParsed() {
        if (!this.parsed) {
            throw new RuntimeException("Parse request is not yet parsed.");
        }
    }
}
