package edu.nd.crc.safa.features.models.tgen.method.bert;

import edu.nd.crc.safa.features.common.SafaRequestBuilder;

/**
 * Bert model trained to predict traces between (natural language) NL to NL artifacts.
 */
public class NLBert extends TBert {
    public NLBert(SafaRequestBuilder safaRequestBuilder) {
        super(safaRequestBuilder);
    }

    @Override
    BertMethodIdentifier getBertMethodIdentifier() {
        return new BertMethodIdentifier(
            "NL_BERT",
            "thearod5/nl-bert"
        );
    }
}
