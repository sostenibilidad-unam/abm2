require(tgp)
s1 <- round(lhs(20000, rbind(c(0,1), c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1))),digits = 2)


colnames(s1)<-c("w_11_demanda_F",	"w_12_presion_F",	"w_21_necesidad_F",	"w_22_presion_F",	"w_31_demanda_S",	"w_32_presion_S",	"w_41_necesidad_S",	"w_42_presion_S")

s2<-  s1[which(s1[,1]+s1[,2] < 1),]
s3<-s2[which(s2[,3]+s2[,4]<1),]
s4<-s3[which(s3[,5]+s3[,6]< 1),]
s5<-s4[which(s4[,7]+s4[,8]< 1),]
write.csv(x = s5,file = "sampling_scenarios_Weights.csv")


#new scheme to obtain a new set of weights and decition metric
#1) varying W but keeping D constant
s1 <- lhs(2000, rbind(c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9), c(0,0.9)))
aa<-cbind(rep(0.25,200),rep(0.25,200),rep(0.25,2000),rep(0.25,2000))
s1 <- data.frame(round(cbind(s1,aa),digits = 3))

colnames(s1)<-c("w1",	"w2",	"w3","w4", "w5","w6",	"w7","w8","alpha1","alpha2","alpha3","alpha4")

s1[,1:8]<-s1[,1:8]/rowSums(s1[,1:8])

s1[,9:12]<-s1[,9:12]/rowSums(s1[,9:12])

write.csv(x = s1,file = "~/MEGADAPT/abm2/sampling_scenarios_var_W.csv")

#1) varying W and D 
s2 <- data.frame(round(lhs(2000, rbind(c(0,0.9),c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9))),digits = 2))

colnames(s2)<-c("w1",	"w2",	"w3","w4", "w5","w6",	"w7","w8","alpha1","alpha2","alpha3","alpha4")

s2[,1:8]<-s2[,1:8]/rowSums(s2[,1:8])

s2[,9:12]<-s2[,9:12]/rowSums(s2[,9:12])


write.csv(x = s2,file = "~/MEGADAPT/abm2/sampling_scenarios_Weights_var_WandD.csv")


#1) varying D but keeping W constant
s3<-lhs(2000, rbind(c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9)))
aa<-cbind(rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,2000),rep(0.25,2000))
s3 <- data.frame(round(cbind(aa,s3),digits = 3))

colnames(s3)<-c("w1",	"w2",	"w3","w4", "w5","w6",	"w7","w8","alpha1","alpha2","alpha3","alpha4")
s3[,1:8]<-s3[,1:8]/rowSums(s3[,1:8])
s3[,9:12]<-s3[,9:12]/rowSums(s3[,9:12])


write.csv(x = s3,file = "~/MEGADAPT/abm2/sampling_scenarios_Weights_var_D.csv")



write.csv(x = rbind(s1,s2,s3),file = "~/MEGADAPT/abm2/sampling_scenarios_Weights_all.csv")
