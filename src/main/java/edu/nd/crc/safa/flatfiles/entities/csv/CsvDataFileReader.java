package edu.nd.crc.safa.flatfiles.entities.csv;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.web.multipart.MultipartFile;

/**
 * Builds readers for data files for a specified file format.
 */
public interface CsvDataFileReader {
    static List<CSVRecord> readArtifactFile(String pathToFile) throws IOException {
        CSVParser parsedFile = FileUtilities.readCSVFile(pathToFile);
        FileUtilities.assertHasColumns(parsedFile, CsvArtifactFile.Constants.REQUIRED_COLUMNS);
        return parsedFile.getRecords();
    }

    static List<CSVRecord> readArtifactFile(MultipartFile file) throws IOException {
        return FileUtilities
            .readMultiPartCSVFile(file, CsvArtifactFile.Constants.REQUIRED_COLUMNS)
            .getRecords();
    }

    static List<CSVRecord> readTraceFile(String pathToFile) throws IOException {
        CSVParser parsedFile = FileUtilities.readCSVFile(pathToFile);
        return parsedFile.getRecords();
    }

    static List<CSVRecord> readTraceFile(MultipartFile file) throws IOException {
        return FileUtilities
            .readMultiPartCSVFile(file, CsvTraceFile.Constants.REQUIRED_COLUMNS)
            .getRecords();
    }
}
