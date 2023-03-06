package edu.nd.crc.safa.features.attributes.entities;

import java.util.List;
import java.util.UUID;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AttributeLayoutAppEntity implements IAppEntity {

    @NotNull
    @NotEmpty
    private UUID id;

    @NotNull
    @NotEmpty
    private String name;

    @NotNull
    private List<String> artifactTypes;

    @NotNull
    private List<AttributePositionAppEntity> positions;
}
