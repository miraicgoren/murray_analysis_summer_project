#!/bin/bash

# Set base input/output paths
base_dir=~/Desktop/TopCoW2024_Data_Release
input_dir="${base_dir}/cow_seg_labelsTr"
output_root="${input_dir}/bifurcation_masks"
vtk_root="${output_root}/vtk_surfaces"
mkdir -p "$output_root"
mkdir -p "$vtk_root"

# Subject ID ranges: 001–090 and 131–165
ids=($(seq -f "%03g" 1 90) $(seq -f "%03g" 131 165))
modalities=("ct" "mr")

for modality in "${modalities[@]}"; do
  for id in "${ids[@]}"; do

    filename="topcow_${modality}_${id}.nii.gz"
    filepath="${input_dir}/${filename}"

    if [ ! -f "$filepath" ]; then
      echo "[SKIP] Missing file: $filepath"
      continue
    fi

    name_no_ext="${filename%.nii.gz}"
    outdir="${output_root}/${name_no_ext}"
    mkdir -p "$outdir"

    echo "🔄 Processing $filename"

    # Right ICA bifurcation mask (labels 4,5,11)
    fslmaths "$filepath" -thr 4 -uthr 4 -bin "$outdir/temp_4.nii.gz"
    fslmaths "$filepath" -thr 5 -uthr 5 -bin "$outdir/temp_5.nii.gz"
    fslmaths "$filepath" -thr 11 -uthr 11 -bin "$outdir/temp_11.nii.gz"
    fslmaths "$outdir/temp_4.nii.gz" -add "$outdir/temp_5.nii.gz" "$outdir/temp_R.nii.gz"
    fslmaths "$outdir/temp_R.nii.gz" -add "$outdir/temp_11.nii.gz" "$outdir/mask_R_ICAbif.nii.gz"

    # Left ICA bifurcation mask (labels 6,7,12)
    fslmaths "$filepath" -thr 6 -uthr 6 -bin "$outdir/temp_6.nii.gz"
    fslmaths "$filepath" -thr 7 -uthr 7 -bin "$outdir/temp_7.nii.gz"
    fslmaths "$filepath" -thr 12 -uthr 12 -bin "$outdir/temp_12.nii.gz"
    fslmaths "$outdir/temp_6.nii.gz" -add "$outdir/temp_7.nii.gz" "$outdir/temp_L.nii.gz"
    fslmaths "$outdir/temp_L.nii.gz" -add "$outdir/temp_12.nii.gz" "$outdir/mask_L_ICAbif.nii.gz"

    rm "$outdir"/temp_*.nii.gz

    # Build Python script for headless Slicer export
    py_script="${outdir}/export_to_vtk.py"
    echo "import slicer, slicer.util, vtk" > "$py_script"

    for side in R L; do
      mask_path="$outdir/mask_${side}_ICAbif.nii.gz"
      vtk_outdir="${vtk_root}/${name_no_ext}"
      mkdir -p "$vtk_outdir"
      out_path="${vtk_outdir}/${name_no_ext}_${side}_bif.vtk"

      cat >> "$py_script" <<EOF

label_node = slicer.util.loadLabelVolume("${mask_path}", returnNode=True)[1]
seg_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", "BifSeg_${side}")
slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(label_node, seg_node)
slicer.app.processEvents()
seg_node.CreateClosedSurfaceRepresentation()
segmentation = seg_node.GetSegmentation()
segment_id = segmentation.GetNthSegmentID(0)
polydata = segmentation.GetSegmentRepresentation(segment_id, slicer.vtkSegmentationConverter.GetSegmentationClosedSurfaceRepresentationName())
model_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "Model_${side}")
model_node.SetAndObservePolyData(polydata)
model_node.CreateDefaultDisplayNodes()
model_node.Modified()
slicer.util.saveNode(model_node, "${out_path}")
print("✅ Exported: ${out_path}")
EOF

    done

    # Run Slicer headlessly
    /Applications/Slicer.app/Contents/MacOS/Slicer --no-main-window --python-script "$py_script" --exit-after-startup

    # Cleanup
    rm "$py_script"
  done
done

echo "✅ All bifurcation masks and surface models exported to: $vtk_root"
