package edu.nd.crc.safa.flatFiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.flatFiles.IDataFile;
import edu.nd.crc.safa.flatFiles.services.DataFileBuilder;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.json.JSONObject;

/**
 * Responsible for parsing a project from a TIM definition.
 */
@NoArgsConstructor
@Data
public class TimParser {

    /**
     * Path to directory containing flat files.
     */
    String pathToFiles;
    /**
     * List of trace link file definitions
     */
    List<IDataFile<TraceAppEntity>> traceFiles = new ArrayList<>();
    /**
     * List of artifact file definitions
     */
    List<IDataFile<ArtifactAppEntity>> artifactFiles = new ArrayList<>();
    /**
     * List of trace generation requests.
     */
    List<TraceGenerationRequest> traceGenerationRequests = new ArrayList<>();
    /**
     * JSON content of tim.json file.
     */
    private JSONObject timFileJson;

    public TimParser(JSONObject timFileJson, String pathToFiles) throws IOException {
        this();
        this.pathToFiles = pathToFiles;
        this.timFileJson = FileUtilities.toLowerCase(timFileJson);
        this.parse();
    }

    private void parse() throws SafaError, IOException {
        JSONObject dataFiles = this.getDataFiles();
        List<String> artifactTypes = this.getArtifactTypes();

        // Step - Create artifact files
        for (String artifactType : artifactTypes) {
            JSONObject artifactDefinition = dataFiles.getJSONObject(artifactType);
            FileUtilities.assertHasKeys(artifactDefinition, AbstractArtifactFile.Constants.REQUIRED_KEYS);
            String fileName = artifactDefinition.getString(TimParser.Constants.FILE_PARAM);
            String pathToFile = ProjectPaths.joinPaths(this.pathToFiles, fileName);
            IDataFile<ArtifactAppEntity> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType, pathToFile);
            this.artifactFiles.add(artifactFile);
        }

        // Step - Parse trace files
        for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next();

            if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                continue;
            }
            JSONObject traceFileDefinition = timFileJson.getJSONObject(traceMatrixKey);
            String fileName = traceFileDefinition.getString(TimParser.Constants.FILE_PARAM);
            String pathToFile = ProjectPaths.joinPaths(this.pathToFiles, fileName);

            boolean isGenerated =
                traceFileDefinition.has(AbstractTraceFile.Constants.GENERATE_LINKS_PARAM)
                    && traceFileDefinition.getBoolean(AbstractTraceFile.Constants.GENERATE_LINKS_PARAM);

            String source = traceFileDefinition.getString(AbstractTraceFile.Constants.SOURCE_PARAM);
            String target = traceFileDefinition.getString(AbstractTraceFile.Constants.TARGET_PARAM);
            for (String artifactType : List.of(source, target)) {
                if (!artifactTypes.contains(artifactType.toLowerCase())) {
                    throw new SafaError(String.format("Unknown artifact type: %s", artifactType));
                }
            }

            IDataFile<TraceAppEntity> traceFile = DataFileBuilder.createTraceFileParser(pathToFile);
            if (isGenerated) {
                TraceGenerationRequest traceGenerationRequest = new TraceGenerationRequest(source, target);
                traceGenerationRequests.add(traceGenerationRequest);
            } else {
                this.traceFiles.add(traceFile);
            }
        }
    }

    public EntityCreation<TraceAppEntity, String> parseTraces() throws SafaError {
        return this.parseDataFiles(this.traceFiles);
    }

    public EntityCreation<ArtifactAppEntity, String> parseArtifacts() throws SafaError {
        return this.parseDataFiles(this.artifactFiles);
    }

    private <D> EntityCreation<D, String> parseDataFiles(List<IDataFile<D>> dataFiles) {
        List<D> traces = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        for (IDataFile<D> traceFile : dataFiles) {
            EntityCreation<D, String> traceAppEntities = traceFile.parseEntities();
            traces.addAll(traceAppEntities.getEntities());
            errors.addAll(traceAppEntities.getErrors());
        }
        return new EntityCreation<>(traces, errors);
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

    public static class Constants {
        public static final String FILE_PARAM = "file";

        private Constants() {
        }
    }
}
