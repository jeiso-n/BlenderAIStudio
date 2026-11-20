# MUTEFRAME — Free AI 3D Asset & Scene Pipeline

**Status:** Approved architecture / implementation specification  
**Date:** 2026-11-20  
**Workflow repository:** BlenderAIStudio (instructions, architecture, MCP and agent coordination only)  
**Production repository:** MuteStudio (all actual production assets, Blender projects, models, textures, renders and reports)

## 1. Mission

Build a reusable, zero-subscription-cost asset pipeline for stylized educational 3D animations. AI should accelerate asset creation, while Blender remains the source of truth for geometry assembly, materials, rigging, animation, cameras, lighting and rendering. This is a Blender production workflow, not AI video generation.

The pipeline must support complete scenes: characters, buildings, environments, vehicles, furniture, vegetation, props, terrain, materials and reusable set dressing.

## 2. Non-negotiable studio constraints

- MUTEFRAME videos are completely silent: no voiceover, music, sound effects, artificial audio or ambient sound. Exported videos must contain no audio stream.
- Initial delivery target: vertical 1080×1920, 9:16, 30 FPS, MP4/H.264, 10–30 seconds; Blender Eevee.
- Save an editable `.blend` project and retain source assets for every production.
- Use stylized educational visuals: readable silhouettes, coherent proportions, clean/simple materials, soft cinematic lighting and consistent art direction.
- Keep the current workstation in mind: Windows 11, AMD Ryzen 5 5500U, integrated AMD Radeon graphics, approximately 7.3 GB usable RAM and approximately 192 GB free on D: at the 2026-11-20 audit.
- Blender 5.3.0, BlendRelay MCP 0.7.8, Python 3.13.17 and FFmpeg 9.0.1 are already installed/verified. Do not install duplicate Blender/Python or large model checkpoints without a measured need.
- Keep previews lightweight: Eevee, low sample counts, simple geometry, small textures and reduced resolution (e.g. 360×640 or 540×960).
- GitHub is the source of truth. All commits must be made directly on GitHub. Never run local `git commit` or `git push`.
- BlenderAIStudio is workflow/reference only. Do not store MUTEFRAME production deliverables here; those belong in the private MuteStudio repository.
- Do not overwrite historical previews or approved projects.

## 3. Free tool strategy

### Primary generation
**Meshy Free** is the first hosted generator to test. Current published free-plan documentation states 100 credits/month and up to 10 downloads/month for eligible Meshy 6 Lite models. Free outputs are CC BY 4.0, so every released asset needs the required attribution recorded. The factory must check model version and download eligibility before spending credits.

Official references:
- https://www.meshy.ai/
- https://help.meshy.ai/en/articles/15696428-what-is-included-on-the-free-plan
- https://docs.meshy.ai/en/webapp/pricing

### Secondary generation
**Tripo Free** may be used for experiments and non-release prototypes. Its published October 2026 pricing states 200 credits/month, but free exports are limited to H2.5 and the free-plan ownership/attribution terms are restrictive. Do not use Tripo free outputs in monetized/public MUTEFRAME deliverables unless the exact current terms are reviewed and cleared first.

- https://www.tripo3d.ai/product-doc/getting-started/pricing-credits

### Asset libraries
- **Poly Haven:** prioritize CC0 models, textures and HDRIs; retain source URLs and downloaded asset names for traceability. https://polyhaven.com/
- **Sketchfab:** use only downloadable assets whose individual licence explicitly permits the intended use; record attribution requirements. https://sketchfab.com/

### Advanced local generation — deferred
- **Microsoft TRELLIS.2:** technically promising and MIT-licensed project, but its documented local setup is Linux-only and requires an NVIDIA GPU with at least 24 GB VRAM. The current Windows AMD integrated-graphics workstation is not suitable. Do not attempt local installation. Reconsider only if an accessible hosted inference route and its terms are verified, or hardware changes. https://github.com/microsoft/TRELLIS.2
- **Tencent Hunyuan3D-2:** has Windows support and Blender integration, but the published project uses the Tencent Hunyuan non-commercial licence. Exclude it from MUTEFRAME commercial/release production unless licensing is independently verified as compatible. https://github.com/Tencent-Hunyuan/Hunyuan3D-2

Never describe a tool as unlimited or fully free when it has credits, export limits, attribution requirements, restrictive licences or hardware costs.

## 4. Core design principle: assemble scenes from reusable assets

Do not ask one image-to-3D model to produce an entire animated scene. Generate or source individual components, then assemble them in Blender.

Example scene: a historical Ugandan telecommunications setting:
- Building shells and architectural details
- Human characters and clothing
- Telephones, switchboards and cables
- Desks, chairs and other furniture
- Roads, terrain, trees and background structures
- Lighting, camera and animation authored in Blender

Use procedural Blender geometry for simple/repetitive assets (walls, floors, roads, poles, fences, stairs, platforms, terrain blocks, stylized trees and primitive props) rather than spending AI credits unnecessarily.

Build reusable collections and scene kits so one approved asset can appear in multiple episodes.

## 5. Production architecture

The asset workflow should have these logical stages:

1. **Brief parser:** receives a scene description or storyboard and produces an asset list with visual references, approximate dimensions, intended use and priority.
2. **Asset source selector:** chooses procedural Blender construction, approved library asset or hosted AI generation. Prefer the cheapest legally safe source.
3. **Generation intake:** records prompt, source image, generator/model/version, date, job ID and original download.
4. **Format importer:** supports GLB/glTF first, then FBX and OBJ where needed. Preserve source files.
5. **Geometry inspection:** detect empty meshes, invalid transforms, extreme polygon counts, missing materials, broken normals, non-manifold geometry where relevant and unexpected dimensions.
6. **Normalization:** apply consistent units/origin/scale conventions; do not destructively alter the preserved original.
7. **Style processing:** assign approved MUTEFRAME materials/palette and optional toon/flat-shaded treatment. Keep materials editable.
8. **Character preparation:** distinguish static props from characters; inspect topology and deformation suitability before rigging. Do not auto-rig every mesh blindly.
9. **Asset registry:** store searchable metadata, tags, preview image, file paths, licence and attribution.
10. **Scene assembly:** place linked/reusable assets into Blender collections with consistent naming and a camera-safe layout.
11. **QA and render:** create a low-cost preview, inspect it, verify the saved .blend, and only then proceed to approved final settings.

## 6. MuteStudio production repository layout

All actual production assets and deliverables go into the private MuteStudio repository. Proposed layout:

```text
MuteStudio/
├── asset-library/
│   ├── characters/
│   ├── buildings/
│   ├── environments/
│   ├── vehicles/
│   ├── furniture/
│   ├── vegetation/
│   ├── props/
│   ├── materials/
│   └── textures/
├── asset-factory/
│   ├── generators/
│   ├── blender-importer/
│   ├── geometry-cleanup/
│   ├── material-manager/
│   ├── character-prep/
│   ├── scene-assembler/
│   └── quality-checks/
├── templates/
│   ├── character/
│   ├── environment/
│   └── scene/
├── projects/
│   └── <episode-id>/
│       ├── assets/
│       ├── scenes/
│       ├── renders/
│       ├── previews/
│       ├── screen-recordings/
│       └── episode.blend
├── documentation/
│   ├── asset-licences.md
│   ├── generation-prompts.md
│   ├── visual-style-guide.md
│   └── production-guide.md
└── current report.md
```

Confirm the existing MuteStudio repository owner/name and current tree before creating files. Do not guess its URL or initialize a replacement repository.

## 7. Asset manifest and licence records

Every external/generated asset must have a manifest entry with:
- Stable asset ID and display name
- Category and descriptive tags
- Original source URL and creator/provider
- Exact licence name and licence URL
- Commercial-use permission status
- Attribution text, if required
- Generator/model/version and generation date, where applicable
- Prompt and source image reference, where applicable
- Original source file and normalized Blender-ready file
- Preview image
- Polygon count, dimensions, texture sizes and QA status

Use explicit statuses: `approved`, `approved-with-attribution`, `prototype-only`, `rejected`, `licence-review-required`.

Unknown or incompatible rights means the asset cannot enter a public/commercial release. Keep licence records with the production project.

## 8. Blender integration

Use the existing Blender 5.3.0 and BlendRelay MCP integration. Keep Blender as the scene authority.

Preferred implementation:
- Blender Python scripts/add-on modules for import, collection organization, metadata, material assignment, previews and QA.
- A small external Python coordinator only where web/API interaction or batch orchestration is needed.
- A clear hand-off directory for generated files; never have an AI web service write directly into a live Blender scene.
- Idempotent operations: rerunning an import/assembly should not duplicate objects.
- Non-destructive source preservation and explicit versioning.
- Unit tests for metadata validation, manifest parsing, file discovery and import decisions; Blender background smoke tests for scene operations.

The factory should not require a paid API. Hosted free tiers are optional sources with quotas; library assets and procedural Blender generation must remain usable when quotas are exhausted.

## 9. Visual consistency standard

Initial target: stylized educational animation, not photorealism.

Establish a MUTEFRAME style guide covering:
- Character body/head proportion ranges and neutral pose
- Silhouette readability and detail density
- Palette and material roughness
- Flat/toon shading decisions
- Lighting direction, softness and contrast
- Environment scale and camera composition
- Texture resolution budgets
- Naming conventions and collection structure

Do not let every AI-generated asset introduce a different visual style. Prefer controlled materials and Blender-side normalization. For recurring characters, preserve a reference sheet and do not regenerate the character for every scene.

## 10. Implementation milestones and acceptance criteria

### Milestone 0 — repository and hardware audit
- Confirm exact MuteStudio GitHub repository identity and current default branch.
- Inspect BlenderAIStudio's existing scripts, docs and BlendRelay connection without changing unrelated work.
- Confirm current disk/RAM/GPU/Blender/Python facts.
- Record the current workstation's limits.
**Acceptance:** no duplicate installs; correct repository separation; verified environment report.

### Milestone 1 — prove one legal generation/import path
- Test one Meshy 6 Lite asset within the free allowance.
- Test one CC0 Poly Haven asset.
- Save original files and manifest/licence records.
- Import both into Blender and verify materials, scale, orientation and editable geometry.
**Acceptance:** two usable assets in a small Blender test scene, with source/rights documented and no audio stream in any test video.

### Milestone 2 — build the reusable asset intake tool
- Implement manifest schema and validation.
- Implement import/normalize/preview/QA scripts.
- Add duplicate detection and safe naming.
**Acceptance:** repeatable import with no duplicate objects; failed assets are reported rather than silently accepted.

### Milestone 3 — build a small style-consistent starter library
- Create a limited test set across characters, buildings, vegetation, props and environment pieces.
- Prefer procedural construction for simple geometry.
- Record all source and licensing data.
**Acceptance:** assets are searchable and can be reused in more than one scene.

### Milestone 4 — scene assembly template
- Create a stylized educational scene template with collections, camera, lighting, world settings and render presets.
- Add scene manifest and asset references.
**Acceptance:** assemble a complete test scene without manual re-import of each asset.

### Milestone 5 — production pilot
- Produce one complete stylized educational scene using the asset factory.
- Save editable .blend, source assets, preview, screen recording and report.
- Render a silent MP4 with no audio stream.
**Acceptance:** independent visual and technical review passes; all deliverables are stored in MuteStudio.

## 11. Immediate first task for Antigravity

Do not begin by installing TRELLIS, Hunyuan3D, large model weights, or any paid service.

First inspect the existing BlenderAIStudio project and the live Blender/BlendRelay integration. Then prepare a focused implementation plan for Milestone 0 and Milestone 1. Confirm the MuteStudio GitHub repository identity before touching production storage.

The first proof should be deliberately small: one stylized prop generated through Meshy Free and one CC0 library asset, imported into a single Blender scene, with a manifest and preview. No character rigging or full scene automation until this import path passes.

Antigravity must report exact files changed, commands run, test results, screenshots/previews, limitations and next step. Update the durable project report. Never create local Git commits or pushes; all commits go directly to GitHub.
