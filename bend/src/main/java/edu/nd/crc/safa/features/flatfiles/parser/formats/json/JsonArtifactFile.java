package edu.nd.crc.safa.features.flatfiles.parser.formats.json;

import java.io.File;
import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

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

    public JsonArtifactFile(List<ArtifactAppEntity> artifacts) {
        super(artifacts);
    }

    public JsonArtifactFile(String pathToFile) throws IOException {
        super(pathToFile);
    }

    public JsonArtifactFile(MultipartFile file) throws IOException {
        super(file);
    }

    @Override
    protected void exportAsFileContent(File file) throws IOException {
        this.getEntities().forEach(a -> a.setId(null));
        JSONObject fileContent = JsonFileUtilities.writeEntitiesAsJson(this.getEntities(),
            Constants.JSON_ARTIFACTS_KEY);
        FileUtilities.writeToFile(file, fileContent.toString());
    }

    @Override
    public List<JSONObject> readFileRecords(String pathToFile) throws IOException {
        JSONObject fileContent = JsonFileUtilities.readJSONFile(pathToFile);
        return JsonFileUtilities.getArrayAsRecords(fileContent, Constants.JSON_ARTIFACTS_KEY);
    }

    @Override
    public List<JSONObject> readFileRecords(MultipartFile file) throws IOException {
        JSONObject fileContent = FileUtilities.readMultiPartJSONFile(file);
        return JsonFileUtilities.getArrayAsRecords(fileContent, Constants.JSON_ARTIFACTS_KEY);
    }

    @Override
    public Pair<ArtifactAppEntity, String> parseRecord(JSONObject entityRecord) {
        try {
            ObjectMapper mapper = ObjectMapperConfig.create();
            ArtifactAppEntity artifactAppEntity = mapper.readValue(entityRecord.toString(), ArtifactAppEntity.class);

            List<String> missingFields = artifactAppEntity.getMissingRequiredFields();
            if (missingFields.size() == 0) {
                return new Pair<>(artifactAppEntity, null);
            } else {
                return new Pair<>(null,
                    String.format("Artifact missing one or more required fields: %s", missingFields));
            }
        } catch (Exception e) {
            return new Pair<>(null, String.format("%s: %s", getFilename(), e.getMessage()));
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String JSON_ARTIFACTS_KEY = "artifacts";
    }
}
