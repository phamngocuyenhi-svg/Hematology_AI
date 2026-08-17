"""
EDA so bo cho 2 bo du lieu dang anh: MDS Bone Marrow va TXL-PBC.
Chay: python eda_images.py
Output: in ra console + luu report txt vao Data/eda/report_images.txt
"""
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent
OUT = []
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp"}

def log(msg=""):
    print(msg)
    OUT.append(str(msg))

def section(title):
    log("\n" + "=" * 70)
    log(title)
    log("=" * 70)

# ---------- 1. MDS Bone Marrow ----------
section("1) MDS BONE MARROW DATASET (images/mds_bone_marrow/extracted)")
mds_root = BASE / "images" / "mds_bone_marrow" / "extracted"
class_counts = {}
for sub in sorted(mds_root.rglob("*")):
    if sub.is_dir():
        n = sum(1 for f in sub.iterdir() if f.is_file() and f.suffix.lower() in IMG_EXT)
        if n > 0:
            class_counts[str(sub.relative_to(mds_root))] = n

total = sum(class_counts.values())
log(f"Tong so anh: {total}")
log(f"Tong so lop (co anh): {len(class_counts)}")
log("\nSo anh theo tung lop (sap xep giam dan):")
for cls, n in sorted(class_counts.items(), key=lambda x: -x[1]):
    log(f"  {cls:45s}: {n:6d}  ({n/total*100:5.2f}%)")

if class_counts:
    vals = list(class_counts.values())
    log(f"\nLop nhieu anh nhat: {max(class_counts, key=class_counts.get)} ({max(vals)} anh)")
    log(f"Lop it anh nhat:    {min(class_counts, key=class_counts.get)} ({min(vals)} anh)")
    log(f"Ty le mat can bang (max/min): {max(vals)/min(vals):.1f}x")

log("\n>> Nhan xet: can kiem tra ky cac lop <100 anh - qua it de train rieng, nen gop nhom hoac dung few-shot/augmentation.")

# ---------- 2. TXL-PBC ----------
section("2) TXL-PBC DATASET (images/txl_pbc_repo/TXL-PBC)")
txl_root = BASE / "images" / "txl_pbc_repo" / "TXL-PBC"

for split in ["train", "val", "test"]:
    img_dir = txl_root / "images" / split
    lbl_dir = txl_root / "labels" / split
    if not img_dir.exists():
        continue
    n_img = sum(1 for f in img_dir.iterdir() if f.is_file() and f.suffix.lower() in IMG_EXT)
    log(f"\n-- Split '{split}': {n_img} anh --")

    class_id_counter = Counter()
    n_boxes = 0
    if lbl_dir.exists():
        for lbl_file in lbl_dir.glob("*.txt"):
            lines = [l for l in lbl_file.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
            n_boxes += len(lines)
            for line in lines:
                cls_id = line.split()[0]
                class_id_counter[cls_id] += 1
    log(f"   Tong so bounding box: {n_boxes}")
    log(f"   Phan bo theo class_id (YOLO format): {dict(sorted(class_id_counter.items()))}")

classes_file = txl_root / "classes.txt"
if classes_file.exists():
    log(f"\nTen cac lop (classes.txt): {classes_file.read_text(encoding='utf-8', errors='ignore').splitlines()}")
else:
    log("\n(Khong tim thay classes.txt - can xem data.yaml de biet ten lop ung voi class_id)")

data_yaml = txl_root / "data.yaml"
if data_yaml.exists():
    log(f"\nNoi dung data.yaml:\n{data_yaml.read_text(encoding='utf-8', errors='ignore')}")

log("\n>> Nhan xet: day la bai toan OBJECT DETECTION (bounding box), khong phai classification.")
log(">> Chi co 3 lop (WBC/RBC/Platelet) - muon phan loai further (neutrophil/eosinophil...) phai dung nguon khac (vd Raabin, PBC Barcelona).")

# ---------- Save report ----------
report_path = BASE / "eda" / "report_images.txt"
report_path.write_text("\n".join(OUT), encoding="utf-8")
log(f"\n\nDa luu report vao: {report_path}")
