# Exercise 1: Build a Cards Block

**Duration**: 20 minutes

## Prerequisites

- Node.js v18+
- AEM CLI installed (`npm install -g @adobe/aem-cli`)
- Dev server running at `http://localhost:3000`

## Background

### What You'll Learn

- How EDS blocks read their DOM structure
- How to add CSS variations

### How It Works

The block decorator reads rows and columns from the HTML table.

## Steps

1. **Create the block folder**

   ```bash
   mkdir -p blocks/cards
   touch blocks/cards/cards.js blocks/cards/cards.css
   ```

2. **Write the decorator**

   ```javascript
   export default function decorate(block) {
     const rows = [...block.querySelectorAll(':scope > div')];
     rows.forEach((row) => row.classList.add('cards-item'));
   }
   ```

## Verification

- [ ] Block folder exists at `blocks/cards/`
- [ ] Dev server shows cards rendering at `http://localhost:3000/test`
- [ ] No console errors

## References

- [Block Collection](https://www.aem.live/developer/block-collection)
