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
-n 20 \\
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
    rds = obj.cellchat.input_rds
    col = obj.cellchat.col
    group = obj.cellchat.group
    treat = obj.cellchat.treat
    control = obj.cellchat.control
    fc = obj.cellchat.fc
    p = obj.cellchat.p
    vs_type = obj.cellchat.vs_type
    anno = obj.cellchat.anno
    out = obj.cellchat.out

    for cell_type in cell_types:
        with open(out,"w") as f:
            f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/scRNA-seq_further_analysis/CellChat_v1.6.1.R \\
                    """)
        if group:
            pass
        else:
            pass