import { describe, it, expect } from "vitest";
import { truncateLines } from "./stringUtils";

describe("truncateLines", () => {
  it("returns 'N/A' for empty string", () => {
    expect(truncateLines("")).toBe("N/A");
  });

  it("returns the same string if shorter than maxLength", () => {
    expect(truncateLines("Hello World", { maxLength: 20 })).toBe("Hello World");
  });

  it("truncates a long string into 2 lines by default", () => {
    const str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const result = truncateLines(str);
    const lines = result.split("\n");
    expect(lines.length).toBe(2);
    expect(result.endsWith("...")).toBe(true);
  });

  it("respects the lines option", () => {
    const str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const result = truncateLines(str, { lines: 3 });
    const lines = result.split("\n");
    expect(lines.length).toBe(3);
    expect(result.endsWith("...")).toBe(true);
  });

  it("respects the maxLength option", () => {
    const str = "abcdefghijklmnopqrstuvwxyz";
    const result = truncateLines(str, { maxLength: 12, lines: 2 });
    expect(result).toBe("abcdef\nghijkl...");
  });
});
