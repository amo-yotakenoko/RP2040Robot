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
