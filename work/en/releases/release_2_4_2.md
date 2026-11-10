# V2.4.2

This is the OrcaSlicer V2.4.2 release — a maintenance update on top of 2.4.1, focused on making profiles, cloud sync, and printer connectivity more dependable. Upgrading from an older version is smoother: presets that were built on a printer or filament that has since been renamed or removed now load correctly, so you should see far fewer "missing preset" warnings. Cloud sync gets several fixes too — filament settings you had turned off no longer switch themselves back on, sync messages now tell you exactly which preset is involved, and running two copies of OrcaSlicer signed into the same account no longer logs you out at random. Installing and updating the Bambu network plugin is reliable again, including when you switch versions on Windows. On top of that, this release fixes several crashes (rotating the prime tower, using the Measure tool, and running a Pressure Advance calibration), a couple of slicing and print-time-estimate problems, and Reload from Disk for STEP models after you reopen a project. New this time: a filename placeholder for the first object's name, clickable wiki links in the Preferences dialog, and add:north filament profiles.

# 🌊 New Features & Improvements

* **`{first_object_name}` filename placeholder** by @raistlin7447 in [14497]({{L1}})
    Adds a new `{first_object_name}` placeholder you can put in the output filename format — it fills in the name of the first printable object on the plate. In older versions the default `{input_filename_base}` would sometimes fall back to the first object's name; that was corrected earlier, but some people had relied on it to get the part name into their file names. This placeholder brings that option back, and it changes nothing unless you add it to your format. Closes #14493 and #14513.

    {{I1}}

* **Wiki links and a tidier Preferences dialog** by @yw4z in [13857]({{L2}})
    The Preferences dialog now shows clickable "Wiki" links next to settings — the same as in the sidebar — so you can open the relevant documentation in one click. It's also reorganized so related options sit together (Draco export quality under Project, the shared-profiles notification under Preset, filament sync mode next to auto-sync), combo boxes now have tooltips, there's a new "Experimental features" section under Developer, and the network-plugin Reload button has moved here from the Developer tab.

    {{I2}}

* **Use number-or-percentage settings in custom G-code** by @Noisyfox in [14526]({{L3}})
    Some settings can be entered either as a fixed number or as a percentage. Custom G-code can now read these values; before, referring to one of them returned nothing. Fixes #14522.

* **Name the preset in cloud-sync messages** by @SoftFever in [14592]({{L4}})
    When cloud sync reports a conflict, asks you to confirm a force-push, or says a preset is too large to sync, the message now names the specific preset involved instead of leaving you to guess which one it means.

# 🛠️ Bug Fixes

## Profiles & presets

* **Repair presets that pointed at renamed or deleted profiles** by @SoftFever in [14595]({{L5}})
    Fixes user presets that were based on — or paired with — a printer or filament profile that has since been renamed or removed, which could leave the preset broken after an upgrade. OrcaSlicer's built-in profile checks now run for every brand by default, so these broken links are caught early.

* **Reconnect older presets to renamed profiles** by @peachismomo and @SoftFever in [14507]({{L6}})
    Presets you created in older versions can now find their original profile even after it was renamed — this covers Ginger (rPLA/rPETG now map to PLA/PETG), Panchroma (PLA Stain → Satin), several Elegoo RAPID/PETG naming variants, and a few Bambu Lab presets. A new automated check also tests presets from past OrcaSlicer versions against the current profiles before each release, so this kind of upgrade problem is caught ahead of time. Together these address the missing-preset reports seen after upgrading past 2.4.1.

* **Keep filaments compatible with renamed printers** by @peachismomo and @SoftFever in [14504]({{L7}})
    When a printer profile is renamed, filaments you had set up for its old name could suddenly look incompatible and drop off the list. OrcaSlicer now recognizes a printer's previous names, so those filaments stay compatible — and your saved files don't need to be edited.

* **Correct the type label in the preset bundle dialog** by @peachismomo in [14481]({{L8}})
    In the preset bundle dialog, process presets were labeled with the type "preset"; they now correctly show "process".

## Cloud sync & accounts

* **Keep disabled filament overrides off after cloud sync** by @ExPikaPaka in [14550]({{L9}})
    A filament override you had switched off — for example *Retract Before Wipe* — could quietly turn itself back on (and reset to its default) after a cloud sync or a restart. Because of how the "off" state was stored, it was being left out of the synced profile and then filled back in with the default value. Disabled overrides are now always saved explicitly, so they stay off. Fixes #13943.

* **Fix version not updating correctly on Linux and macOS** by @SoftFever in [14617]({{L10}})
    On Linux and macOS, the app version wasn't being refreshed properly after an update, so the cloud-sync "profile sync change" notification could keep appearing on every launch with the auto-sync checkbox greyed out and impossible to turn off. The version is now detected correctly on all platforms, so the sync notification behaves as it should. Fixes #14581.

* **Stop two open copies from logging each other out** by @peachismomo in [14531]({{L11}})
    Running more than one copy of OrcaSlicer signed into the same account on one computer could log you out at random, because the copies could interfere with each other's login session. They now coordinate through your system's secure credential store and take turns renewing the session, so they no longer knock each other offline. (This covers copies on the same computer; using the same account on separate computers is unchanged.)

## Networking plugin

* **Stop the repeated "reinstall Bambu network plugin" prompt** by @Noisyfox in [14511]({{L12}})
    If you had used the older ("legacy") network plugin in the past, installing a newer version from the update prompt could leave OrcaSlicer unable to find the plugin on the next launch, so it kept asking you to reinstall it. That's fixed, so a plugin you install now stays installed. Fixes #14373 and #14441.

* **Fix "plug-in file may be in use" when switching plugin versions on Windows** by @ExPikaPaka in [14528]({{L13}})
    On Windows, changing or reinstalling the Bambu network plugin while OrcaSlicer was running could fail with "The plug-in file may be in use," leaving networking broken until you restarted. The installer now works around the file being in use, so the new plugin installs successfully without a restart. Reported in #14373.

## Slicing & G-code

* **Fix slicing failure when filament end G-code uses `{layer_z}` with a prime tower** by @raistlin7447 in [14462]({{L14}})
    If your filament's end G-code used `{layer_z}` — for example, a Z-lift to clear the print — slicing could fail on multi-filament prints that use the prime tower, such as a print with a separate support filament. `{layer_z}` now has a value in that situation, so slicing completes and the command runs at each filament change as expected. Fixes #10119.

* **Fix an inaccurate print-time estimate** by @SoftFever in [14573]({{L15}})
    Corrects a mistake in how the print time was calculated, so the estimated print time OrcaSlicer shows is more accurate. Supersedes #14525.

## Crashes

* **Fix crash when rotating the prime tower** by @raistlin7447 in [14499]({{L16}})
    Selecting the prime tower and rotating it with PageUp/PageDown could crash OrcaSlicer. Rotating, scaling, and mirroring the prime tower are now handled safely. Fixes #14498.

* **Fix crash in the Measure tool** by @raistlin7447 in [14538]({{L17}})
    Using the Measure tool could crash if you picked a straight edge first and then selected a second feature. That case is now handled, so measuring from a straight edge works. Fixes #14018.

* **Fix crash in Pressure Advance pattern calibration** by @raistlin7447 in [14447]({{L18}})
    Running a Pressure Advance pattern calibration could crash OrcaSlicer if the first layer line width was set to 0 (which means "use the default"). A width of 0 now correctly falls back to the automatic default, so the calibration slices normally. Fixes #13188.

## Models & project

* **Fix Reload from Disk for STEP models after reopening a project** by @SoftFever in [14591]({{L19}})
    After you saved a project and reopened it, Reload from Disk stopped working for models imported from STEP files — it failed with "Error during reload," and kept asking you to locate the file if the STEP wasn't stored next to the project (a problem since 2.3.2). Reload now finds the file by name as well as by its saved path, so it can pick up the model next to the project (or the one you point it to) and update it in place. A new "export full source paths" option in Preferences helps when you keep the STEP file and the project in different folders. Fixes #12992.

    {{I3}}

# 🖨️ Printer & Filament Profiles

* **add:north filaments** — adds ready-made profiles for add:north filaments to the Orca Filament Library by @valerii-bokhan in [13366]({{L20}})

    {{I4}}

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
  <a href="{{L21}}">{{I5}}</a>
</p>
<p align="center">
  <a href="{{L22}}">{{I6}}</a>
</p>
