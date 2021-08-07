package unit.utilities;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.junit.jupiter.api.Test;

/**
 * Responsible for testing OSHelper IO capabilities.
 */
public class TestOSHelperTest {

    @Test
    public void canCreateAndDeleteFolder() throws ServerError {
        String pathToDummyFolder = ProjectPaths.PATH_TO_BUILD + "/dummy_folder";
        File folder = new File(pathToDummyFolder);
        assertFalse(folder.exists());
        OSHelper.clearOrCreateDirectory(pathToDummyFolder);
        assertTrue(folder.exists());

        OSHelper.deletePath(pathToDummyFolder);
        assertFalse(folder.exists());
    }

    @Test
    public void deleteNestedDirectories() throws ServerError {
        String pathToParent = ProjectPaths.PATH_TO_BUILD + "/dummy_folder";
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
