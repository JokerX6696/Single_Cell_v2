def diff_anno_run(obj):
    input_rds = obj.diff_anno.input_rds
    cell_types = obj.diff_anno.cell_types
    analysis_type = obj.diff_anno.analysis_type
    treat = obj.diff_anno.treat
    control = obj.diff_anno.control
    fc = obj.diff_anno.fc
    p = obj.diff_anno.p
    vs_type = obj.diff_anno.vs_type
    anno = obj.diff_anno.anno
    top = obj.diff_anno.top
    out = obj.out

    for cell_type in cell_types:
        with open(f'{out}/cmd_{cell_type}-{treat}-vs-{control}.diff.sh',"w") as f:
            f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i {input_rds}     \\
-f h5seurat     \\
-o ./{cell_type}-Diffexp/{treat}-vs-{control}     \\
--assay RNA     \\
--dataslot data,counts     \\
-j 10  \\
--predicate "{analysis_type} %in% c(\\'{cell_type}\\')" \\
diffexp     \\
-c {vs_type}:{treat}:{control}     \\
-k {fc}     \\
-p {p}    \\
-e presto

Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \\
-g ./{cell_type}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-all_diffexp_genes.xls \\
--anno {anno}/gene_annotation.xls

Rscript   /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \\
-g ./{cell_type}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls \\
--anno {anno}/gene_annotation.xls

### diffexp_heatmap
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
-i {input_rds}  \\
-f h5seurat \\
-o ./{cell_type}-Diffexp/{treat}-vs-{control}  \\
-t 10 \\
--assay RNA \\
--slot data,scale.data \\
--predicate "{analysis_type} %in% c(\\'{cell_type}\\') & {vs_type} %in% c(\\'{treat}\\',\\'{control}\\')" \\
diff_heatmap \\
-d ./{cell_type}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls \\
-n {top} \\
-g {vs_type} \\
--group_colors customecol2 \\
--sample_ratio 0.8

rm ./{cell_type}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-all_diffexp_genes.xls ./{cell_type}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls

perl /gpfs/oe-scrna/ziqingzhen/script/enrichment/enrich_go_kegg.pl -infile {cell_type}-Diffexp/{treat}-vs-{control}/*-vs-*-diff-*.xls \\
-go_bg {anno}/gene_go.backgroud.xls \\
-category /gpfs/oe-scrna/ziqingzhen/script/enrichment/category.xls \\
-kegg_bg {anno}/gene_kegg.backgroud.xls \\
-outdir {cell_type}-Diffexp/{treat}-vs-{control}/enrichment  \\
-shelldir {cell_type}-Diffexp/{treat}-vs-{control}/enrichment_sh
                    """)
            

def cellchat_run(obj):
    rds = obj.cellchat.rds
    species=obj.cellchat.species
    col = obj.cellchat.col  # 用来进行通讯分析的metadata列名
    group_need = obj.cellchat.group_need
    group_type = obj.cellchat.group_type
    group_list = obj.cellchat.group_list
    out = obj.cellchat.out
    part = obj.cellchat.part
    part_name = obj.cellchat.part_name
    part_list = obj.cellchat.part_list
    out_sc = obj.out
    
    if part:
        for p in part_list:
            script_out = "cmd_cellchat_" + part_name + "_" + str(p) + ".sh"
            with open(f"{out_sc}/{script_out}","w") as f:
                f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/scRNA-seq_further_analysis/CellChat_v1.6.1.R \\
-i {rds} \\
-f rds \\
-s {species}  \\
-c {col} \\
""")
                if group_need:
                    group_vs = "+".join(group_list)
                    f.write(f"-g {group_type}  \\\n-d {group_vs} \\\n")
                f.write(f"-q {part_name} \\\n-u {p} \\\n")
                f.write(f"-o {out}\n")
    else:
        script_out = "cmd_cellchat.sh"
        with open(f"{out_sc}/{script_out}","w") as f:
            f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/scRNA-seq_further_analysis/CellChat_v1.6.1.R \\
-i {rds} \\
-f rds \\
-s {species}  \\
-c {col} \\
""")
            if group_need:
                group_vs = "+".join(group_list)
                f.write(f"-g {group_type}  \\\n-d {group_vs} \\\n")
            f.write(f"-o {out}\n")

def modified_cell_type_run(obj):
    out = obj.out
    seurat = obj.modified_cell_type.input
    output = obj.modified_cell_type.output
    updata = obj.modified_cell_type.updata
    if updata:
        bl = 'T'
    else:
        bl = 'F'
    newcelltype_file = obj.modified_cell_type.newcelltype_file
    Modified_col = obj.modified_cell_type.Modified_col
    reduct = obj.modified_cell_type.reduct
    with open(f'{out}/cmd_modified_cell_type.sh',"w") as f:
        f.write(f"""set -e
module purge && module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \
-i {seurat} \\
-f h5seurat \\
-o {output} \\
-d h5seurat \\
--update {bl} \\
--assay RNA \\
--dataslot counts,data,scale.data  \\
changecelltype \\
-c {newcelltype_file}\\
-C {Modified_col} \\
--palette customecol2 \\
--reduct {reduct} \\
-b F
                """)

def gsva_run(obj):
    pass