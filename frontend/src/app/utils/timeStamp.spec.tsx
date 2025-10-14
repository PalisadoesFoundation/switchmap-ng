import { describe, it, expect } from "vitest";
import { formatUnixTimestamp } from "./timeStamp";

describe("formatUnixTimestamp", () => {
  it("returns 'Unknown' for undefined, null, or empty string", () => {
    expect(formatUnixTimestamp()).toBe("Unknown");
    expect(formatUnixTimestamp(null)).toBe("Unknown");
    expect(formatUnixTimestamp("")).toBe("Unknown");
  });

  it("returns 'Unknown' for non-numeric or non-positive values", () => {
    expect(formatUnixTimestamp("abc")).toBe("Unknown");
    expect(formatUnixTimestamp(-123)).toBe("Unknown");
    expect(formatUnixTimestamp(0)).toBe("Unknown");
  });

  it("formats valid numeric timestamps correctly", () => {
    const ts = 1693574400;
    const formatted = formatUnixTimestamp(ts);
    expect(new Date(ts * 1000).toLocaleString()).toBe(formatted);
  });

  it("formats valid string timestamps correctly", () => {
    const tsStr = "1693574400";
    const formatted = formatUnixTimestamp(tsStr);
    expect(new Date(Number(tsStr) * 1000).toLocaleString()).toBe(formatted);
  });
});
