package edu.nd.crc.safa.features.models.services;

import edu.nd.crc.safa.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.method.bert.NLBert;
import edu.nd.crc.safa.features.tgen.method.bert.PLBert;
import edu.nd.crc.safa.features.tgen.method.bert.TBert;

import org.apache.commons.lang3.NotImplementedException;
import org.springframework.stereotype.Service;

@Service
public class BertService {

    public TBert getBertModel(BaseGenerationModels generationModel,
                              SafaRequestBuilder safaRequestBuilder) {
        switch (generationModel) {
            case PLBert:
                return new PLBert(safaRequestBuilder);
            case NLBert:
                return new NLBert(safaRequestBuilder);
            default:
                throw new NotImplementedException("Trace method not implemented:" + generationModel);
        }
    }
}
