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
    # 处理 cell
    for j in cells:
        if type(j) == list:
            str_list = [str(k) for k in j]
            cell_name = "_".join(str_list)
            cell_type = ",".join(["\\'" + k + "\\'" for k in str_list])
        elif type(j) == str:
            cell_name = str(j)
            cell_type = "\\'" + str(j) + "\\'"


        with open(f'{out}/cmd_sub_{cell_name}.sh',"w") as f:
            f.write(f"""set -e\nmodule purge && module load OESingleCell/3.0.d\n""")
            if reduct1 == 'pca':
                f.write(f"""Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i  {seurat}  \\
-f h5seurat  \\
-o sub_{cell_name}/Clustering  \\
-d h5seurat   \\
--assay $assay  \\
--dataslot counts,data,scale.data   \\
--update F   \\
--predicate  "{col_name} %in% c({cell_type})"   \\
bclust   \\
--reduct1 pca  \\
--reduct2 umap   \\
--clusteringuse snn  \\
--resolution $resolution   \\
--rerun T   \\
--pointsize  0.5  \\
--palette customecol2\\
""")
        



# seurat_sub="sub_$cell/Clustering/seurat.h5seurat"
# Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
#   -i  ${seurat_sub} \
#   -f h5seurat \
#   -o sub_$cell/Clustering \
#   --assay $assay \
#   --dataslot data \
#   summarize \
#   --reduct umap \
#   --palette customecol2 \
#   -c clusters \
#   -b sampleid,group \
#   --pointsize 0.5 \
#   --dosummary T


# Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \
#   -i ${seurat_sub}  \
#   -f h5seurat \
#   -o sub_${cell}/Clustering/clusters_correlation \
#   -t 6 \
#   --assay $assay \
#   --slot data \
#   --reduct umap \
#   coefficient \
#   -g clusters

# Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
#   -i ${seurat_sub}  \
#   -f h5seurat \
#   -o sub_${cell}/Marker \
#   --assay $assay \
#   --dataslot data,counts \
#   -j 10 \
#   findallmarkers \
#   -c 2 \
#   -N 10 \
#   -k 1 \
#   -p 0.05 \
#   -s F \
#   -e presto \
#   -n clusters


# #2.可视化+anno
# # marker热图
# Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \
#   -i ${seurat_sub}  \
#   -f h5seurat \
#   -o sub_${cell}/Marker \
#   -t 10 \
#   --assay $assay \
#   --slot data,scale.data \
#   heatmap \
#   -l sub_$cell/Marker/top10_markers_for_each_cluster.xls \
#   -c gene_diff \
#   -n 10 \
#   -g clusters \
#   --group_colors customecol2 \
#   --sample_ratio 0.8 \
#   --style seurat

# Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
#   -i ${seurat_sub}   \
#   -f h5seurat \
#   -o sub_${cell}/Marker \
#   -j 10 \
#   --assay $assay \
#   --dataslot data \
#   visualize \
#   -l sub_$cell/Marker/top10_markers_for_each_cluster.xls \
#   -g clusters \
#   --reduct umap \
#   --topn  10  \
#   --topby gene_diff \
#   -m vlnplot,featureplot \
#   --vcolors customecol2 \
#   --ccolors spectral \
#   --pointsize 0.3 \
#   --dodge F


# Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \
#   -g sub_${cell}/Marker/all_markers_for_each_cluster.xls \
#   --anno $anno  # 根据物种修改
# Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \
#   -g sub_${cell}/Marker/top10_markers_for_each_cluster.xls \
#   --anno $anno  # 根据物种修改

# # 判断人和小鼠使用哪个参考数据集
# if [[ $species == 'mm' ]];then
#   sjj=/data/database/celltype_refdata/logNorm_rds/immgen.rds
# elif [[ $species == "hm" ]];then
#   sjj='/data/database/celltype_refdata/logNorm_rds/hpca.rds'
# else
#   echo 'species error! only human mouse'
#   exit
# fi
# Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \
# -i ${seurat_sub}  \
# -f h5seurat \
# -o sub_${cell}/Reference_celltype \
# -d h5seurat \
# --update T \
# --assay $assay \
# --dataslot counts \
# celltyping \
# -r $sjj \
# --annolevel single \
# --usecluster F \
# --demethod classic \
# --pointsize 0.3 \
# -n 25 \
# --reduct umap \
# --species $specie
# """)
