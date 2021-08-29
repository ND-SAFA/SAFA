package edu.nd.crc.safa.services;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.Warning;
import edu.nd.crc.safa.repositories.WarningRepository;
import edu.nd.crc.safa.warnings.Rule;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class WarningService {

    WarningRepository warningRepository;

    @Autowired
    public WarningService(WarningRepository warningRepository) {
        this.warningRepository = warningRepository;
    }

    public List<Rule> getProjectRules(Project project) {
        List<Warning> projectWarnings = this.warningRepository.findAllByProject(project);
        List<Rule> projectRules = new ArrayList<Rule>();

        for (Warning warning : projectWarnings) {
            projectRules.add(new Rule(warning));
        }
        return projectRules;
    }
}
