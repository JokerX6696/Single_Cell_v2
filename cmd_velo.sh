set -e
module load git \
module load ./dev_fangying \
sctool -i seurat.h5seurat -f h5seurat --assay RNA -j 10 -o ././output  pyscvelo --loom_dir yourloomdir --groupby clusters,new_celltype --reduction umap

