package edu.nd.crc.safa.features.tgen.method.bert;

import edu.nd.crc.safa.common.SafaRequestBuilder;

/**
 * Bert model trained to predict traces between (natural language) NL to NL artifacts.
 */
public class AutomotiveBert extends TBert {
    public AutomotiveBert(SafaRequestBuilder safaRequestBuilder) {
        super(safaRequestBuilder);
    }

    @Override
    BertMethodIdentifier getBertMethodIdentifier() {
        return new BertMethodIdentifier(
            "nl_bert",
            "thearod5/automotive"
        );
    }
}
