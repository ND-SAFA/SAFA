package edu.nd.crc.safa.utilities;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;

import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONObject;

/**
 * Provides API for uploading, downloading, or deleting a file on the cloud storage.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class CloudStorage {
    /**
     * Downloads content of given blob and parses it as JSON.
     *
     * @param blob The blob representing the file.
     * @return JSONObject parsed json from file content
     * @throws IOException If error occurred while reading file.
     */
    public static JSONObject downloadJsonFileBlob(Blob blob) throws IOException {
        // Step - Create temp file in local memory
        String tempDirectory = ProjectPaths.Storage.createTemporaryDirectory();
        String tempFileName = UUID.randomUUID() + ".json";
        String tempFilePath = FileUtilities.buildPath(tempDirectory, tempFileName);

        // Step - Get block
        blob.downloadTo(Paths.get(tempFilePath));

        // Step - Parse json
        JSONObject response = JsonFileUtilities.readJSONFile(tempFilePath);

        // Step - Delete temp directory
        FileUtilities.deletePath(tempDirectory);
        return response;
    }

    public static void deleteFile(String filePath) {
        if (CloudStorage.exists(filePath)) {
            CloudStorage.getBlob(filePath).delete();
        }
    }

    public static Blob getBlob(String objectName) {
        Storage storage = getStorage();
        BlobId blobId = getBlobId(objectName);
        return storage.get(blobId);
    }

    public static Storage getStorage() {
        return StorageOptions.newBuilder().setProjectId(Defaults.PROJECT_ID).build().getService();
    }

    public static BlobId getBlobId(String objectName) {
        return BlobId.of(Defaults.BUCKET_NAME, objectName);
    }

    public static boolean exists(String objectName) {
        Storage storage = getStorage();
        Blob blob = storage.get(getBlobId(objectName));
        if (blob == null) {
            return false;
        }
        return blob.exists();
    }

    public static String getJobOutputPath(String jobId) {
        return "prediction/output/" + jobId + "/output.json";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final String PROJECT_ID = "poised-elf-246319";
        static final String BUCKET_NAME = "safa-tgen-models";
    }
}
