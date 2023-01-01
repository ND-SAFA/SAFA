package edu.nd.crc.safa.features.attributes.services;

import edu.nd.crc.safa.features.attributes.repositories.layouts.ArtifactTypeToLayoutMappingRepository;
import edu.nd.crc.safa.features.attributes.repositories.layouts.AttributeLayoutRepository;
import edu.nd.crc.safa.features.attributes.repositories.layouts.AttributePositionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AttributeLayoutService {

    private final ArtifactTypeToLayoutMappingRepository typeToLayoutRepo;
    private final AttributeLayoutRepository layoutRepo;
    private final AttributePositionRepository positionRepo;

    @Autowired
    public AttributeLayoutService(ArtifactTypeToLayoutMappingRepository typeToLayoutRepo,
                                  AttributeLayoutRepository layoutRepo, AttributePositionRepository positionRepo) {
        this.typeToLayoutRepo = typeToLayoutRepo;
        this.layoutRepo = layoutRepo;
        this.positionRepo = positionRepo;
    }
}
