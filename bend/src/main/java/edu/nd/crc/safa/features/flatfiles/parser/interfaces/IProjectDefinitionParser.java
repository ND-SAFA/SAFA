package edu.nd.crc.safa.features.flatfiles.parser.interfaces;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import org.javatuples.Pair;

/**
 * Defines interface with a TIM parser.
 */
public interface IProjectDefinitionParser {

    /**
     * Reads project definition file and parses list of artifact files.
     *
     * @return Parsed artifact files.
     * @throws IOException Throws error if any problem occurs while reading an artifact file
     */
    List<IDataFile<ArtifactAppEntity>> parseArtifactFiles() throws IOException;


    /**
     * Reads project definition and parses list of trace files.
     *
     * @return Parsed trace files.
     * @throws IOException Throws error if any problem occurs while reading a trace file
     */
    Pair<List<IDataFile<TraceAppEntity>>, TGenRequestAppEntity> parseTraceFiles()
        throws IOException;
}
