package edu.nd.crc.safa.features.tgen.method;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class BertMethodIdentifier {
    /**
     * The transformers class defining model architecture.
     */
    String baseModel;
    /**
     * Path to model weights.
     */
    String statePath;
}
