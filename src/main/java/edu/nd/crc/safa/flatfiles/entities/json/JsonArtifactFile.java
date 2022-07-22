package edu.nd.crc.safa.flatfiles.entities.json;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.flatfiles.entities.AbstractArtifactFile;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.springframework.web.multipart.MultipartFile;

/**
 * A JSON file defining a set of artifacts.
 */
public class JsonArtifactFile extends AbstractArtifactFile<JSONObject> {
    public JsonArtifactFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    public JsonArtifactFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    public List<JSONObject> readFileRecords(String pathToFile) throws IOException {
        JSONObject fileContent = FileUtilities.readJSONFile(pathToFile);
        return JsonDataFileReader.getArrayAsRecords(fileContent, JsonArtifactConstants.JSON_ARTIFACTS_KEY);
    }

    @Override
    public List<JSONObject> readFileRecords(MultipartFile file) throws IOException {
        JSONObject fileContent = FileUtilities.readMultiPartJSONFile(file);
        return JsonDataFileReader.getArrayAsRecords(fileContent, JsonArtifactConstants.JSON_ARTIFACTS_KEY);
    }

    @Override
    public Pair<ArtifactAppEntity, String> parseRecord(JSONObject entityRecord) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            ArtifactAppEntity artifactAppEntity = mapper.readValue(entityRecord.toString(), ArtifactAppEntity.class);
            return new Pair<>(artifactAppEntity, null);
        } catch (Exception e) {
            return new Pair<>(null, e.getMessage());
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class JsonArtifactConstants {
        public static final String JSON_ARTIFACTS_KEY = "artifacts";
    }
}
