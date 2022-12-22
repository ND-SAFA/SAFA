package edu.nd.crc.safa.features.artifacts.services;

import edu.nd.crc.safa.features.artifacts.repositories.schema.CustomAttributeRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactFieldVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.BooleanFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.FloatFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.IntegerFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.StringArrayFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.StringFieldValueRepository;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Data
@Scope("singleton")
public class ArtifactSystemServiceProvider {

    private ArtifactFieldVersionRepository artifactFieldVersionRepository;
    private CustomAttributeRepository customAttributeRepository;
    private BooleanFieldValueRepository booleanFieldValueRepository;
    private FloatFieldValueRepository floatFieldValueRepository;
    private IntegerFieldValueRepository integerFieldValueRepository;
    private StringArrayFieldValueRepository stringArrayFieldValueRepository;
    private StringFieldValueRepository stringFieldValueRepository;
}
