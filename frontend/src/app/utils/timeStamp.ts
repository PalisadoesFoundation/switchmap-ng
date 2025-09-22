/**
 * Converts a Unix timestamp (in seconds) to a human-readable date and time string.
 * If the timestamp is invalid or not provided, it returns "Unknown".
 * @param timestamp - The Unix timestamp in seconds (string or number).
 * @returns A formatted date and time string or "Unknown".
 */
export const formatUnixTimestamp = (timestamp?: string | number | null): string => {
  if (!timestamp) return "Unknown";

  const tsNumber = typeof timestamp === "string" ? Number(timestamp) : timestamp;

  if (isNaN(tsNumber) || tsNumber <= 0) return "Unknown";

  const date = new Date(tsNumber * 1000);
  return date.toLocaleString();
}
