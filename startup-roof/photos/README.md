# Photo slots

Put licensed photos in this folder using the filenames below, then rebuild. Each photo is cropped to fill its slot automatically. When a file is missing, the vector illustration is used instead.

| Filename | Used in | Suggested subject | Minimum size |
|---|---|---|---|
| `community.jpg` | Full deck: "Founders do better together" (right half). Full brochure: community and mentoring page (banner). | A small group of founders working or talking around a table, natural light | 1600 × 1800 px |
| `dubai.jpg` | Full deck: "Rooted in the UAE. Built to travel." (right half). Full brochure: UAE context page (banner). | A restrained Dubai skyline or business-district street scene, not a real-estate advert | 2400 × 1200 px |
| `learning.jpg` | Full deck: "Learn it on Monday. Use it on Tuesday." (right half) | A workshop or learning session with a facilitator and participants | 1600 × 1800 px |

`.jpg`, `.jpeg`, `.png` and `.webp` are all accepted.

## Rebuild

```bash
cd startup-roof
python3 src/build_full.py deliverables/Startup_Roof_Full_Presentation.pptx
soffice --headless --convert-to pdf --outdir deliverables deliverables/Startup_Roof_Full_Presentation.pptx
python3 src/build_brochure_full.py deliverables/Startup_Roof_Full_Brochure.pdf
```

Use only photos you have the rights to. Don't use images of identifiable participants unless they have agreed.
