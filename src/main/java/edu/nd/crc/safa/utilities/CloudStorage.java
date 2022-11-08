package edu.nd.crc.safa.utilities;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;

import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import com.google.common.collect.ImmutableList;
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

    /**
     * Deletes file in SAFA bucket.
     * TODO: Throw error if not access to file
     *
     * @param filePath Path of the file to delete.
     */
    public static void deleteFile(String filePath) {
        if (CloudStorage.hasAccess(filePath)) {
            CloudStorage.getBlob(filePath).delete();
        }
    }

    /**
     * Returns the block representing the file at given path.
     *
     * @param filePath The relative file path from the SAFA bucket.
     * @return Google blob representing file
     */
    public static Blob getBlob(String filePath) {
        Storage storage = getStorage();
        BlobId blobId = getBlobId(filePath);
        return storage.get(blobId);
    }

    /**
     * Returns the storage of the SAFA project.
     *
     * @return Google storage object.
     */
    public static Storage getStorage() {
        return StorageOptions.newBuilder().setProjectId(Defaults.PROJECT_ID).build().getService();
    }

    /**
     * Return the blob id of the file at given path.
     *
     * @param filePath The relative path to file in default bucket.
     * @return The ID of the blob at given file path in default bucket.
     */
    public static BlobId getBlobId(String filePath) {
        return BlobId.of(Defaults.BUCKET_NAME, filePath);
    }

    /**
     * Returns whether path with name exists or no access to bucket location.
     *
     * @param filePath The name of the file to check if exists.
     * @return Returns whether current thread has access to file at path.
     */
    public static boolean hasAccess(String filePath) {
        Storage storage = getStorage();
        if (!hasBucketAccess(Defaults.BUCKET_NAME)) {
            return false;
        }
        Blob blob = storage.get(getBlobId(filePath));
        if (blob == null) {
            return false;
        }
        return blob.exists();
    }

    /**
     * Returns whether the current thread as acccess to the storage bucket.
     *
     * @param bucket The bucket to check for access
     * @return True if current thread has access, false otherwise.
     */
    public static boolean hasBucketAccess(String bucket) {
        Storage storage = getStorage();
        List<String> permissions = ImmutableList.of("storage.buckets.get");
        List<Boolean> hasPermissions = storage.testIamPermissions(bucket, permissions);
        return hasPermissions.get(0);
    }

    /**
     * Returns the relative output path of a job with the default bucket.
     *
     * @param jobId - The ID of the job
     * @return Path to job output
     */
    public static String getJobOutputPath(String jobId) {
        return "prediction/output/" + jobId + "/output.json";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final String PROJECT_ID = "poised-elf-246319";
        static final String BUCKET_NAME = "safa-tgen-models";
    }
}
