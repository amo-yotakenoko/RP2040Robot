# Current FreeCAD document context

## Source

- File: `arm_v4.FCStd`
- FreeCAD: 1.1.3R20260725
- Units: mm
- Source was opened read-only and was not saved or overwritten.

## Body inventory

| Source object | Label | Final volume (mm3) |
|---|---|---:|
| `Body003` | `ServoHorn_Master_Single` | 495.472719325 |
| `Body006` | `ベース` | 3163.260675250 |
| `Body007` | `ServoHorn_Master_Cross` | 885.146328392 |
| `Body` | `上腕` | 3138.471993844 |
| `Body008` | `下腕` | 3360.666766188 |
| `Body009` | `ロール` | 1727.312424861 |
| `Body010` | `Body010` | 1727.312424861 |

## Split attempt

`freecad/scripts/split_arm_v4.py` generated `arm_parts/*.FCStd`. Final Body volume and bounding box matched the source for all seven outputs.

However, FreeCAD reported missing `Binder`/external sketch references while opening or recomputing several outputs. The files are therefore not accepted as error-free parametric parts. `ArmUnit.FCStd` was intentionally not created.

The source document remains the authoritative model. The next repair step must replace or reconstruct cross-Body `Binder`/`Boolean` dependencies before creating the Assembly.

## External Binder experiment

## Accepted external-link result

`freecad/scripts/relink_parts_to_external_sources.py` created `arm_external/*.FCStd` by reconnecting Binders to the real saved component files and `sg90.FCStd`. On reopen, all seven Body volumes matched the source within `4e-10 mm3`, all external geometry entries resolved, and no FreeCAD Object State errors were reported.

`freecad/scripts/create_armunit_assembly.py` created `arm_external/ArmUnit.FCStd` as a native `Assembly::AssemblyObject` with seven external component links and a `Joints` group. The Base link is marked grounded; motion joints still need to be defined from the robot's intended axes.

## Final directory

`freecad/scripts/build_final_arm_directory.py` created `Arm/` with six clean component files and `Arm/ArmUnit.FCStd`. Each component contains exactly one `PartDesign::Body`; `Body010` was omitted because it duplicates `Roll`. Reopen validation found no broken external geometry and no bad Object State entries. The final Assembly contains six external component links and a native `Assembly::JointGroup`.

`freecad/scripts/fix_final_visibility.py` normalized display state: each component shows only its primary final Body and ArmUnit shows its component links. Geometry and external-link validation remain unchanged.

Intermediate directories and rejected probe files were removed. The maintained output is now only `Arm/`; retained scripts are `build_final_arm_directory.py`, `fix_final_visibility.py`, and `validate_final_arm_directory.py`.

`freecad/scripts/add_sg90_to_armunit.py` added six external SG90 links to `Arm/ArmUnit.FCStd`, using the original `arm_v4.FCStd` Link placements. ArmUnit now contains 12 component links: six arm parts and six SG90 instances.

Visibility audit: every component primary Body and Tip is visible; ArmUnit root and all 12 component links are visible. Hidden objects are only expected construction/history items (sketches, axes, planes, origins, and Binders). The visual-only ArmSkeleton file and its associated experiment outputs were removed because they were not dependencies of the final model.

Shared/reference models were moved to `Reference/`: `ServoHorn_Master_Single.FCStd`, `ServoHorn_Master_Cross.FCStd`, `sg90.FCStd`, `asv-15-a.FCStd`, `ssd1306.FCStd`, and `camera.FCStd`. Links in `ArmUnit`, Arm parts, `arm_v4`, `main`, `HeadUnit`, and `Head_base` were redirected before the original locations were removed.

`arm_v4.FCStd` and all `arm_v4*.FCBak` files were subsequently removed. The maintained model is now `Arm/` plus `Reference/`.

After the Reference move, the Assembly parent visibility was found false even though its 12 child links were true. `fix_final_visibility.py` was corrected to set the Assembly root visible; a reopen audit now reports Assembly root true, all 12 links true, and all component Body/Tip pairs true.

The omitted original Roll mirror was restored as `Arm/Roll_Mirrored.FCStd`, mirrored across X=0, and added to `ArmUnit` as `Roll_Mirrored_Link` with the Roll mounting placement. Its reopened shape is one solid with bounding box X=-17..15.4, matching the expected mirrored Roll envelope.

The Roll mirror was then converted from a baked file into a normal `App::Link` to `Arm/Roll.FCStd#Body009` with `ScaleVector=(-1,1,1)` and X=0 mirror placement; no update script is required when Roll changes. A trial six-joint setup was rejected because its guessed part-to-motor topology allowed the solver to change the original poses. The trial joints were removed and the pre-joint pose restored. A second trial using direct whole-link references still caused the native solver to reposition the Roll mirror and other links; it was not saved. Assembly joints require explicit connector/JCS geometry and correct rigid/flexible topology before re-adding them.

## Arm file and label rename (2026-11-26)

`freecad/scripts/rename_arm_files_and_verify.py` was executed with FreeCAD
1.1.3. Component files and display labels are now `BaseYaw`, `UpperArm`,
`Forearm`, and `WristRoll`; the mirrored Roll link is labeled `WristPitch`.
ArmUnit external links were updated to the new filenames. After saving, all
component primary Bodies and Tips, the ArmUnit Assembly root, and all five arm
links were reopened and verified visible and linked.

The `WristPitch` mirrored link initially retained the old `Roll.FCStd` path.
`freecad/scripts/repair_armunit_mirrored_link.py` reconnected it to
`WristRoll.FCStd#Body009` while preserving its mirror scale and placement.
ArmUnit was reopened again; all five links now resolve and are visible.

Because headless FreeCADCmd did not persist GUI view-provider state, the
GUI-enabled `freecad/scripts/force_arm_visibility.py` was then run. It saved a
`GuiDocument.xml` with `Assembly` and all five links visible. The file was
reopened and the persisted GUI visibility flags were verified as true.
## Label rename (2026-11-26)

`freecad/scripts/rename_arm_link_labels.py` was executed with FreeCAD 1.1.3.
Only display labels were changed; internal object names, geometry, placements,
and dimensions were preserved.

| Existing part/link | New label |
|---|---|
| Base / `Base_Link` | `Link1_BaseYaw` |
| UpperArm / `UpperArm_Link` | `Link2_UpperArm` |
| LowerArm / `LowerArm_Link` | `Link3_Forearm` |
| Roll / `Roll_Link` | `Link4_WristRoll` |
| `Roll_Mirrored_Link` (Roll2) | `Link5_WristPitch` |
