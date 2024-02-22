def diff_anno_run(
  input_rds,
  cell_types,
  analysis_type,
  treat,
  control,
  fc,
  p,
  vs_type,
  anno,
  out
):
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