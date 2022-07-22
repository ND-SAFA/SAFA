package edu.nd.crc.safa.flatfiles.services;

import java.io.IOException;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.flatfiles.IDataFile;
import edu.nd.crc.safa.flatfiles.entities.csv.CsvArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.csv.CsvTraceFile;
import edu.nd.crc.safa.flatfiles.entities.json.JsonArtifactFile;
import edu.nd.crc.safa.flatfiles.entities.json.JsonTraceFile;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;

import lombok.AllArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

/**
 * Returns the parser for specified file type.
 */
public class DataFileBuilder {
    private static final String UNSUPPORTED_FILE_TYPE = "File type is not supported: ";

    public static IDataFile<ArtifactAppEntity> createArtifactFileParser(String artifactType, String pathToFile) throws IOException {
        switch (getFileType(pathToFile)) {
            case CSV:
                return new CsvArtifactFile(artifactType, pathToFile);
            case JSON:
                return new JsonArtifactFile(pathToFile);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + pathToFile);
        }
    }

    public static IDataFile<ArtifactAppEntity> createArtifactFileParser(String artifactType, MultipartFile file) throws IOException {
        switch (getFileType(file.getOriginalFilename())) {
            case CSV:
                return new CsvArtifactFile(artifactType, file);
            case JSON:
                return new JsonArtifactFile(file);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + file.getOriginalFilename());
        }
    }

    public static IDataFile<TraceAppEntity> createTraceFileParser(String pathToFile) throws IOException {
        switch (getFileType(pathToFile)) {
            case CSV:
                return new CsvTraceFile(pathToFile);
            case JSON:
                return new JsonTraceFile(pathToFile);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + pathToFile);
        }
    }

    public static IDataFile<TraceAppEntity> createTraceFileParser(MultipartFile file) throws IOException {
        switch (getFileType(file.getOriginalFilename())) {
            case CSV:
                return new CsvTraceFile(file);
            case JSON:
                return new JsonTraceFile(file);
            default:
                throw new SafaError(UNSUPPORTED_FILE_TYPE + file.getOriginalFilename());
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
    private enum AcceptedFileTypes {
        CSV(".csv"),
        JSON(".json");
        private final String key;
    }
}
