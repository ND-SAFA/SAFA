package edu.nd.crc.safa.features.flatfiles.parser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IArtifactFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IDataFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IProjectDefinitionParser;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.ITraceFIle;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.tgen.entities.ArtifactTypeTraceGenerationRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationMethod;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;

/**
 * Responsible for parsing a project from a TIM definition.
 */
@NoArgsConstructor()
public class TimFileParser implements IProjectDefinitionParser {
    /**
     * JSON content of tim.json file.
     */
    private JSONObject timFileJson;

    /**
     * The artifacts types present in tim.json
     */
    private List<String> artifactTypes;

    /**
     * Path to directory containing flat files.
     */
    private String pathToFiles;

    public TimFileParser(JSONObject timFileJson, String pathToFiles) {
        super();
        this.pathToFiles = pathToFiles;
        this.timFileJson = FileUtilities.toLowerCase(timFileJson);
        this.artifactTypes = this.getArtifactTypes();
    }

    @Override
    public List<IDataFile<ArtifactAppEntity>> parseArtifactFiles() throws IOException {
        JSONObject dataFilesDefinition = this.getDefinitionForDataFiles();
        List<IDataFile<ArtifactAppEntity>> artifactFiles = new ArrayList<>();
        // Step - Create artifact files
        for (String artifactType : artifactTypes) {
            // Step - Parse and validate artifact definition
            JSONObject artifactDefinition = dataFilesDefinition.getJSONObject(artifactType);
            IArtifactFile.validateArtifactDefinition(artifactDefinition);

            // Step - Get required params
            String fileName = artifactDefinition.getString(Constants.FILE_PARAM);
            DocumentType documentType = artifactDefinition.has(Constants.TYPE_PARAM)
                ? DocumentType.valueOf(artifactDefinition.getString(Constants.TYPE_PARAM)) : DocumentType.ARTIFACT_TREE;

            // Step - Create artifact file parser
            String pathToFile = FileUtilities.buildPath(this.pathToFiles, fileName);
            AbstractArtifactFile<?> artifactFile = DataFileBuilder.createArtifactFileParser(artifactType,
                documentType,
                pathToFile);
            artifactFiles.add(artifactFile);
        }
        return artifactFiles;
    }

    @Override
    public Pair<List<IDataFile<TraceAppEntity>>, List<ArtifactTypeTraceGenerationRequestDTO>> parseTraceFiles() throws IOException {
        List<IDataFile<TraceAppEntity>> traceFiles = new ArrayList<>();
        List<ArtifactTypeTraceGenerationRequestDTO> artifactTypeTraceGenerationRequestDTOS = new ArrayList<>();

        for (Iterator<String> keyIterator = timFileJson.keys(); keyIterator.hasNext(); ) {
            String traceMatrixKey = keyIterator.next();
            if (traceMatrixKey.equalsIgnoreCase(ProjectVariables.DATAFILES_PARAM)) {
                continue;
            }

            // Step - Parse and validate trace definition
            JSONObject traceFileDefinition = timFileJson.getJSONObject(traceMatrixKey);
            ITraceFIle.validateTraceDefinition(traceFileDefinition);

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
                TraceGenerationMethod traceGenerationMethod;
                if (traceFileDefinition.has(ITraceFIle.Constants.LINK_GENERATION_METHOD)) {
                    String methodStr = traceFileDefinition.getString(ITraceFIle.Constants.LINK_GENERATION_METHOD);
                    traceGenerationMethod = TraceGenerationMethod.getMethodWithDefault(methodStr,
                        TraceGenerationMethod.VSM);
                } else {
                    traceGenerationMethod = TraceGenerationMethod.VSM;
                }
                ArtifactTypeTraceGenerationRequestDTO artifactTypeTraceGenerationRequestDTO =
                    new ArtifactTypeTraceGenerationRequestDTO(
                        traceGenerationMethod,
                        source,
                        target);
                artifactTypeTraceGenerationRequestDTOS.add(artifactTypeTraceGenerationRequestDTO);
            }

            // Step - If file is defined, create trace file parser
            if (traceFileDefinition.has(Constants.FILE_PARAM)) {
                String fileName = traceFileDefinition.getString(Constants.FILE_PARAM);
                String pathToFile = FileUtilities.buildPath(this.pathToFiles, fileName);
                AbstractTraceFile<?> traceFile = DataFileBuilder.createTraceFileParser(pathToFile);
                traceFiles.add(traceFile);
            }
        }
        return new Pair<>(traceFiles, artifactTypeTraceGenerationRequestDTOS);
    }

    protected JSONObject getDefinitionForDataFiles() {
        return this.timFileJson.getJSONObject(ProjectVariables.DATAFILES_PARAM);
    }

    private List<String> getArtifactTypes() {
        return Arrays.stream(this.getDefinitionForDataFiles()
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
