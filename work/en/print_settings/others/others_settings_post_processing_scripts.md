# Post-Processing Scripts

{{M1}}
Here you can set up post-processing scripts that run on the generated G-code.  
For Bambu Lab printers, they run right after slicing, so the preview shows the processed G-code. For other printers, they run only when a G-code file is exported or sent to a network printer with **Print** or **Send**, so the preview and sliced 3MF files keep the unprocessed G-code.  
This allows you to modify the G-code output or perform additional tasks.

Check the script's documentation for dependencies, available parameters and usage instructions.

Example Python script:

{{C1}}
