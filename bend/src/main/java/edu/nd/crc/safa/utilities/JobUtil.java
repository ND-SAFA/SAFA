package edu.nd.crc.safa.utilities;

import static edu.nd.crc.safa.config.ProjectVariables.EMPTY_TIM_CONTENT;
import static edu.nd.crc.safa.config.ProjectVariables.TIM_FILENAME;

import java.nio.charset.StandardCharsets;
import java.util.List;

import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

public class JobUtil {
    /**
     * Supplies a default list of files for an upload in case an empty upload is given.
     *
     * @return The default files. Currently, just the most basic tim.json
     */
    public static List<MultipartFile> defaultFileListSupplier() {
        return List.of(new MockMultipartFile(TIM_FILENAME, TIM_FILENAME,
            null, EMPTY_TIM_CONTENT.getBytes(StandardCharsets.UTF_8)));
    }
}
