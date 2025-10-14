package edu.nd.crc.safa.features.permissions.checks.utility;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

public class NoAdditionalPermissionCheck implements AdditionalPermissionCheck {
    @Override
    public boolean doCheck(PermissionCheckContext context) {
        return true;
    }

    @Override
    public String getMessage() {
        // Since we always return true above, there's no reason for anyone to see this message
        return "If you are seeing this message, please report it to the devs";
    }

    @Override
    public boolean superuserCanOverride() {
        return false;
    }
}
