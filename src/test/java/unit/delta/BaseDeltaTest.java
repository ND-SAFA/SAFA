package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import unit.ApplicationBaseTest;

/**
 * Setups two version for comparison containing:
 * Addition: D12
 * Modified: F3
 * Removed: D7
 */
public abstract class BaseDeltaTest extends ApplicationBaseTest {
    String projectName = "test-project";
    ProjectVersion beforeVersion;
    ProjectVersion afterVersion;

    @BeforeEach
    public void setupVersion() throws Exception {
        Pair<ProjectVersion, ProjectVersion> versionPair = createDualVersions(projectName);
        this.beforeVersion = versionPair.getValue0();
        this.afterVersion = versionPair.getValue1();
    }

    public void verifyArtifactInDelta(JSONObject artifactDelta,
                                      String deltaName,
                                      String artifactName) {
        assertThat(artifactDelta.getJSONObject(deltaName).has(getId(projectName, artifactName))).isTrue();
    }

    public void verifyNumOfChangesInDelta(JSONObject entityDelta,
                                          String deltaName,
                                          int expected) {
        String assertionTitle = String.format("# of entities %s", deltaName);
        int nTracesAdded = entityDelta.getJSONObject(deltaName).keySet().toArray().length;
        assertThat(nTracesAdded).as(assertionTitle).isEqualTo(expected);

    }

    protected static class Constants {
        public static String ARTIFACT_ADDED = "D12";
        public static String ARTIFACT_REMOVED = "D7";
        public static String ARTIFACT_MODIFIED = "F3";
        public static int N_CHANGES = 3;
        public static int N_TRACES_ADDED = 1;
        public static int N_TRACES_REMOVED = 1;
        public static int N_TRACES_MODIFIED = 0;
    }
}
