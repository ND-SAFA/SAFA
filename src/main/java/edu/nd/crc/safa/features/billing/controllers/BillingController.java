package edu.nd.crc.safa.features.billing.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
public class BillingController extends BaseController {

    private final BillingService billingService;

    public BillingController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                             BillingService billingService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
    }

    @PostMapping(AppRoutes.Billing.CHECKOUT)
    public TransactionAppEntity purchaseCredits(@RequestBody PurchaseDetailsDTO purchaseDetails) {
        Organization organization = getResourceBuilder().fetchOrganization(purchaseDetails.getOrganizationId())
            .withPermission(OrganizationPermission.VIEW_BILLING, getCurrentUser())
            .get();
        return billingService.startTransaction(organization, purchaseDetails.getAmount(),
            purchaseDetails.getDescription());
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PurchaseDetailsDTO {
        private UUID organizationId;
        private int amount;
        private String description;
    }

}
