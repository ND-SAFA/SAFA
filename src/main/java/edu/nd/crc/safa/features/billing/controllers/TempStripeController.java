package edu.nd.crc.safa.features.billing.controllers;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class TempStripeController extends BaseController {

    private final BillingService billingService;
    private final OrganizationService organizationService;

    public TempStripeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                BillingService billingService, OrganizationService organizationService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
        this.organizationService = organizationService;
    }

    @GetMapping("/stripe/checkout/{amount}")
    public String getCheckoutUrl(@PathVariable int amount) {
        Organization organization = organizationService.getPersonalOrganization(getCurrentUser());
        return billingService.startTransaction(organization, amount, "Test transaction");
    }
}
