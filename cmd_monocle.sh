
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
-i seurat.h5seurat  \
-f h5seurat \
--assay RNA \
-o ./monocle/ \
-j 8 \
--predicate   "new_celltype %in% c(\'B_cells\',\'T_cells\')" \
--update FALSE \
monocle \
-d new_celltype \
-x 0.01 \
-r 0.4 \
-C clusters,sampleid,group \
-s 1
