package edu.nd.crc.safa.features.billing.entities.app;

import edu.nd.crc.safa.features.billing.entities.MonthlyUsage;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class BillingInfoAppEntity {
    private PaymentTier paymentTier;
    private int monthlyRemainingCredits;
    private int monthlyUsedCredits;
    private int monthlySuccessfulCredits;
    private int totalUsedCredits;
    private int totalSuccessfulCredits;

    public BillingInfoAppEntity(Organization organization, BillingInfo billingInfo, MonthlyUsage monthlyUsage) {
        this.paymentTier = organization.getPaymentTier();
        this.monthlyRemainingCredits = billingInfo.getBalance();
        this.monthlyUsedCredits = monthlyUsage.getUsedCredits();
        this.monthlySuccessfulCredits = monthlyUsage.getSuccessfulCredits();
        this.totalUsedCredits = billingInfo.getTotalUsed();
        this.totalSuccessfulCredits = billingInfo.getTotalSuccessful();
    }
}
