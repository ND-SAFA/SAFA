package edu.nd.crc.safa.utilities;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.function.Function;

import edu.nd.crc.safa.features.flatfiles.parser.formats.csv.CsvArtifactFile;
import edu.nd.crc.safa.features.flatfiles.parser.formats.csv.CsvTraceFile;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVPrinter;
import org.apache.commons.csv.CSVRecord;
import org.springframework.web.multipart.MultipartFile;

/**
 * Builds readers for data files for a specified file format.
 */
public interface CsvFileUtilities {
    static List<CSVRecord> readArtifactFile(String pathToFile) throws IOException {
        try (CSVParser parsedFile = FileUtilities.readCSVFile(pathToFile)) {
            FileUtilities.assertHasColumns(parsedFile, CsvArtifactFile.Constants.REQUIRED_COLUMNS);
            return parsedFile.getRecords();
        }
    }

    static List<CSVRecord> readArtifactFile(MultipartFile file) throws IOException {
        try (CSVParser parser = FileUtilities.readMultiPartCSVFile(file, CsvArtifactFile.Constants.REQUIRED_COLUMNS)) {
            return parser.getRecords();
        }
    }

    static List<CSVRecord> readTraceFile(String pathToFile) throws IOException {
        try (CSVParser parsedFile = FileUtilities.readCSVFile(pathToFile)) {
            return parsedFile.getRecords();
        }
    }

    static List<CSVRecord> readTraceFile(MultipartFile file) throws IOException {
        try (CSVParser parser = FileUtilities.readMultiPartCSVFile(file, CsvTraceFile.Constants.REQUIRED_COLUMNS)) {
            return parser.getRecords();
        }
    }

    static <T> void writeEntitiesAsCsvFile(File file,
                                           String[] headers,
                                           List<T> entities,
                                           Function<T, String[]> entity2values) throws IOException {
        try (FileWriter reader = new FileWriter(file)) {
            try (CSVPrinter printer = new CSVPrinter(reader, createCsvFormat(headers))) {
                for (T entity : entities) {
                    printer.printRecord((Object[]) entity2values.apply(entity));
                }
                printer.flush();
            }
        }
    }

    private static CSVFormat createCsvFormat(String[] headers) {
        return CSVFormat
            .Builder
            .create()
            .setHeader(headers)
            .setSkipHeaderRecord(false)
            .setAllowMissingColumnNames(true)
            .build();
    }
}
