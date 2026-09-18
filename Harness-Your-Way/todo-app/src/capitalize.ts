export function capitalize(value: string): string {
  const [first = "", ...rest] = value.trim();

  return first.toUpperCase() + rest.join("");
}
