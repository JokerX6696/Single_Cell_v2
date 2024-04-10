def modified_cell_type_run(obj):
    out = obj.out
    seurat = obj.modified_cell_type.input
    output = obj.modified_cell_type.output
    updata = obj.modified_cell_type.updata
    updata_bynewcelltype = obj.modified_cell_type.updata_bynewcelltype  # 是否更新后续基于 newcelltype的分析
    type_name = obj.modified_cell_type.type_name
    newseurat = obj.modified_cell_type.newseurat
    species = obj.modified_cell_type.species # human
    if updata:
        bl = 'T'
    else:
        bl = 'F'
    newcelltype_file = obj.modified_cell_type.newcelltype_file
    Modified_col = obj.modified_cell_type.Modified_col
    reduct = obj.modified_cell_type.reduct
    newcelltype_file_type = obj.modified_cell_type.newcelltype_file_type
    if newcelltype_file_type == 'tsv':
        fgf = 'F'
    elif newcelltype_file_type == 'csv':
        fgf = 'T'
    else:
        print('细胞文件名后缀只能是 tsv 或 csv，请检查 config 文件中 newcelltype_file_type 参数！')
        exit(1)
    with open(f'{out}/cmd_modified_cell_type.sh',"w") as f:
        f.write(f"""set -e
module purge && module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
-i {seurat} \\
-f h5seurat \\
-o {output} \\
-d h5seurat \\
--update {bl} \\
--assay RNA \\
--dataslot counts,data,scale.data  \\
changecelltype \\
-c {newcelltype_file} \\
-C {Modified_col} \\
--palette customecol2 \\
--reduct {reduct} \\
-b {fgf}
                """)

        if updata_bynewcelltype:
            seurat=newseurat
            if species == 'human':
                anno = '/data/database/cellranger-refdata/refdata-gex-GRCh38-2020-A/annotation/gene_annotation.xls'
            elif species == 'mouse':
                anno = '/data/database/cellranger-refdata/refdata-gex-mm10-2020-A/annotation/gene_annotation.xls'
            f.write(f"""
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
  -i  {seurat} \\
  -f h5seurat \\
  -o ./ \\
  --assay RNA \\
  --dataslot data \\
  summarize \\
  --reduct umap \\
  --palette customecol2 \\
  -c {type_name} \\
  -b sampleid,group \\
  --pointsize 0.5 \\
  --dosummary T

Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
-i {seurat} \\
-f h5seurat \\
-o ./clusters_correlation \\
-t 6 \\
--assay RNA \\
--slot data \\
--reduct umap \\
coefficient \\
-g {type_name}

# 1.鉴定marker
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
  -i {seurat} \\
  -f h5seurat \\
  -o Marker \\
  --assay RNA \\
  --dataslot data,counts \\
  -j 10 \\
  findallmarkers \\
  -c 2 \\
  -N 10 \\
  -k 1 \\
  -p 0.05 \\
  -s F \\
  -e presto \\
  -n {type_name}

#2.可视化+anno
# marker热图
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
  -i {seurat} \\
  -f h5seurat \\
  -o ./Marker \\
  -t 10 \\
  --assay RNA \\
  --slot data,scale.data \\
  heatmap \\
  -l Marker/top10_markers_for_each_cluster.xls \\
  -c gene_diff \\
  -n 10 \\
  -g {type_name} \\
  --group_colors customecol2 \\
  --sample_ratio 0.8 \\
  --style seurat
 
# featureplot小提琴图
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
  -i {seurat}  \\
  -f h5seurat \\
  -o ./Marker \\
  -j 10 \
  --assay RNA \\
  --dataslot data \\
  visualize \
  -l Marker/top10_markers_for_each_cluster.xls \
  -g {type_name} \\
  --reduct umap \\
  --topn  10  \\
  --topby gene_diff \\
  -m vlnplot,featureplot \\
  --vcolors customecol2 \\
  --ccolors spectral \\
  --pointsize 0.3 \\
  --dodge F
 
#anno


Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \\
  -g Marker/all_markers_for_each_cluster.xls \\
  --anno {anno}  # 根据物种修改
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool annotation \\
  -g Marker/top10_markers_for_each_cluster.xls \\
  --anno {anno}  # 根据物种修改
""")