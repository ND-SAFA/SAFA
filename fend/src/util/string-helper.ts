import { VersionSchema } from "@/types";

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
 * Converts `camelCase` to `Sentence Case`.
 *
 * @param str - The string to convert.ize.
 *
 * @return The capitalized string.
 */
export function camelcaseToDisplay(str: string): string {
  return capitalize(str.replace(/([A-Z])/g, " $1"));
}

/**
 * Converts `UPPER_CASE` to `Sentence Case`.
 *
 * @param str - The string to convert.
 *
 * @return The capitalized string.
 */
export function uppercaseToDisplay(str: string): string {
  return str
    .split("_")
    .map((word) => capitalize(word))
    .join(" ");
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

  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    weekday: "short",
    hour: "numeric",
    minute: "numeric",
  });
}

/**
 * Stringifies the version number.
 *
 * @param currentVersion - The current version number.
 *
 * @return The stringified version number.
 */
export function versionToString(currentVersion?: VersionSchema): string {
  if (currentVersion === undefined) {
    return "X.X.X";
  }
  return `${currentVersion.majorVersion}.${currentVersion.minorVersion}.${currentVersion.revision}`;
}

/**
 * Sanitizes the id of a node so it is valid in the DOM.
 * @param id - The artifact id.
 * @return The sanitized artifact id.
 */
export function sanitizeNodeId(id?: string): string {
  return id?.replace(/^[^a-z]+|[^\w:.-]+/gi, "") || "";
}

/**
 * Converts a duration in ms to a displayable string.
 * @param duration - The duration in ms.
 * @return The displayable duration.
 */
export function displayDuration(duration: number): string {
  if (duration <= 0) return "0 Minutes";

  const hours = Math.floor(duration / 3600000);
  const minutes = Math.floor((duration % 3600000) / 60000);
  const hoursDisplay = `${hours} Hour${hours === 1 ? "" : "s"}`;
  const minutesDisplay = `${minutes} Minute${minutes === 1 ? "" : "s"}`;

  return hours ? `${hoursDisplay}, ${minutesDisplay}` : minutesDisplay;
}
