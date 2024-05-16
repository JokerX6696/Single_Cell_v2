def sub_clusters_run(obj):
    import os
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
        sjj='/data/database/celltype_refdata/logNorm_rds/hpca.rds'
    elif species == 'mouse':
        anno='/data/database/cellranger-refdata/refdata-gex-mm10-2020-A/annotation/gene_annotation.xls'
        sjj='/data/database/celltype_refdata/logNorm_rds/immgen.rds'
    else:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!! 非常见物种, 请在生成的脚本文件中手动填写 marker genen 注释文件!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        anno = 'unknow'
    # 处理 cell
    for j in cells:
        if type(j) == list:
            str_list = [str(k) for k in j]
            cell_name = "_".join(str_list)
            cell_type = ",".join(["\\'" + k + "\\'" for k in str_list])
        elif type(j) == str:
            cell_name = str(j)
            cell_type = "\\'" + str(j) + "\\'"
        else:
            exit("config.yaml 文件中 sub_clusters cells 填写格式错误 请查看注释信息！")

        with open(f'{out}/cmd_sub_{cell_name}.sh',"w") as f:
            f.write(f"""set -e\nmodule purge && module load OESingleCell/3.0.d\n""")
            if reduct1 == 'pca':
                f.write(f"""Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i  {seurat}  \\
-f h5seurat  \\
-o sub_{cell_name}/Clustering  \\
-d h5seurat   \\
--assay {assay}  \\
--dataslot counts,data,scale.data   \\
--update F   \\
--predicate  "{col_name} %in% c({cell_type})"   \\
bclust   \\
--reduct1 {reduct1}  \\
--reduct2 {reduct2}   \\
--clusteringuse snn  \\
--resolution {resolution}   \\
--rerun T   \\
--pointsize  0.5  \\
--palette customecol2

""")
            elif reduct2 == 'mnn':
                f.write(f"""Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i  {seurat}  \\
-f h5seurat  \\
-o sub_{cell_name}/Clustering  \\
-d h5seurat   \\
--assay {assay}  \\
--dataslot counts,data,scale.data   \\
--update F   \\
--predicate  "{col_name} %in% c({cell_type})"   \\
bclust   \\
--reduct1 {reduct1} \\
--batchid {batchid} \\
--components 10  \\
--reduct2 {reduct2} \\
--clusteringuse snn  \\
--resolution {resolution}   \\
--rerun T   \\
--pointsize  0.5   \\
--palette customecol2

""")
            elif reduct2 == 'harmony':
                f.write(f"""Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
  -i {seurat}  \
  -f h5seurat  \
  -o sub_{cell_name}/Clustering  \
  -d h5seurat   \
  --assay {assay}  \
  --dataslot counts,data,scale.data  \
  --update F \
  --predicate  "{col_name} %in% c({cell_type})"  \
  bclust   \
  --reduct1 "pca,harmony"  \
  --reduct2 {reduct2}  \
  --batchid {batchid}  \
  --clusteringuse snn  \
  --resolution {resolution}  \
  --rerun T \
  -t 20 \
  -y 30 \
  --pointsize  0.5   \
  --palette customecol2

""")
            else:
                exit("reduct type error")
            seurat_sub=f"sub_{cell_name}/Clustering/seurat.h5seurat"
            f.write(f"""
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
-i {seurat_sub} \\
-f h5seurat \\
-o sub_{cell_name}/Clustering \\
--assay {assay} \\
--dataslot data \\
summarize \\
--reduct {reduct2} \\
--palette customecol2 \\
-c clusters \\
-b sampleid,group \\
--pointsize 0.5 \\
--dosummary T


Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
-i {seurat_sub}  \\
-f h5seurat \\
-o sub_{cell_name}/Clustering/clusters_correlation \\
-t 6 \\
--assay {assay} \\
--slot data \\
--reduct {reduct2} \\
coefficient \\
-g clusters

Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
-i {seurat_sub}  \\
-f h5seurat \\
-o sub_{cell_name}/Marker \\
--assay {assay} \\
--dataslot data,counts \\
-j 10 \\
findallmarkers \\
-c 2 \\
-N 10 \\
-k 1 \\
-p 0.05 \\
-s F \\
-e presto \\
-n clusters


#2.可视化+anno
# marker热图
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
-i {seurat_sub}  \\
-f h5seurat \\
-o sub_{cell_name}/Marker \\
-t 10 \\
--assay {assay} \\
--slot data,scale.data \\
heatmap \\
-l sub_{cell_name}/Marker/top10_markers_for_each_cluster.xls \\
-c gene_diff \\
-n 10 \\
-g clusters \\
--group_colors customecol2 \\
--sample_ratio 0.8 \\
--style seurat

Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
-i {seurat_sub}   \\
-f h5seurat \\
-o sub_{cell_name}/Marker \\
-j 10 \\
--assay {assay} \\
--dataslot data \\
visualize \\
-l sub_{cell_name}/Marker/top10_markers_for_each_cluster.xls \\
-g clusters \\
--reduct umap \\
--topn  10  \\
--topby gene_diff \\
-m vlnplot,featureplot \\
--vcolors customecol2 \\
--ccolors spectral \\
--pointsize 0.3 \\
--dodge F

anno={anno}
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \\
-g sub_{cell_name}/Marker/all_markers_for_each_cluster.xls \\
--anno $anno  # 根据物种修改
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \\
-g sub_{cell_name}/Marker/top10_markers_for_each_cluster.xls \\
--anno $anno  # 根据物种修改


Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i {seurat_sub}  \\
-f h5seurat \\
-o sub_{cell_name}/Reference_celltype \\
-d h5seurat \\
--update T \\
--assay {assay} \\
--dataslot counts \\
celltyping \\
-r {sjj} \\
--annolevel single \\
--usecluster F \\
--demethod classic \\
--pointsize 0.3 \\
-n 25 \\
--reduct {reduct2} \\
--species {species}

""")


