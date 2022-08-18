package features.utilities;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;
import java.io.IOException;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.utilities.OSHelper;

import org.junit.jupiter.api.Test;

/**
 * Responsible for testing OSHelper IO capabilities.
 */
class TestOSHelperTest {

    @Test
    void canCreateAndDeleteFolder() throws IOException {
        String pathToDummyFolder = ProjectPaths.BUILD + "/dummy_folder";
        File folder = new File(pathToDummyFolder);
        assertFalse(folder.exists());
        OSHelper.clearOrCreateDirectory(pathToDummyFolder);
        assertTrue(folder.exists());

        OSHelper.deletePath(pathToDummyFolder);
        assertFalse(folder.exists());
    }

    @Test
    void deleteNestedDirectories() throws IOException {
        String pathToParent = ProjectPaths.BUILD + "/dummy_folder";
        String pathToChild = pathToParent + "/pathToChild";

        File parentFolder = new File(pathToParent);
        File childFolder = new File(pathToChild);

        //VP 1: Verify ready for testing
        assertFalse(parentFolder.exists());
        assertFalse(childFolder.exists());

        //VP 2: Verify able to create subdirectories
        OSHelper.clearOrCreateDirectory(pathToChild);
        assertTrue(parentFolder.exists());
        assertTrue(childFolder.exists());

        //VP 3: Verify able to delete subdirectories
        OSHelper.deletePath(pathToParent);
        assertFalse(parentFolder.exists());
        assertFalse(childFolder.exists());
    }
}
