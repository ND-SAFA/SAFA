package edu.nd.crc.safa.features.permissions.checks.utility;

import java.util.List;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class AndPermissionCheck implements AdditionalPermissionCheck {

    private List<AdditionalPermissionCheck> children;

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        return children.stream().allMatch(c -> c.doCheck(context));
    }

    @Override
    public String getMessage() {
        return "All of the following:\n  "
            + String.join("  \n", children.stream().map(AdditionalPermissionCheck::getMessage).toList());
    }
}
