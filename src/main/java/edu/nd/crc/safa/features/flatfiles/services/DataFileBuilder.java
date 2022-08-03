package edu.nd.crc.safa.features.flatfiles.services;

import java.io.IOException;
import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.flatfiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.features.flatfiles.entities.AbstractTraceFile;
import edu.nd.crc.safa.features.flatfiles.entities.csv.CsvArtifactFile;
import edu.nd.crc.safa.features.flatfiles.entities.csv.CsvTraceFile;
import edu.nd.crc.safa.features.flatfiles.entities.json.JsonArtifactFile;
import edu.nd.crc.safa.features.flatfiles.entities.json.JsonTraceFile;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;

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
            String fileTypeExtension = "." + acceptedFileTypes.key;
            if (fileName.contains(fileTypeExtension)) {
                return acceptedFileTypes;
            }
        }
        throw new SafaError(UNSUPPORTED_FILE_TYPE + fileName);
    }

    @AllArgsConstructor
    public enum AcceptedFileTypes {
        CSV("csv"),
        JSON("json");
        private final String key;

        @Override
        public String toString() {
            return this.key;
        }
    }
}
