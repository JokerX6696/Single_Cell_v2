set -e 
Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \
-i /gpfs/oe-scrna/zhengfuxing/Project/scRNA/DZOE2023120213_Mouse/20240227/4.GSVA/GSVA_GO_BP/GSVA_enrichment_results.xls \
-v rds/data_ob_v3.rds \
-c clusters:all:all \
-p 0.05 \
-n 10 \
-d TRUE \
-o ./GSVA_GO_BP_clusters_all_all \
--cell_heatmap False

Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \
-i /gpfs/oe-scrna/zhengfuxing/Project/scRNA/DZOE2023120213_Mouse/20240227/4.GSVA/GSVA_KEGG/GSVA_enrichment_results.xls \
-v rds/data_ob_v3.rds \
-c clusters:all:all \
-p 0.05 \
-n 10 \
-d TRUE \
-o ./GSVA_KEGG_clusters_all_all \
--cell_heatmap False

