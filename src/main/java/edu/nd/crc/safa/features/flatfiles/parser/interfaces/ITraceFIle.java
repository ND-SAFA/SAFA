package edu.nd.crc.safa.features.flatfiles.parser.interfaces;

import java.util.List;

import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractTraceFile;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONObject;

public interface ITraceFIle extends IDataFile<TraceAppEntity> {
    static void validateTraceDefinition(JSONObject traceDefinition) {
        FileUtilities.assertHasKeys(traceDefinition, AbstractTraceFile.Constants.REQUIRED_DEFINITION_FIELDS);
        List<String> oneRequired = List.of(AbstractTraceFile.Constants.GENERATE_LINKS_PARAM, TimFileParser.Constants.FILE_PARAM);
        boolean containsOne = false;
        for (String oneRequiredField : oneRequired) {
            if (traceDefinition.has(oneRequiredField)) {
                containsOne = true;
            }
        }
        if (!containsOne) {
            throw new SafaError("Definition missing one of required fields:" + oneRequired);
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    class Constants {
        public static final String GENERATE_LINKS_PARAM = "generatelinks";
        public static final String SOURCE_PARAM = "source";
        public static final String TARGET_PARAM = "target";
        public static final List<String> REQUIRED_DEFINITION_FIELDS = List.of(SOURCE_PARAM, TARGET_PARAM);
    }
}
