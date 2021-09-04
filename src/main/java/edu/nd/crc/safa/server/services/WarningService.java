package edu.nd.crc.safa.server.services;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.Warning;
import edu.nd.crc.safa.db.repositories.sql.WarningRepository;
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
