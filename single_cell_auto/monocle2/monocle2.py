def monocle2_run(obj):
    seurat = obj.monocle2.seurat
    out = obj.monocle2.out
    var_gene = obj.monocle2.var_gene
    split_group = obj.monocle2.split_group
    sel = obj.monocle2.sel
    sel_clusters = obj.monocle2.sel_clusters
    fbl = obj.monocle2.fbl
    outsc = obj.out
    sel_clusters = sel_clusters.replace("'","\\'")

    with open(f"{outsc}/cmd_monocle.sh",'w')as f:
        f.write(f"""set -e
module purge
module load OESingleCell/3.0.d
Rscript /public/scRNA_works/pipeline/oesinglecell3/exec/sctool \\
-i {seurat}  \\
-f h5seurat \\
--assay RNA \\
-o ./{out}/ \\
-j 8 \\
""")
        if sel:
                f.write(f"""--predicate   "{sel_clusters}" \\
""")
        f.write(f"""--update FALSE \\
monocle \\
-d {var_gene} \\
-x 0.01 \\
-r {fbl} \\
-C {split_group} \\
-s 1
""")
