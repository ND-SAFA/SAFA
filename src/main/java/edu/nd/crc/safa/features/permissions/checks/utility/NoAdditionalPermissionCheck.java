package edu.nd.crc.safa.features.permissions.checks.utility;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

public class NoAdditionalPermissionCheck implements AdditionalPermissionCheck {
    @Override
    public boolean doCheck(PermissionCheckContext context) {
        return true;
    }
}
