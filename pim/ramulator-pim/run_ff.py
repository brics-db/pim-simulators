import os

#files = ["phoenix.kmeans","phoenix.mm","phoenix.pca","phoenix.wordcount", 
#         "rodinia.bfs","rodinia.bp1","rodinia.bp2","rodinia.kmeans","rodinia.myocyte","rodinia.nw","rodinia.sc",
#         "ligra","ligra.usa", "ligra.kcore.usa.emd", "ligra.radii.rmat.emd", "ligra.kcore.rmat.emd", "ligra.radii.usa.ems", "ligra.kcore.usa.ems", "ligra.radii.rmat.ems", "ligra.kcore.rmat.ems",
#         "graphmat.ds","graphmat.pg.usa",  
#         "select",
#         "splash.fft", "splash.luncb", "splash.ocean.jacobcalc","splash.ocean.laplacalc","splash.ocean.relax","splash.radiosity","splash.slave2"]

#files = ["select"]
files = ["blk_matmult","dot_product","image_filter","mandelbrot","sobel","wf"]
for f in files:
    cmd = "./ramulator --config filtered-trace-paper-configs/HMC-config.cfg --mode=cpu --stats "+f+".hmc.pim --trace fastflow_traces/"+f
    print cmd
    os.system(cmd) 