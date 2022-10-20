package edu.nd.crc.safa.features.flatfiles.parser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IDataFile;
import edu.nd.crc.safa.features.flatfiles.parser.interfaces.IProjectDefinitionParser;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.Data;
import org.javatuples.Pair;

@Data
public class FlatFileParser {
    /**
     * List of artifact file definitions
     */
    protected List<IDataFile<ArtifactAppEntity>> artifactFiles = new ArrayList<>();
    /**
     * List of trace link file definitions
     */
    protected List<IDataFile<TraceAppEntity>> traceFiles = new ArrayList<>();
    /**
     * List of trace generation requests.
     */
    protected TraceGenerationRequest traceGenerationRequest = new TraceGenerationRequest();

    protected IProjectDefinitionParser timParser;

    public FlatFileParser(IProjectDefinitionParser projectDefinitionParser) throws IOException {
        this.artifactFiles = projectDefinitionParser.parseArtifactFiles();
        Pair<List<IDataFile<TraceAppEntity>>, TraceGenerationRequest> response =
            projectDefinitionParser.parseTraceFiles();
        this.traceFiles = response.getValue0();
        this.traceGenerationRequest = response.getValue1();
        this.timParser = projectDefinitionParser;
    }

    protected <E> EntityParsingResult<E, String> parseDataFiles(List<IDataFile<E>> dataFiles,
                                                                ProjectAppEntity projectAppEntity) {
        List<E> entities = new ArrayList<>();
        List<String> errors = new ArrayList<>();
        for (IDataFile<E> dataFile : dataFiles) {
            Pair<List<E>, List<String>> validationResponse = dataFile.validateInProject(projectAppEntity);
            entities.addAll(validationResponse.getValue0());
            errors.addAll(dataFile.getErrors());
            errors.addAll(validationResponse.getValue1());
        }
        return new EntityParsingResult<>(entities, errors);
    }

    public EntityParsingResult<TraceAppEntity, String> parseTraces(List<ArtifactAppEntity> artifacts) throws SafaError {
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.getArtifacts().addAll(artifacts);
        return this.parseDataFiles(this.traceFiles, projectAppEntity);
    }

    public EntityParsingResult<ArtifactAppEntity, String> parseArtifacts() {
        return parseArtifacts(new ProjectAppEntity());
    }

    public EntityParsingResult<ArtifactAppEntity, String> parseArtifacts(ProjectAppEntity projectAppEntity)
        throws SafaError {
        return this.parseDataFiles(this.artifactFiles, projectAppEntity);
    }
}
