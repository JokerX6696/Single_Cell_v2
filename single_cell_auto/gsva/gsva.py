def gsva_run(obj):
    out = obj.out


    print(out)
    with open(f"{out}/cmd_gsva.sh", 'w')as f:
        f.write(
"""
set -e
module purge && module load OESingleCell/2.0.0
Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_enrich.R \
-i $rds \
-f seurat   \
-g $go_bp  \
-o  ./GSVA_GO_BP  \
-c  $num  \
-k Poisson \
-a  FALSE  \
-s 2  \
-S 10000  \
-j 4 \
-x  TRUE &

Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_enrich.R \
-i $rds \
-f seurat   \
-g $kegg  \
-o  ./GSVA_KEGG  \
-c  $num  \
-k Poisson \
-a  FALSE  \
-s 2  \
-S 10000  \
-j 4 \
-x  TRUE &

Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_enrich.R \
-i $rds \
-f seurat   \
-g $kegg  \
-o  ./GSVA_Hallmakr  \
-c  $num  \
-k Poisson \
-a  FALSE  \
-s 2  \
-S 10000  \
-j 4 \
-x  TRUE &

wait
# 2
Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \
-i ./GSVA_GO_BP/GSVA_enrichment_results.xls \
-v $rds \
-c $group \
-p 0.05 \
-n 10 \
-d TRUE \
-o ./GSVA_GO_BP

Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \
-i ./GSVA_KEGG/GSVA_enrichment_results.xls \
-v $rds \
-c $group \
-p 0.05 \
-n 10 \
-d TRUE \
-o ./GSVA_KEGG
"""
)
        