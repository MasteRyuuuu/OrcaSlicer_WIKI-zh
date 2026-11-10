# V2.4.0 Alpha

This is the OrcaSlicer V2.4.0 Alpha release. The headline feature is **Orca Cloud** — a new centralized platform for profile sync, preset bundle sharing, and community discovery at cloud.orcaslicer.com. This release also introduces **Z Anti-Aliasing (ZAA) contouring** for smoother top surfaces, an Expert user mode, native Wayland support for Linux, Machine Input Shaping, Optimized Gyroid infill, Prusa-style combined brims, a redesigned printer selection dialog, and a large number of bug fixes and profile updates.

**Note:** Please check #13828 for known issues.

# ☁️ Orca Cloud

Orca Cloud is now live at [cloud.orcaslicer.com]({{L1}}) — a centralized platform that brings your 3D printing workflow online.

It keeps your printer, filament, and process profiles synchronized across every machine you use, lets you share finely tuned preset bundles with the community, and helps you discover configurations created by fellow makers around the world.

Think of it as the connective tissue between your slicer, your profiles, and the broader OrcaSlicer ecosystem — no more manually copying config files between computers or hunting through forums for the right profile.

**Note:** Orca Cloud is optional. Local profiles and existing OrcaSlicer workflows continue to work as before. You can keep using OrcaSlicer without logging in to Orca Cloud.

**Open ecosystem:** Orca Cloud is part of our long-term vision for an open 3D printing ecosystem. We want OrcaSlicer to connect users, contributors, printer manufacturers, filament makers, and hardware/software partners through shared profiles, better compatibility data, and smoother workflows. We welcome users, makers, manufacturers, and partners to join, integrate, and collaborate with us to build an ecosystem that benefits the whole community and the wider 3D printing industry.

This is just the beginning. We have many more features planned for Orca Cloud and the broader OrcaSlicer ecosystem.

Orca Cloud is designed with privacy in mind. Data is currently hosted in the USA. In the future, we plan to add more region-specific servers and allow users to choose their preferred data center location for improved performance, data residency, and privacy needs.

* **Orca Cloud — Profile Sync, Version History, Preset Bundles, and Community Sharing** [PR 13414]({{L2}})

    **Profile Sync:** Log in to OrcaSlicer with your Orca Cloud account, and your printer, filament, and process profiles sync automatically across machines. You can also view and manage all synced profiles from the Orca Cloud web interface.

    {{I1}}

    **Profile Version History:** Your cloud-backed profiles support version history on Orca Cloud. Mark milestones, track what changed, and revert to a previous version whenever you need — useful for recovering from a tuning session that did not work out, or rolling back to a known-good configuration before an important print.

    {{I2}}

    **Preset Bundles:** Create shareable preset bundles with descriptions, images, version info, and compatible printer metadata. Publish them publicly for the community to discover, or keep them private and share only with specific collaborators.

    {{I3}}

    **Community Explore:** Browse public bundles shared by the community on the Orca Cloud website. Subscribe to bundles you like and they will sync to your slicer automatically, with update notifications when the author publishes a new version.

    {{I4}}

    **Full introduction video:**

    <video controls width="800" src="{{L290}}"></video>

    **Orca Cloud Wiki:** [cloud.orcaslicer.com/wiki/]({{L3}})

* **Orca Cloud improvements and fixes** by @peachismomo, @ExPikaPaka, @SoftFever, @andrewsoonqn, and @erpalma in [PR 13755]({{L4}}), [PR 13745]({{L5}}), [PR 13757]({{L6}}), [PR 13778]({{L7}}), [PR 13673]({{L8}}), [PR 13738]({{L9}}), [PR 13793]({{L10}}), [PR 13645]({{L11}}), [PR 13756]({{L12}}), [PR 13779]({{L13}}), [PR 13776]({{L14}}), [PR 13781]({{L15}}), [PR 13796]({{L16}}), and [PR 13797]({{L17}})
    Multiple follow-up improvements to the Orca Cloud experience: clearer visual distinction between Orca Cloud and Bambu Cloud login UIs, a force sync button for manually pushing profiles to the cloud (with a fix for the false "modified" highlight during sync), synced preset values now reflect in the UI immediately without needing to switch tabs, a consistent account display name between login and refresh, restored printer camera live view for cloud-connected printers (including H2D), clearer cloud error messages, HTTP error responses now show user-visible message boxes instead of failing silently, cloud sync during startup now runs in the background to eliminate UI freezes, and fixes for detached custom presets not appearing after download, spurious 401 login errors on slow networks, 409 sync conflicts on startup, and a crash from cloud preset sync racing the GUI at startup.

* **Add more logs to track Orca Cloud logout issues** by @peachismomo in [PR 13713]({{L18}})
    Added diagnostic logging around cloud logout events to help identify unexpected logouts.

# 🌊 New Features & Improvements

* **Z Anti-Aliasing (ZAA) contouring** by @adob in [PR 12736]({{L19}}) with fixes and improvements by @valerii-bokhan, @RF47, and @ianalexis in [PR 13452]({{L20}}), [PR 13508]({{L21}}), [PR 13510]({{L22}}), [PR 13450]({{L23}}), [PR 13766]({{L24}}), and [PR 13446]({{L25}})
    Z Anti-Aliasing (ZAA) reduces visible stair-stepping on curved and sloped top surfaces by raycasting each extrusion point against the original 3D mesh and micro-adjusting the Z height to follow the actual surface geometry. Instead of keeping every move at a single flat Z for the whole layer, OrcaSlicer emits varying Z values inside the affected layer — noticeably smoothing domes, chamfers, and shallow slopes without changing the nominal layer height of the rest of the print. Five new settings are available under Print Settings > Quality (`zaa_enabled`, `zaa_min_z`, `zaa_minimize_perimeter_height`, `zaa_dont_alternate_fill_direction`, `zaa_region_disable`). This is an Expert mode feature currently targeting top-facing curved or sloped surfaces. [Wiki]({{L26}})

    {{I5}}

* **Fuzzy skin ripple mode** by @GeordieTomo in [PR 13471]({{L27}}) with improvements by @ianalexis in [PR 13506]({{L28}}) and [PR 12479]({{L29}})
    Adds a new Ripple generator mode to fuzzy skin that produces uniform patterned textures instead of noise-based perturbation. Three new parameters are available when Ripple mode is selected: ripples per layer, ripple offset, and layers between ripple offset. Also includes fixes for fuzzy skin artifacts when combined with painted fuzzy skin regions and sacrificial bridge layers. Fixes #13325. [Wiki]({{L30}})

    {{I6}}

    | Classic noise | Ripple mode |
    |---------------|-------------|
    | {{I7}} | {{I8}} |

* **Optimized Gyroid infill** by @peyton-marcotte in [PR 13379]({{L31}})
    Adds an experimental "Optimize gyroid wave" option that automatically tunes the gyroid wavelength and amplitude per region based on density, line spacing, and layer height. The optimization uses Euler-Bernoulli buckling physics: by tightening the wave along the Z (layer-stacking) axis, each vertical strand gains higher resistance to buckling under compression — the dominant failure mode for FFF parts under load. Standard gyroid output is byte-identical when the option is unchecked. Developed as part of the CRAMP project at Brown University with NASA Space Grant funding, in collaboration with ELEGOO and Polymaker. Winning architectures from this research beat commodity baselines by up to 60% in compressive strength-to-mass.

    {{I9}}

* **Combine brims (Prusa-style brims)** by @RF47 in [PR 12343]({{L32}})
    Refactors brim generation to follow PrusaSlicer methodology: the unified brim creates a continuous ring around all objects on the build plate for stronger bed adhesion. If multiple materials are used on the first layer, normal brim is recommended to avoid staining parts with different colors. For by-object sequence prints, normal brim generation is maintained. Fixes #10635. [Wiki]({{L33}})

    | Normal brim | Combined brim |
    |-------------|---------------|
    | {{I10}} | {{I11}} |

* **Multiple dovetail cuts** by @Xipit in [PR 12318]({{L34}})
    The dovetail cutting tool now supports cutting with multiple dovetails in a single cut operation (previously limited to one). You can specify the count and gap between dovetails — ideal for splitting large models into pieces that fit on the build plate and can be reassembled accurately.

    {{I12}}

* **Non-Crossing Tri-hexagon infill pattern** by @RF47 in [PR 13433]({{L35}}) and [PR 13422]({{L36}})
    Adds a non-crossing tri-hexagon pattern to trapezoidal fill that prevents intersection lines, producing a stronger and more isotropic infill. Each layer is rotated by 120 degrees for uniform strength along X and Y axes. The pattern grid has been centered and symmetrically aligned for even infill distribution.

    {{I13}}

* **Machine Input Shaping** by @ianalexis in [PR 11202]({{L37}}) with wiki and calibration updates in [PR 13569]({{L38}}) and [PR 13571]({{L39}})
    Adds Resonance Compensation override to the Printer Settings, allowing you to set X/Y axis frequency and damping values directly in OrcaSlicer. Supports Adaptive Klipper, RRF, and Marlin 2 input shaper types. Particularly useful for Marlin printers where the IS menu is disabled, or when you want to manage input shaping from the slicer side. Emits the appropriate G-code for each firmware type. [Wiki]({{L40}})

    {{I14}}

* **Kinematics (Jerk & Acceleration) visualization** by @ianalexis in [PR 13169]({{L41}})
    Adds Jerk/Junction Deviation and Acceleration preview modes to the G-code viewer. JD values are calculated dynamically based on the current acceleration, making it easy to correlate motion parameters with specific print features and identify potential quality issues.

    {{I15}}

* **Elephant foot compensation for solid layers** by @pi-squared-studio in [PR 11526]({{L42}}) with fixes by @ianalexis in [PR 13476]({{L43}}) and [PR 13523]({{L44}})
    Extends elephant foot compensation to solid layers above the bottommost layer by manipulating infill density. Instead of only compensating the first layer, density increases linearly up to 100% across the specified number of compensation layers, absorbing excess plastic more gradually for better dimensional accuracy.

    | Before | After |
    |--------|-------|
    | {{I16}} | {{I17}} |

    [Wiki]({{L45}})

* **Max Resolution and Deviation settings exposed for Arachne** by @valerii-bokhan in [PR 11925]({{L46}})
    Exposes the Arachne wall generator's internal resolution and deviation constants as user-configurable settings. Maximum Resolution (0.005–0.5, default 0.5) and Maximum Deviation (0.005–0.05, default 0.025) give experienced users finer control over wall quality and slicing performance. Lower values produce cleaner walls with fewer artifacts at the cost of longer slicing times — particularly useful for high-detail prints where Arachne's default settings introduce visible artefacts compared to the Classic wall generator. Fixes #10235.

    | Classic | Arachne (default) | Arachne (min resolution/deviation) |
    |---------|-------------------|-------------------------------------|
    | {{I18}} | {{I19}} | {{I20}} |

* **First layer travel acceleration and jerk configurable** by @rcopra in [PR 11674]({{L47}}) with toggle improvements by @kisslorand in [PR 13320]({{L48}}) and wiki by @ianalexis in [PR 13324]({{L49}})
    Adds separate configurable travel acceleration and jerk values for the first layer. Fast travel accelerations on the first layer help reduce oozing and stringing, while slower print accelerations maintain good bed adhesion. The toggle behavior now correctly groups all first layer motion settings.

    {{I21}}
    {{I22}}

    <video controls width="800" src="{{L291}}"></video>

* **Brim flow ratio setting** by @valerii-bokhan in [PR 11876]({{L50}})
    Adds a dedicated flow ratio setting for brims that operates independently of the first layer flow ratio. Previously, brim flow was tied to the first layer flow ratio, meaning any adjustment for the brim also affected the entire first layer. Now you can fine-tune brim extrusion separately — increase flow for stronger bed adhesion on the brim while keeping the first layer flow at its optimal value. Fixes #11853.

    {{I23}}

* **Inverse print direction for holes** by @RF47 in [PR 12669]({{L51}})
    Reverses the printing direction of internal hole walls for improved surface consistency on internal perimeters. The "Auto" wall direction option has been simplified to direct on/off toggles for each direction, also separating internal and overhang wall reversing for finer control. Based on an idea from @discip. Fixes #11630.

    | Before | After |
    |--------|-------|
    | {{I24}} | {{I25}} |

* **Cooling: per-printer min fan PWM floor** by @igiannakas in [PR 13715]({{L52}})
    Adds a per-printer "Minimum non-zero part cooling fan speed" setting — any non-zero fan command is clamped up to this percentage at G-code emission time. Also fixes a silent override that forced `close_fan_the_first_x_layers` from 0 to 1 when `full_fan_speed_layer` was set. Fixes #11029.

    {{I26}}
    {{I27}}

    {{I28}}

    {{I29}}

* **Hybrid tree support: fix first-layer behavior and expose density** by @kisslorand in [PR 13454]({{L53}})
    Hybrid tree supports now correctly use support material flow instead of brim flow on the first layer, fixing over-extrusion and potential bed collisions. The first-layer density and expansion settings are properly exposed in the UI. First-layer spacing on the support base is now derived from the actual first-layer support flow, and tree-only regions use existing brim expansion settings independently. Fixes #13430.

    {{I30}}

    | Before (incorrect line width) | After (correct line width) |
    |-------------------------------|----------------------------|
    | {{I31}} | {{I32}} |

    {{I33}}

    | Circular base (meaningless density before fix) | Rectilinear base (meaningful density after fix) |
    |-------------------------------------------------|-------------------------------------------------|
    | {{I34}} | {{I35}} |

* **Reduce Spiral Z generation segment density** by @igiannakas in [PR 12564]({{L54}})
    Reduced precision of spiral Z-hop moves to lower the G-code command rate, preventing "Timer Too Close" errors on high-speed Klipper machines running on Raspberry Pi 5. Extreme precision is less critical for non-printing moves.

* **Remove "Auto" wall direction option** by @vovodroid in [PR 6193]({{L55}})
    Simplified wall direction settings by removing the ambiguous "Auto" mode in favor of direct on/off toggles for each direction. The rewrite also separates internal and overhang wall reversing, and adds an option to print overhangs after internal walls for improved adhesion while keeping the external wall first in outer-inner and inner-outer-inner modes. Spiral vase mode can now be printed in any direction.

* **Fix gaps between walls and sparse infill** by @echipachenko in [PR 12770]({{L56}})
    When "Detect Narrow Infill" was enabled, sparse infill (Grid pattern) showed visible gaps between infill lines and walls. Root cause: the inner area was shrunk by `scaled_spacing * 0.5` but infill was only expanded by `scaled_spacing * 0.1`, creating a net 0.4x gap. Expansion now matches the shrinkage at `scaled_spacing * 0.5`. Fixes #12304.

    | Before | After |
    |--------|-------|
    | {{I36}} | {{I37}} |

* **Correct gap fill width bounds in outer-only and mixed-wall cases** by @kisslorand in [PR 12057]({{L57}})
    Previously, internal wall geometry was used unconditionally when computing gap fill bounds, which could misrepresent safe overlap when external and internal walls differ in thickness or spacing. The minimum gap fill width is now derived from the smaller of internal and external wall widths, preventing overestimation of allowable overlap. This is a geometry reference correction — existing gap fill behavior is unchanged except where wall geometry references were incorrect. Fixes #12030.

    | Before | After |
    |--------|-------|
    | {{I38}} | {{I39}} |

* **Extend short-travel smoothing to external overhang walls** by @kisslorand in [PR 11975]({{L58}})
    Short micro-travels immediately before a perimeter can cause a sudden acceleration impulse, leading to vibration and ringing on visible surfaces. Acceleration and jerk for short travels before standard external walls were already reduced, but external overhang walls were excluded and still used full travel acceleration/jerk. This fix extends the same short-travel smoothing to external overhang walls, using the configured overhang-wall (bridge) acceleration and consistent jerk handling for these transitions. External walls, internal walls, infill, supports, and regular travel remain unchanged.

    | Before | After |
    |--------|-------|
    | {{I40}} | {{I41}} |

* **Ignore Jerk values warning when using Junction Deviation** by @ianalexis in [PR 13575]({{L59}})
    Suppressed misleading jerk value warnings when Junction Deviation is the active motion mode.

* **Granular exhaust fan speed control** by @misterff1 in [PR 13228]({{L60}})
    Adds independent checkboxes to control exhaust fan speed during printing and after print completion, replacing the previous all-or-nothing behavior. Both default to enabled for backward compatibility. Addresses #13116.

    {{I42}}

* **Extrusion role change G-code in Process and Filament** by @ianalexis in [PR 11784]({{L61}})
    New G-code insertion points for handling extrusion role changes, available at both the process and filament preset levels. This separates role-change G-code from the machine level, so you can define behavior at role transitions (e.g., perimeter to infill, support material changes) and save it with your process or filament presets without depending on the machine configuration. G-code execution order is: Machine → Filament → Process. A power-user feature inspired by @RF47, useful for per-role fan speed adjustments, temperature changes, or custom toolhead actions.

    {{I43}}

* **Per-vendor profile version updates** by @softfever and @peachismomo in [PR 13394]({{L62}})
    OrcaSlicer now checks for updated printer, filament, and process profiles on a per-vendor basis via `check-version.orcaslicer.com/profiles`. When a vendor publishes newer profiles for your machine, a notification appears prompting you to upgrade to the latest tuned configurations with a single click — no more wondering if your profiles have fallen behind. This lays the groundwork for coming OrcaSlicer profile OTA support.

    {{I44}}

    {{I45}}

* **Expert user mode** by @SoftFever in [PR 13348]({{L63}})
    Adds a new Expert user mode between Advanced and Developer modes. The mode switch button now uses a three-way toggle (Simple / Advanced / Expert). Expert mode exposes experimental and advanced options that require a deeper understanding of the 3D printing process, without overwhelming users who don't need them. Settings like ZAA contouring and Machine Input Shaping are assigned to this mode.

    {{I46}}

    [Wiki]({{L64}})

* **3MF Export/Import with Orca version tags** by @ianalexis in [PR 12509]({{L65}})
    3MF files now include OrcaSlicer-specific version tags alongside Bambu Studio tags, enabling accurate version-aware import behavior. When opening a 3MF file, OrcaSlicer checks the embedded version information and warns you if the file was created with a newer version that may use features or settings not available in your current one. Files from versions ≤ 2.3.2 are treated as legacy and imported with appropriate compatibility handling. Fixes a bug where Orca versions like 2.3.2 were incorrectly interpreted as 2.3.0.2.

    | Feature | Screenshot |
    |---------|-----------|
    | Version tag system | {{I47}} |
    | Future BBS version warning | {{I48}} |
    | Future Orca version warning | {{I49}} |
    | BBS version warning | {{I50}} |

* **CGAL Fix Model for Linux and Mac** by @ianalexis in [PR 12155]({{L66}})
    The "Fix Model" function now works on Linux and macOS using CGAL instead of Windows-only APIs. Multi-part STL files are fixed part-by-part; non-3D elements (points, lines, planes) are automatically removed. Considerably faster than the previous Windows-only implementation. Fixes #5013, #4923, #8740, #9156.

    | Before (broken model) | After (repaired) |
    |-----------------------|-------------------|
    | {{I51}} | {{I52}} |

* **CLI: add layer_height, sparse_infill_density, and wall_loops to results** by @Eldenroot in [PR 13001]({{L67}})
    The CLI `--export` output now includes layer height, sparse infill density, and wall loop count values, making it easier for automation scripts and print farm management tools to extract key print parameters without parsing the full configuration.

* **Native Wayland support for Linux** by @SoftFever in [PR 13197]({{L68}}) with additional fixes by @thomashenauer, @SoftFever, and @yw4z in [PR 13707]({{L69}}), [PR 13721]({{L70}}), [PR 13723]({{L71}}), [PR 13563]({{L72}}), and [PR 13747]({{L73}})
    OrcaSlicer now runs natively on Wayland — no XWayland required. Includes fixes for multi-monitor setups, submenu popup parenting, data-view and dropdown submenu popups, faint toolbar icons under Wayland, and a crash when opening the Preview tab on startup.

* **Flatpak 2.4 update** by @SoftFever in [PR 13799]({{L74}})
    Updated the Flatpak manifest and build configuration for the 2.4 release.

* **Enhance network share experience for flatpak** by @SoftFever in [PR 13809]({{L75}})
    Improved network share and filesystem access when running OrcaSlicer as a Flatpak, addressing sandbox-related limitations.

## Multi-Material

* **Keep painting after mesh changes** by @Noisyfox in [PR 13472]({{L76}})
    A new experimental option under Preferences > Developer > "Keep painted feature after mesh change" preserves your painted regions across planar cuts, dovetail cuts, splitting to parts/objects, mesh boolean operations, reloading from disk, fix model, and simplify/smooth operations. No more losing your support enforcers or seam paintings after making a cut.

    {{I53}}

* **Option to always travel to wipe tower before Tx on multi-toolhead setups** by @igiannakas in [PR 13703]({{L77}})
    Adds an option for type 2 wipe towers on multi-toolhead printers backed by an MMU to always travel to the wipe tower before executing tool change commands, reducing oozing during multi-material prints.

* **Filament compatibility temperature-aware** by @ianalexis in [PR 13522]({{L78}})
    The temperature-based filament compatibility check is now more intelligent: instead of using hardcoded temperature range tables per material type, it checks actual material temperatures against each other's recommended ranges. A message explains how to disable this check if needed. Fixes #10543.

* **Warn for abnormal temperature differences** by @kisslorand in [PR 12345]({{L79}})
    If the temperature difference between first layer and other layers exceeds 15°C for the bed or 30°C for the nozzle, a warning popup now alerts you when saving or closing the preset. You can temporarily suppress the warning for the current session. Fixes #12310.

    {{I54}}

## Improved Printer Support

* **Repetier G-code flavor** by @yogihybo in [PR 13126]({{L80}})
    Adds Repetier as a selectable G-code flavor with appropriate defaults: machine limits emission and remaining time (M73) are turned off, and jerk handling is refactored for Repetier compatibility. Includes a generic Repetier printer profile.
    {{I55}}
    {{I56}}

* **Improved SnapmakerPrinterAgent filament sync** by @gaaat98 in [PR 13265]({{L81}})
    Snapmaker filament syncing now matches against vendor-specific and custom filament presets using filament type, vendor name, and color distance for more accurate matching. Generic matching is kept as a fallback. Inspired by #13202.

* **Add fallback for Qidi series ID matching** by @thelegendtubaguy in [PR 13065]({{L82}})
    Some Qidi printers (Max 4, Q2) don't report their model identifier via Moonraker's `/server/info` endpoint, preventing filament matching. A fallback now uses the configured machine type when the printer doesn't identify itself.

* **Support file uploads and device details for Elegoo Centauri Carbon 2** by @anjis-elegoo in [PR 13212]({{L83}})
    Adds LAN file upload support and the device details page for the Elegoo Centauri Carbon 2. You can now send files to the printer over LAN and manage prints from the device details page. Note: upload-and-print is not supported — printing must be initiated from the device details page. If access code protection is enabled on the printer, enter the code in the API Key/Password field.

    {{I57}}

* **Allow printing without nozzle info from firmware** by @lynaghk in [PR 12814]({{L84}})
    Printers that don't report nozzle size and hardness (such as older Bambu firmware) no longer block printing. The UI now shows "unknown" instead of incorrectly assuming 0.4mm, and the size/hardness checks are bypassed when this information isn't available. Fixes #8280, #12279, #12674.

    | Before (printing blocked with error) | After (prints with "unknown" nozzle) |
    |---------------------------------------|---------------------------------------|
    | {{I58}} | {{I59}} |

    | Before: blocked with nozzle mismatch error | After: shows "unknown" and allows printing |
    |---------------------------------------------|---------------------------------------------|
    | {{I60}} | {{I61}} |

* **Linux: use GTK sink for Wayland Bambu liveview** by @thomashenauer in [PR 13432]({{L85}})
    On native Wayland sessions, Bambu printer liveview could show a black screen or crash because the default GStreamer video overlay path relied on X11 window handles. This fix detects native Wayland and uses an explicit GTK widget sink via `wxNativeWindow` for reliable embedded playback. Also fixes a race condition where Orca validated the video size before wx/GStreamer had finished loading the stream. Fixes #13300, #9280.

    | Before (black screen) | After (working liveview) |
    |-----------------------|---------------------------|
    | {{I62}} | {{I63}} |

## Performance & Optimizations

* **Increase profile loading timeout** by @SoftFever in [PR 13661]({{L86}})
    Raised the profile-loading timeout to three minutes so slower computers can finish loading large profile sets. Fixes #12728, #12789, #13565.
* **Speed up startup and show splash progress** by @JustNotesa in [PR 13667]({{L87}})
    Reduces startup time and shows live loading progress in the splash screen.
* **Add persistent cookie storage for PrinterWebView on WebKitGTK** by @Ocraftyone in [PR 13135]({{L88}})
    Printer web views on Linux now persist cookies between sessions, improving the experience with print hosts that require authentication (such as SimplyPrint).

# 📐 Calibration Improvements

* **Improved flow rate calibration menu** by @tome9111991 in [PR 11956]({{L89}})
    The Flow Rate Calibration dialog now lets you choose your preferred top surface pattern instead of being forced to use Archimedean Chords. A dedicated selector gives you full control over the calibration's surface finish.

    {{I64}}

* **Temperature tower nozzle-based adjustment** by @ianalexis in [PR 12269]({{L90}})
    Temperature tower calibration now scales the tower based on nozzle size and readjusts test temperatures for the resized height. Layer height is automatically adjusted for optimal calibration results. Fixes #6978, #12281.

    {{I65}}

* **Preserve model placement in calibration tests** by @ianalexis in [PR 13252]({{L91}})
    Calibration tests no longer re-center loaded project (.3mf/.amf) models, preserving their original placement. Fixes #12645.

# 🎨 UI & UX

* **Printer selection dialog redesign** by @yw4z in [PR 12248]({{L92}})
    A major redesign of the printer selection dialog with two new layout options: Compact view (50% less scroll height) and List view (70% less). Sticky titlebars keep vendor names always visible while scrolling, any key press automatically focuses the search bar, indeterminate checkboxes track partial selections, and a new sidebar enables faster vendor jumping. Each printer card now shows nozzle information, and a "Create" button makes adding new printers straightforward. Vendors are now sorted alphabetically.

    Cover view:
    {{I66}}

    Compact view:
    {{I67}}

    List view:
    {{I68}}

* **Line Type preview: display distances and amount values** by @ianalexis in [PR 13681]({{L93}})
    The Line Type view in the Preview tab now shows travel distances, extrusion amounts, and estimated times per line type. Extrusion weights automatically scale from grams to kilograms/tons when needed. Seam travel distance is calculated as `seam_gap + seam_slope_min_length`. Based on work by @sscargal in #11187.

    | Before | After |
    |--------|-------|
    | {{I69}} | {{I70}} |

* **Tool Position window: improved vertex info** by @yw4z in [PR 12614]({{L94}})
    The Tool Position info window now reports travel, seam, wipe, retraction, and unretraction feature types in addition to the existing type data. Fixed "????" values that appeared on Windows by properly initializing the read buffer.

    {{I71}}

* **Display tool change count after slicing** by @unixunion in [PR 12474]({{L95}})
    The slicing results now show the total number of filament tool changes, giving a quick estimate of purge waste and print complexity for multi-material prints. Implements #12464.
    {{I72}}

* **Release Notes dialog improvements** by @yw4z in [PR 12265]({{L96}})
    The release notes dialog now has a cleaner layout with more space for content, properly sized web content without horizontal scrolling, a "Check on GitHub" button to view the release online, and improved hyperlink colors. Also fixes large images causing horizontal overflow.

    | Before | After |
    |--------|-------|
    | {{I73}} | {{I74}} |

* **MultiChooseDialog & Profile Dependencies improvements** by @yw4z in [PR 9971]({{L97}})
    The multi-select dialog now has proper window captions and labels, fixed "All" checkbox state handling, filtering support with select/deselect for visible items, and a right-click context menu. Optimized drawing for better performance.

    | Before | After |
    |--------|-------|
    | {{I75}} | {{I76}} |

* **Restructured Painting Tool UI** by @Xipit in [PR 12852]({{L98}}) with follow-ups by @Xipit and @yw4z in [PR 13340]({{L99}}), [PR 13421]({{L100}}), and [PR 13365]({{L101}})
    Reorganizes the painting tool interface for better usability: "On Overhangs only" is now placed under the overhang highlight slider (making the relationship clear), Vertical/Horizontal checkboxes appear under the Brush size slider and only when they affect the selected tool, and the Section View slider is available for the Gap Fill tool. The "Pen size" control is renamed to "Brush size" for consistency. Also fixes MMuSegmentation window width changes and standardizes brush size and smart fill angle controls.

    | Before | After |
    |--------|-------|
    | {{I77}} | {{I78}} |
    | {{I79}} | {{I80}} |

* **Restructure Text/Emboss Tool UI** by @Xipit in [PR 12864]({{L102}})
    Reorganized the Text/Emboss tool for a better workflow: the Style setting is now above Font (since it dictates the remaining options), Revert buttons follow their settings instead of preceding them, Operations are on a single line, and inconsistent spacing between elements has been fixed.

    | Before | After |
    |--------|-------|
    | {{I81}} | {{I82}} |

* **Unify Tool UI Footer** by @Xipit in [PR 12850]({{L103}})
    Standardized the footer across all gizmo tools with consistent "Done"/"Cancel" buttons, Reset button behavior (only enabled when changes have been made), and unified warning positions. The Text tool gains a Reset button. The Gap Fill tool's Apply buttons have been moved underneath the Gap Area slider. The detailed footer structure is: Content → Action Buttons → Tooltip / Reset / Confirm / Cancel → Warnings.

    | Before | After |
    |--------|-------|
    | {{I83}} | {{I84}} |
    | {{I85}} | {{I86}} |

* **Refactor Tooltip Button** by @Xipit in [PR 12848]({{L104}})
    Consolidated 9 slightly different tooltip button implementations into a single shared utility in GLGizmoUtils. Added tooltips to the Text gizmo and shortcut descriptions to the Cut gizmo. Shortcut labels now consistently use "Left mouse button" and platform-appropriate modifier key visuals throughout the UI.

    | Assembly gizmo tooltips (before) | Assembly gizmo tooltips (after) |
    |----------------------------------|--------------------------------|
    | {{I87}} | {{I88}} |

    | Emboss gizmo tooltips (before) | Emboss gizmo tooltips (after) |
    |----------------------------------|--------------------------------|
    |{{I89}}|{{I90}}|

    | Assembly Gizmo tooltip before | Assembly Gizmo tooltip after |
    |-------------------------------|------------------------------|
    | {{I91}} | {{I92}} |

* **Graphics Preferences: Anti-aliasing + FPS** by @ianalexis in [PR 13538]({{L105}})
    A new Graphics settings tab exposes MSAA multiplier (default 4x, was previously hardcoded) and adds FXAA (Fast Approximate Anti-Aliasing) as a post-process option. Lower MSAA improves performance on integrated GPUs; higher values improve quality on powerful GPUs or low-DPI monitors. Also adds an FPS counter and FPS limiter for diagnostic purposes.

    {{I93}}

    | FXAA Disabled | FXAA Enabled |
    |---------------|--------------|
    | {{I94}} | {{I95}} |

## QoL Improvements

* **Mouse button assignment (None/Pan/Rotate)** by @r3dbaba in [PR 10736]({{L106}})
    Left, Middle, and Right mouse buttons can now be independently assigned to None, Pan, or Rotate functions. This is particularly useful for left-handed users, those coming from other CAD tools with different mouse conventions, or anyone who wants a customized 3D viewport navigation experience. Addresses #4440 and #7272.

    {{I96}}

* **"Change type" UX as submenu with checkmarks** by @Eldenroot in [PR 12205]({{L107}})
    The "Change type" dialog is now an inline submenu with checkmarks, matching the "Change Filament" UX.

{{I97}}

* **Auto-select external spool if it's the only installed filament** by @Noisyfox in [PR 13356]({{L108}})
    When a printer has only an external spool installed (no AMS/multi-material unit), the external spool is automatically selected, eliminating an extra click. Also adds a warning when the model's filament type doesn't match the type set in the device. Fixes #13103.
    {{I98}}
    {{I99}}

* **Show filament edit button or action menu dynamically** by @yw4z in [PR 12651]({{L109}})
    The filament area now shows a simpler edit button instead of a full action menu for toolchanger/IDEX printers (where filament usage is fixed) and single-filament configurations. The Delete button has been moved to the end of the menu to prevent accidental clicks. Fixes #12649.

    {{I100}}

* **Disable "snap to build plate" option** by @Xipit in [PR 11801]({{L110}})
    Adds a per-object "Auto Drop" toggle (default enabled, shortcut `D`) surfaced in the context menu. When disabled, small arrows appear under the object's bounding box to indicate it won't snap to the bed. The setting is preserved across splitting and assembly operations, and survives in 3MF files. An "Auto Drop" checkbox is also available in the import dialog. Useful for preserving relative positioning when loading multi-part models. Addresses #8194.

    {{I101}}

* **Toggle printability with keyboard shortcut** by @datapaganism in [PR 13279]({{L111}})
    Press `V` to toggle the printability of selected objects on the build plate — a fast alternative to right-clicking each part. The shortcut is shown in the right-click context menu and documented in Keyboard Shortcuts preferences. Addresses #9120.

    {{I102}}

* **Linux: left-side window buttons option** by @yw4z in [PR 12831]({{L112}})
    Adds an option to place minimize/maximize/close buttons on the left side of the titlebar for Linux users who prefer a macOS-style layout. Tested on Debian GNOME, Mint Cinnamon, and Fedora KDE.

    {{I103}}

* **Require fewer clicks to change filament in object list** by @Xipit in [PR 12603]({{L113}})
    Changing filament for an object now takes 3 clicks instead of 5+: single click on the filament indicator, second click opens the dropdown, third click selects. This mirrors the existing name-change behavior.

    Before:

    <video controls width="800" src="{{L292}}"></video>

    After:

    <video controls width="800" src="{{L293}}"></video>

* **Show sparse infill rotation warning only once** by @RF47 in [PR 13461]({{L114}})
    The sparse infill rotation template warning now appears only once instead of repeatedly. Fixes #10963.

* **Improve generic 3MF import** by @ianalexis in [PR 13403]({{L115}})
    Generic and CAD-authored 3MF files are now imported silently as geometry instead of prompting an unnecessary dialog. Fixes #12434.

## Text / Description Improvements

* **Fix "cancle" typo** by @theshantanujoshi in [PR 13769]({{L116}})
    Corrected a misspelled "cancle" to "cancel" in the UI.
* **Add tooltips to Transfer buttons** by @ianalexis in [PR 13535]({{L117}})
    Transfer setting buttons now show descriptive tooltips.
* **Fix reverse on even hint** by @igiannakas in [PR 13739]({{L118}})
    Fixed an issue with wall direction reversal on even-numbered layers. Fixes #13425.
* **Clarify Create nozzle for existing printer** by @yw4z in [PR 11773]({{L119}})
    Users were often confused when they couldn't proceed past the nozzle selection step while trying to add a common nozzle size (like 0.4mm) that already existed as a preset. Instead of a dead end, the dialog now offers to switch to the existing preset so users can view, edit, and customize it directly — turning a blocking point into a guided workflow.

    | Before | After |
    |--------|-------|
    | {{I104}} | {{I105}} |

## Fixes & Consistency Improvements

* **UI fixes and improvements** by @yw4z in [PR 12513]({{L120}})
    A wide-ranging UI polish pass touching 15 areas: fixed Bambu device selector search box borders on dark mode, aligned titlebar menus with their associated buttons, improved combobox dropdown widths to match content, fixed version text size on macOS, corrected message dialog sizing (they were too wide), fixed canvas menu overlapping with the sliced plates toolbar, improved STEP import dialog styling with rounded rectangle tips section, fixed drop file dialog filename clipping by showing names on a separate line, improved hyperlink colors in canvas notifications, fixed Bambu bind dialog button alignment, enhanced the color picker margins, aligned project page welcome screen buttons, and corrected URL casing on web-related translations.

    **Drop file dialog**
    | Drop file dialog Before | After |
    |--------|-------|
    | {{I106}} | {{I107}} |

    **Preferences > Combobox dropdowns with content width**
    | Before | After |
    |--------|-------|
    | {{I108}} | {{I109}} |

    **Step mesh dialog**
    | Before | After |
    |--------|-------|
    | {{I110}} | {{I111}} |

    **Properly sized message dialogs**
    | Before | After |
    |--------|-------|
    | {{I112}} | {{I113}} |

* **Improve mode button visuals** by @yw4z in [PR 13795]({{L121}})
    Fixed the mode toggle button's colors (dark mode, pressed state), visual state after enable/disable from preferences, track drawing shape, and focus border. Developer mode now shows "DEV" text.

    Before
    {{I114}}
    After
    {{I115}}

* **Don't steal focus from text inputs on mouse hover** by @RF47 in [PR 12834]({{L122}})
    Hovering the mouse over the 3D viewport no longer steals keyboard focus from active text input fields. Fixes #12823.
* **Fix FilamentGroupPopup not dismissing on macOS** by @SoftFever in [PR 13574]({{L123}})
    Fixed a macOS freeze caused by the filament group popup dialog failing to dismiss.
* **Fix printer name disappearing when editing a nozzle variant** by @Noisyfox in [PR 13653]({{L124}})
    Editing a non-first nozzle variant of a multi-nozzle printer profile could cause the printer name to disappear.
* **Fix UI freeze after hiding sync popup on Linux** by @erpalma in [PR 13657]({{L125}})
    Hiding the filament sync popup on Linux/GTK could leave the UI unresponsive because `BaseTransparentDPIFrame::on_hide()` always called `mainframe->Show()`. Now only calls Show() when the main frame is not already visible. Fixes #11288, #11701, #12553.
* **Fix right edge of G-code viewer legend not interactive** by @kisslorand in [PR 11899]({{L126}})
    The rightmost edge of legend rows in the G-code viewer was not responding to clicks.
* **Fix sidebar filament count for multi-extruder printers** by @SoftFever in [PR 13706]({{L127}})
    Multi-extruder printers could show fewer filament slots in the sidebar than the printer actually has nozzles. This happened when switching between dual-extruder profiles (the sidebar would drop to a single filament) or when loading a partial saved filament list. The sidebar now always shows at least one filament slot per nozzle, and saved filament colors are preserved rather than truncated.
    {{I116}}
* **Fix vertical alignment issues** by @yw4z in [PR 13133]({{L128}})
    Fixed vertical misalignment of the printer name display and clone progress indicator in the sidebar, which were noticeably off-center.
* **Fix TextInput & ComboBox glitches after scrolling on scaled displays** by @yw4z in [PR 13805]({{L129}})
    Borders around text inputs and comboboxes were not filling the available space after scrolling on scaled displays. Tested on Windows 11.

* **Fix dirty-state marker for edited system printer presets** by @kisslorand in [PR 11900]({{L130}})
    System printer presets now correctly show the "*" (modified) indicator when edited, matching the behavior of all other preset types. Fixes #11705.
    | Before | After |
    |--------|-------|
    | {{I117}} | {{I118}} |

* **Fix ObjectTableDialog close on Escape** by @Jo-Con-El in [PR 12979]({{L131}})
    The Object Table dialog now correctly closes when pressing Escape.

* **Auto hide/show ironing angle settings** by @ansonl in [PR 11451]({{L132}})
    Ironing angle settings are automatically hidden when a concentric ironing pattern is selected, since they don't apply.

* **Remove black borders on controls on Linux and fix assertion errors** by @yw4z in [PR 13718]({{L133}}), [PR 13362]({{L134}}), and [PR 13363]({{L135}})
    Fixed GTK assertion errors on window resize, removed black borders on checkbox and switch buttons, and fixed unnecessary scrollbars appearing with only one filament.

    | Before | After |
    |--------|-------|
    | {{I119}} | {{I120}} |

* **Fix macOS object-list filament editor crash/glitch** by @thelegendtubaguy in [PR 13700]({{L136}})
    The filament column in the object list could enter Cocoa native text editing exposing `wxCustomRendererObject` or crash on invalid `DataViewBitmapText` values on macOS. Multiple defensive fixes applied, and on macOS filament-column editing now routes through the custom bitmap-choice renderer. Fixes #13682.

* **Fix Windows double window and title bar issues** by @ianalexis, @Noisyfox, and @yw4z in [PR 13074]({{L137}}), [PR 13020]({{L138}}), and [PR 13117]({{L139}})
    Fixed a double title bar issue on Windows 10 by removing the window caption style, enlarged the resize grabber zone for easier window resizing, and fixed overscaled controls (color picker, sidebar icons, titlebar buttons) that appeared after the wxWidgets upgrade due to missing scaling values on wxBitmaps. Fixes #13046, #13130, #13073.

    | Before | After |
    |--------|-------|
    | {{I121}} | {{I122}} |
    | {{I123}} | {{I124}} |

* **Fix "Jump to" links for non-print preset settings** by @kisslorand in [PR 13381]({{L140}})
    Validation notification "Jump to" links always targeted Print preset settings, even for issues in other preset types. Now correctly resolves the target preset type. Fixes #13350.

* **Fix stale keyboard refresh and auto-resize flicker in Preview** by @kisslorand in [PR 12707]({{L141}})
    Keyboard navigation in the Preview tab now immediately refreshes the speed profile popup, and the popup no longer flickers with an incorrect height before correcting itself.

* **Fix Flow Ratio dialog shrinking after minimize** by @packerlschupfer in [PR 13545]({{L142}})
    On Linux/wxGTK, minimizing the main window collapsed the Flow Ratio calibration dialog to ~222x249px with the OK button unreachable. The dialog was missing `SetSizeHints()` which all other calibration dialogs already use.

* **Fix filament combobox not working after adding extruder** by @Noisyfox in [PR 13194]({{L143}})
    For multi-tool printers, the filament selection combobox would stop working after adding a new extruder, leaving the filament slot unconfigurable.

    | Before | After |
    |--------|-------|
    | {{I125}} | {{I126}} |

* **Fix font rendering pixelated when ClearType disabled** by @yw4z in [PR 12201]({{L144}})
    Added grid-fitting metadata to the UI font using FontForge so text renders correctly on Windows when ClearType is turned off (common on high-resolution or non-RGB displays). Fixes #11732.

    | Before (ClearType off) | After |
    |------------------------|-------|
    | {{I127}} | {{I128}} |

* **Fix flushing volume dialog OK/Cancel buttons clipped** by @Blumlaut in [PR 13762]({{L145}})
    The flushing volume dialog's OK/Cancel buttons could fall below the visible area when the window was clamped to screen size (many filaments, small displays, or high DPI). Converted to flexbox layout with a scrollable table area, and added an accurate fixed overhead calculation in C++. Fixes #13511.

    | Before (buttons clipped below visible area) | After (scrollable table, buttons always visible) |
    |----------------------------------------------|---------------------------------------------------|
    | {{I129}} | {{I130}} |

* **Allow the flush volumes dialog to be resized** by @erpalma in [PR 13663]({{L146}})
    The flushing volumes dialog can now be resized, making it easier to manage long filament lists for multi-material printers.

* **Linux: match titlebar font** by @yw4z in [PR 12828]({{L147}})
    The custom titlebar font now matches the system UI font on Linux by applying `SetFont()` to the ArtProvider and window title, bringing the titlebar text visually closer to native windows. Previously the ArtProvider used the default system font which caused a noticeable mismatch between the titlebar and the rest of the window.

    {{I131}}

* **Improved Splash screen rendering** by @yw4z in [PR 12586]({{L148}})
    Simplified the splash screen drawing code, fixed blank splash screen on Linux (#13441), and fixed a niche crash (#12576). Fonts now use the correct size on scaled monitors by using wxPaintDC which already accounts for DPI scaling.

* **Hide non-applicable settings for tree supports** by @kisslorand in [PR 12367]({{L149}})
    Settings that don't apply to tree-based supports (such as Independent Support Layer Height for Organic trees and Threshold Overlap for all tree styles) are now hidden from the UI when a tree support style is selected, reducing confusion and incorrect bug reports.

* **Improve readability of "Only one wall" settings** by @yw4z in [PR 13121]({{L150}})
    The one-wall threshold option is now hidden when its parent setting is disabled, reducing clutter and making the "Only one wall on top/bottom/internal surfaces" parameters easier to read.

    | Before | After |
    |--------|-------|
    | {{I132}} | {{I133}} |

* **Fix seams glitch on Linux** by @RF47 in [PR 13233]({{L151}})
    Fixed missing faces in seam geometry on Linux that appeared as visual glitches in the preview.

    | Before | After |
    |--------|-------|
    | {{I134}} | {{I135}} |

# 🛠️ Bug Fixes

* **Fix crash when selecting or moving wipe tower** by @icedrone in [PR 13243]({{L152}})
    Fixed a regression from the auto-drop feature where selecting or moving the wipe tower caused a crash due to a garbage pointer dereference. The wipe tower has a synthetic object index outside the normal range, which was not guarded against in `Selection::get_auto_drop()`.

* **Fix support interface semantics, gap handling, and tree support interfaces** by @kisslorand in [PR 11812]({{L153}})
    A comprehensive 4-part fix for support structures: replaced the global soluble interface flag with explicit per-side zero-gap detection, fixed interface spacing/density coupling, corrected bottom interface generation for both organic and non-organic tree supports, fixed deterministic interlacing, and resolved issues with independent layer height interface count semantics. Fixes #8887, #10763.

* **Fix extrusion of support layers at wrong Z height** by @kisslorand in [PR 13327]({{L154}}) and [PR 13460]({{L155}})
    In rare cases, two support layers were created back-to-back without moving to the correct Z height between them, causing missing support layers. Height tracking info was being cleared too early, and the ZAA port in #12736 reverted the original fix. Both issues are now resolved.

* **Fix support preview artifacts (missing layers)** by @kisslorand in [PR 13310]({{L156}})
    Floating-point imprecision in gap subdivision (`ceil(0.20000001/0.2)` = 2 instead of 1) could produce duplicate splits, causing missing support layers in the preview. Added epsilon tolerance to prevent this. Fixes #12846.

    | Before | After |
    |--------|-------|
    | {{I136}} | {{I137}} |

* **Fix collision with the bed using tree supports** by @RF47 in [PR 13524]({{L157}})
    Added a safeguard ensuring the first layer height is never less than the brim height, preventing a rare bed collision with tree supports. Fixes #13500.

* **Fix tree support "on build plate only" missing interface layers** by @Argolein in [PR 13192]({{L158}})
    Tree supports with "on build plate only" enabled were not generating support interface layers, resulting in poor surface quality on supported overhangs.

    | Before | After |
    |--------|-------|
    | {{I138}} | {{I139}} |

* **Fix role-based fan speeds lost on layer change** by @kisslorand in [PR 13390]({{L159}})
    Feature-specific fan speed overrides could be silently lost when crossing layer boundaries because Orca skipped emitting a fresh G-code marker, thinking it was already active. Now correctly layer-aware — each new layer emits a fresh marker when a feature continues across the boundary. Fixes #8143.

* **Fix fan stuck at wrong speed after role-based override ends** by @kisslorand in [PR 13336]({{L160}})
    When fan speed-up time was enabled with role-based fan overrides, the fan could stay stuck at the higher override speed because Orca lost track of the actual fan speed output. Now correctly returns to the expected speed after overrides complete.

* **Fix first layer speed and slow down handling with rafts** by @yogihybo in [PR 13224]({{L161}}) and [PR 13415]({{L162}})
    Initial layer speed and slow-down logic now correctly account for raft layers. The first raft base layer gets the correct infill speed, overhang slowdown is excluded for the first layer above the raft, and slow-down layer interpolation is split into separate branches for rafts vs. no rafts. Fixed an operator precedence bug (`!m_config.raft_layers > 0` → `m_config.raft_layers == 0`).

    | Before (with raft) | After (with raft) |
    |---------------------|-------------------|
    | {{I140}} | {{I141}} |

* **Fix overhang reverse threshold being ignored** by @kisslorand in [PR 13061]({{L163}})
    Wall direction was reversing on alternating layers even with disabled fuzzy skin, because disabled fuzzy skin was still treated as active internally, triggering an alternative wall generation path that skipped the overhang threshold check. Also fixes arc fitting and contour simplification. Fixes #13055.

* **Fix crash from inconsistent draft shield layer height** by @RF47 in [PR 12937]({{L164}})
    Multi-object prints with per-object draft shields and independent support layer heights could produce erratic draft shield layers or crash with large object counts. Support layer height is now properly isolated and does not interfere with draft shield generation. Fixes #10950, #10788.

    | Before | After |
    |--------|-------|
    | {{I142}} | {{I143}} |

* **Fix fuzzy skin regression with classic wall generator** by @RF47 in [PR 12920]({{L165}})
    Fixed a regression where the classic wall generator produced artifacts with fuzzy skin enabled. Still fixes the original fuzzy skin artifact from the prior commit without the regression. Fixes #12911.

    {{I144}}

* **Fix save custom machine profiles with different extruder count** by @RF47 in [PR 13035]({{L166}})
    Custom machine profiles with a different extruder count than their parent now save correctly. The root cause: this function was cherry-picked from Bambu Studio, which doesn't allow changing the number of extruders. Fixes #12949, #12994.

* **Fix trapezoidal fill layer rotation with infill combination** by @RF47 in [PR 13276]({{L167}})
    Rotation was calculated from layer ID rather than the actual layer position, causing incorrect rotation when infill combination was active. Fixes #13275.

* **Fix flush_multiplier type mismatch** by @SoftFever in [PR 13062]({{L168}})
    Fixed a type mismatch where `flush_multiplier` was using a single float instead of a vector of floats, causing incorrect flush volume behavior.

* **Fix air filtration and chamber heater UI controls** by @kisslorand in [PR 12525]({{L169}}), [PR 13384]({{L170}}), and [PR 13440]({{L171}}), and by @brandonfhall in [PR 13393]({{L172}})
    Fixed air filtration and exhaust fan settings being incorrectly hidden on printers that support them (Bambu H2D, P1S, X1, X1C, Elegoo Centauri). Chamber temperature control is now always visible for Klipper users who need it for macros and heat soaking, while M141/M191 emission is still gated by the "activate temperature control" flag. The support chamber temperature control flag is also now exposed in filament profiles without requiring developer mode (#12924).

* **Fix first layer toolhead preheating with 2+ extruders and ooze prevention** by @igiannakas in [PR 13741]({{L173}})
    With ooze prevention enabled and preheat_time > 0, the first layer's early M104 used "Other layers" temperature instead of first-layer temperature because `m_layer_id` had already advanced by post-process time. Now tracks a local `current_layer_id` that increments on layer changes. Fixes #13351.

* **Fix vase mode zero flow bug** by @RF47 in [PR 13517]({{L174}})
    Extremely short extrusions in vase mode could cause flow to drop to zero, particularly problematic with large nozzles. These are now filtered out with a minimum extrusion length that depends on slice resolution.

* **Fix collision warnings for overlapping instances** by @tome9111991 in [PR 12122]({{L175}})
    Duplicate instances of the same object were not flagged with collision warnings because collision detection relied on cached convex hulls at the ModelObject/ModelVolume level. Also improved wipe tower conflict detection. Fixes #12077.

    {{I145}}

* **Fix outer wall for bridges** by @kisslorand in [PR 13411]({{L176}})
    Enabling "Bridge counterbore holes" by "Partially bridged" caused ordinary bridges to lose their overhang-wall generation. The partial-bridge rewrite was being applied to all unsupported bridge islands, not just counterbore-like surfaces. Now restricted to hole-bearing bridge islands only. Fixes #13344.

    | Before | After |
    |--------|-------|
    | {{I146}} | {{I147}} |

* **Fix auto-arrangement boundary for skirt loops** by @Eldenroot in [PR 12999]({{L177}})
    Cherry-picked from Bambu Studio. Auto-arrange now correctly accounts for skirt loops when calculating object placement boundaries.

* **Fix sacrificial bridge layer edge case with only 2 perimeters** by @RF47 in [PR 13018]({{L178}})
    With only 2 perimeters, walls could disappear from sacrificial bridge layers because the filter consumed the entire ExPolygon. The geometry handling now preserves walls at low perimeter counts. Fixes #12953.

    | Before | After |
    |--------|-------|
    | {{I148}} | {{I149}} |

* **Fix LAN printing crashes and hangs on Bambu H2D** by @hyiger in [PR 13296]({{L179}})
    Fixed two LAN printing issues with newer Bambu networking plugins: a crash from missing file transfer symbols, and indefinite hangs at 30% upload progress caused by the eMMC print path on H2D. LAN mode now correctly falls back to the standard FTP transfer path. Also fixes H2D LAN print job routing by @erpalma in [PR 13662]({{L180}}).

* **Fix non-ASCII path corruption on Windows** by @SoftFever in [PR 13036]({{L181}})
    Fixed file path corruption when paths contain non-ASCII characters on Windows using a `from_path()` helper.

* **Fix "Access Violation" crash** by @RF47 in [PR 12856]({{L182}})
    Added range checks to prevent access violations when parsed extruder or filament IDs are out of bounds in M1020 and T command processing. Fixes #12704.

* **Fix crash with painted line on corrupted models** by @RF47 in [PR 12806]({{L183}})
    Fixed an infinite loop condition when rasterizing a painted line across corrupted mesh geometry. Fixes #12648, #13083.

* **Fix crash when returning from assembly view on Linux** by @RF47 in [PR 13091]({{L184}})
    Refactored the "Return" toolbar button handling to use deferred actions and null checks, fixing a crash when exiting assembly view. Fixes #12768.

* **Fix crash when changing SVG/TEXT type to Support Blocker/Enforcer** by @yw4z in [PR 13120]({{L185}}) and @DImagine in [PR 13281]({{L186}})
    Disabled Support Blocker/Enforcer menu items are now properly grayed out when the selection contains SVG or TEXT volumes (which don't support these modifiers). A follow-up further hardens the original fix and removes a dead code path. Fixes #5070.

* **Fix crash with SVG "use surface"** by @RF47 in [PR 13262]({{L187}})
    Added preflight mesh validation (validity, emptiness, self-intersection check) before CGAL corefinement operations when applying "use surface" to SVG modifiers. Fixes #13167.

* **Fix crash on launch from temporary object reference** by @Noisyfox in [PR 13341]({{L188}})
    Fixed a crash on application startup caused by a dangling reference to a temporary object introduced in the tooltip button refactor (#12848).

* **Fix stealth mode handling** by @RF47 in [PR 13285]({{L189}})
    Stealth mode now correctly avoids network connections and cloud sync operations when enabled. Fixes #13049.

* **Fix per-feature filament assignments ignored at slice time** by @ianalexis in [PR 13607]({{L190}})
    Filament assignments made for specific features (e.g., per-role filament) were not honored during slicing. Fixes #10470.
* **Fix one wall on top/bottom surfaces for assembly objects** by @igiannakas in [PR 13714]({{L191}})
    The "one wall on top/bottom surfaces" setting was applied incorrectly to assembly objects, and is now handled correctly.
* **Fix partial sacrificial bridge anchors** by @ianalexis in [PR 13052]({{L192}})
    Improves anchor generation for partial sacrificial bridges, producing more reliable bridging over overhangs.
* **Fix false out-of-bounds validation for large paths** by @ianalexis in [PR 13179]({{L193}})
    When a feature's bounding box extended beyond the build volume, Orca could raise a false "out of bed" error. It now falls back to per-move validation. Fixes #11965.
* **Skip small-area compensation validation when disabled** by @ianalexis in [PR 12528]({{L194}})
    Model validation no longer raises false errors related to small-area flow compensation when that feature is turned off.
* **Fix .gcode.3mf files not displaying** by @Noisyfox in [PR 13360]({{L195}})
    Fixed an issue where opening a .gcode.3mf file would not display its contents. Fixes #13159.
* **Harden CLI export without OpenGL** by @mwnickerson in [PR 13532]({{L196}})
    CLI export now continues in headless environments where OpenGL thumbnail generation is unavailable, instead of failing.
* **Fix crash when embossing text** by @Noisyfox in [PR 13772]({{L197}})
    Bumped the worker thread stack size to 16MB to prevent a crash when embossing text into models via CGAL on macOS and Linux. Fixes #13313.
* **Fix assembly view crash and empty canvas on Flatpak** by @yw4z in [PR 13413]({{L198}})
    Fixed a crash when entering assembly mode and an empty 3D canvas when running the Flatpak build.
* **Ignore SIGPIPE at startup to prevent crashes on dropped printer connections** by @zsiddique in [PR 13788]({{L199}})
    Prevents crashes caused by SIGPIPE signals when printer network connections are unexpectedly dropped.
* **Fix possible null dereference in DeviceManager during timer refresh** by @SoftFever in [PR 13802]({{L200}})
    Fixed a potential crash when `DeviceManager::check_pushing()` is called while the selected machine reference is missing or stale during a timer refresh.
* **Fix flatpak crash on start** by @SoftFever in [PR 13808]({{L201}})
    Fixed a crash that occurred when launching the Flatpak build of OrcaSlicer.
* **Fix single-instance IPC by preserving "OrcaSlicer" suffix in title** by @AMoo-Miki in [PR 13017]({{L202}})
    Fixed the single-instance file handoff mechanism on Windows that was broken by a title bar change.
* **Fix stealth mode cloud service logout** by @SoftFever in [PR 13531]({{L203}})
    When stealth mode is enabled, cloud services are now logged out and the sideboard is hidden for privacy.
* **Fix wxWidgets 3.3.2 upgrade issues** by @SoftFever in [PR 13740]({{L204}}), @bwees in [PR 13737]({{L205}}), @thomashenauer in [PR 13707]({{L206}}), and @SoftFever in [PR 13747]({{L207}})
    Various fixes following the wxWidgets 3.3.2 upgrade: ObjectTable crash on cell deselect, macOS deep link handling, submenu popup parenting on Wayland, and a Preview tab crash on Linux/Wayland at startup.
* **Fix filament syncing with nozzle diameter guards** by @lynaghk in [PR 13330]({{L208}})
    Fixed a regression where filament syncing was incorrectly blocked by nozzle diameter compatibility checks, affecting printers that don't report nozzle information. The fix encapsulates the checking logic in a dedicated helper function for more robust compatibility validation. Fixes #13236 and #13176.
* **Fix Bambu Cloud login via embedded WebView** by @andrewsoonqn in [PR 13768]({{L209}})
    Fixed an issue where Bambu Cloud login via the embedded WebView would fail after submitting the verification code. Newer Bambu network plugin flows return a `user_ticket_login` command with a short-lived ticket, which the embedded WebView dialog did not handle — the login result was ignored and the UI appeared to keep loading. The fix adds the missing ticket exchange flow so embedded WebView login works consistently with the external browser path.
* **Fix Bambu login regression** by @SoftFever in [PR 13407]({{L210}})
    Fixed a regression introduced in the 3MF version tag update (#12509) that prevented logging into Bambu Cloud. Added a ticket-based OAuth flow.
* **Fix "could not load bitmap printer_preview_" crash on Linux** by @yw4z in [PR 12425]({{L211}})
    The code used a non-existent printer cover bitmap for non-BBL printers, causing a crash on Linux. Now uses covers from the vendor folder.
* **Fix PrinterWebView deferred URL clearing** by @RobertKuszmar in [PR 11508]({{L212}})
    PrinterWebView now only clears the deferred URL on successful load, retrying when returning to the device tab after the printer was off.
* **Fix Windows test linking** by @Wachhund in [PR 12939]({{L213}})
    wxWidgets Unicode defines caused Catch2 to provide wmain() instead of main(), breaking all test executables on MSVC.
* **Fix registration of filament_dynamic_map and filament_switcher config options** by @malventano in [PR 13623]({{L214}})
    Two config options added for X2D support were never registered in PrintConfig.cpp, causing crashes when loading .3mf files containing these keys.
* **Fix input_filename_base using object name instead of project name** by @raistlin7447 in [PR 13753]({{L215}})
    Export G-code always used the first object's name instead of the saved project name because three export functions were passing empty strings to `output_filepath_for_project()`. Now correctly uses the saved project path. Fixes #1945.
* **Fix crash on startup from low max volumetric speed** by @yw4z in [PR 13716]({{L216}})
    Some profiles inherited a max volumetric speed of 0, causing a crash. A default value of 12 is now set for all common profiles.
* **Fix model/step MIME type support on Unix** by @Eldenroot in [PR 13000]({{L217}})
    Cherry-picked from Bambu Studio. Added model/step to the list of supported MIME types on Unix, enabling proper file association for STEP files on Linux and macOS.
* **Fix crash when color was not specified** by @Eldenroot in [PR 13002]({{L218}})
    Added a fallback when a color value was not specified, preventing a crash.
* **Fix generic locale fallback on all platforms** by @icedrone in [PR 12948]({{L219}})
    When the system locale was set to an unavailable regional variant (e.g., en_IL), OrcaSlicer could crash on startup. The fallback logic (try base language, then chain through best available translations) was previously Linux-only; now works on all platforms.
* **Fix CLI segfault with P1S profiles** by @sparkleHazard in [PR 13193]({{L220}})
    CLI slicing with BBL printer profiles crashed due to nullptr dereference when extruder/filament options were absent from the resolved config. Added null guards.
* **Fix Linux segfault when loading Fluidd/Mainsail printer hosts** by @SoftFever in [PR 13724]({{L221}})
    WebKitGTK segfaults on `<object>` elements in older Fluidd (<1.37.0) and Mainsail (<2.16.1). A document-start user script injected inside PrinterWebView replaces vue-resize's `<object>` elements with `<div>` shims. Linux only. Credit to @VittC for diagnosing the root cause. Fixes #7210.
* **Fix macOS crash on close** by @Noisyfox in [PR 13215]({{L222}})
    Fixed a crash that occurred when closing OrcaSlicer on macOS.
* **Fix Windows file handoff when single-instance mode enabled** by @kisslorand in [PR 12944]({{L223}})
    Opening files from Explorer while Orca runs in single-instance mode was silently dropping files because the forwarding logic looked up the running instance by its title text, which had changed. Now uses stable window properties and instance hashes instead. Fixes #12925.
* **Fix arc fitting time progress with firmware retraction** by @vovodroid in [PR 12888]({{L224}})
    Fixed an issue where arc fitting broke the remaining time progress indicator when firmware retraction was enabled. Fixes #12796.
* **Fix Bambu camera stream freeze on Linux** by @tofublock in [PR 13359]({{L225}})
    The X1C live camera view froze after a few seconds on Linux due to unreliable decode timestamps from the Bambu tunnel library causing GStreamer to wait indefinitely for future timestamps. Fixed by synthesizing monotonic timestamps using EWMA-based period adaptation. Linux only.
* **Fix filament/printer selection stuck on loading** by @yw4z in [PR 13492]({{L226}})
    Fixed the filament and printer selection dialog getting stuck in an indefinite loading state.
* **Fix second extruder settings not handled for H2D/X2D** by @Noisyfox in [PR 13648]({{L227}})
    A signed/unsigned comparison bug caused extruder_id=-1 ("all extruders") to be treated as 0xFFFFFFFF and reset to 0, so only the first extruder received the correct settings variant. Fixes #13559.
* **Fix MANUAL_TOOL_CHANGE regression for BBL printers** by @SoftFever in [PR 13516]({{L228}})
    BBL-specific M1020 S handling in `toolchange()` bypassed `toolchange_prefix()`, so `manual_filament_change` had no effect and M1020 was always emitted regardless of the setting. The BBL logic is now properly moved into `toolchange_prefix()`. Fixes #11795.
* **Fix unicode preset name crash** by @SoftFever and @Noisyfox in [PR 13458]({{L229}}) and [PR 13503]({{L230}})
    Fixed a crash when preset names contained characters outside the ASCII range (e.g., accented characters, CJK characters, or other Unicode text).

# 📜 Profiles

## Profile Processing Improvements

* **Fix generic filaments not showing on list** by @Sabriel-Koh in [PR 13037]({{L231}})
    Multiple fixes for the printer/filament selection dialog: blank selections on first open, default filaments not being pre-selected during initial setup, @System filament naming missing the postfix, and single-item sub-dropdowns not rendering. Also refactored code to properly save profile data before updating the selection. Fixes #12297, #12922.
* **Fix stray "Default Filament" preset selection** by @SoftFever in [PR 13570]({{L232}})
    A stray "Default Filament" entry could be written to OrcaSlicer.conf and cause a misleading filament selection on load. It is now ignored.
* **Fix preset variant truncation on load** by @cgarwood82 in [PR 13316]({{L233}})
    When a child printer preset has more extruders than its parent, `set_with_restore` silently truncated per-extruder settings during project load. Added a guard to skip the parent-shaped merge when the child has more extruders. Fixes #12085.

## New Printer Profiles
* **X2D Support** by @glowstab in [PR 13388]({{L234}})
    Adds full printer definition, machine/process/filament presets, and dual-nozzle handling for the Bambu Lab X2D. Includes support for custom filament mapping, auto-mapping, wipe tower cooling, LAN mode printing, and left/right filament distinction. Validated with 20+ hours of dual-nozzle printing and all CTest tests passing. Fixes #13294.
* **Bambu Lab P2S** printer and process profile updates matching latest official tweaks by @misterff1 in [PR 13118]({{L235}}) and [PR 13355]({{L236}})
* **Flashforge Artemis** printer profile by @midnight-creator in [PR 11902]({{L237}})
* **Flashforge Creator 5 and Creator 5 Pro** printer profiles by @FlashforgeOfficial in [PR 13259]({{L238}})
* **Anycubic Kobra 3 Max** printer profile by @robertbaker in [PR 11586]({{L239}})
* **Anycubic Kobra X** printer profile by @CSLRDoesntGameDev in [PR 13529]({{L240}}) and [PR 13677]({{L241}})
* **re:3D** printer profiles by @re3Dev in [PR 12935]({{L242}})
* **LH Stinger** printer profiles by @lhndo in [PR 13410]({{L243}})
* **Cubicon xCeler-Mini** printer and material profiles by @Hyvision in [PR 13172]({{L244}})

## New Filament Profiles

* **Bambu Lab Beta Filaments** (PLA, PETG, ABS, TPU) profiles by @ericwong-person in [PR 13318]({{L245}})
* **GreenGate3D PETG** filament profile by @stringlapse in [PR 13448]({{L246}})
* **FILL3D PLA Basic, PETG, PP, PPCF, PA** filament profiles by @julianramirezarango-source in [PR 12973]({{L247}})

## Profile Updates & Fixes
* **Profile folder optimizations** — SVG textures fır best quality, 50% size reduction (68MB → 34MB), bed model optimizations and updates HQ covers for Anet, Anker, Anycubic, Artillery, BIQU, Creality, Elegoo, Flashforge, FLSUN, Prusa, Qidi, Re3D, Rh3D, Snapmaker, Sovol, and more by @yw4z in [PR 13149]({{L248}})
* **Bambu Lab X2D** printer definition, machine/process/filament presets, and dual-nozzle support by @glowstab in [PR 13388]({{L249}})
* **Bump printers version to propagate X2D to existing users** by @RJAudas in [PR 13806]({{L250}})
* **Snapmaker U1** — 5 bug fixes and new 0.6mm/mixed-nozzle profiles by @kbaker827 in [PR 12824]({{L251}})
* **Anycubic Kobra Neo** 0.4mm nozzle profiles by @AndyHazz in [PR 12913]({{L252}})
* **Qidi X-Max 4** nozzle profile updates by @HYzd766 in [PR 13526]({{L253}})
* **Qidi X-Max 4** hotbed temperature adjustments by @HYzd766 in [PR 13717]({{L254}})
* **Qidi** disable Reduce infill retraction by @HYzd766 in [PR 13267]({{L255}})
* **Creality K2** STL and texture updates by @folofse in [PR 13098]({{L256}})
* **Creality K2 Plus/K2** adaptive bed mesh bounding box by @imammedo in [PR 13290]({{L257}})
* **Creality generic ASA** first layer temp adjusted from 60°C to 100°C by @pghwinter in [PR 13558]({{L258}})
* **Elegoo Centauri Carbon 2** filament_type fix by @Wegerich in [PR 13012]({{L259}})
* **Elegoo** profile cleanup by @SoftFever in [PR 13148]({{L260}})
* **Elegoo Centauri Carbon 2** file upload and device details support by @anjis-elegoo in [PR 13212]({{L261}})
* **Improved Z-Bolt Profiles** — filament renaming, G-code thumbnails, 0.6mm processes, and macros by @Transistor427 in [PR 13240]({{L262}})
* **Fix custom ZBolt profile filament selection** showing only @system by @peachismomo in [PR 13468]({{L263}})
* **Fix Ender-3 V3 KE** nozzle switching by @dennisklappe in [PR 13438]({{L264}})
* **Junction Deviation profiles & calibration limits** — JD values updated across Marlin printer profiles, with calibration capped at 0.3 and a warning above 0.25 by @ianalexis in [PR 13241]({{L265}}) and [PR 13253]({{L266}})
* **Printer cover images** added and improved (RatRig, Centauri Carbon, Kingroon, and more) by @ianalexis in [PR 13660]({{L267}})
* **Fix K2 family chamber temperature control defaults** by @brandonfhall in [PR 13399]({{L268}})
    Chamber temperature control was hidden on Creality K2, K2 Plus, and K2 Pro because it required Developer mode. Now enabled by default.
* **Fix Ender-3 V3 KE nozzle switching** by @dennisklappe in [PR 13438]({{L269}})
    Missing printer_variant keys in nozzle profiles caused the slicer to always revert to 0.2mm.

# 🗪 Localization

* Brazilian Portuguese translations by @afmenez in [PR 12891]({{L270}})
* Spanish translation update by @Jo-Con-El in [PR 12981]({{L271}}), @ianalexis in [PR 13652]({{L272}}), and @peterm-m in [PR 13196]({{L273}})
* German translation updates by @hliebscher in [PR 13785]({{L274}}), STEP typo fix by @hliebscher in [PR 13100]({{L275}})
* Czech translation with full menu by @jakubhencl in [PR 13465]({{L276}})
* Turkish translations update by @GlauTechCo in [PR 13155]({{L277}})
* Italian translation updates by @Kappa971 in [PR 13585]({{L278}}), [PR 13674]({{L279}}), and [PR 13720]({{L280}})
* Hungarian language update by @kisslorand in [PR 13321]({{L281}})
* Simplified Chinese locale fixes by @Neko-vecter in [PR 13225]({{L282}}) and [PR 13235]({{L283}})
* Globally fix "milimeters" typo by @valerii-bokhan in [PR 13295]({{L284}})
* Globally fix "milisecond" typo by @afmenez in [PR 13329]({{L285}})
* Remove wrong c-format/boost-format markers from non-format strings by @afmenez in [PR 13251]({{L286}})
* Improve language on some GUI strings by @afmenez in [PR 13553]({{L287}})
* General translation and string-list refresh by @ianalexis in [PR 13622]({{L288}})
* **Fix Simplified Chinese locale issues** by @Neko-vecter in [PR 13225]({{L289}})
    Fixed incorrect translations for several UI elements in Simplified Chinese: corrected the "On" key label, changed the filament term from `细丝` to `耗材`, and fixed the view cube labels.

---

# ❤️ Support OrcaSlicer

> **OrcaSlicer is — and will remain — free and open source.**
>
> Every release represents countless hours of behind-the-scenes work: building features, fixing bugs, validating profiles, and testing across real machines.
>
> If OrcaSlicer helps you bring ideas to life, please consider supporting the project. Donations are used to support the open-source contributors who help build and maintain OrcaSlicer, and to cover project costs such as servers, development tools, test machines, filament, printer parts, and other infrastructure.
>
> Your support helps us keep improving OrcaSlicer for everyone — while keeping the project free, open, and community-driven.
>
> **Thank you for being part of the OrcaSlicer journey.** 🙏

<p align="center">
  <a href="{{L294}}">{{I150}}</a>
</p>
<p align="center">
  <a href="{{L295}}">{{I151}}</a>
</p>
