package edu.nd.crc.safa.features.models.tgen.method.bert;

import edu.nd.crc.safa.features.common.SafaRequestBuilder;

/**
 * Bert model trained to predict traces between natural language to programming language artifacts.
 */
public class PLBert extends TBert {

    public PLBert(SafaRequestBuilder safaRequestBuilder) {
        super(safaRequestBuilder);
    }

    @Override
    BertMethodIdentifier getBertMethodIdentifier() {
        return new BertMethodIdentifier(
            "PL_BERT",
            "thearod5/tbert"
        );
    }
}
