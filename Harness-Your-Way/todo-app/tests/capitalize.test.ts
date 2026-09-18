import assert from "node:assert/strict";
import test from "node:test";

import { capitalize } from "../src/capitalize.ts";

test("capitalizes the first character", () => {
  assert.equal(capitalize("hello"), "Hello");
});

test("trims surrounding whitespace before capitalizing", () => {
  assert.equal(capitalize("  hello  "), "Hello");
});

test("returns an empty string for empty or whitespace-only input", () => {
  assert.equal(capitalize(""), "");
  assert.equal(capitalize("   \t\n"), "");
});

test("preserves the remaining characters", () => {
  assert.equal(capitalize("hELLO"), "HELLO");
});

test("handles the first Unicode code point without splitting it", () => {
  assert.equal(capitalize("élan"), "Élan");
  assert.equal(capitalize("😀smile"), "😀smile");
  assert.equal(capitalize("你好"), "你好");
});
