library(ape)
library(analogue)
library(parallel)
library(phytools)

edgecol <- c()
edgecol[1:20] = "gray"

tipcol = c("red","purple","purple","red","purple","purple","red","purple","black","red","red")

host_tree <- read.tree("host.nwk")
host_tree$tip.label <- gsub("'", "", host_tree$tip.label)
host_tree$node.label <- gsub("'", "", host_tree$node.label)
png(filename = "Tree.png")
plot.phylo(host_tree, edge.color = edgecol, tip.color = tipcol, show.tip.label = TRUE, font = 3, cex = 1)
dev.off()

