# Authoring diagrams in docs

This page is for **documentation authors** (not end users). It explains how to render Ladder Diagram and Function Block Diagram examples inline in the Autonomy Edge user manual using the built-in JSON-based diagram viewers.

The two viewers are React components that ship inside the docs renderer:

- `<LadderDiagramViewer src="..." />` — renders a Ladder Diagram from JSON.
- `<FBDDiagramViewer src="..." />` — renders a Function Block Diagram from JSON.

Both fetch their JSON from a path under `/docs/...` in the autonomy-edge frontend's `public/` tree. Paths must be absolute (start with `/`), point at a file inside `public/docs/`, and not contain `..` traversal.

## MDX usage

In a docs `.md` (rendered as MDX), embed:

```mdx
<LadderDiagramViewer src="/docs/diagrams/ladder/seal-in.json" />

<FBDDiagramViewer src="/docs/diagrams/fbd/sfb-ton-basic.json" />
```

The viewer is scrollable, pannable, zoomable. Errors (missing file, bad JSON, schema violations) render inline as a small red box with the message.

## Where the JSON files live

Authored JSON lives in:

```
autonomy-edge/apps/frontend/public/docs/diagrams/
  ├─ ladder/
  │   ├─ basic-contact-coil.json
  │   ├─ seal-in.json
  │   └─ ...
  └─ fbd/
      ├─ sfb-ton-basic.json
      ├─ fbd-examples-pump-control.json
      └─ ...
```

There are already 26 LD and 22 FBD examples checked in — use them where they fit. Add new ones only when the existing library doesn't cover the case.

## Ladder schema

```jsonc
{
  "comment": "optional header text",
  "rungNumber": 1,
  "elements": [
    {
      "type": "contact",
      "variant": "default" | "negated" | "risingEdge" | "fallingEdge",
      "variable": "start_button"
    },
    {
      "type": "coil",
      "variant": "default" | "negated" | "set" | "reset" | "risingEdge" | "fallingEdge",
      "variable": "motor"
    },
    {
      "type": "block",
      "name": "TON",
      "inputs": ["IN", "PT"],
      "outputs": ["Q", "ET"]
    },
    {
      "type": "parallel",
      "branches": [
        [ /* DiagramElement[] for top branch */ ],
        [ /* DiagramElement[] for bottom branch */ ]
      ]
    }
  ]
}
```

The renderer auto-lays out the rung horizontally across a fixed 1000-pixel viewBox. Variable labels render above each contact and coil. Edge contacts and coils show `P` (rising) or `N` (falling) markers. Negated variants show a slash; set/reset coils show `S` or `R` inside the coil ovals.

## FBD schema

```jsonc
{
  "comment": "optional header text",
  "diagramNumber": 1,
  "nodes": [
    {
      "id": "ton",
      "type": "block",
      "position": { "x": 280, "y": 50 },
      "data": {
        "name": "TON",
        "blockType": "function-block",  // or "function"
        "executionControl": false,       // optional; true prepends EN/ENO
        "instanceName": "delay_5s",      // optional small label above the block
        "inputs":  [{ "name": "IN", "type": "BOOL" }, { "name": "PT", "type": "TIME" }],
        "outputs": [{ "name": "Q",  "type": "BOOL" }, { "name": "ET", "type": "TIME" }]
      }
    },
    {
      "id": "in_var",
      "type": "input-variable",   // or "output-variable", "inout-variable"
      "position": { "x": 50, "y": 60 },
      "data": { "name": "sensor1" }
    },
    {
      "id": "c1",
      "type": "connector",        // or "continuation"
      "position": { "x": 200, "y": 100 },
      "data": { "label": "X1" }
    },
    {
      "id": "note",
      "type": "comment",
      "position": { "x": 0, "y": 0 },
      "data": { "content": "Multi-line\nnote text", "width": 200, "height": 80 }
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "in_var",
      "sourceHandle": "output",
      "target": "ton",
      "targetHandle": "IN"
    }
  ]
}
```

### Handle conventions

- **Block** — handle names are the literal pin names from `data.inputs[].name` and `data.outputs[].name`. With `executionControl: true`, implicit `EN` (input) and `ENO` (output) handles come first.
- **input-variable** — one output handle named `output` (right side).
- **output-variable** — one input handle named `input` (left side).
- **inout-variable** — input handle `input` on the left, output handle `output` on the right.
- **connector** / **continuation** — single handle each; the renderer ignores the handle name.

### Layout tips

Positions are absolute pixels in a coordinate space the viewer auto-fits via `computeViewBox`.

Standard sizes (so you can hand-author lined-up diagrams):

- Block width: **216**.
- Block input/output row pitch: **48** (`y` offset of pin `i` is `48 + 48 * i` from block top).
- Variable size: **128 × 32**.
- Comment box: whatever `data.width` × `data.height` you set.

To wire a block input to an input-variable, place the variable so its connector Y (`y + 16`) lines up with the block's input pin Y (`y + 48 + 48 * pinIndex`).

## Example: TON with two input variables

```jsonc
{
  "comment": "Pulse-extending delay",
  "nodes": [
    { "id": "trigger", "type": "input-variable", "position": { "x": 50, "y": 50 },
      "data": { "name": "start" } },
    { "id": "preset", "type": "input-variable", "position": { "x": 50, "y": 110 },
      "data": { "name": "delay_ms" } },
    { "id": "ton", "type": "block", "position": { "x": 240, "y": 24 },
      "data": {
        "name": "TON", "blockType": "function-block", "instanceName": "delay",
        "inputs":  [{ "name": "IN", "type": "BOOL" }, { "name": "PT", "type": "TIME" }],
        "outputs": [{ "name": "Q",  "type": "BOOL" }, { "name": "ET", "type": "TIME" }]
      } },
    { "id": "out", "type": "output-variable", "position": { "x": 540, "y": 50 },
      "data": { "name": "motor" } }
  ],
  "edges": [
    { "id": "e1", "source": "trigger", "sourceHandle": "output", "target": "ton", "targetHandle": "IN" },
    { "id": "e2", "source": "preset",  "sourceHandle": "output", "target": "ton", "targetHandle": "PT" },
    { "id": "e3", "source": "ton", "sourceHandle": "Q", "target": "out", "targetHandle": "input" }
  ]
}
```

## When to use a diagram viewer vs. a screenshot

- **Use a diagram viewer** for stable, canonical reference content (block specs, pattern examples, conceptual illustrations). Crisp at any zoom. Diffable in git.
- **Use a screenshot** for showing the editor's UI surrounding a body (the activity bar, the variables table above, modal dialogs, the breadcrumb). Anything that's about the **editor**, not the **diagram**.

## What's next

- Browse the existing example library at `autonomy-edge/apps/frontend/public/docs/diagrams/{ladder,fbd}/`.
- For block reference pages, use the same JSON-driven approach — see **[Timer function blocks](standard-function-blocks/timer-blocks)** for a worked example.
