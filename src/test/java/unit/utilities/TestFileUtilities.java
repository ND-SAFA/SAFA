package unit.utilities;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;
import unit.TestConstants;

public class TestFileUtilities extends EntityBaseTest {
    @Test
    public void readCSVFile() throws Exception {
        String pathToFile = ProjectPaths.getPathToTestResources("Design.csv");
        CSVParser designFile = FileUtilities.readCSVFile(pathToFile);

        //Verification points
        int testArtifactIndex = 0;
        String testArtifactId = "D1";
        String testSummaryQuery = "warning";
        String testContentQuery = "RPIC";
        int nTotalRecords = TestConstants.N_DESIGNS;

        // VP 1 - Headers were parsed correctly
        List<String> headerNames = designFile.getHeaderNames();
        assertThat(headerNames.size()).as("number of headers").isEqualTo(3);

        // VP 2 - All records read
        List<CSVRecord> records = designFile.getRecords();
        assertThat(records.size()).as("record size").isEqualTo(nTotalRecords);

        // VP 3 - Some particular record contains correct content
        CSVRecord testRecord = records.get(testArtifactIndex);
        assertThat(testRecord.get("id")).as("artifact id").isEqualTo(testArtifactId);
        assertThat(testRecord.get("summary")).as("artifact summary").contains(testSummaryQuery);
        assertThat(testRecord.get("content")).as("artifact content").contains(testContentQuery);
    }

    @Test
    public void csvFileNotFound() {
        Exception exception = assertThrows(ServerError.class, () -> {
            FileUtilities.readCSVFile("/abc/123");
        });
        assertThat(exception.getMessage()).contains("not exist");
    }
}
