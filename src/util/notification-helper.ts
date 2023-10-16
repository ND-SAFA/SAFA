const PROJECT_TOPICS = ["/topic/project", "/topic/version"];

/**
 * Creates human readable log for topic.
 * @param topic The topic to translate.
 */
export function formatTopic(topic: string): string {
  const sections = topic.split("/");
  return sections[2] + "(" + sections[3] + ").";
}

/**
 * Determines if topic is related to a project or version of a project.
 * @param topic The topic to evaluate.
 */
export function isProjectTopic(topic: string): boolean {
  return PROJECT_TOPICS.map((t) => topic.includes(t)).reduce((p, c) => p || c);
}
