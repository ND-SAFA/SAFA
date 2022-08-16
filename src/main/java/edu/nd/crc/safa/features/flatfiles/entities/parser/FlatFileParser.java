package edu.nd.crc.safa.features.flatfiles.entities.parser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.entities.common.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.entities.common.AbstractDataFile;
import edu.nd.crc.safa.features.flatfiles.entities.common.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;

/**
 * Responsible for parsing a project from a TIM definition.
 */
@NoArgsConstructor
@Data
public class FlatFileParser {

    /**
     * Path to directory containing flat files.
     */
    String pathToFiles;
    /**
     * List of trace link file definitions
     */
    List<AbstractDataFile<TraceAppEntity, ?>> traceFiles = new ArrayList<>();
    /**
     * List of artifact file definitions
     */
    List<AbstractDataFile<ArtifactAppEntity, ?>> artifactFiles = new ArrayList<>();
    /**
     * List of trace generation requests.
     */
    List<TraceGenerationRequest> traceGenerationRequests = new ArrayList<>();
    /**
     * JSON content of tim.json file.
     */
    private JSONObject timFileJson;

    public FlatFileParser(JSONObject timFileJson, String pathToFiles) throws IOException {
        this();
        this.pathToFiles = pathToFiles;
        this.timFileJson = FileUtilities.toLowerCase(timFileJson);
        this.parse();
    }

    private void parse() throws SafaError, IOException {
        JSONObject dataFiles = this.getDataFiles();
        List<String> artifactTypes = this.getArtifactTypes();
        parseArtifactDefinitions(dataFiles, artifactTypes);
        parseTraceDefinitions(artifactTypes);
    }

    private void parseArtifactDefinitions(JSONObject dataFiles, List<String> artifactTypes) throws IOException {
        // Step - Create artifact files
        for (String artifactType : artifactTypes) {
            // Step - Parse and validate artifact definition
            JSONObject artifactDefinition = dataFiles.getJSONObject(artifactType);
            AbstractArtifactFile.validateArtifactDefinition(artifactDefinition);

            // Step - Get required params
            String fileName = artifactDefinition.getString(Constants.FILE_PARAM);
            DocumentType documentType = artifactDefinition.has(Constants.TYPE_PARAM)
                ? DocumentType.valueOf(artifactDefinition.getString(Constants.TYPE_PARAM)) : DocumentType.ARTIFACT_TREE;

            // Step - Create artifact file parser
            String pathToFile = ProjectPaths.joinPaths(this.pathToFiles, fileName);
            AbstractArtifactFile<?> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType,
                documentType,
                pathToFile);
            this.artifactFiles.add(artifactFile);
        }
    }

    private void parseTraceDefinitions(List<String> artifactTypes) throws IOException {
        for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next();
            if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                continue;
            }

            // Step - Parse and validate trace definition
            JSONObject traceFileDefinition = timFileJson.getJSONObject(traceMatrixKey);
            AbstractTraceFile.validateTraceDefinition(traceFileDefinition);

            // Step - Get required params
            String source = traceFileDefinition.getString(AbstractTraceFile.Constants.SOURCE_PARAM);
            String target = traceFileDefinition.getString(AbstractTraceFile.Constants.TARGET_PARAM);

            // Step - Validate trace definition
            for (String artifactType : List.of(source, target)) {
                if (!artifactTypes.contains(artifactType.toLowerCase())) {
                    throw new SafaError(String.format("Unknown artifact type: %s", artifactType));
                }
            }

            // Step - If generation is set, create generation request.
            boolean isGenerated =
                traceFileDefinition.has(AbstractTraceFile.Constants.GENERATE_LINKS_PARAM)
                    && traceFileDefinition.getBoolean(AbstractTraceFile.Constants.GENERATE_LINKS_PARAM);
            if (isGenerated) {
                TraceGenerationRequest traceGenerationRequest = new TraceGenerationRequest(source, target);
                traceGenerationRequests.add(traceGenerationRequest);
            }

            // Step - If file is defined, create trace file parser
            if (traceFileDefinition.has(Constants.FILE_PARAM)) {
                String fileName = traceFileDefinition.getString(Constants.FILE_PARAM);
                String pathToFile = ProjectPaths.joinPaths(this.pathToFiles, fileName);
                AbstractTraceFile<?> traceFile = DataFileBuilder.createTraceFileParser(pathToFile);
                this.traceFiles.add(traceFile);
            }
        }
    }

    public EntityParsingResult<TraceAppEntity, String> parseTraces(List<ArtifactAppEntity> artifacts) throws SafaError {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.getArtifacts().addAll(artifacts);
        return this.parseDataFiles(this.traceFiles, projectAppEntity);
    }

    public EntityParsingResult<TraceAppEntity, String> parseTraces(ProjectAppEntity projectAppEntity) throws SafaError {
        return this.parseDataFiles(this.traceFiles, projectAppEntity);
    }

    public EntityParsingResult<ArtifactAppEntity, String> parseArtifacts() {
        return parseArtifacts(new ProjectAppEntity());
    }

    public EntityParsingResult<ArtifactAppEntity, String> parseArtifacts(ProjectAppEntity projectAppEntity)
        throws SafaError {
        return this.parseDataFiles(this.artifactFiles, projectAppEntity);
    }

    private <E> EntityParsingResult<E, String> parseDataFiles(List<AbstractDataFile<E, ?>> dataFiles,
                                                              ProjectAppEntity projectAppEntity) {
        List<E> entities = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        for (AbstractDataFile<E, ?> dataFile : dataFiles) {
            Pair<List<E>, List<String>> validationResponse = dataFile.validateInProject(projectAppEntity);
            entities.addAll(validationResponse.getValue0());
            errors.addAll(dataFile.getErrors());
            errors.addAll(validationResponse.getValue1());
        }
        return new EntityParsingResult<>(entities, errors);
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

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String FILE_PARAM = "file";
        public static final String TYPE_PARAM = "type";
    }
}
