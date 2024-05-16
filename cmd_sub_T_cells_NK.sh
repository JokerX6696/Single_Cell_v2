set -e
module purge && module load OESingleCell/3.0.d
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \
-i  seurat.h5seurat  \
-f h5seurat  \
-o sub_T_cells_NK/Clustering  \
-d h5seurat   \
--assay RNA  \
--dataslot counts,data,scale.data   \
--update F   \
--predicate  "new_celltype %in% c(\'T_cells\',\'NK\')"   \
bclust   \
--reduct1 pca  \
--reduct2 umap   \
--clusteringuse snn  \
--resolution 0.4   \
--rerun T   \
--pointsize  0.5  \
--palette customecol2


Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
-i sub_T_cells_NK/Clustering/seurat.h5seurat \
-f h5seurat \
-o sub_T_cells_NK/Clustering \
--assay RNA \
--dataslot data \
summarize \
--reduct umap \
--palette customecol2 \
-c clusters \
-b sampleid,group \
--pointsize 0.5 \
--dosummary T


Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \
-i sub_T_cells_NK/Clustering/seurat.h5seurat  \
-f h5seurat \
-o sub_T_cells_NK/Clustering/clusters_correlation \
-t 6 \
--assay RNA \
--slot data \
--reduct umap \
coefficient \
-g clusters

Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
-i sub_T_cells_NK/Clustering/seurat.h5seurat  \
-f h5seurat \
-o sub_T_cells_NK/Marker \
--assay RNA \
--dataslot data,counts \
-j 10 \
findallmarkers \
-c 2 \
-N 10 \
-k 1 \
-p 0.05 \
-s F \
-e presto \
-n clusters


#2.可视化+anno
# marker热图
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \
-i sub_T_cells_NK/Clustering/seurat.h5seurat  \
-f h5seurat \
-o sub_T_cells_NK/Marker \
-t 10 \
--assay RNA \
--slot data,scale.data \
heatmap \
-l sub_T_cells_NK/Marker/top10_markers_for_each_cluster.xls \
-c gene_diff \
-n 10 \
-g clusters \
--group_colors customecol2 \
--sample_ratio 0.8 \
--style seurat

Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
-i sub_T_cells_NK/Clustering/seurat.h5seurat   \
-f h5seurat \
-o sub_T_cells_NK/Marker \
-j 10 \
--assay RNA \
--dataslot data \
visualize \
-l sub_T_cells_NK/Marker/top10_markers_for_each_cluster.xls \
-g clusters \
--reduct umap \
--topn  10  \
--topby gene_diff \
-m vlnplot,featureplot \
--vcolors customecol2 \
--ccolors spectral \
--pointsize 0.3 \
--dodge F

anno=/data/database/cellranger-refdata/refdata-gex-mm10-2020-A/annotation/gene_annotation.xls
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \
-g sub_T_cells_NK/Marker/all_markers_for_each_cluster.xls \
--anno $anno  # 根据物种修改
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \
-g sub_T_cells_NK/Marker/top10_markers_for_each_cluster.xls \
--anno $anno  # 根据物种修改


Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \
-i sub_T_cells_NK/Clustering/seurat.h5seurat  \
-f h5seurat \
-o sub_T_cells_NK/Reference_celltype \
-d h5seurat \
--update T \
--assay RNA \
--dataslot counts \
celltyping \
-r /data/database/celltype_refdata/logNorm_rds/immgen.rds \
--annolevel single \
--usecluster F \
--demethod classic \
--pointsize 0.3 \
-n 25 \
--reduct umap \
--species mouse

