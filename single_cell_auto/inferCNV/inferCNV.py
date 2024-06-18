# -*- coding: utf-8 -*-
def inferCNV_run(obj):
    out = obj.out
    seurat = obj.sub_clusters.seurat
    reduct1 = obj.sub_clusters.reduct1
    reduct2 = obj.sub_clusters.reduct2
    batchid = obj.sub_clusters.batchid
    resolution = obj.sub_clusters.resolution
    col_name = obj.sub_clusters.col_name
    cells = obj.sub_clusters.cells
    species = obj.sub_clusters.species
    assay = obj.sub_clusters.assay
    if species == 'human':
        anno = '/data/database/cellranger-refdata/refdata-gex-GRCh38-2020-A/annotation/gene_annotation.xls'
        sjj = '/data/database/celltype_refdata/logNorm_rds/hpca.rds'
    elif species == 'mouse':
        anno = '/data/database/cellranger-refdata/refdata-gex-mm10-2020-A/annotation/gene_annotation.xls'
        sjj = '/data/database/celltype_refdata/logNorm_rds/immgen.rds'
    else:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!! 非常见物种, 请在生成的脚本文件中 105 左右 行手动填写 marker gene 注释文件!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        anno = 'unknow'
        sjj = 'unknow'
# Rscript /home/luyao/10X_scRNAseq_v3/src/CNV/infercnv.R \\
# -i singlecell_object.clustering_resolution0.4.rds \\
# -f seurat \\
# -l celltype \\
# -r "type1,type2" \\
# -z genes.gtf \\
# -o ./

# Rscript /home/luyao/10X_scRNAseq_v3/src/CNV/infercnv_vis.R \\
# -i singlecell_object.clustering_resolution0.4.rds \\
# -f  seurat \\
# -l ./ -g cnv_group,new_celltype,clusters,sampleid,group  \\
# -p all \\
# --reduct umap \\
# -y sampleid,group \\
# --hmm F
