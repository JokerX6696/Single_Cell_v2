
module load OESingleCell/3.0.d
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  \
-i /gpfs/oe-scrna/zhengfuxing/Project/scRNA/DZOE2023101132_Human/20240222/2.B_cells/change_sampleid.h5seurat     \
-f h5seurat     \
-o ./1-Diffexp/After-vs-Before     \
--assay RNA     \
--dataslot data,counts     \
-j 10  \
--predicate "clusters %in% c('1')" \
diffexp     \
-c sampleid:After:Before     \
-k 1.2     \
-p 0.05    \
-e presto

Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \
-g ./1-Diffexp/After-vs-Before/sampleid_After-vs-Before-all_diffexp_genes.xls \
--anno /data/database/cellranger-refdata/refdata-gex-GRCh38-2020-A/annotation//gene_annotation.xls

Rscript   /public/scRNA_works/pipeline/oesinglecell3/exec/sctool  annotation \
-g ./1-Diffexp/After-vs-Before/sampleid_After-vs-Before-diff-pval-0.05-FC-1.2.xls \
--anno /data/database/cellranger-refdata/refdata-gex-GRCh38-2020-A/annotation//gene_annotation.xls

### diffexp_heatmap
Rscript  /public/scRNA_works/pipeline/oesinglecell3/exec/scVis \
-i /gpfs/oe-scrna/zhengfuxing/Project/scRNA/DZOE2023101132_Human/20240222/2.B_cells/change_sampleid.h5seurat  \
-f h5seurat \
-o ./1-Diffexp/After-vs-Before  \
-t 10 \
--assay RNA \
--slot data,scale.data \
--predicate "clusters %in% c('1') & sampleid %in% c('After','Before')" \
diff_heatmap \
-d ./1-Diffexp/After-vs-Before/sampleid_After-vs-Before-diff-pval-0.05-FC-1.2.xls \
-n 20 \
-g sampleid \
--group_colors customecol2 \
--sample_ratio 0.8

rm ./1-Diffexp/After-vs-Before/sampleid_After-vs-Before-all_diffexp_genes.xls ./1-Diffexp/After-vs-Before/sampleid_After-vs-Before-diff-pval-0.05-FC-1.2.xls

perl /gpfs/oe-scrna/ziqingzhen/script/enrichment/enrich_go_kegg.pl -infile 1-Diffexp/After-vs-Before/*-vs-*-diff-*.xls \
-go_bg /data/database/cellranger-refdata/refdata-gex-GRCh38-2020-A/annotation//gene_go.backgroud.xls \
-category /gpfs/oe-scrna/ziqingzhen/script/enrichment/category.xls \
-kegg_bg /data/database/cellranger-refdata/refdata-gex-GRCh38-2020-A/annotation//gene_kegg.backgroud.xls \
-outdir 1-Diffexp/After-vs-Before/enrichment  \
-shelldir 1-Diffexp/After-vs-Before/enrichment_sh
                    