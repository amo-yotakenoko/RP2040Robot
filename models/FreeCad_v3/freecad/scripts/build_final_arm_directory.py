"""Build the clean final Arm directory.

Inputs: arm_external/*.FCStd and sg90.FCStd; arm_v4.FCStd is read-only.
Outputs: Arm/<part>.FCStd and Arm/ArmUnit.FCStd.
Each part keeps one primary PartDesign Body; external Binder links are
reconnected to clean component files. Units: mm.
"""
import FreeCAD as App
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT = os.path.join(ROOT, "arm_external")
FINAL = os.path.join(ROOT, "Arm")
os.makedirs(FINAL, exist_ok=True)

PARTS = [
    ("ServoHorn_Master_Single", "Body003"),
    ("Base", "Body006"),
    ("ServoHorn_Master_Cross", "Body007"),
    ("UpperArm", "Body"),
    ("LowerArm", "Body008"),
    ("Roll", "Body009"),
]

old = {}
for name, _ in PARTS:
    old[name] = App.openDocument(os.path.join(INPUT, name + ".FCStd"), False)
sg90 = App.openDocument(os.path.join(ROOT, "sg90.FCStd"), False)

def ext(doc, name, subs):
    obj = doc.getObject(name)
    if obj is None:
        raise RuntimeError("Missing object %s in %s" % (name, doc.FileName))
    return (obj, tuple(subs))

def set_binder(doc, name, supports):
    obj = doc.getObject(name)
    if obj is not None:
        obj.Support = supports

def relink(doc, sources):
    single, cross, upper = sources
    for n in ("Binder", "Binder001", "Binder012", "Binder013", "Binder020"):
        set_binder(doc, n, [ext(single, "Pad001", ("",))])
    set_binder(doc, "Binder009", [ext(cross, "Pad002", ("",))])
    set_binder(doc, "Binder003", [ext(sg90, "PolarPattern", ("PolarPattern.Face18",))])
    if doc.Label == "UpperArm":
        set_binder(doc, "Binder005", [ext(sg90, "PolarPattern", ("PolarPattern",))])
        set_binder(doc, "Binder016", [ext(sg90, "PolarPattern", ("PolarPattern.Face9", "PolarPattern.Face10"))])
    if doc.Label == "LowerArm":
        set_binder(doc, "Binder007", [ext(sg90, "PolarPattern", ("PolarPattern.Face19",)), ext(upper, "Mirrored", ("",))])
        set_binder(doc, "Binder008", [ext(sg90, "PolarPattern", ("PolarPattern.Face9", "PolarPattern.Face13"))])
        set_binder(doc, "Binder010", [ext(sg90, "PolarPattern", ("PolarPattern.Face11",))])
        set_binder(doc, "Binder011", [ext(sg90, "PolarPattern", ("PolarPattern.Face68",))])
        set_binder(doc, "Binder017", [ext(upper, "Mirrored", ("Mirrored.Face71",))])
        set_binder(doc, "Binder018", [ext(sg90, "PolarPattern", ("PolarPattern.Face11",))])
        set_binder(doc, "Binder019", [ext(sg90, "PolarPattern", ("PolarPattern.Face13", "PolarPattern.Face9"))])
    if doc.Label == "Roll":
        set_binder(doc, "Binder021", [ext(sg90, "PolarPattern", ("PolarPattern.Face9", "PolarPattern.Face13", "PolarPattern.Face12", "PolarPattern.Face10"))])

def clean_part(name, body_name):
    source = old[name]
    path = os.path.join(FINAL, name + ".FCStd")
    if os.path.exists(path):
        raise RuntimeError("Refusing to overwrite " + path)
    source.saveAs(path)
    # Relink against the existing, validated component documents before deleting
    # copied dependency objects from this document.
    relink(source, (old["ServoHorn_Master_Single"], old["ServoHorn_Master_Cross"], old["UpperArm"]))
    source.recompute()
    body = source.getObject(body_name)
    if body is None:
        raise RuntimeError("Missing primary body " + body_name)
    keep = {body.Name}
    for child in body.Group:
        keep.add(child.Name)
    origin = getattr(body, "Origin", None)
    if origin:
        keep.add(origin.Name)
        for child in getattr(origin, "OriginFeatures", []):
            keep.add(child.Name)
    for obj in list(source.Objects):
        if obj.Name not in keep:
            source.removeObject(obj.Name)
    source.recompute()
    source.save()
    return source

clean = {}
for name, body_name in PARTS:
    clean[name] = clean_part(name, body_name)

# Reopen the clean files and reconnect links to the clean files, not arm_external.
for doc in list(clean.values()):
    App.closeDocument(doc.Name)
clean = {name: App.openDocument(os.path.join(FINAL, name + ".FCStd"), False) for name, _ in PARTS}
for name, _ in PARTS:
    relink(clean[name], (clean["ServoHorn_Master_Single"], clean["ServoHorn_Master_Cross"], clean["UpperArm"]))
    clean[name].recompute()
    clean[name].save()

# Native FreeCAD 1.1 Assembly containing only the six actual arm components.
source = App.openDocument(os.path.join(ROOT, "arm_v4.FCStd"), False)
assembly_doc = App.newDocument("ArmUnit")
assembly_doc.saveAs(os.path.join(FINAL, "ArmUnit.FCStd"))
assembly = assembly_doc.addObject("Assembly::AssemblyObject", "Assembly")
assembly.Label = "ArmUnit"
assembly.Type = "Assembly"
assembly.newObject("Assembly::JointGroup", "Joints").Label = "Joints (to be defined)"
for name, body_name in PARTS:
    link = assembly.newObject("App::Link", name + "_Link")
    link.Label = name
    link.LinkedObject = clean[name].getObject(body_name)
    link.Placement = source.getObject(body_name).Placement
assembly_doc.recompute()
assembly_doc.save()
print("FINAL", FINAL, "PARTS", len(PARTS), "ASSEMBLY", os.path.join(FINAL, "ArmUnit.FCStd"))
