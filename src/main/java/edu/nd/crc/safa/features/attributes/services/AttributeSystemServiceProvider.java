package edu.nd.crc.safa.features.attributes.services;

import edu.nd.crc.safa.features.attributes.repositories.definitions.CustomAttributeRepository;
import edu.nd.crc.safa.features.attributes.repositories.definitions.FloatAttributeInfoRepository;
import edu.nd.crc.safa.features.attributes.repositories.definitions.IntegerAttributeInfoRepository;
import edu.nd.crc.safa.features.attributes.repositories.definitions.SelectionAttributeOptionRepository;
import edu.nd.crc.safa.features.attributes.repositories.values.ArtifactAttributeVersionRepository;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Data
@Scope("singleton")
public class AttributeSystemServiceProvider {
    private ArtifactAttributeVersionRepository artifactAttributeVersionRepository;
    private CustomAttributeRepository customAttributeRepository;
    private FloatAttributeInfoRepository floatAttributeInfoRepository;
    private IntegerAttributeInfoRepository integerAttributeInfoRepository;
    private SelectionAttributeOptionRepository selectionAttributeOptionRepository;
}
