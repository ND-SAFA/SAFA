package edu.nd.crc.safa.features.tgen.method.bert;

import edu.nd.crc.safa.common.SafaRequestBuilder;

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
            "se_bert",
            "thearod5/sebert-task-cls"
        );
    }
}
