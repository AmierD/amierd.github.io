// Discord-style spoilers: ||hidden text|| -> <span class="spoiler" tabindex="0">.
// Runs on the raw markdown (textTransform), so formatting inside the spoiler
// (bold, `code`) is still parsed normally between the span tags.
// Code blocks are handled separately after highlighting (see rehypeCodeSpoilers).
// Styled in quartz/styles/custom.scss.

export const manifest = {
  name: "spoiler-syntax",
  displayName: "Spoiler syntax",
  description: "Turns ||text|| into a Discord-style spoiler span",
  version: "0.1.0",
  category: "transformer",
}

const FENCE = /^[\s>]*(```|~~~)/ // `>` so fences inside blockquotes/callouts count
const TABLE_ROW = /^\s*\|/ // `||` in a table means an empty cell
const INLINE_CODE = /(`+)[^`]*?\1/g
// no space just inside the pipes, so `a || b` in prose is left alone
const SPOILER = /\|\|(?=\S)(.+?)(?<=\S)\|\|/g

function transformLine(line) {
  if (TABLE_ROW.test(line)) return line

  // hide inline code so `a || b` isn't matched, but code *inside* a spoiler survives
  const codes = []
  const masked = line.replace(INLINE_CODE, (code) => `\u0000${codes.push(code) - 1}\u0000`)

  return masked
    .replace(SPOILER, '<span class="spoiler" tabindex="0">$1</span>')
    .replace(/\u0000(\d+)\u0000/g, (_, i) => codes[i])
}

// Code blocks: fences are left alone above, so their `||` survive until after
// syntax highlighting. Here we split them into spoiler spans, but only inside
// comment and string tokens, since `||` in real code is logical OR.
const CODE_TOKEN_TYPES = new Set(["comment", "string"])

function spoilerSpan(text) {
  return {
    type: "element",
    tagName: "span",
    properties: { className: ["spoiler"], tabIndex: 0 },
    children: [{ type: "text", value: text }],
  }
}

function splitSpoilers(value) {
  const parts = []
  let last = 0
  for (const match of value.matchAll(SPOILER)) {
    if (match.index > last) parts.push({ type: "text", value: value.slice(last, match.index) })
    parts.push(spoilerSpan(match[1]))
    last = match.index + match[0].length
  }
  if (parts.length === 0) return null
  if (last < value.length) parts.push({ type: "text", value: value.slice(last) })
  return parts
}

function rehypeCodeSpoilers() {
  const walk = (node) => {
    if (!node.children) return
    const isToken = CODE_TOKEN_TYPES.has(node.properties?.dataTokenType)
    node.children = node.children.flatMap((child) => {
      if (isToken && child.type === "text") return splitSpoilers(child.value) ?? child
      walk(child)
      return child
    })
  }
  return (tree) => walk(tree)
}

export default function SpoilerSyntax() {
  return {
    name: "SpoilerSyntax",
    // must run after syntax highlighting (see `order` in quartz.config.yaml)
    htmlPlugins: () => [rehypeCodeSpoilers],
    textTransform(_ctx, src) {
      let inFence = false
      return src
        .split("\n")
        .map((line) => {
          if (FENCE.test(line)) {
            inFence = !inFence
            return line
          }
          return inFence ? line : transformLine(line)
        })
        .join("\n")
    },
  }
}
