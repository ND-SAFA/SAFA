from tgen.data.prompts.prompt import Prompt


class ArtifactPrompt(Prompt):

    def build_as_xml(self):
        """
        <artifact>
            <id>ID</id>
            <body>BODY</body>
        </artifact>
        """
        raise NotImplementedError()

    def build_without_id(self):
        """
        [BODY]
        """
        raise NotImplementedError()

    def build_with_id(self):
        """
        [ID]: [BODY]
        """
        raise NotImplementedError()
