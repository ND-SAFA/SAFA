package edu.nd.crc.safa.features.permissions.checks.billing;

import java.util.Set;

import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.permissions.checks.utility.CompositeCheck;

/**
 * Class to give a name to checking if an org is recurring/unlimited payment tier
 */
public class HasUnlimitedCreditsCheck extends CompositeCheck {
    public HasUnlimitedCreditsCheck() {
        super(new PaymentTierCheck(Set.of(PaymentTier.RECURRING, PaymentTier.UNLIMITED)));
    }

    @Override
    public String getMessage() {
        return "Payment tier must allow for unlimited credit usage";
    }
}
