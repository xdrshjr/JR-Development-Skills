---
name: nano-banana-draw
description: "Generate or edit images using Google's Nano Banana Pro (Gemini 3 Pro Image) model. Use when the user asks to generate an image, create artwork, draw something, edit a photo, or mentions 'generate image', 'draw', 'create picture', 'image generation', 'edit image', '生成图片', '画图', '绘图', '修图', '图片编辑'."
---

# Nano Banana Draw — AI Image Generation & Editing

Generate new images from text prompts or edit existing images using Google's Gemini 3 Pro Image API (codename: Nano Banana Pro).

## When to Use

- User asks to generate, create, or draw an image
- User wants to edit, modify, or transform an existing image
- User asks for artwork, illustrations, concept art, or visual designs
- User mentions "generate image", "draw", "create picture", "edit image"

**Do NOT use when:**
- User wants to analyze or describe an existing image (use Read tool instead)
- User wants to create charts/diagrams from data (use code-based visualization)

## The Process

### Phase 0: Initialization

#### Step 1: Language Selection

Ask the user which language to use for this session:

```
question: "Which language would you like for this session?"
header: "Language"
options:
  - label: "English"
    description: "All prompts and status messages in English"
  - label: "中文 (Chinese)"
    description: "所有提示和状态信息使用中文"
```

Store the choice and use it for all subsequent interactions.

#### Step 2: Check API Key

Verify that a Gemini API key is available. Check in this order:

1. Check environment variable:
```bash
echo ${GEMINI_API_KEY:+"KEY_EXISTS"}
```

2. Check `.env` file in the skill directory:
```bash
cat {skill_path}/.env 2>/dev/null | grep GEMINI_API_KEY
```

3. Check `.env` file in the current working directory:
```bash
cat .env 2>/dev/null | grep GEMINI_API_KEY
```

#### Step 3: Handle Missing Key

**If key found in any location** → Proceed to Phase 1.

**If key is missing everywhere** → Use `AskUserQuestion`:
```
question: "No GEMINI_API_KEY found. How would you like to provide it?"
header: "API Key Required"
options:
  - label: "Paste my API key"
    description: "I have a Gemini API key ready to use"
  - label: "Help me get a key"
    description: "Guide me to Google AI Studio to create a free API key"
```

**If user chooses "Help me get a key":**
Inform the user:
```
You can get a free Gemini API key from Google AI Studio:
  https://aistudio.google.com/apikey

1. Sign in with your Google account
2. Click "Create API Key"
3. Copy the key and paste it here
```

Then use `AskUserQuestion` again to collect the key:
```
question: "Please paste your Gemini API key:"
header: "Enter API Key"
```

**Once the key is obtained**, set it for the current session:
```bash
export GEMINI_API_KEY="<user_provided_key>"
```

Then ask if they want to persist it:
```
question: "Save this API key permanently so you don't need to provide it again?"
header: "Save API Key"
options:
  - label: "Yes, save to system environment (Recommended)"
    description: "Set GEMINI_API_KEY as a persistent user environment variable"
  - label: "No, just use it for this session"
    description: "The key will only be available in the current terminal session"
```

If user chooses to save permanently, on Windows:
```bash
powershell -Command "[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', '<key>', 'User')"
```

On macOS/Linux, append to shell profile:
```bash
echo 'export GEMINI_API_KEY="<key>"' >> ~/.bashrc
```

---

### Phase 1: Task Understanding

#### Step 1: Determine Task Type

Based on the user's request, classify the task:

- **Text-to-Image Generation**: User describes what they want drawn/created (no source image)
- **Image Editing**: User wants to modify an existing image (has a source image)

#### Step 2: Collect Parameters

Use `AskUserQuestion` to gather generation parameters:

```
question: "What resolution would you like for the output image?"
header: "Resolution"
options:
  - label: "1K (~1024px) — Fast, good for previews"
    description: "Generation time: ~2-3 minutes"
  - label: "2K (~2048px) — Balanced quality and speed"
    description: "Generation time: ~3-4 minutes"
  - label: "4K (~4096px) — Maximum quality"
    description: "Generation time: ~4-6 minutes"
```

**Skip this question if** the user already specified resolution in their request (e.g., "high-res", "4K", "thumbnail").

Resolution mapping for implicit requests:
- "high-res", "4K", "ultra", "maximum quality" → 4K
- "medium", "2K", "balanced" → 2K
- "quick", "preview", "thumbnail", "draft", or unspecified → 1K

#### Step 3: Craft the Prompt

Refine the user's description into an effective image generation prompt:

- Preserve the user's creative intent exactly
- Add technical quality terms if appropriate (e.g., "highly detailed", "professional lighting")
- For editing tasks, be specific about what to change and what to keep
- Do NOT override the user's artistic choices

---

### Phase 2: Image Generation

#### Step 1: Prepare Output Path

Generate a timestamped filename following this pattern:
```
yyyy-mm-dd-hh-mm-ss-descriptive-name.png
```

Example: `2026-03-10-14-30-00-cyberpunk-cityscape.png`

Determine the output directory:
- If the user specified a path → use that path
- If user's project has an `img/` or `images/` directory → use it
- Otherwise → create `img/` in the current working directory

#### Step 2: Run Generation Script

Locate the generation script at the skill's script directory and execute:

**For text-to-image:**
```bash
uv run {skill_path}/scripts/generate_image.py \
  --prompt "{refined_prompt}" \
  --filename "{output_path}" \
  --resolution {resolution}
```

**For image editing:**
```bash
uv run {skill_path}/scripts/generate_image.py \
  --prompt "{edit_instructions}" \
  --filename "{output_path}" \
  --input-image "{source_image_path}" \
  --resolution {resolution}
```

Note: `{output_path}` should be an **absolute path** (e.g., `/home/user/project/img/2026-03-10-14-30-00-sunset.png`). The script handles both absolute and relative paths correctly.

**Important execution notes:**
- Set timeout to at least 180 seconds (3 minutes) for 1K, 240 seconds for 2K, 360 seconds for 4K
- The script will be silent during generation — this is normal
- Run from the user's working directory, not the skill directory
- Do NOT pass `--input-image` when generating new images

#### Step 3: Verify Output

After the script completes:

1. Check if the output file exists using `Glob`
2. If successful, inform the user of the saved path
3. Do NOT attempt to read/display the generated image back (the tool cannot render generated images meaningfully)

**If generation fails:**
- Check error output for API key issues, quota limits, or content policy blocks
- Report the error clearly to the user
- Suggest fixes (e.g., check API key, try a different prompt if content-blocked)

---

### Phase 3: Follow-up

After successful generation, offer next steps:

```
question: "Image generated successfully. What would you like to do next?"
header: "Next Steps"
options:
  - label: "Generate another image"
    description: "Create a new image with a different prompt"
  - label: "Edit this image"
    description: "Modify the image I just generated"
  - label: "Change resolution"
    description: "Re-generate the same image at a different resolution"
  - label: "Done"
    description: "I'm satisfied with the result"
```

If user wants to edit the generated image, loop back to Phase 2 with `--input-image` pointing to the just-generated file.

## Script Location

The generation script is bundled with this skill at:
```
nano-banana-draw/scripts/generate_image.py
```

It requires `uv` to run (auto-installs dependencies: `google-genai`, `pillow`).

## Constraints

- **Do not read generated images** — The Read tool shows raw image data, not a useful preview
- **Preserve user intent** — Do not override the user's creative choices in prompts
- **Run from user's working directory** — Output paths should be relative to where the user is working
- **Filename convention** — Always use `yyyy-mm-dd-hh-mm-ss-descriptive-name.png` format
- **Timeout** — Set Bash timeout to at least 180000ms (3 minutes) for generation commands
