#R script to plot the SIMD versus scalar results

library(ggplot2)
library(reshape)

setwd('.')
data=read.table('vector_scalar_pct.txt', header=T, fill=T, colClasses="integer", sep=' ')
data2= data[, !(names(data) %in% "KNL")]
data = melt(data, id=c("Stride"))
data2 = melt(data2, id=c("Stride"))
colnames(data) = c("stride", "Platform", "pct")
colnames(data2) = c("stride", "Platform", "pct")
data$Platform = as.factor(data$Platform)
data2$Platform = as.factor(data2$Platform)

p = ggplot(data, aes(x=stride, y=pct, group=Platform)) + 
    geom_line(aes(col=Platform), size=1) + theme_bw() + labs(x="Stride", y="Percent Increase", title="Vector vs Scalar Loads", subtitle="Single Threaded, Cray Compiler") + 
    scale_x_continuous(breaks=c(1,2,4,8,16,32,64,128), trans="log2") + 
    scale_color_manual(values=c("#999999", "#E69F00",  "#56B4E9","coral")) + 
    geom_hline(yintercept=0, linetype="dashed")
p

p2 = ggplot(data2, aes(x=stride, y=pct, group=Platform)) + 
  geom_line(aes(col=Platform), size=1) + theme_bw() + labs(x="Stride", y="Percent Increase", title="Vector vs Scalar Loads", subtitle="Single Threaded, Cray Compiler") + 
  scale_x_continuous(breaks=c(1,2,4,8,16,32,64,128), trans="log2") + 
  scale_color_manual(values=c("#999999", "#E69F00", "#56B4E9")) + 
  geom_hline(yintercept=0, linetype="dashed")

p2

ggsave("vector_vs_scalar_speedup.png", plot = p, height=6, width=6, units="in")
ggsave("vector_vs_scalar_speedup_no_knl.png", plot = p2, height=6, width=6, units="in")
data
