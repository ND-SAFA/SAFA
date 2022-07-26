package edu.nd.crc.safa.flatfiles.services;

import java.io.IOException;
import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.flatfiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.flatfiles.entities.csv.CsvArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.csv.CsvTraceFile;
import edu.nd.crc.safa.flatfiles.entities.json.JsonArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.json.JsonTraceFile;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.DocumentType;

import lombok.AllArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

/**
 * Returns the parser for specified file type.
 */
public class DataFileBuilder {
    private static final String UNSUPPORTED_FILE_TYPE = "File type is not supported: ";

    public static AbstractArtifactFile<?> createArtifactFileParser(String artifactType,
                                                                   DocumentType documentType,
                                                                   String pathToFile) throws IOException {
        switch (getFileType(pathToFile)) {
            case CSV:
                return new CsvArtifactFile(artifactType, documentType, pathToFile);
            case JSON:
                return new JsonArtifactFile(pathToFile);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + pathToFile);
        }
    }

    public static AbstractArtifactFile<?> createArtifactFileParser(String artifactType,
                                                                   DocumentType documentType,
                                                                   MultipartFile file) throws IOException {
        switch (getFileType(file.getOriginalFilename())) {
            case CSV:
                return new CsvArtifactFile(artifactType, documentType, file);
            case JSON:
                return new JsonArtifactFile(file);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + file.getOriginalFilename());
        }
    }

    public static AbstractArtifactFile<?> createArtifactFileParser(String artifactType,
                                                                   String fileName,
                                                                   DocumentType documentType,
                                                                   List<ArtifactAppEntity> artifacts) {
        switch (getFileType(fileName)) {
            case CSV:
                return new CsvArtifactFile(artifactType, documentType, artifacts);
            case JSON:
                return new JsonArtifactFile(artifacts);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + fileName);
        }
    }

    public static AbstractTraceFile<?> createTraceFileParser(String pathToFile) throws IOException {
        switch (getFileType(pathToFile)) {
            case CSV:
                return new CsvTraceFile(pathToFile);
            case JSON:
                return new JsonTraceFile(pathToFile);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + pathToFile);
        }
    }

    public static AbstractTraceFile<?> createTraceFileParser(MultipartFile file) throws IOException {
        switch (getFileType(file.getOriginalFilename())) {
            case CSV:
                return new CsvTraceFile(file);
            case JSON:
                return new JsonTraceFile(file);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + file.getOriginalFilename());
        }
    }

    public static AbstractTraceFile<?> createTraceFileParser(String fileName, List<TraceAppEntity> traces) {
        switch (getFileType(fileName)) {
            case CSV:
                return new CsvTraceFile(traces);
            case JSON:
                return new JsonTraceFile(traces);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + fileName);
        }
    }

    @NotNull
    public static AcceptedFileTypes getFileType(String fileName) {
        for (AcceptedFileTypes acceptedFileTypes : AcceptedFileTypes.values()) {
            if (fileName.contains(acceptedFileTypes.key)) {
                return acceptedFileTypes;
            }
        }
        throw new SafaError(UNSUPPORTED_FILE_TYPE + fileName);
    }

    @AllArgsConstructor
    public enum AcceptedFileTypes {
        CSV(".csv"),
        JSON(".json");
        private final String key;
    }
}
