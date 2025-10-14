package edu.nd.crc.safa.test.features.delta.base;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.javatuples.Pair;
import org.junit.jupiter.api.BeforeEach;

/**
 * Setups two version for comparison containing:
 * Addition: D12
 * Modified: F3
 * Removed: D7
 */
public abstract class AbstractDeltaTest extends ApplicationBaseTest {
    protected String projectName = "test-project";
    protected ProjectVersion beforeVersion;
    protected ProjectVersion afterVersion;

    @BeforeEach
    public void setupVersion() throws Exception {
        Pair<ProjectVersion, ProjectVersion> versionPair = this.creationService.createDualVersions(projectName);
        this.beforeVersion = versionPair.getValue0();
        this.afterVersion = versionPair.getValue1();
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
