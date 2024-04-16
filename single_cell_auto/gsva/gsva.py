def gsva_run(obj):
    out = obj.out
    species = obj.gsva.mouse
    step1 = obj.gsva.step1
    rds =  obj.gsva.rds
    GO_BP =  obj.gsva.GO_BP
    bin_cells = obj.gsva.bin_cells
    KEGG = obj.gsva.KEGG
    Hallmakr =  obj.gsva.Hallmakr
    cpu =  obj.gsva.cpu
    step2 =  obj.gsva.step2
    ret_GO = obj.gsva.ret_GO
    ret_KEGG = obj.gsva.ret_KEGG
    ret_Hallmakr = obj.gsva.ret_Hallmakr #  如果为 None 则不会执行 对应数据框的 step2
    rds2 = obj.gsva.rds2
    cell_heatmap = obj.gsva.cell_heatmap
    groups = obj.gsva.groups
    sub = obj.gsva.sub
    q = obj.gsva.q
    u = obj.gsva.u
    species_all = {
        "mouse":{
            'GO_BP':'/data/database/GSEA_gmt/mouse/v2023/m5.go.bp.v2023.1.Mm.symbols.gmt',
            'KEGG':'/data/database/GSEA_gmt/mouse/gene_kegg.gmt',
            'Hallmakr':'/gpfs/oe-scrna/zhengfuxing/Publc/mh.all.v2023.1.Mm.symbols.gmt'
        },
        "human":{
            'GO_BP':'/data/database/GSEA_gmt/human/v2023/c5.go.bp.v2023.1.Hs.symbols.gmt',
            'KEGG':'/data/database/GSEA_gmt/human/v2023/c2.cp.kegg.v2023.1.Hs.symbols.gmt',
            'Hallmakr':'/gpfs/oe-scrna/zhengfuxing/Publc/h.all.v2023.1.Hs.symbols.gmt'
        },
        "rat":{
            'GO_BP':'/data/database/GSEA_gmt/rat/gene_go_bp.backgroud.gmt',
            'KEGG':'/data/database/GSEA_gmt/rat/gene_kegg.gmt',
            'Hallmakr':'no_data'
        }
    }

    if step1:
        if GO_BP:
            with open(f"{out}/cmd_gsva_step1_GO_BP.sh", 'w')as f:
                f.write(
f"""set -e
module purge && module load OESingleCell/2.0.0
Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_enrich.R \\
-i {rds} \\
-f seurat   \\
-g {species_all[species]['GO_BP']}  \\
-o  ./GSVA_GO_BP_step1  \\
-c  {bin_cells}  \\
-k Poisson \\
-a  FALSE  \\
-s 2  \\
-S 10000  \\
-j {cpu} \\
-x  TRUE 
""")
            
        if KEGG:
            with open(f"{out}/cmd_gsva_step1_KEGG.sh", 'w')as f:
                f.write(f"""set -e
Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_enrich.R \\
-i {rds} \\
-f seurat   \\
-g {species_all[species]['KEGG']}  \\
-o  ./GSVA_KEGG_step1  \\
-c  {bin_cells}  \\
-k Poisson \\
-a  FALSE  \\
-s 2  \\
-S 10000  \\
-j {cpu} \\
-x  TRUE &
""")
        if Hallmakr:
            with open(f"{out}/cmd_gsva_step1_Hallmakr.sh", 'w')as f:
                f.write(f"""set -e
Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_enrich.R \\
-i {rds} \\
-f seurat   \\
-g {species_all[species]['Hallmakr']}  \\
-o  ./GSVA_Hallmakr_step1  \\
-c  {bin_cells}  \\
-k Poisson \\
-a  FALSE  \\
-s 2  \\
-S 10000  \\
-j {cpu} \\
-x  TRUE &
""")
                


    if step2:
        if not sub:
            for g in groups:
                group_by = g.split(":")[0]
                t = g.split(":")[1]
                c = g.split(":")[2]
                with open(f"{out}/cmd_gsva_step2_{group_by}_{t}_{c}.sh", 'w')as f:
                    f.write("set -e \nmodule purge && module load OESingleCell/2.0.0\n")
                    if ret_GO != "None":
                        f.write(f"""Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \\
-i {ret_GO} \\
-v {rds2} \\
-c {g} \\
-p 0.05 \\
-n 10 \\
-d TRUE \\
-o ./GSVA_GO_BP_{group_by}_{t}_{c} \\
--cell_heatmap {cell_heatmap}

""")
                    if ret_KEGG != "None":
                        f.write(f"""Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \\
-i {ret_KEGG} \\
-v {rds2} \\
-c {g} \\
-p 0.05 \\
-n 10 \\
-d TRUE \\
-o ./GSVA_KEGG_{group_by}_{t}_{c} \\
--cell_heatmap {cell_heatmap}

""")
                    if  ret_Hallmakr != "None":
                        f.write(f"""Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \\
-i {ret_Hallmakr} \\
-v {rds2} \\
-c {g} \\
-p 0.05 \\
-n 10 \\
-d TRUE \\
-o ./GSVA_Hallmakr_{group_by}_{t}_{c} \\
--cell_heatmap {cell_heatmap}

"""
)
        else:
            for i in u:
                for g in groups:
                    group_by = g.split(":")[0]
                    t = g.split(":")[1]
                    c = g.split(":")[2]
                    with open(f"{out}/cmd_gsva_step2_{group_by}_{t}_{c}_{q}_{i}.sh", 'w')as f:
                        f.write("set -e \nmodule purge && module load OESingleCell/2.0.0\n")
                        if ret_GO != "None":
                            f.write(f"""Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \\
    -i {ret_GO} \\
    -v {rds2} \\
    -c {g} \\
    -q {q} \\
    -u {i} \\
    -p 0.05 \\
    -n 10 \\
    -d TRUE \\
    -o ./GSVA_GO_BP_{q}_{i}_{t}_{c} \\
    --cell_heatmap {cell_heatmap}

    """)
                        if ret_KEGG != "None":
                            f.write(f"""Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \\
    -i {ret_KEGG} \\
    -v {rds2} \\
    -c {g} \\
    -q {q} \\
    -u {i} \\
    -p 0.05 \\
    -n 10 \\
    -d TRUE \\
    -o ./GSVA_KEGG_{q}_{i}_{t}_{c} \\
    --cell_heatmap {cell_heatmap}

    """)
                        if  ret_Hallmakr != "None":
                            f.write(f"""Rscript /home/luyao/10X_scRNAseq_v3/src/Enrichment/GSVA_pathway_diffxp.R  \\
    -i {ret_Hallmakr} \\
    -v {rds2} \\
    -c {g} \\
    -q {q} \\
    -u {i} \\
    -p 0.05 \\
    -n 10 \\
    -d TRUE \\
    -o ./GSVA_Hallmakr_{q}_{i}_{t}_{c} \\
    --cell_heatmap {cell_heatmap}

    """
    )