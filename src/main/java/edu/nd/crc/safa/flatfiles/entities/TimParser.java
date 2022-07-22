package edu.nd.crc.safa.flatfiles.entities;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.flatfiles.IDataFile;
import edu.nd.crc.safa.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.TraceGenerationRequest;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
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
        parseArtifactDefinitions(dataFiles, artifactTypes);
        parseTraceDefinitions(artifactTypes);
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
                IDataFile<TraceAppEntity> traceFile = DataFileBuilder.createTraceFileParser(pathToFile);
                this.traceFiles.add(traceFile);
            }
        }
    }

    private void parseArtifactDefinitions(JSONObject dataFiles, List<String> artifactTypes) throws IOException {
        // Step - Create artifact files
        for (String artifactType : artifactTypes) {
            // Step - Parse and validate artifact definition
            JSONObject artifactDefinition = dataFiles.getJSONObject(artifactType);
            AbstractArtifactFile.validateArtifactDefinition(artifactDefinition);

            // Step - Get required params
            String fileName = artifactDefinition.getString(Constants.FILE_PARAM);

            // Step - Create artifact file parser
            String pathToFile = ProjectPaths.joinPaths(this.pathToFiles, fileName);
            IDataFile<ArtifactAppEntity> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType, pathToFile);
            this.artifactFiles.add(artifactFile);
        }
    }

    public EntityCreation<TraceAppEntity, String> parseTraces(ProjectCommit projectCommit) throws SafaError {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.getArtifacts().addAll(projectCommit.getArtifacts().getAdded());
        return this.parseDataFiles(this.traceFiles, projectAppEntity);
    }

    public EntityCreation<TraceAppEntity, String> parseTraces(ProjectAppEntity projectAppEntity) throws SafaError {
        return this.parseDataFiles(this.traceFiles, projectAppEntity);
    }

    public EntityCreation<ArtifactAppEntity, String> parseArtifacts() {
        return parseArtifacts(new ProjectAppEntity());
    }

    public EntityCreation<ArtifactAppEntity, String> parseArtifacts(ProjectAppEntity projectAppEntity) throws SafaError {
        return this.parseDataFiles(this.artifactFiles, projectAppEntity);
    }

    private <D> EntityCreation<D, String> parseDataFiles(List<IDataFile<D>> dataFiles,
                                                         ProjectAppEntity projectAppEntity) {
        List<D> entities = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        for (IDataFile<D> dataFile : dataFiles) {
            EntityCreation<D, String> entitiesInDataFile = dataFile.parseAndValidateEntities(projectAppEntity);
            entities.addAll(entitiesInDataFile.getEntities());
            errors.addAll(entitiesInDataFile.getErrors());
        }
        return new EntityCreation<>(entities, errors);
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
    }
}
