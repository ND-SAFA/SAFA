package edu.nd.crc.safa.test.features.utilities;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.test.common.DefaultProjectConstants;
import edu.nd.crc.safa.test.common.EntityBaseTest;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.junit.jupiter.api.Test;

/**
 * Tests that we are able to read a CSV file containing headers.
 */
class TestCSVReader extends EntityBaseTest {
    @Test
    void readCSVFile() throws Exception {
        String pathToFile = ProjectPaths.Resources.Tests.DefaultProject.getPathToFile(
            DefaultProjectConstants.File.DESIGN_FILE
        );
        CSVParser designFile = FileUtilities.readCSVFile(pathToFile);

        //Verification points
        int testArtifactIndex = 0;
        String testArtifactId = "D1";
        String testSummaryQuery = "warning";
        String testContentQuery = "RPIC";
        int nTotalRecords = DefaultProjectConstants.Entities.N_DESIGNS;

        // VP 1 - Headers were parsed correctly
        List<String> headerNames = designFile.getHeaderNames();
        assertThat(headerNames).as("number of headers").hasSize(3);

        // VP 2 - All records read
        List<CSVRecord> records = designFile.getRecords();
        assertThat(records).as("record size").hasSize(nTotalRecords);

        // VP 3 - Some particular record contains correct content
        CSVRecord testRecord = records.get(testArtifactIndex);
        assertThat(testRecord.get("id")).as("artifact id").isEqualTo(testArtifactId);
        assertThat(testRecord.get("summary")).as("artifact summary").contains(testSummaryQuery);
        assertThat(testRecord.get("content")).as("artifact content").contains(testContentQuery);
    }

    @Test
    void csvFileNotFound() {
        Exception exception = assertThrows(IOException.class, () -> {
            FileUtilities.readCSVFile("/abc/123");
        });
        // Check file path independent of the operating system
        assertThat(exception.getMessage())
            .contains(Paths.get("abc", "123").toString());
    }
}
