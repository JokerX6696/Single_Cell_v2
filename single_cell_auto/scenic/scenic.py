# -*- coding: utf-8 -*-
def scenic_run(obj):
    out = obj.out
    step1 = obj.scenic.step1
    species = obj.scenic.species
    method = obj.scenic.method
    rds = obj.scenic.rds
    step2 = obj.scenic.step2
    rds2 = obj.scenic.rds2
    col = obj.scenic.col
    ret1_out = obj.scenic.ret1_out
    ret2_out = obj.scenic.ret2_out
    clustering_num = obj.scenic.clustering_num
    RSS_rank_mark = obj.scenic.RSS_rank_mark
    step1_wkdir = obj.scenic.step1_wkdir
    if species == 'human':
        anno = '/data/database/SCENIC/human'
        specie = 'hgnc'
    elif species == 'mouse':
        anno = '/data/database/SCENIC/mouse'
        specie = 'mgi'
    else:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Error scenic 只能分析人和小鼠！!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        exit()

    
    with open(f'{out}/cmd_scenic.sh',"w") as f:
        pass
        
        f.write(f"""set -e
module purge
source /home/lipeng/miniconda3/bin/activate Scenic""")
        if step1:
            f.write(f"""
Rscript /home/luyao/10X_scRNAseq_v3/src/GRN/scenic.R \\
-i {rds} \\
-f seurat \\
-d {anno} \\
-s {specie} \\
--coexMethod {method} \\
-o {ret1_out}
                    """)
        if  step2:
            f.write(f"""
Rscript /home/luyao/10X_scRNAseq_v3/src/GRN/RunRAS-RSS.R \\
-i {rds2} \\
-v {step1_wkdir}/int/3.4_regulonAUC.Rds \\
-f rds \\
-t {RSS_rank_mark} \\
-c {col} \\
-o {ret2_out} \\
-s 0

Rscript /home/luyao/10X_scRNAseq_v3/src/GRN/RunCSI.R \\
-i {rds2} \\
-v {step1_wkdir}/int/3.4_regulonAUC.Rds \\
-f rds \\
-c {col} \\
-n {clustering_num} \\
-o {ret2_out}
                    """)

