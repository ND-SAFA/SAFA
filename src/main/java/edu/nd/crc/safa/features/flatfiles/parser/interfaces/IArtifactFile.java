package edu.nd.crc.safa.features.flatfiles.parser.interfaces;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONObject;

public interface IArtifactFile extends IDataFile<ArtifactAppEntity> {
    static void validateArtifactDefinition(JSONObject artifactDefinition) {
        FileUtilities.assertHasKeys(artifactDefinition, AbstractArtifactFile.Constants.REQUIRED_KEYS);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    class Constants {
        public static final List<String> REQUIRED_KEYS = List.of(TimFileParser.Constants.FILE_PARAM);
    }
}
