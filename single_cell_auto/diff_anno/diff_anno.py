def diff_anno_run(obj):
    import re
    input_rds = obj.diff_anno.input_rds
    cell_types = obj.diff_anno.cell_types
    analysis_type = obj.diff_anno.analysis_type
    treat_all = obj.diff_anno.treat
    control_all = obj.diff_anno.control
    fc = obj.diff_anno.fc
    p = obj.diff_anno.p
    vs_type = obj.diff_anno.vs_type
    anno = obj.diff_anno.anno
    top = obj.diff_anno.top
    out = obj.out

    len_t = len(treat_all); len_c = len(control_all)
    if len_t != len_c:
        exit('请检查 yaml 文件 实验组与对照组数量不一致')
    
    for num in range(0,len_t):
        treat = treat_all[num]
        control = control_all[num]


        for cell_type in cell_types:
            cell_type_out = re.sub(r'\s+|\/|\(|\)|\||\&|\^|\%', '_', cell_type)
            if cell_type == 'all':
                with open(f'{out}/cmd_{cell_type_out}-{treat}-vs-{control}.diff.sh',"w") as f:
                    f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i {input_rds}     \\
-f h5seurat     \\
-o ./{cell_type_out}-Diffexp/{treat}-vs-{control}     \\
--assay RNA     \\
--dataslot data,counts     \\
-j 10  \\
diffexp     \\
-c {vs_type}:{treat}:{control}     \\
-k {fc}     \\
-p {p}    \\
-e presto

Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \\
-g ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-all_diffexp_genes.xls \\
--anno {anno}/annotation/gene_annotation.xls

Rscript   /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \\
-g ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls \\
--anno {anno}/annotation/gene_annotation.xls

### diffexp_heatmap
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
-i {input_rds}  \\
-f h5seurat \\
-o ./{cell_type_out}-Diffexp/{treat}-vs-{control}  \\
-t 10 \\
--assay RNA \\
--slot data,scale.data \\
--predicate "{vs_type} %in% c(\\'{treat}\\',\\'{control}\\')" \\
diff_heatmap \\
-d ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls \\
-n {top} \\
-g {vs_type} \\
--group_colors customecol2 \\
--sample_ratio 0.8

rm ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-all_diffexp_genes.xls ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls

/public/scRNA_works/pipeline/scRNA-seq_further_analysis/enrichwrap.sh \\
-i {cell_type_out}-Diffexp/{treat}-vs-{control}/*-vs-*-diff-*.xls \\
-g  {anno} \\
-o ./diffexp \\
-d TRUE
                    """)
            else:
                with open(f'{out}/cmd_{cell_type_out}-{treat}-vs-{control}.diff.sh',"w") as f:
                    f.write(f"""set -e
module load OESingleCell/3.0.d
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \\
-i {input_rds}     \\
-f h5seurat     \\
-o ./{cell_type_out}-Diffexp/{treat}-vs-{control}     \\
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
-g ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-all_diffexp_genes.xls \\
--anno {anno}/annotation/gene_annotation.xls

Rscript   /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \\
-g ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls \\
--anno {anno}/annotation/gene_annotation.xls

### diffexp_heatmap
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \\
-i {input_rds}  \\
-f h5seurat \\
-o ./{cell_type_out}-Diffexp/{treat}-vs-{control}  \\
-t 10 \\
--assay RNA \\
--slot data,scale.data \\
--predicate "{analysis_type} %in% c(\\'{cell_type}\\') & {vs_type} %in% c(\\'{treat}\\',\\'{control}\\')" \\
diff_heatmap \\
-d ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls \\
-n {top} \\
-g {vs_type} \\
--group_colors customecol2 \\
--sample_ratio 0.8

rm ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-all_diffexp_genes.xls ./{cell_type_out}-Diffexp/{treat}-vs-{control}/{vs_type}_{treat}-vs-{control}-diff-pval-{p}-FC-{fc}.xls



/public/scRNA_works/pipeline/scRNA-seq_further_analysis/enrichwrap.sh \\
-i {cell_type_out}-Diffexp/{treat}-vs-{control}/*-vs-*-diff-*.xls \\
-g  {anno} \\
-o ./diffexp \\
-d TRUE
                    """)
            
