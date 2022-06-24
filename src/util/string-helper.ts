/**
 * Returns given string with newlines inserted after maxWordCount
 * has been reached.
 *
 * @param str - The original string.
 * @param maxWordCount - The maximum number of words to have per line.
 *
 * @returns The updated input string.
 */
export function splitIntoLines(str: string, maxWordCount: number): string {
  const words = str.split(" ");
  let finalString = "";
  let count = 0;

  words.forEach((w) => {
    if (count < maxWordCount) {
      finalString += w + " ";
      count++;
    } else {
      finalString += w + "\n";
      count = 0;
    }
  });

  return finalString;
}

/**
 * Capitalizes the first letter of the given string.
 *
 * @param str - The string to capitalize.
 *
 * @return The capitalized string.
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/**
 * Capitalizes the first letter of all words in the given string.
 *
 * @param str - The string to capitalize.
 *
 * @return The capitalized string.
 */
export function capitalizeSentence(str: string): string {
  return str
    .split(" ")
    .map((word) => capitalize(word))
    .join(" ");
}

/**
 * @deprecated Remove when project creator done.
 *
 * Returns the sentence case name of the artifact type.
 *
 * @param type - The type to stringify.
 *
 * @return The sentence case type name.
 */
export function getArtifactTypePrintName(type?: string): string {
  const nameMap: Record<string, string> = {
    requirement: "Requirements",
    design: "Designs",
    hazard: "Hazards",
    environmentalassumption: "Environmental Assumptions",
    safetyrequirement: "Safety Requirement",
  };

  return type
    ? nameMap[type.toLowerCase()] || capitalizeSentence(type.toLowerCase())
    : "Unknown Type";
}

/**
 * Converts an enum value in capital snake case into a title case string.
 *
 * @param value - The value to convert.
 * @return The displayable value.
 */
export function enumToDisplay(value: string): string {
  return value
    .split("_")
    .map((word) => capitalize(word.toLowerCase()))
    .join(" ");
}
/**
 * Converts a timestamp to a display value.
 *
 * @param timestamp - The timestamp to convert.
 * @return The displayable value.
 */
export function timestampToDisplay(timestamp: string): string {
  const date = new Date(timestamp);
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
    hour: "numeric",
    minute: "numeric",
  };

  return date.toLocaleDateString("en-US", options);
}
