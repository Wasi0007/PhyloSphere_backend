library(ape)
library(analogue)
library(parallel)
library(phytools)



filename <- "hpmatrix.txt"
hpmatrix_read <- read.table(filename, header = TRUE, row.names = 1, sep = ",", comment.char = "", check.names = FALSE)
hpmatrix_read <- as.matrix(hpmatrix_read)
hpmatrix <- hpmatrix_read


host_tree <- read.tree("host.nwk")
host_tree$tip.label <- gsub("'", "", host_tree$tip.label)
host_tree$node.label <- gsub("'", "", host_tree$node.label)


parasite_tree <- read.tree("parasite.nwk")
parasite_tree$tip.label <- gsub("'", "", parasite_tree$tip.label)
parasite_tree$node.label <- gsub("'", "", parasite_tree$node.label)


host.patristic.dist <- as.matrix(cophenetic(host_tree))
host.patristic.dist <- host.patristic.dist[rownames(hpmatrix), rownames(hpmatrix)]


parasite.patristic.dist <- as.matrix(cophenetic(parasite_tree))
parasite.patristic.dist <- parasite.patristic.dist[colnames(hpmatrix), colnames(hpmatrix)]


runParaFit<- function(i){
  tmp <- parafit(host.patristic.dist, parasite.patristic.dist, hpmatrix, nperm=999, test.links=T, correction='cailliez')
  return (tmp)
}

cat("Scheduled",length(host_tree),"jobs to run in parallel ... Running ...
Nothing will be printed on screen until all runs are completed ...",sep=" ")

iteration <- 5

res <- lapply(1:iteration, function(i){
  simplify2array(mclapply(1,runParaFit,mc.preschedule=T,mc.cores=1,mc.set.seed=F))
})


data.class(res)

res_p<-sapply(res, "[[",2)
data.class(res_p) 
as.matrix(res_p)


p_global_mean<-mean(res_p)

res_link<-c()
for (i in 1:iteration){
  res_link<-cbind(res_link,res[[i]])
}
data.class(res_link)


links_parafit_order=cbind(rownames(hpmatrix)[res_link[,1]$link.table[,1]],colnames(hpmatrix)[res_link[,1]$link.table[,2]])
p_level<-0.055

p_table=NULL
for (i in 1:ncol(res_link)){
  p.F1=res_link[,i]$link.table[,4] 
  p_table=rbind(p_table,p.F1)
}
p_table_adj<-apply(p_table,2,p.adjust,method="BH")
data.class(p_table_adj) 


p_means<-colMeans(p_table_adj)
p_means_table<-cbind(links_parafit_order,(p_means))
p_means_table_df<-as.data.frame(p_means_table)


ptable<-cbind(links_parafit_order,t(p_table))
colnames(ptable)<-c("Host","Parasite",sprintf("p.F1_tree_%s",seq(1:ncol(res_link))))

p_tableadj<-cbind(links_parafit_order,t(p_table_adj))
colnames(p_tableadj)<-c("Host","Parasite",sprintf("p.F1.adj_tree_%s",seq(1:ncol(res_link))))


p_colors=NULL

for (i in 1:ncol(p_table_adj)){
  p_min=min(p_table_adj[,i]);p_max=max(p_table_adj[,i])
  color="red3" 
  if(p_min>p_level && p_max>p_level){color="gray55"} 
  if(p_min<=p_level && p_max<=p_level){color="green3"}
  p_colors[i]=color
}

p_type=NULL

for (i in 1:ncol(p_table_adj)){
  p_min=min(p_table_adj[,i]);p_max=max(p_table_adj[,i])
  lty="dotdash"
  if(p_min>p_level && p_max>p_level){lty="longdash"} 
  if(p_min<=p_level && p_max<=p_level){lty="solid"} 
  p_type[i]=lty
}


ph1 <- host_tree
ph2 <- parasite_tree
assoc_links <- links_parafit_order
cophy <- cophylo(ph1, ph2, assoc=assoc_links, rotate=F)

png("Tanglegram.png", width=800, height=600)
cophyloplot_min<-plot(cophy,link.type = "curved",link.lty=p_type, link.col=p_colors, link.lwd=1, fsize=0.7,pts=F,hang = -1,width = 6)
dev.off()



