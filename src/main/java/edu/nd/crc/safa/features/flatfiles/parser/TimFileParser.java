package edu.nd.crc.safa.features.flatfiles.parser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IDataFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IProjectDefinitionParser;
import edu.nd.crc.safa.features.flatfiles.parser.tim.TimArtifactDefinition;
import edu.nd.crc.safa.features.flatfiles.parser.tim.TimSchema;
import edu.nd.crc.safa.features.flatfiles.parser.tim.TimTraceDefinition;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.models.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.javatuples.Pair;
import org.json.JSONObject;

/**
 * Responsible for parsing a project from a TIM definition.
 */
public class TimFileParser implements IProjectDefinitionParser {
    /**
     * Content of tim.json file.
     */
    private final TimSchema timSchema;

    /**
     * Path to directory containing flat files.
     */
    private final String pathToFiles;

    public TimFileParser(JSONObject timFileJson, String pathToFiles) throws JsonProcessingException {
        super();
        this.pathToFiles = pathToFiles;
        this.timSchema = new ObjectMapper().readValue(timFileJson.toString(), new TypeReference<>() {});
    }

    @Override
    public List<IDataFile<ArtifactAppEntity>> parseArtifactFiles() throws IOException {
        List<IDataFile<ArtifactAppEntity>> artifactFiles = new ArrayList<>();

        // Step - Create artifact files
        for (TimArtifactDefinition artifact : timSchema.getArtifacts()) {

            // Step - Get required params
            String fileName = artifact.getFileName();
            String artifactType = artifact.getType();
            DocumentType documentType = DocumentType.ARTIFACT_TREE; //TODO do we ever set this to anything else?

            // Step - Create artifact file parser
            String pathToFile = FileUtilities.buildPath(this.pathToFiles, fileName);
            AbstractArtifactFile<?> artifactFile
                = DataFileBuilder.createArtifactFileParser(artifactType, documentType, pathToFile);
            artifactFiles.add(artifactFile);
        }

        return artifactFiles;
    }

    @Override
    public Pair<List<IDataFile<TraceAppEntity>>, TraceGenerationRequest> parseTraceFiles() throws IOException {
        List<IDataFile<TraceAppEntity>> traceFiles = new ArrayList<>();
        TraceGenerationRequest traceGenerationRequest = new TraceGenerationRequest();

        List<String> artifactTypes = getArtifactTypes();

        for (TimTraceDefinition trace : timSchema.getTraces()) {
            if (!trace.isValid()) {
                throw new SafaError("Trace definition is missing one or more required fields: %s", trace);
            }

            // Step - Get required params
            String source = trace.getSourceType();
            String target = trace.getTargetType();

            // Step - Validate trace definition
            for (String artifactType : List.of(source, target)) {
                if (!artifactTypes.contains(artifactType)) {
                    throw new SafaError(String.format("Unknown artifact type: %s", artifactType));
                }
            }

            // Step - If generation is set, create generation request.\
            if (trace.generateLinks()) {
                //TODO do we ever set this to anything else?
                BaseGenerationModels baseGenerationModels = BaseGenerationModels.getDefault();
                traceGenerationRequest.addTracingRequest(baseGenerationModels, null, source, target);
            }

            if (trace.hasFilename()) {
                String fileName = trace.getFileName();
                String pathToFile = FileUtilities.buildPath(this.pathToFiles, fileName);
                AbstractTraceFile<?> traceFile = DataFileBuilder.createTraceFileParser(pathToFile);
                traceFiles.add(traceFile);
            }
        }

        return new Pair<>(traceFiles, traceGenerationRequest);
    }

    private List<String> getArtifactTypes() {
        return this.timSchema.getArtifacts().stream()
            .map(TimArtifactDefinition::getType)
            .collect(Collectors.toList());
    }

}
