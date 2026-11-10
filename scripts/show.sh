#!/bin/bash
# print hints + prepared English for one or more pages (paths relative to work/en, .md optional)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for p in "$@"; do
  p="${p%.md}"
  echo "################ PAGE: $p.md"
  echo "-- terms (H=heading G=glossary; '=' official zh UI name):"
  head -n 45 "$ROOT/work/hints/$p.txt"
  echo "-- text:"
  cat "$ROOT/work/en/$p.md"
done
