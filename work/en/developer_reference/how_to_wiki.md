# How to Contribute to the Wiki

This guide explains how to contribute to the OrcaSlicer wiki.

OrcaSlicer's wiki is generated automatically from the files in the [OrcaSlicer WIKI repository]({{L1}}).  
To suggest small changes or improvements, please [open an issue in that repository]({{L2}}).  
If you prefer to make the edits yourself, follow this guide for best practices when creating a pull request (PR).

We encourage developers and users to contribute by updating existing pages and adding new content. This helps keep the documentation accurate and useful.  
When adding new features, consider updating the wiki so users can access the latest guidance.

{{T1}}

## Wiki Structure

Each page of the Wiki is a Markdown file located in the [OrcaSlicer_WIKI repository]({{L3}}).  
The wiki is organized into sections that cover different areas of the project.

### Home

The Home page is the starting point for the OrcaSlicer wiki. From there you can navigate to sections and topics related to the project.

When you create a new page or section, link it from the Home page under the appropriate category.  
The Home page currently organizes content in these top-level entries:

- {{I1}} [Printer Settings]({{L4}})
- {{I2}} [Material Settings]({{L5}})
- {{I3}} [Process Settings]({{L6}})
- {{I4}} [Prepare]({{L7}})
- {{I5}} [Calibrations]({{L8}})
- {{I6}} [Developer Section]({{L9}})

Each section can have multiple pages covering specific topics. For example, the [Process Settings]({{L10}}) section includes pages on [quality]({{L11}}), [support]({{L12}}), and [others]({{L13}}).

#### Index and Navigation

GitHub Wiki uses file names as page identifiers. To link to a page, use the file name without the `.md` extension. If a file lives in a subdirectory, **do not include the subdirectory** in the link; link directly to the file name from the Home page.

For example, if you add `calibration/flow_ratio_calib.md`, link it like this:

{{C1}}

Inside each section, the website sidebar follows the order of the list links on the Home page, so place the link where the page sits in the slicer.

For long pages, include a table of contents at the top to help readers find sections quickly.

{{C2}}

> [!NOTE]
> If you're adding a new section, follow the existing structure and make sure it doesn't already fit an existing category. Link it from the Home page accordingly.

### File Naming and Organization

When creating new pages, follow these file-naming conventions:

- Use unique file names to avoid conflicts.
- Use descriptive names that reflect the page's content.
- Use snake_case for filenames (e.g.: `how_to_wiki.md`).
- If a page belongs to a section, include a suffix that clarifies it (for example, calibration pages should end with `-calib.md`, e.g. `flow_ratio_calib.md`).
- Place files in the appropriate subdirectory when applicable (e.g.: `calibration/` for calibration-related content).

## Orca to Wiki Redirection

OrcaSlicer can redirect users from the GUI to the appropriate wiki pages, making it easier to find relevant documentation.

The option-to-wiki mapping is defined in [src/slic3r/GUI/Tab.cpp]({{L14}}).
The links naming uses the same format as the [Wiki Navigation described above]({{L15}}), `[filename]#[section(optional)]` e.g. `quality_settings_seam` or `quality_settings_seam#scarf-joint-seam`.

There are 3 main ways to set up these links:

1. Using `append_single_option_line` with a second string argument for the wiki page.  

    {{C3}}

     Example:

    {{C4}}

    An option that is customized first is passed as an `Option` object; the sync script reads its key from the `get_option` call that created it:

    {{C5}}

2. Using `append_option_line` with a third string argument for the wiki page.

    {{C6}}

    Example:

    {{C7}}

3. Using grouped rows with `append_line` and setting the wiki target via `line.label_path`.

    {{C8}}

    Example:

    {{C9}}

### Option Mode and Variables Metadata

Most option sections start with one or two metadata lines directly under the heading, for example:

{{C10}}

- The `[Mode](option_mode)` line records the option's visibility level (`Simple`, `Advanced`, `Expert`, or `Developer`).
- The `[Variable](built_in_placeholders_variables)` line (or `[Variables]` when there is more than one) records the config key(s) that the section documents.

> [!IMPORTANT]
> Do **not** write or edit these lines by hand. They are generated and normalized by the [`sync-tab-options-to-wiki.ps1`]({{L16}}) script at the repository root. Any manual edits will be overwritten the next time the script runs.

The script reads the option-to-page mappings from [Tab.cpp]({{L17}}) and the option mode from [PrintConfig.cpp]({{L18}}), then inserts or refreshes the metadata under the matching heading in each page. It also prunes metadata from sections that are no longer referenced from `Tab.cpp`.

When you add or rename an option's documentation, **write only the heading and the descriptive body** — the section must exist and its anchor must match the `Tab.cpp` link (see above). Then run the script to populate the metadata:

{{C11}}

By default the script downloads `Tab.cpp` and `PrintConfig.cpp` from the OrcaSlicer `main` branch. To run it against a local checkout, pass the paths explicitly:

{{C12}}

> [!NOTE]
> If the script reports `Missing heading anchors`, the `Tab.cpp` link points to a section that does not yet exist in the target page. Create that heading (matching the anchor) so the redirect resolves and the metadata can be inserted.

## Formatting and Style

Follow these style and formatting conventions when contributing to the wiki.

### Markdown Formatting

The wiki uses standard Markdown syntax for formatting and aims to maintain a consistent style across all pages. Avoid using raw HTML tags and prefer Markdown formatting instead.

Ensure your indentation is consistent, especially for code blocks and lists.

Refer to the [GitHub Markdown Guide]({{L19}}) for more information on Markdown syntax.

### Alerts and Callouts

Use GitHub's alert syntax to add inline notes and warnings:

{{C13}}

> [!NOTE]
> Refer to the [GitHub Alerts documentation]({{L20}}) for more details.

#### New Content

The Wiki should be updated to reflect the latest stable release with the addition of new features present in current nightly builds.  

When new features or upgrades are merged into the main branch, please add a note using the following format:

{{C14}}

Example:

> [!IMPORTANT]
> NEW FEATURE: **Inverse Hole Direction**  
> Available in: [Nightly builds]({{L21}}) or Releases greater than **2.4.0**.

This notes should be removed after a new stable release is made that includes the new feature.

## Images

Images are encouraged to enhance the clarity and quality of the wiki content. They help illustrate concepts, provide examples, and improve readability.

> [!CAUTION]
> Do not use images from third-party sources unless you have the proper permissions.

### Image Sources

#### OrcaSlicer Resources

Use images from the OrcaSlicer resources folder located at `\resources\images` in the OrcaSlicer repository. These images are designed to match the application's UI and maintain consistency.

#### Wiki Images

Use or add images in the `images/` directory of the [OrcaSlicer_WIKI repository]({{L22}}).  
There you can find images already used in the wiki like screenshots, diagrams, and icons.

##### Image Naming

- Use clear, descriptive filenames that reflect the image content.
- For section-specific images, include the section name or initials (for example `pa-[description].png` for Pressure Advance images).

##### Image Placement

- General images should be placed in the `images/` directory.
- Section-specific images should be stored in their corresponding subdirectories (e.g., `images/calibration/` for calibration content).

> [!TIP]
> You can use `\resources\images` images used in the GUI.

##### Linking Images

Always use raw GitHub URLs for image links to ensure correct display:

Format = `![`filename`](` + Base URL + filename.extension + Raw tag + `)`

- Base URL:

  {{C15}}

- Raw tag:

  {{C16}}

###### Examples

- For an image in `images/` named `calibration.png`:

  {{C17}}

- For an image in a subdirectory like `images/GUI/combobox.png`:

  {{C18}}

> [!IMPORTANT]
> New or moved images may not appear in previews until the pull request is merged. Double-check paths and update links if you move files.

### Avoid the Following

- Relative paths
- GitHub Assets/user-content/user-images URLs
- External image links from temporary or unreliable hosts
- Images containing personal or sensitive information
- Using images for content that can be expressed in text, such as equations or code—use Markdown syntax or Mermaid/Math formatting instead.

> [!NOTE]
> When contributing section-specific images, follow the naming conventions and directory structure.

#### Resize Images

Avoid the resize of images and let the Wiki handle it automatically.

If resizing is necessary (e.g., for thumbnails), use the following syntax:

HTML Format = `<img alt="` + filename + `"` + `src="` + Base URL + filename.extension + Raw tag + size limit.
Example:

{{C19}}

### Image Cropping and Highlighting

To ensure clarity:

- Crop images to focus on relevant areas.
- Use simple annotations (arrows, circles, rectangles) to highlight important parts without overloading the image.

### Recommended Formats

- **JPG:** Suitable for photographs. Avoid for images with text or fine detail due to compression artifacts.
- **PNG:** Ideal for screenshots or images with transparency. Ensure sufficient contrast for light and dark modes.
- **SVG:** Preferred when possible. SVGs support theme adaptation (light/dark mode), making them ideal for icons and diagrams.

## Structuring Content

Each page should have a clear objective. After a short introduction, choose a structure that fits the content:

- **Step-by-step guides:** Use for sequential procedures (for example calibration).
- **GUI-based reference:** Describe settings following OrcaSlicer's UI when sequence isn't required.

Example: explain **Layer Height** before **Initial Layer Height**, since the former is global and the latter only applies to the first layer.

## Commands and Code Blocks

When adding commands or code blocks please use the [Code Block with Syntax Highlighting feature of Markdown]({{L23}}).

- Use triple backticks (```) to enclose code blocks.
- Specify the language for proper highlighting and readability.

{{C20}}

{{C21}}

## External Links

Be careful when linking to external resources.  
Ensure links are relevant and reliable and cite papers or articles when appropriate.
