package edu.nd.crc.safa.features.permissions.checks;

import java.util.List;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class AndPermissionCheck implements AdditionalPermissionCheck {

    private List<AdditionalPermissionCheck> children;

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        return children.stream().allMatch(c -> c.doCheck(context));
    }
}
