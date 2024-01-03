package edu.nd.crc.safa.features.permissions.checks.billing;

import java.util.List;

import edu.nd.crc.safa.features.permissions.checks.utility.CompositeCheck;
import edu.nd.crc.safa.features.permissions.checks.utility.OrPermissionCheck;

/**
 * A check determining if an organization can afford a particular charge,
 * taking into account that some payment tiers ignore balance
 */
public class CanAffordChargeCheck extends CompositeCheck {

    public CanAffordChargeCheck(int chargeAmount) {
        super(
            new OrPermissionCheck(List.of(
                new HasUnlimitedCreditsCheck(),
                new MinimumBalanceCheck(chargeAmount)
            ))
        );
    }
}
