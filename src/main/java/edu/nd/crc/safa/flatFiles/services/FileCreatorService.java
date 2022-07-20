package edu.nd.crc.safa.flatFiles.services;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.flatFiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.flatFiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating files representing project entities.
 */
@Service
public class FileCreatorService {

    /**
     * Writes artifact to specified file in SAFA data file format.
     *
     * @param pathToFile Path of the file to write the artifacts to.
     * @param artifacts  The artifacts to write to the file.
     * @throws IOException Throws error if unable to create file at path.
     */
    public void writeArtifactsToFile(String pathToFile,
                                     List<ArtifactAppEntity> artifacts) throws IOException {
        FileWriter out = new FileWriter(pathToFile);
        try (CSVPrinter printer = new CSVPrinter(out, CSVFormat.DEFAULT
            .withHeader(AbstractArtifactFile.Constants.REQUIRED_COLUMNS))) {
            for (ArtifactAppEntity artifact : artifacts) {
                printer.printRecord(artifact.name,
                    artifact.documentType,
                    artifact.logicType,
                    artifact.safetyCaseType,
                    artifact.summary,
                    artifact.body);
            }
        }
        out.close();
    }

    /**
     * Writes traces to specified file in SAFA trace file format.
     *
     * @param pathToFile Path of the file to write the traces to.
     * @param traces     The traces to write to the file.
     * @throws IOException Throws error if unable to create file at path.
     */
    public void writeTracesToFile(String pathToFile,
                                  List<TraceAppEntity> traces) throws IOException {
        FileWriter out = new FileWriter(pathToFile);
        try (CSVPrinter printer = new CSVPrinter(out, CSVFormat.DEFAULT
            .withHeader(AbstractTraceFile.Constants.REQUIRED_COLUMNS))) {
            for (TraceAppEntity trace : traces) {
                printer.printRecord(trace.sourceName, trace.targetName);
            }
        }
        out.close();
    }
}
